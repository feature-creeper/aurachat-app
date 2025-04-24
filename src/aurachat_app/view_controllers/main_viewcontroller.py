import sys
import os
import tkinter as tk
import threading
import time


# Add the parent directory to the Python path so we can import from views
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from views.main_view import root, client_response_label, model_response_label, update_client_text, update_model_text, initialize_ui, set_button_handler, set_issue_button_handler, update_client_name
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
        self._client_message_text = "Waiting for client message..."
        self._model_response_text = "Waiting for input..."
    
    @property
    def client_message_text(self):
        """Get the current client message text."""
        return self._client_message_text
    
    @client_message_text.setter
    def client_message_text(self, value):
        """Set the client message text and update the UI."""
        self._client_message_text = value
        # Use the update_client_text function to update the Text widget
        update_client_text(value)
    
    @property
    def model_response_text(self):
        """Get the current model response text."""
        return self._model_response_text
    
    @model_response_text.setter
    def model_response_text(self, value):
        """Set the model response text and update the UI."""
        self._model_response_text = value
        # Use the update_model_text function to update the Text widget
        update_model_text(value)


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
        # Set up button handlers
        set_button_handler(self.copy_response_to_clipboard)
        set_issue_button_handler(self.report_issue)
        # Initialize the message watcher
        self.init_message_watcher()

        self.process_client_message(CONFIG_CHAT_ID)
    
    def bind_ui(self):
        """Bind the view model to UI elements."""
        # Set initial values
        update_client_text(self.view_model.client_message_text)
        update_model_text(self.view_model.model_response_text)
    
    def update_client_message(self, message):
        """Update the client message text through the view model."""
        self.view_model.client_message_text = message
        # Force UI update is handled by update_client_text
    
    def update_model_response(self, response):
        """Update the model response text through the view model."""
        self.view_model.model_response_text = response
        # Force UI update is handled by update_model_text
    
    def init_message_watcher(self):
        """Initialize the MongoDB messages watcher."""
        # Initialize watcher - no polling, only change stream
        self.message_watcher = MessagesWatcher()
        self.message_watcher.register_callback(self.handle_message_update)
        
        # Add specific chat_ids to watch using the configured chat_id
        self.message_watcher.add_chat_id_to_watch(CONFIG_CHAT_ID)
        
        self.message_watcher.start()
        print(f"Watching for changes to chat ID: {CONFIG_CHAT_ID}")
        
        # Do a single initial check to get current data
        self.manual_refresh()
    
    def manual_refresh(self):
        """Manually check for the current state of the watched chat ID."""
        if hasattr(self, 'message_watcher'):
            print(f"Manually checking chat ID: {CONFIG_CHAT_ID}...")
            result = self.message_watcher.manual_check(CONFIG_CHAT_ID)
            if result:
                print(f"Manual check completed - found messages")
            else:
                print(f"Manual check completed - no new messages")
    
    def watch_chat_id(self, chat_id):
        """Add a chat_id to the watch list."""
        if self.message_watcher.add_chat_id_to_watch(chat_id):
            print(f"Now watching chat ID: {chat_id}")
        else:
            print(f"Already watching chat ID: {chat_id}")
    
    def unwatch_chat_id(self, chat_id):
        """Remove a chat_id from the watch list."""
        if self.message_watcher.remove_chat_id_from_watch(chat_id):
            print(f"Stopped watching chat ID: {chat_id}")
        else:
            print(f"Not watching chat ID: {chat_id}")
    
    def process_client_message(self, chat_id):
        """Process the latest client message for a specific chat_id."""
        # Get the latest client message using the dedicated function
        latest_client_message = get_latest_client_message(chat_id)
        
        if latest_client_message:
            content = latest_client_message.get('text')
            created_at = latest_client_message.get('created_at')
            
            if content:
                # Update the client message display
                client_message = content
                self.update_client_message(client_message)
                
                # Log message
                print(f"New message: {content[:30]}..." if len(content) > 30 else f"New message: {content}")
            
            return True
        else:
            self.update_client_message("Waiting for client message...")
            return False
    
    def handle_message_update(self, updated_document):
        """Handle updates to messages in the database."""
        chat_id = updated_document.get('chat_id')
        messages = updated_document.get('messages', [])
        message_count = len(messages)
        
        # Extract client name from client_profile if it exists
        client_profile = updated_document.get('client_profile', {})
        client_name = client_profile.get('name')
        
        # Update the client name label
        update_client_name(client_name)
        
        # Check if there are messages
        if messages and message_count > 0:
            # Get the most recent message
            latest_message = messages[-1]
            
            # Check the role of the latest message
            role = latest_message.get('role')
            
            if role == 'client':
                self.process_client_message(chat_id)
                # Clear model response area
                self.update_model_response("Waiting for response...")
                
            elif role == 'model':
                # For model messages, update the model response display
                content = latest_message.get('text')
                if content:
                    # Format and display the model's response
                    formatted_response = content
                    self.update_model_response(formatted_response)

    
    def run(self):
        """Start the main UI loop."""
        if self.root:
            self.root.mainloop()
    
    def cleanup(self):
        """Clean up resources before application exit."""
        if hasattr(self, 'message_watcher'):
            self.message_watcher.stop()
        
        # Remove polling thread cleanup since it's no longer used
    
    def copy_response_to_clipboard(self):
        """Copy the current model response to the clipboard."""
        # Get the text from the model response text widget
        model_response_label.config(state=tk.NORMAL)
        response_text = model_response_label.get("1.0", tk.END).strip()
        model_response_label.config(state=tk.DISABLED)
        
        # Copy to clipboard using tkinter clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(response_text)
        self.root.update()  # Required to finalize clipboard operations


    def report_issue(self):
        """Handle the issue button click."""
        print("Issue detected")
        
        # Get the current client and model messages
        client_message = self.view_model.client_message_text
        
        # Get text directly from the model response widget
        model_response_label.config(state=tk.NORMAL)
        model_message = model_response_label.get("1.0", tk.END).strip()
        model_response_label.config(state=tk.DISABLED)
        
        # Print detailed information that could be useful for troubleshooting
        print(f"Issue report details:")
        print(f"Chat ID: {CONFIG_CHAT_ID}")
        print(f"Client message: {client_message}")
        print(f"Model response: {model_message}")
        
        # Provide visual feedback
        original_text = self.view_model.client_message_text
        self.update_client_message("Issue reported!")
        
        # Reset client message after 1.5 seconds
        def reset_message():
            self.update_client_message(original_text)
        
        self.root.after(1500, reset_message)

