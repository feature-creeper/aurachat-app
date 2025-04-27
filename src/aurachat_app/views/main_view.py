import tkinter as tk
from tkinter import ttk
from .account_view import AccountView
from .signin_view import SignInView
import sys
import os

# Add parent directory to path to import from model instead of controller
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.user_state import user_signedin
from services.menu_services import add_signout_menu_option

# UI spacing configuration variables
MODEL_VERTICAL_SPACING = 0  # Controls vertical spacing around the model response section

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

# Create a canvas for scrolling
canvas = tk.Canvas(container_frame, bg="#2c2f36", highlightthickness=0)
scrollbar = ttk.Scrollbar(container_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#2c2f36")

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a window inside the canvas to contain the scrollable frame
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Configure scrollable_frame to update scroll region when its size changes
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# List to store all account views
account_views = []

# Variables for view references
signin_view = None
client_response_label = None
model_response_label = None
account_view = None

# Initialize based on sign-in state
def initialize_views():
    """Initialize either the sign-in view or account views based on sign-in status."""
    global signin_view, account_view, client_response_label, model_response_label, _signin_handler
    
    # Clear existing views if any
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    account_views.clear()
    
    if user_signedin():
        # When signed in, we don't create any account views by default
        # They will be created based on the actual account count
        
        # Initialize variables as None since we don't have any account views yet
        account_view = None
        client_response_label = None
        model_response_label = None
        
        # Hide signin view if it exists
        if signin_view:
            if signin_view.container_frame.winfo_exists():
                signin_view.container_frame.pack_forget()
            # We'll recreate it when needed to avoid stale references
            signin_view = None
    else:
        # Create sign-in view
        signin_view = SignInView(scrollable_frame)
        
        # No account views
        account_view = None
        client_response_label = None
        model_response_label = None
        
        # Reattach the signin handler if available
        if _signin_handler:
            signin_view.set_signin_handler(_signin_handler)

# Function to add a new account view
def add_account_view():
    """
    Create a new AccountView instance and add it to the scrollable frame.
    
    Returns:
        AccountView: The newly created account view or None if user isn't signed in
    """
    if not user_signedin():
        return None
        
    new_account_view = AccountView(scrollable_frame, MODEL_VERTICAL_SPACING)
    account_views.append(new_account_view)
    
    # Update scroll region
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    # Update window size to accommodate the new view
    adjust_window_size()
    
    return new_account_view

# Function to get all account views
def get_account_views():
    """Return the list of all account views."""
    return account_views

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
    global signin_view, account_view
    
    # Destroy all children in scrollable_frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    # Clear all account views
    account_views.clear()
    
    # Reset view references
    signin_view = None
    account_view = None
    
    # Reinitialize views to show sign-in view
    initialize_views()
    
    print("User signed out successfully")

# Public functions to access the AccountView methods (for the first account view)
def update_client_name(name):
    """Update the client name label with the provided name."""
    if account_view:
        account_view.update_client_name(name)

def update_client_text(text):
    """Update client response text and adjust height."""
    if account_view:
        account_view.update_client_text(text)

def update_model_text(text):
    """Update model response text and adjust height."""
    if account_view:
        account_view.update_model_text(text)

# Set the button handlers
def set_button_handler(handler_function):
    """Set the handler function for the copy button."""
    if account_view:
        account_view.set_button_handler(handler_function)

def set_issue_button_handler(handler_function):
    """Set the handler function for the issue button."""
    if account_view:
        account_view.set_issue_button_handler(handler_function)

# Set the signin handler
def set_signin_handler(handler_function):
    """Set the handler function for the sign-in button."""
    global _signin_handler
    # Store for reuse after sign-out
    _signin_handler = handler_function
    
    if signin_view:
        signin_view.set_signin_handler(handler_function)

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