from aurachat_helper_app.views.signin_view import SignInView
import tkinter.messagebox as messagebox
from aurachat_helper_app.controllers.onlyfans_accounts_controller import OnlyFansAccountsController
import tkinter as tk
from aurachat_helper_app.managers.user_manager import UserManager

class SignInController:
    """Sign-in controller class for handling authentication logic."""
    
    def __init__(self, parent):
        """Initialize the sign-in controller with its view."""
        self.parent = parent
        self.view = SignInView(parent)
        self.view.signin_button.config(command=self.handle_signin)
        self.user_manager = UserManager()
        print("SignInController: Initialized")
        
    def handle_signin(self):
        """Handle the sign-in button click event."""
        print("SignInController: Sign in button clicked")
        if not self.view.is_valid_email():
            print("SignInController: Invalid email")
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return
            
        email = self.view.get_email()
        print(f"SignInController: Attempting sign in with email: {email}")
        try:
            success = self.user_manager.sign_in(email)
            print(f"SignInController: Sign in result: {success}")
            
            if not success:
                print("SignInController: Sign in failed - user not found")
                messagebox.showerror("Sign In Error", "User not found")
                return
            
            print("SignInController: Sign in successful, showing accounts view")
            # Show OnlyFans accounts view
            self.view.frame.pack_forget()  # Hide sign-in view
            self.accounts_controller = OnlyFansAccountsController(self.parent, self.user_manager)
            self.accounts_controller.pack(expand=True, fill=tk.BOTH)
        except Exception as e:
            print(f"SignInController: Error during sign in: {e}")
            messagebox.showerror("Sign In Error", f"An error occurred: {str(e)}")
        
    def pack(self, **kwargs):
        """Pack the sign-in view into its parent."""
        self.view.pack(**kwargs) 