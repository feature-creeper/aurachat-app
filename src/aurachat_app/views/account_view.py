import tkinter as tk
from tkinter import ttk
from .container_manager import show_chats_container

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
        
        # Bind click event to the entire frame
        self.frame.bind("<Button-1>", self._on_click)
        self.info_frame.bind("<Button-1>", self._on_click)
        self.name_label.bind("<Button-1>", self._on_click)
        self.email_label.bind("<Button-1>", self._on_click)
        
        # Add hover effect
        self.frame.bind("<Enter>", self._on_enter)
        self.frame.bind("<Leave>", self._on_leave)
    
    def _on_click(self, event):
        """Handle click event on the account view."""
        show_chats_container()
    
    def _on_enter(self, event):
        """Handle mouse enter event."""
        self.frame.configure(bg="#3c3f46")  # Slightly lighter background
        self.info_frame.configure(bg="#3c3f46")
    
    def _on_leave(self, event):
        """Handle mouse leave event."""
        self.frame.configure(bg="#2c2f36")  # Original background
        self.info_frame.configure(bg="#2c2f36")
    
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