import tkinter as tk
from tkinter import ttk

class AccountView:
    """A view that displays account information."""
    
    def __init__(self, parent):
        """
        Initialize the account view.
        
        Args:
            parent: The parent frame to pack this view into
        """
        self.parent = parent
        
        # Create main frame
        self.frame = tk.Frame(parent, bg="#2c2f36", padx=10, pady=10)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create account info frame
        self.info_frame = tk.Frame(self.frame, bg="#2c2f36")
        self.info_frame.pack(fill=tk.X)
        
        # Create labels for account info
        self.name_label = tk.Label(
            self.info_frame,
            text="Account Name:",
            bg="#2c2f36",
            fg="white",
            font=("Helvetica", 12)
        )
        self.name_label.pack(anchor="w")
        
        self.email_label = tk.Label(
            self.info_frame,
            text="Email:",
            bg="#2c2f36",
            fg="white",
            font=("Helvetica", 12)
        )
        self.email_label.pack(anchor="w")
        
        # Create a separator
        self.separator = ttk.Separator(self.frame, orient="horizontal")
        self.separator.pack(fill=tk.X, pady=5)
    
    def update_name(self, name):
        """
        Update the account name label.
        
        Args:
            name (str): The account name to display
        """
        self.name_label.config(text=f"Account Name: {name}")
    
    def update_email(self, email):
        """
        Update the email label.
        
        Args:
            email (str): The email to display
        """
        self.email_label.config(text=f"Email: {email}") 