import time
import threading
import logging
from typing import Callable, Dict, Any, List, Optional, Set
from pymongo.collection import Collection
from pymongo.errors import PyMongoError, OperationFailure
from pymongo.cursor import CursorType
from .db_client import get_mongodb_client

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MessagesWatcher')

class MessagesWatcher:
    """Watches for changes to the 'messages' array in documents in the telegram.messages collection."""
    
    def __init__(self):
        self._client = get_mongodb_client()
        self._db = self._client["telegram"]
        self._messages_collection = self._db["messages"]
        self._watch_thread = None
        self._running = False
        self._callbacks = []
        self._watched_chat_ids = set()
        self._change_stream = None
        self._lock = threading.Lock()  # For thread-safe operations on watched_chat_ids
        self._last_document_versions = {}  # To track changes between notifications
        
        logger.info("MessagesWatcher initialized")
    
    def start(self):
        """Start the watch process in a background thread."""
        if self._running:
            logger.info("Watcher already running, ignoring start request")
            return
        
        self._running = True
        self._watch_thread = threading.Thread(target=self._watch_messages, daemon=True)
        self._watch_thread.start()
        logger.info("MessagesWatcher thread started")
        
    def stop(self):
        """Stop the watch process."""
        logger.info("Stopping MessagesWatcher")
        self._running = False
        if self._watch_thread and self._watch_thread.is_alive():
            self._watch_thread.join(timeout=1.0)
        
        # Close the change stream if it exists
        if self._change_stream:
            self._change_stream.close()
            
        self._client.close()
        logger.info("MessagesWatcher stopped")
    
    def register_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback function to be called when a messages array changes.
        
        The callback will receive the document that was updated.
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Unregister a previously registered callback function."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def add_chat_id_to_watch(self, chat_id: int) -> bool:
        """Add a chat_id to the list of watched chat_ids.
        
        Args:
            chat_id: The chat_id to watch (integer)
            
        Returns:
            bool: True if the chat_id was added, False if it was already being watched
        """
        with self._lock:
            if chat_id in self._watched_chat_ids:
                return False
                
            self._watched_chat_ids.add(chat_id)
            
            # Restart the change stream to pick up the new chat_id
            if self._change_stream:
                self._change_stream.close()
                self._change_stream = None
                
            return True
    
    def remove_chat_id_from_watch(self, chat_id: int) -> bool:
        """Remove a chat_id from the list of watched chat_ids.
        
        Args:
            chat_id: The chat_id to stop watching (integer)
            
        Returns:
            bool: True if the chat_id was removed, False if it wasn't being watched
        """
        with self._lock:
            if chat_id not in self._watched_chat_ids:
                return False
                
            self._watched_chat_ids.remove(chat_id)
            
            # Restart the change stream to update the watched chat_ids
            if self._change_stream:
                self._change_stream.close()
                self._change_stream = None
                
            return True
    
    def get_watched_chat_ids(self) -> Set[int]:
        """Get the set of currently watched chat_ids.
        
        Returns:
            Set[int]: A copy of the set of watched chat_ids
        """
        with self._lock:
            return self._watched_chat_ids.copy()
    
    def _create_change_stream(self):
        """Create a change stream to watch for updates to the messages array for watched chat_ids."""
        pipeline = []
        
        with self._lock:
            watched_chat_ids_list = list(self._watched_chat_ids)
            logger.info(f"Creating change stream for chat_ids: {watched_chat_ids_list}")
            
            if self._watched_chat_ids:
                pipeline = [
                    {'$match': {
                        'operationType': {'$in': ['update', 'insert', 'replace']},
                        'fullDocument.chat_id': {'$in': watched_chat_ids_list}
                    }}
                ]
            else:
                logger.info("No chat_ids being watched, using empty filter")
                pipeline = [
                    {'$match': {
                        'operationType': 'update',
                        'fullDocument.chat_id': {'$in': []}
                    }}
                ]
        
        logger.info(f"Change stream pipeline: {pipeline}")
        
        return self._messages_collection.watch(
            pipeline=pipeline,
            full_document='updateLookup'
        )
    
    def _watch_messages(self):
        """Watch for changes to the messages array in documents with watched chat_ids."""
        try:
            # Create a change stream
            self._change_stream = self._create_change_stream()
            logger.info("Change stream created successfully")
            
            # Iterate over the change stream as long as the watcher is running
            while self._running:
                try:
                    # Try to get the next change - this will block until a change is available
                    change = next(self._change_stream, None)
                    
                    if change is not None:
                        logger.info(f"Change detected: {change.get('operationType')} - Document ID: {change.get('documentKey', {}).get('_id')}")
                        
                        if 'fullDocument' in change and change['fullDocument'] is not None:
                            updated_document = change['fullDocument']
                            self._process_updated_document(updated_document)
                        else:
                            logger.warning(f"Change event missing fullDocument: {change}")
                    else:
                        # If next() returned None (should not happen in normal operation),
                        # sleep briefly to avoid CPU spinning
                        time.sleep(0.1)
                        
                    # If the change stream is None, it means we need to recreate it
                    if self._change_stream is None:
                        logger.info("Change stream was reset, recreating it")
                        self._change_stream = self._create_change_stream()
                        
                except PyMongoError as e:
                    logger.error(f"MongoDB error in change stream: {e}", exc_info=True)
                    # Try to reconnect after a delay
                    time.sleep(1)
                    
                    # Recreate the change stream
                    self._change_stream = self._create_change_stream()
            
            # Close the change stream when no longer running
            if self._change_stream:
                self._change_stream.close()
                self._change_stream = None
                logger.info("Change stream closed")
            
        except Exception as e:
            logger.error(f"Error in messages watcher: {e}", exc_info=True)
            self._running = False
            if self._change_stream:
                self._change_stream.close()
                self._change_stream = None
    
    def _process_updated_document(self, document):
        """Process an updated document and notify callbacks."""
        chat_id = document.get('chat_id')
        messages = document.get('messages', [])
        message_count = len(messages)
        logger.info(f"Processing document for chat_id {chat_id}, contains {message_count} messages")
        
        # Check if the document has changed since last time
        document_id = document.get('_id')
        messages_str = str(messages)  # Simple way to compare
        
        if document_id in self._last_document_versions:
            if self._last_document_versions[document_id] == messages_str:
                logger.info(f"Document for chat_id {chat_id} hasn't changed, ignoring")
                return False
        
        # Store current version
        self._last_document_versions[document_id] = messages_str
        
        # Notify all registered callbacks
        callback_count = len(self._callbacks)
        logger.info(f"Notifying {callback_count} callbacks about the change")
        
        for callback in self._callbacks:
            try:
                callback(document)
            except Exception as e:
                logger.error(f"Error in callback: {e}", exc_info=True)
        
        return True
    
    def manual_check(self, chat_id: int):
        """Manually check for a document by chat_id and process it if found."""
        logger.info(f"Manually checking chat_id {chat_id}")
        try:
            # Directly query the latest document
            document = self._messages_collection.find_one({"chat_id": chat_id})
            
            if document:
                logger.info(f"Found document for chat_id {chat_id}")
                return self._process_updated_document(document)
            else:
                logger.info(f"No document found for chat_id {chat_id}")
        except Exception as e:
            logger.error(f"Error checking for document: {e}")
        
        return False

# Example usage (commented out)
"""
def handle_message_update(updated_document):
    chat_id = updated_document.get('chat_id')
    messages = updated_document.get('messages', [])
    print(f"Messages updated for chat {chat_id}, new messages count: {len(messages)}")

# Create and start the watcher
watcher = MessagesWatcher()
watcher.add_chat_id_to_watch(123456789)  # Watch a specific chat_id
watcher.register_callback(handle_message_update)
watcher.start()

# Later, to add another chat_id to watch
watcher.add_chat_id_to_watch(987654321)

# Later, to stop watching a chat_id
watcher.remove_chat_id_from_watch(123456789)

# Later, to stop the watcher entirely:
# watcher.stop()
""" 