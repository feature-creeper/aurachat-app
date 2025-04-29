import tkinter as tk
from tkinter import ttk

class OnlyFansAccountCellView:
    """Component view for displaying a single OnlyFans account cell."""
    
    def __init__(self, parent, account_info):
        """Initialize the account cell view."""
        self.frame = ttk.Frame(parent)
        self.account_info = account_info
        
        # Account username
        self.username_label = ttk.Label(self.frame, text=account_info['username'])
        self.username_label.pack(side=tk.LEFT, padx=5)
        
        # Make both the frame and label clickable
        self.frame.bind('<Button-1>', self._on_click)
        self.username_label.bind('<Button-1>', self._on_click)
        
    def _on_click(self, event):
        """Handle click event."""
        if hasattr(self, 'click_command'):
            self.click_command()
            
    def set_click_command(self, command):
        """Set the command to execute when clicked."""
        self.click_command = command
        
    def pack(self, **kwargs):
        """Pack the cell into its parent."""
        self.frame.pack(fill=tk.X, **kwargs) 