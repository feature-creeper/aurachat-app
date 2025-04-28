import tkinter as tk
from tkinter import ttk
from .signin_view import SignInView
from .navbar_view import NavbarView
from .chats_container_view import ChatsContainerView
from .accounts_container_view import AccountsContainerView
import sys
import os

# Add parent directory to path to import from model instead of controller
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.user_state import user_signedin
from services.menu_services import add_signout_menu_option

# Store the sign-in handler for reuse
_signin_handler = None

# Create the root window
root = tk.Tk()
root.title("AuraChat")
root.geometry("450x600")  # Increased height to accommodate multiple accounts
root.minsize(400, 400)  # Increased minimum height
root.attributes('-topmost', True)  # Stay on top of other windows

# Use standard colors for macOS Dark Mode compatibility
root.configure(bg="#2c2f36")  # Standard background color

# Create a scrollable container for all account views
container_frame = tk.Frame(root, bg="#2c2f36")
container_frame.pack(fill=tk.BOTH, expand=True)

# Create the navbar
navbar = NavbarView(container_frame)

# Create a content frame to hold the containers
content_frame = tk.Frame(container_frame, bg="#2c2f36")
content_frame.pack(fill=tk.BOTH, expand=True)

# Create the containers
chats_container = ChatsContainerView(content_frame)
accounts_container = AccountsContainerView(content_frame)

# Initially show chats container and hide accounts container
chats_container.container_frame.pack(fill=tk.BOTH, expand=True)
accounts_container.container_frame.pack_forget()

# Variables for view references
signin_view = None

def show_chats_container():
    """Show the chats container and hide the accounts container."""
    # Hide accounts container first
    accounts_container.container_frame.pack_forget()
    # Show chats container
    chats_container.container_frame.pack(fill=tk.BOTH, expand=True)
    # Update the window
    root.update_idletasks()
    # Force a redraw
    root.update()
    # Print debug info
    print("Showing chats container")

def show_accounts_container():
    """Show the accounts container and hide the chats container."""
    # Hide chats container first
    chats_container.container_frame.pack_forget()
    # Show accounts container
    accounts_container.container_frame.pack(fill=tk.BOTH, expand=True)
    # Update the window
    root.update_idletasks()
    # Force a redraw
    root.update()
    # Print debug info
    print("Showing accounts container")

# Initialize based on sign-in state
def initialize_views():
    """Initialize either the sign-in view or chat views based on sign-in status."""
    global signin_view, _signin_handler
    
    # Clear existing views if any
    chats_container.clear_chat_views()
    accounts_container.clear_account_views()
    
    if user_signedin():
        # Hide signin view if it exists
        if signin_view:
            if signin_view.container_frame.winfo_exists():
                signin_view.container_frame.pack_forget()
            # We'll recreate it when needed to avoid stale references
            signin_view = None
        # Show chats container
        show_chats_container()
    else:
        # Create sign-in view
        signin_view = SignInView(chats_container.scrollable_frame)
        
        # Reattach the signin handler if available
        if _signin_handler:
            signin_view.set_signin_handler(_signin_handler)
        
        # Show chats container with sign-in view
        show_chats_container()

# Function to add a new chat view
def add_chat_view():
    """
    Create a new ChatView instance and add it to the chats container.
    
    Returns:
        ChatView: The newly created chat view or None if user isn't signed in
    """
    if not user_signedin():
        return None
        
    return chats_container.add_chat_view()

# Function to get all chat views
def get_chat_views():
    """Return the list of all chat views."""
    return chats_container.get_chat_views()

# Function to add a new account view
def add_account_view():
    """
    Create a new AccountView instance and add it to the accounts container.
    
    Returns:
        AccountView: The newly created account view or None if user isn't signed in
    """
    if not user_signedin():
        return None
        
    return accounts_container.add_account_view()

# Function to get all account views
def get_account_views():
    """Return the list of all account views."""
    return accounts_container.get_account_views()

# Function to adjust window size based on content
def adjust_window_size():
    """Update window size to fit all contents."""
    # Update all idle tasks to get correct widget sizes
    root.update_idletasks()
    
    # Get the required width and height
    required_width = max(root.winfo_reqwidth(), 450)
    required_height = min(max(root.winfo_reqheight(), 400), 800)  # Cap height at 800
    
    # Set the window size
    root.geometry(f"{required_width}x{required_height}")

# Initialize UI function to be called externally
def initialize_ui():
    """Initialize and show the UI without starting mainloop."""
    # Add "Sign out" menu option
    add_signout_menu_option(root, handle_signout)
    
    # Adjust window size after initialization
    root.after(100, adjust_window_size)  # Small delay to ensure all widgets are ready
    
    return root

def handle_signout():
    """Handle the sign out action from the menu."""
    print("User signing out...")
    
    # Import here to avoid circular import
    from model.user_state import set_user_signed_in
    
    # Set user as signed out
    set_user_signed_in(False)
    
    # Clear all views first
    global signin_view
    
    # Clear all chat views and account views
    chats_container.clear_chat_views()
    accounts_container.clear_account_views()
    
    # Reset view references
    signin_view = None
    
    # Reinitialize views to show sign-in view
    initialize_views()
    
    print("User signed out successfully")

# Public functions to access the ChatView methods (for the first chat view)
def update_client_name(name):
    """Update the client name label with the provided name."""
    chat_views = get_chat_views()
    if chat_views:
        chat_views[0].update_client_name(name)

def update_client_text(text):
    """Update client response text and adjust height."""
    chat_views = get_chat_views()
    if chat_views:
        chat_views[0].update_client_text(text)

def update_model_text(text):
    """Update model response text and adjust height."""
    chat_views = get_chat_views()
    if chat_views:
        chat_views[0].update_model_text(text)

# Set the button handlers
def set_button_handler(handler_function):
    """Set the handler function for the copy button."""
    chat_views = get_chat_views()
    if chat_views:
        chat_views[0].set_button_handler(handler_function)

def set_issue_button_handler(handler_function):
    """Set the handler function for the issue button."""
    chat_views = get_chat_views()
    if chat_views:
        chat_views[0].set_issue_button_handler(handler_function)

# Set the signin handler
def set_signin_handler(handler_function):
    """Set the handler function for the sign-in button."""
    global _signin_handler
    # Store for reuse after sign-out
    _signin_handler = handler_function
    
    if signin_view:
        signin_view.set_signin_handler(handler_function)

# Set the accounts handler
def set_accounts_handler(handler_function):
    """Set the handler function for the accounts button."""
    if navbar:
        navbar.set_accounts_handler(handler_function)

# DO NOT call initialize_views() here at the module level
# It will be called at the end of the file

# Only start mainloop if this file is run directly
if __name__ == "__main__":
    # Initial UI setup
    initialize_views()
    root.mainloop()
else:
    # When imported as a module, also do initial setup
    initialize_views()