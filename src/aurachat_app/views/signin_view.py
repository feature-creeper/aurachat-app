import tkinter as tk
from tkinter import ttk
import re

class SignInView:
    """Class representing the sign-in view components."""
    
    def __init__(self, parent):
        """Initialize the SignInView with all UI elements."""
        self.parent = parent
        
        # Button handler callback
        self.signin_handler = None
        
        # Create main container frame for the entire SignInView
        self.container_frame = tk.Frame(
            self.parent,
            bg="#2c2f36",  # Match background
            padx=20,
            pady=20
        )
        self.container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a placeholder label
        self.signin_label = tk.Label(
            self.container_frame,
            text="Sign In",
            font=("Arial", 18, "bold"),
            bg="#2c2f36",
            fg="#ffffff"
        )
        self.signin_label.pack(pady=20)
        
        # Add an empty frame for future content
        self.content_frame = tk.Frame(
            self.container_frame,
            bg="#2c2f36",
            padx=20,
            pady=20,
            highlightbackground="#4a5568",
            highlightthickness=1
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create email entry field
        self.email_label = tk.Label(
            self.content_frame,
            text="Enter Email:",
            font=("Arial", 12),
            bg="#2c2f36",
            fg="#ffffff",
            anchor="w"
        )
        self.email_label.pack(fill=tk.X, padx=5, pady=(5, 5), anchor="w")
        
        # Create text entry field
        self.entry_frame = tk.Frame(
            self.content_frame,
            bg="#2c2f36",
            highlightbackground="#4a5568",
            highlightthickness=1
        )
        self.entry_frame.pack(fill=tk.X, padx=5, pady=(0, 15))
        
        self.email_entry = tk.Entry(
            self.entry_frame,
            font=("Arial", 12),
            bg="#1e2129",
            fg="#ffffff",
            insertbackground="#ffffff",  # Cursor color
            relief=tk.FLAT,
            bd=10
        )
        self.email_entry.pack(fill=tk.X, expand=True)
        
        # Error message label (hidden initially)
        self.error_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10),
            bg="#2c2f36",
            fg="#ff4d4d",  # Red text for errors
            anchor="w"
        )
        self.error_label.pack(fill=tk.X, padx=5, pady=(0, 5), anchor="w")
        
        # Set up button style
        self._setup_button_style()
        
        # Create sign-in button
        self.signin_button = ttk.Button(
            self.content_frame,
            text="Sign In",
            style="SignIn.TButton",
            command=self._signin_clicked
        )
        self.signin_button.pack(pady=(10, 5), padx=5, ipady=8)
    
    def _setup_button_style(self):
        """Set up the button style."""
        style = ttk.Style()
        style.theme_use("default")  # Use a consistent base theme
        
        # Style for SignIn button
        style.configure("SignIn.TButton",
            font=("Arial", 14),
            foreground="white",
            background="#007aff",  # Blue color
            padding=(20, 0),
            relief="flat"
        )
        
        # Apply the same look to all states for SignIn button
        style.map("SignIn.TButton",
            foreground=[("active", "white"), ("pressed", "white"), ("disabled", "white"), ("focus", "white")],
            background=[("active", "#007aff"), ("pressed", "#007aff"), ("disabled", "#007aff"), ("focus", "#007aff")]
        )
    
    def _validate_email(self, email):
        """
        Validate email format.
        
        Args:
            email: The email string to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        # Basic email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _signin_clicked(self):
        """Handle sign-in button click."""
        if self.signin_handler:
            # Get the entered email
            email = self.email_entry.get().strip()
            
            # Validate email format
            if not email:
                self.error_label.config(text="Please enter your email address")
                return
            elif not self._validate_email(email):
                self.error_label.config(text="Please enter a valid email address")
                return
            
            # Clear any error message
            self.error_label.config(text="")
            
            # Call the handler with the email
            self.signin_handler(email)
    
    def set_signin_handler(self, handler_function):
        """Set the handler function for the sign-in button."""
        self.signin_handler = handler_function 