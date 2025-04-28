import sys
import os
import tkinter as tk
import threading
import time


# Add the parent directory to the Python path so we can import from views
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from views.main_view import (
    root,
    update_client_text,
    update_model_text,
    initialize_ui,
    set_button_handler,
    set_issue_button_handler,
    update_client_name,
    add_chat_view,
    get_chat_views,
    set_signin_handler,
    initialize_views,
    show_chats_container,
    show_accounts_container,
    set_accounts_handler,
    add_account_view
)
from db.db_watcher import MessagesWatcher
from db.db_client import get_latest_client_message, fetch_connected_accounts, find_user_by_email, list_mongodb_info
from model.user_state import user_signedin, set_user_signed_in, get_current_user_id, set_current_user_id

# Import the chat_id from config.py using absolute path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, project_root)  # Ensure project root is first in path

try:
    from config import chat_id as CONFIG_CHAT_ID
except ImportError:
    print("Warning: Could not import config.py, using default chat_id")
    CONFIG_CHAT_ID = 6172560874  # Default value from config.py

# The user_id will be set dynamically upon sign-in
# It should be None in config.py

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
        
        # Initialize user ID as None (will be set on sign-in)
        self.current_user_id = None
        
        # Set up sign-in handler (always do this regardless of sign-in state)
        # Store this handler as a bound method that can be reused
        self.signin_handler_method = self.handle_signin
        set_signin_handler(self.signin_handler_method)
        
        # Set up accounts handler
        set_accounts_handler(self.handle_accounts_click)
        
        # Check if user is signed in
        if user_signedin():
            # Only set up handlers and fetch data if signed in
            set_button_handler(self.copy_response_to_clipboard)
            set_issue_button_handler(self.report_issue)
            # Initialize the message watcher
            self.init_message_watcher()

            # Skip fetching accounts here - we don't have a user_id yet
            # This will only run if the app is restarted while signed in,
            # which isn't fully supported without persistent storage of the user_id
            
            print("User is signed in but no user ID is available. Please sign in again.")
            # Force sign out to avoid inconsistent state
            set_user_signed_in(False)
            import views.main_view as main_view
            main_view.initialize_views()
        else:
            # Not signed in - don't initialize message watcher or fetch accounts
            print("User not signed in - showing sign-in view")
    
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
        # Get the text from the first chat view's model response
        chat_views = get_chat_views()
        if chat_views:
            chat_view = chat_views[0]
            chat_view.model_response_label.config(state=tk.NORMAL)
            response_text = chat_view.model_response_label.get("1.0", tk.END).strip()
            chat_view.model_response_label.config(state=tk.DISABLED)
            
            # Copy to clipboard using tkinter clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(response_text)
            self.root.update()  # Required to finalize clipboard operations


    def report_issue(self):
        """Handle the issue button click."""
        print("Issue detected")
        
        # Get the current client and model messages
        client_message = self.view_model.client_message_text
        
        # Get text from the first chat view's model response
        chat_views = get_chat_views()
        if chat_views:
            chat_view = chat_views[0]
            chat_view.model_response_label.config(state=tk.NORMAL)
            model_message = chat_view.model_response_label.get("1.0", tk.END).strip()
            chat_view.model_response_label.config(state=tk.DISABLED)
            
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

    def fetch_and_print_connected_accounts(self, user_identifier):
        """
        Fetch and print connected accounts for a specific user.
        
        Args:
            user_identifier: Either a chat_id (int) or MongoDB _id (str)
            
        Returns:
            int: Number of connected accounts found
        """
        accounts = fetch_connected_accounts(user_identifier)
        account_count = 0
        
        if accounts:
            account_count = len(accounts)
            id_type = "ObjectId" if isinstance(user_identifier, str) else "chat_id"
            print(f"Connected accounts for user ({id_type}: {user_identifier}):")
            for account in accounts:
                print(f"  - {account}")
        else:
            print(f"No connected accounts found for user identifier: {user_identifier}")
            
        return account_count

    def update_first_account_view_references(self, account_view):
        """Update global references for the first account view."""
        # This is a helper function to update references to account view elements
        # We need to do this since we're now creating account views dynamically
        
        # Import the main_view module to update its variables
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import views.main_view as main_view
        
        # Update references if the account view is valid
        if account_view:
            main_view.client_response_label = account_view.client_response_label
            main_view.model_response_label = account_view.model_response_label

    def handle_signin(self, email):
        """
        Handle the sign-in process with the provided email.
        
        Args:
            email: The email address entered by the user
        """
        # Don't proceed if we're already in the process of signing in
        if hasattr(self, '_signing_in') and self._signing_in:
            print("Sign-in already in progress, ignoring duplicate request")
            return
            
        try:
            # Set flag to prevent duplicate sign-in
            self._signing_in = True
            
            print(f"Attempting to sign in with email: {email}")
            
            # Get MongoDB database info
            list_mongodb_info()
            
            # Find the user by email in the database
            user = find_user_by_email(email)
            
            if user:
                # User found, set as signed in
                print(f"User found: {user.get('name', 'Unknown User')}")
                
                # Print user details for debugging
                print(f"User details: _id={user.get('_id')}, type={type(user.get('_id'))}")
                if 'accounts' in user:
                    print(f"User has {len(user['accounts'])} accounts in the user document")
                    print(f"Accounts: {user['accounts']}")
                else:
                    print("User has no 'accounts' field in the user document")
                    print(f"Available fields: {list(user.keys())}")
                
                # Store the user ID in the user_state module - convert ObjectId to string if needed
                user_id = user.get('_id')
                if hasattr(user_id, '__str__'):
                    user_id = str(user_id)  # Convert ObjectId to string
                    print(f"Converted _id to string: {user_id}")
                    
                set_current_user_id(user_id)
                
                # Set the user as signed in
                set_user_signed_in(True)
                
                # Reinitialize the UI to show account views
                import views.main_view as main_view
                main_view.initialize_views()
                
                # Now initialize the message watcher and other signed-in functionality
                set_button_handler(self.copy_response_to_clipboard)
                set_issue_button_handler(self.report_issue)
                self.init_message_watcher()
                
                # Debug: Print the user_id that will be used
                print(f"About to fetch accounts using user_id: {user_id} (type: {type(user_id)})")
                
                # Fetch connected accounts and create account views
                accounts = fetch_connected_accounts(user_id)
                
                # Debug: Print the accounts result
                print(f"fetch_connected_accounts returned: {accounts}")
                
                # Create chat views based on the actual count
                if accounts and len(accounts) > 0:
                    account_count = len(accounts)
                    print(f"Found {account_count} connected accounts")
                    
                    for i, account_name in enumerate(accounts):
                        # Create a new chat view
                        new_chat_view = add_chat_view()
                        
                        # Update the account name
                        if new_chat_view:
                            new_chat_view.update_client_name(account_name)
                    
                    print(f"Successfully signed in with {account_count} connected accounts!")
                else:
                    print("No connected accounts found for the signed-in user")
                    
                print(f"Successfully signed in as {email}!")
            else:
                # User not found
                print(f"No user found with email: {email}")
                
                # Show error on the UI
                self._show_signin_error(f"No user with email '{email}' exists. Please check and try again.")
                
        finally:
            # Clear sign-in flag when done
            self._signing_in = False

    def _show_signin_error(self, error_message):
        """
        Show an error message in the sign-in view.
        
        Args:
            error_message: The error message to display
        """
        # Import here to avoid circular import
        import views.main_view as main_view
        
        # Make sure signin_view exists and has an error_label
        if hasattr(main_view, 'signin_view') and main_view.signin_view:
            if hasattr(main_view.signin_view, 'error_label'):
                main_view.signin_view.error_label.config(text=error_message)

    def handle_accounts_click(self):
        """Handle the accounts button click event."""
        if user_signedin():
            # Show the accounts container
            show_accounts_container()
            
            # Get the current user ID
            user_id = get_current_user_id()
            if user_id:
                # Fetch connected accounts
                accounts = fetch_connected_accounts(user_id)
                if accounts:
                    # Create an account view for each account
                    for account_name in accounts:
                        account_view = add_account_view()
                        if account_view:
                            account_view.update_name(account_name)
                else:
                    print("No connected accounts found")
        else:
            self._show_signin_error("Please sign in to view accounts")

