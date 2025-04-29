import tkinter as tk
from tkinter import ttk

class NavbarView:
    """A navigation bar view that contains buttons for different sections of the app."""
    
    def __init__(self, parent_frame):
        """
        Initialize the navigation bar.
        
        Args:
            parent_frame: The parent frame to pack this navbar into
        """
        self.container_frame = tk.Frame(parent_frame, bg="#2c2f36")
        self.container_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create the Accounts button
        self.accounts_button = ttk.Button(
            self.container_frame,
            text="Accounts",
            command=self._on_accounts_click
        )
        
        # Store the click handler (will be set by set_accounts_handler)
        self._accounts_handler = None
    
    def set_accounts_handler(self, handler_function):
        """
        Set the handler function for the Accounts button click.
        
        Args:
            handler_function: Function to call when Accounts button is clicked
        """
        print("Setting accounts handler")
        self._accounts_handler = handler_function
    
    def _on_accounts_click(self):
        """Handle the Accounts button click event."""
        print("Accounts button clicked")
        if self._accounts_handler:
            print("Calling accounts handler")
            self._accounts_handler()
        else:
            print("No accounts handler set")
            
    def update_visibility(self, is_chats_visible):
        """
        Update the visibility of the Accounts button based on container state.
        
        Args:
            is_chats_visible: Boolean indicating if chats container is visible
        """
        if is_chats_visible:
            # Show Accounts button if chats container is visible
            self.accounts_button.pack(side=tk.LEFT, padx=5)
        else:
            # Hide Accounts button if chats container is not visible
            self.accounts_button.pack_forget() 