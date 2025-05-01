import tkinter as tk
from tkinter import ttk
from .components.chat_cell_view import ChatCellView
from .components.selected_chat_cell_view import SelectedChatCellView

class ChatsView:
    """View class for displaying and managing chats."""
    
    def __init__(self, parent):
        """Initialize the chats view."""
        self.frame = tk.Frame(parent, bg='#2b2b2b')
        
        # Header with back button
        header_frame = tk.Frame(self.frame, bg='#2b2b2b')
        header_frame.pack(fill=tk.X, pady=10)
        
        # Back frame
        self.back_frame = tk.Frame(header_frame, bg='#2b2b2b')
        self.back_frame.pack(side=tk.LEFT, padx=5)
        self.back_label = tk.Label(self.back_frame,
                                 text="← Back",
                                 bg='#2b2b2b',
                                 fg='white',
                                 font=('Helvetica', 10),
                                 padx=10,
                                 pady=5)
        self.back_label.pack()
        self.back_frame.bind('<Button-1>', lambda e: self._on_back_click())
        self.back_label.bind('<Button-1>', lambda e: self._on_back_click())
        
        tk.Label(header_frame, 
                text="Chats", 
                font=('Helvetica', 14, 'bold'),
                bg='#2b2b2b',
                fg='white').pack(side=tk.LEFT, padx=5)
        
        # Selected chat area
        self.selected_chat_frame = tk.Frame(self.frame, bg='#2b2b2b')
        self.selected_chat_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Chats list
        self.chats_frame = tk.Frame(self.frame, bg='#2b2b2b')
        self.chats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def _on_back_click(self):
        """Handle back click."""
        if hasattr(self, 'back_command'):
            self.back_command()
        
    def on_generate(self):
        """Handle generate button click."""
        if hasattr(self, 'generate_command'):
            self.generate_command()
        
    def on_sync(self):
        """Handle sync button click."""
        if hasattr(self, 'sync_command'):
            self.sync_command()
        
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        self.frame.pack(**kwargs)
        
    def set_selected_chat(self, chat_info: dict):
        """Set the selected chat information."""
        # Clear any existing selected chat
        for widget in self.selected_chat_frame.winfo_children():
            widget.destroy()
            
        # Create and show the new selected chat cell
        self.selected_chat_cell = SelectedChatCellView(self.selected_chat_frame, chat_info)
        self.selected_chat_cell.set_generate_command(self.on_generate)
        self.selected_chat_cell.set_sync_command(self.on_sync)
        self.selected_chat_cell.pack()
        
    def add_chat(self, chat_info, click_command):
        """Add a chat to the display."""
        cell = ChatCellView(self.chats_frame, chat_info)
        cell.set_click_command(click_command)
        cell.pack(pady=2)
        
    def clear_chats(self):
        """Clear all displayed chats."""
        for widget in self.chats_frame.winfo_children():
            widget.destroy()
            
    def set_back_command(self, command):
        """Set the command for the back action."""
        self.back_command = command
        
    def set_generate_command(self, command):
        """Set the command for the generate action."""
        self.generate_command = command
        
    def set_sync_command(self, command):
        """Set the command for the sync action."""
        self.sync_command = command 