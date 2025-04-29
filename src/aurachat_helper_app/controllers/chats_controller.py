from views.chats_view import ChatsView
import tkinter as tk

class ChatsController:
    """Controller class for managing chats."""
    
    def __init__(self, parent, accounts_controller):
        """Initialize the chats controller."""
        self.parent = parent
        self.accounts_controller = accounts_controller
        self.view = ChatsView(parent)
        self.chats = []
        self.selected_chat = None
        
        # Set up back button
        self.view.set_back_command(self.handle_back)
        
        # Add sample chats
        self.add_chat({'username': 'chat1'})
        self.add_chat({'username': 'chat2'})
        
    def handle_chat_click(self, chat_info):
        """Handle chat cell click event."""
        self.selected_chat = chat_info
        self.view.set_selected_chat(chat_info)
        
    def handle_back(self):
        """Handle back button click."""
        self.view.frame.pack_forget()  # Hide chats view
        self.accounts_controller.pack(expand=True, fill=tk.BOTH)  # Show accounts view
        
    def add_chat(self, chat_info):
        """Add a chat to the list and display."""
        self.chats.append(chat_info)
        self.view.add_chat(chat_info, lambda: self.handle_chat_click(chat_info))
            
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        self.view.pack(**kwargs) 