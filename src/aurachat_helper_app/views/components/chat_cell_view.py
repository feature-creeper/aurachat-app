import tkinter as tk
from tkinter import ttk

class ChatCellView:
    """Component view for displaying a single chat cell."""
    
    def __init__(self, parent, chat_info):
        """Initialize the chat cell view."""
        self.frame = tk.Frame(parent, bg='#2b2b2b')
        self.chat_info = chat_info
        
        # Left container for fan name and last message
        left_container = tk.Frame(self.frame, bg='#2b2b2b')
        left_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Fan name
        self.fan_name_label = tk.Label(left_container, 
                                     text=chat_info['display_name'],
                                     bg='#2b2b2b',
                                     fg='white',
                                     font=('Helvetica', 10, 'bold'))
        self.fan_name_label.pack(anchor=tk.W)
        
        # Last message
        self.last_message_label = tk.Label(left_container,
                                         text=chat_info['last_message'],
                                         bg='#2b2b2b',
                                         fg='#a0a0a0',
                                         font=('Helvetica', 9))
        self.last_message_label.pack(anchor=tk.W)
        
        # Unread count if any
        if chat_info.get('unread_count', 0) > 0:
            unread_frame = tk.Frame(self.frame, bg='#4CAF50')
            unread_frame.pack(side=tk.RIGHT, padx=5)
            self.unread_label = tk.Label(unread_frame,
                                       text=str(chat_info['unread_count']),
                                       bg='#4CAF50',
                                       fg='white',
                                       font=('Helvetica', 9),
                                       padx=5,
                                       pady=2)
            self.unread_label.pack()
        
        # Make both the frame and labels clickable
        self.frame.bind('<Button-1>', self._on_click)
        self.fan_name_label.bind('<Button-1>', self._on_click)
        self.last_message_label.bind('<Button-1>', self._on_click)
        
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