from aurachat_helper_app.views.root_view import RootView
from aurachat_helper_app.controllers.signin_controller import SignInController
from aurachat_helper_app.controllers.onlyfans_accounts_controller import OnlyFansAccountsController
import tkinter as tk

class RootController:
    """Root controller class for handling the main application logic."""
    
    def __init__(self):
        """Initialize the root controller with its view."""
        self.view = RootView()
        self.view.set_signout_command(self.handle_signout)
        self.show_signin()
        
    def show_signin(self):
        """Show the sign-in view."""
        self.signin_controller = SignInController(self.view.root)
        self.signin_controller.pack(expand=True)
        
    def handle_signout(self):
        """Handle sign-out action."""
        # Clear any existing views
        for widget in self.view.root.winfo_children():
            if isinstance(widget, tk.Menu):
                continue  # Don't destroy the menu
            widget.pack_forget()
            
        # Show sign-in view
        self.show_signin()
        
    def start(self):
        """Start the application by launching the main window."""
        self.view.start() 