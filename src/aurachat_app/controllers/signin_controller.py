from views.signin_view import SignInView
import tkinter.messagebox as messagebox
from controllers.onlyfans_accounts_controller import OnlyFansAccountsController
import tkinter as tk

class SignInController:
    """Sign-in controller class for handling authentication logic."""
    
    def __init__(self, parent):
        """Initialize the sign-in controller with its view."""
        self.parent = parent
        self.view = SignInView(parent)
        self.view.signin_button.config(command=self.handle_signin)
        
    def handle_signin(self):
        """Handle the sign-in button click event."""
        if not self.view.is_valid_email():
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return
            
        email = self.view.get_email()
        # TODO: Implement actual authentication logic
        print(f"Attempting to sign in with email: {email}")
        
        # Show OnlyFans accounts view
        self.view.frame.pack_forget()  # Hide sign-in view
        self.accounts_controller = OnlyFansAccountsController(self.parent)
        self.accounts_controller.pack(expand=True, fill=tk.BOTH)
        
    def pack(self, **kwargs):
        """Pack the sign-in view into its parent."""
        self.view.pack(**kwargs) 