import sys
import os
import tkinter as tk


# Add the parent directory to the Python path so we can import from views
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from views.main_view import root, status_label, title_label, initialize_ui
from db.db_watcher import MessagesWatcher
from db.db_client import get_latest_client_message

# Import the chat_id from config.py using absolute path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, project_root)  # Ensure project root is first in path

try:
    from config import chat_id as CONFIG_CHAT_ID
except ImportError:
    print("Warning: Could not import config.py, using default chat_id")
    CONFIG_CHAT_ID = 6172560874  # Default value from config.py

class MainViewModel:
    """View model for the main view containing string properties for UI elements."""
    
    def __init__(self):
        # Initialize default values
        self._status_text = "Status: Ready"
        self._title_text = "AuraChat Bot Interface"
    
    @property
    def status_text(self):
        """Get the current status text."""
        return self._status_text
    
    @status_text.setter
    def status_text(self, value):
        """Set the status text and update the UI."""
        self._status_text = value
        if status_label:
            status_label.config(text=value)
    
    @property
    def title_text(self):
        """Get the current title text."""
        return self._title_text
    
    @title_text.setter
    def title_text(self, value):
        """Set the title text and update the UI."""
        self._title_text = value
        if title_label:
            title_label.config(text=value)


class MainViewController:
    """Controller for the main view that manages the view model and UI bindings."""
    
    def __init__(self):
        """Initialize the controller with a view model and bind UI elements."""
        # Initialize the UI
        self.root = initialize_ui()
        # Create the view model
        self.view_model = MainViewModel()
        # Bind UI elements
        self.bind_ui()
        # Initialize the message watcher
        self.init_message_watcher()

        self.process_client_message(CONFIG_CHAT_ID)
    
    def bind_ui(self):
        """Bind the view model to UI elements."""
        # Set initial values
        if status_label:
            status_label.config(text=self.view_model.status_text)
        
        if title_label:
            title_label.config(text=self.view_model.title_text)
    
    def update_status(self, status):
        """Update the status text through the view model and ensure UI is updated."""
        self.view_model.status_text = status
        # Force UI update by manually updating the label and processing events
        if status_label:
            status_label.config(text=status)
            # Process pending events to ensure the UI updates immediately
            if self.root:
                self.root.update_idletasks()
    
    def update_title(self, title):
        """Update the title text through the view model."""
        self.view_model.title_text = title
        if title_label:
            title_label.config(text=title)
    
    def init_message_watcher(self):
        """Initialize the MongoDB messages watcher."""
        self.message_watcher = MessagesWatcher()
        self.message_watcher.register_callback(self.handle_message_update)
        
        # Add specific chat_ids to watch using the configured chat_id
        self.message_watcher.add_chat_id_to_watch(CONFIG_CHAT_ID)
        
        self.message_watcher.start()
        self.update_status(f"Message watcher started for chat ID: {CONFIG_CHAT_ID}")
    
    def watch_chat_id(self, chat_id):
        """Add a chat_id to the watch list."""
        if self.message_watcher.add_chat_id_to_watch(chat_id):
            self.update_status(f"Now watching chat ID: {chat_id}")
        else:
            self.update_status(f"Already watching chat ID: {chat_id}")
    
    def unwatch_chat_id(self, chat_id):
        """Remove a chat_id from the watch list."""
        if self.message_watcher.remove_chat_id_from_watch(chat_id):
            self.update_status(f"Stopped watching chat ID: {chat_id}")
        else:
            self.update_status(f"Not watching chat ID: {chat_id}")
    
    def process_client_message(self, chat_id):
        """Process the latest client message for a specific chat_id."""
        # Get the latest client message using the dedicated function
        latest_client_message = get_latest_client_message(chat_id)
        
        if latest_client_message:
            # Process the latest client message
            print(f"Latest client message: {latest_client_message}")
            
            # Example: Access specific fields from the latest client message
            content = latest_client_message.get('text')
            created_at = latest_client_message.get('created_at')
            
            if content:
                status_text = f"New client message: {content[:30]}..." if len(content) > 30 else f"New client message: {content}"
                print(f"Updating status to: {status_text}")
                self.update_title(status_text)
                # Double-check that label was updated
                if status_label:
                    print(f"Current status label text: {status_label['text']}")
            
            return True
        else:
            print(f"No client message found for chat_id: {chat_id}")
        
        return False
    
    def handle_message_update(self, updated_document):
        """Handle updates to messages in the database."""
        chat_id = updated_document.get('chat_id')
        messages = updated_document.get('messages', [])
        message_count = len(messages)
        
        # Process the latest client message
        self.process_client_message(chat_id)
        
        # Process all messages if needed
        if messages and message_count > 0:
            latest_message = messages[-1]  # Get the most recent message
            # Do something with the latest message (any role)
            print(f"Latest message (any role): {latest_message}")
    
    def run(self):
        """Start the main UI loop."""
        if self.root:
            self.root.mainloop()
    
    def cleanup(self):
        """Clean up resources before application exit."""
        if hasattr(self, 'message_watcher'):
            self.message_watcher.stop()

