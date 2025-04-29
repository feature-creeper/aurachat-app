import tkinter as tk
from tkinter import ttk
import re

class SignInView:
    """Sign-in view class for handling user authentication."""
    
    def __init__(self, parent):
        """Initialize the sign-in view with input fields."""
        self.frame = ttk.Frame(parent)
        
        # Email field
        ttk.Label(self.frame, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self.frame)
        self.email_entry.pack(pady=5)
        
        # Sign in button
        self.signin_button = ttk.Button(self.frame, text="Sign In")
        self.signin_button.pack(pady=20)
        
    def pack(self, **kwargs):
        """Pack the sign-in frame into its parent."""
        self.frame.pack(**kwargs)
        
    def get_email(self):
        """Get the entered email."""
        return self.email_entry.get()
        
    def is_valid_email(self):
        """Check if the entered email is valid."""
        email = self.get_email()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email)) 