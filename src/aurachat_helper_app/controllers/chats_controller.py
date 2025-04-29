from views.chats_view import ChatsView
from aurachat_helper_app.services.chat_service import ChatService
import tkinter as tk

class ChatsController:
    """Controller class for managing chats."""
    
    def __init__(self, parent, accounts_controller, account_id: str):
        """Initialize the chats controller."""
        self.parent = parent
        self.accounts_controller = accounts_controller
        self.account_id = account_id
        self.view = ChatsView(parent)
        self.chats = []
        self.selected_chat = None
        self.chat_service = ChatService()
        
        # Set up back button
        self.view.set_back_command(self.handle_back)
        
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
        # Format chat info for display with safe access to nested fields
        fan = chat_info.get('fan') or {}
        last_message = chat_info.get('lastMessage') or {}
        
        # Clean HTML from last message if present
        last_message_text = last_message.get('text', '')
        if last_message_text.startswith('<p>') and last_message_text.endswith('</p>'):
            last_message_text = last_message_text[3:-4]  # Remove <p> and </p>
        
        display_info = {
            'display_name': fan.get('name', '') if fan else '',
            'last_message': last_message_text
        }
        self.view.add_chat(display_info, lambda: self.handle_chat_click(chat_info))
            
    def pack(self, **kwargs):
        """Pack the view into its parent and fetch chats."""
        self.view.pack(**kwargs)
        # Fetch and display chats
        chats_data = self.chat_service.get_chats_for_account(self.account_id)
        if chats_data:
            # Clear existing chats
            self.chats = []
            for widget in self.view.chats_frame.winfo_children():
                widget.destroy()
            # Add new chats
            for chat in chats_data:
                self.add_chat(chat) 