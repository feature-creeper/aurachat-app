import tkinter as tk
from tkinter import ttk

class ChatCellView:
    """Component view for displaying a single chat cell."""
    
    def __init__(self, parent, chat_info):
        """Initialize the chat cell view."""
        self.frame = tk.Frame(parent, bg='#2b2b2b')
        self.chat_info = chat_info
        
        # Chat username
        self.username_label = tk.Label(self.frame, 
                                     text=chat_info['username'],
                                     bg='#2b2b2b',
                                     fg='white')
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