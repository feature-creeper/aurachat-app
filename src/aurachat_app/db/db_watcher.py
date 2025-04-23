import time
import threading
from typing import Callable, Dict, Any, List, Optional, Set
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from .db_client import get_mongodb_client

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
    
    def start(self):
        """Start the watch process in a background thread."""
        if self._running:
            return
        
        self._running = True
        self._watch_thread = threading.Thread(target=self._watch_messages, daemon=True)
        self._watch_thread.start()
        
    def stop(self):
        """Stop the watch process."""
        self._running = False
        if self._watch_thread and self._watch_thread.is_alive():
            self._watch_thread.join(timeout=1.0)
        
        # Close the change stream if it exists
        if self._change_stream:
            self._change_stream.close()
            
        self._client.close()
    
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
            if self._watched_chat_ids:
                # Watch updates to the messages array for specific chat_ids
                pipeline = [
                    {'$match': {
                        'operationType': 'update',
                        'updateDescription.updatedFields.messages': {'$exists': True},
                        'fullDocument.chat_id': {'$in': list(self._watched_chat_ids)}
                    }}
                ]
            else:
                # If no chat_ids are being watched, use a filter that will match nothing
                # This is more efficient than watching all documents when we don't want any
                pipeline = [
                    {'$match': {
                        'operationType': 'update',
                        'fullDocument.chat_id': {'$in': []}
                    }}
                ]
        
        return self._messages_collection.watch(
            pipeline=pipeline,
            full_document='updateLookup'
        )
    
    def _watch_messages(self):
        """Watch for changes to the messages array in documents with watched chat_ids."""
        try:
            # Create a change stream
            self._change_stream = self._create_change_stream()
            
            # Iterate over the change stream as long as the watcher is running
            while self._running:
                try:
                    # Check if there are any changes available (with timeout)
                    if self._change_stream.alive and self._change_stream.has_next(max_await_time_ms=1000):
                        change = self._change_stream.next()
                        
                        if 'fullDocument' in change and change['fullDocument'] is not None:
                            # Notify all registered callbacks
                            updated_document = change['fullDocument']
                            for callback in self._callbacks:
                                try:
                                    callback(updated_document)
                                except Exception as e:
                                    print(f"Error in callback: {e}")
                    else:
                        # To avoid CPU spinning if there are no changes for a while
                        time.sleep(0.1)
                        
                    # If the change stream is None, it means we need to recreate it
                    # This happens when watched_chat_ids changes
                    if self._change_stream is None:
                        self._change_stream = self._create_change_stream()
                        
                except PyMongoError as e:
                    print(f"MongoDB error in change stream: {e}")
                    # Try to reconnect after a delay
                    time.sleep(1)
                    
                    # Recreate the change stream
                    self._change_stream = self._create_change_stream()
            
            # Close the change stream when no longer running
            if self._change_stream:
                self._change_stream.close()
                self._change_stream = None
            
        except Exception as e:
            print(f"Error in messages watcher: {e}")
            self._running = False
            if self._change_stream:
                self._change_stream.close()
                self._change_stream = None

# Example usage:
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