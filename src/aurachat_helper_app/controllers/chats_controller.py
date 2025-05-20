from aurachat_helper_app.views.chats_view import ChatsView
from aurachat_helper_app.views.components.chat_cell_view import ChatCellView
from aurachat_helper_app.views.components.selected_chat_cell_view import SelectedChatCellView
from aurachat_helper_app.services.chat_service import ChatService
from aurachat_helper_app.services.message_service import MessageService
from aurachat_helper_app.services.generate_message_service import GenerateMessageService
from aurachat_helper_app.models.chat import Chat
from aurachat_helper_app.api.aurachat_webportal_client import AuraChatWebPortalClient
from aurachat_helper_app.db.db_client import db_client
import tkinter as tk
from datetime import datetime
from typing import List
import asyncio
import threading

# Global event loop
_loop = None

def get_event_loop():
    """Get or create the global event loop."""
    global _loop
    if _loop is None:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop

class ChatsController:
    """Controller class for managing chats."""
    
    def __init__(self, parent, accounts_controller, account_id: str):
        """Initialize the chats controller."""
        self.parent = parent
        self.accounts_controller = accounts_controller
        self.account_id = account_id
        self.view = ChatsView(parent)
        self.chats: List[Chat] = []
        self.selected_chat = None
        self.chat_service = ChatService()
        self.message_service = MessageService()
        self.generate_message_service = GenerateMessageService()
        self.webportal_client = AuraChatWebPortalClient()
        self.db_client = db_client
        
        # Set up commands
        self.view.set_back_command(self.handle_back)
        self.view.set_generate_command(self.handle_generate)
        self.view.set_sync_command(self.handle_sync)
        
    def format_time(self, iso_time: str) -> str:
        """
        Convert ISO 8601 timestamp to readable format.
        
        Args:
            iso_time: ISO 8601 timestamp string
            
        Returns:
            Formatted time string (e.g., "Feb 3 12:34 PM")
        """
        if not iso_time:
            return ''
        try:
            # If it's already a datetime object, use it directly
            if isinstance(iso_time, datetime):
                return iso_time.strftime('%b %d %I:%M %p')
                
            # Otherwise parse the string
            dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
            return dt.strftime('%b %d %I:%M %p')
        except (ValueError, TypeError):
            return iso_time  # Return the original string if parsing fails
        
    def get_display_name(self, chat: Chat) -> str:
        """
        Get the display name for a chat with fallbacks.
        
        Args:
            chat: The chat object
            
        Returns:
            The best available display name in order: display_name → name → username
        """
        # Check display_name first
        if chat.fan.display_name and chat.fan.display_name.strip():
            return chat.fan.display_name
            
        # Then check name
        if chat.fan.name and chat.fan.name.strip():
            return chat.fan.name
            
        # Finally check username
        if chat.fan.username and chat.fan.username.strip():
            return chat.fan.username
            
        # If we get here, all fields are empty or None
        print(f"Warning: No display name found for chat with fan ID {chat.fan.id}")
        return "Unknown User"
        
    def handle_chat_click(self, chat: Chat):
        """Handle chat cell click event."""
        print(f"Chat clicked - Fan ID: {chat.fan.id}, Display Name: {self.get_display_name(chat)}")
        self.selected_chat = chat
        
        # Format display info with default values first
        display_info = {
            'display_name': self.get_display_name(chat),
            'last_message': '',  # Use empty string instead of None
            'last_message_time': self.format_time(chat.last_message.created_at)
        }
        print(f"Setting selected chat with display info: {display_info}")
        self.view.set_selected_chat(display_info)
        
        # Schedule database call to run after current event is processed
        self.parent.after_idle(self._fetch_messages, chat)
        
    def _fetch_messages(self, chat: Chat):
        """Fetch messages from database and update display."""
        messages = self.db_client.get_chat_messages(self.account_id, str(chat.fan.id))
        if messages:
            # Get the last message from the fan
            last_fan_message = self.message_service.get_last_fan_message(messages, str(chat.fan.id))
            
            # Update the display with the last fan message
            display_info = {
                'display_name': self.get_display_name(chat),
                'last_message': last_fan_message.content if last_fan_message else 'No messages from fan',
                'last_message_time': self.format_time(last_fan_message.timestamp) if last_fan_message else ''
            }
            self.view.set_selected_chat(display_info)
        else:
            # Show message to sync when no messages found
            display_info = {
                'display_name': self.get_display_name(chat),
                'last_message': 'Please press Sync',
                'last_message_time': ''
            }
            self.view.set_selected_chat(display_info)
        
    def handle_sync(self):
        """Handle sync button click."""
        if self.selected_chat:
            response = self.webportal_client.sync_messages(self.account_id, str(self.selected_chat.fan.id))
            if response:
                # Fetch and display messages for the selected chat
                self._fetch_messages(self.selected_chat)
                self.fetch_and_display_chats()
            else:
                print("Sync failed")
                
    def handle_generate(self):
        """Handle generate button click."""
        if self.selected_chat:
            print("Generate clicked for chat:", self.selected_chat.fan.id)
            response = self.generate_message_service.generate_response(self.account_id, str(self.selected_chat.fan.id))
            if response != 'Generate response error':
                print("Generated response:", response)
                self.view.set_response_text(response)
            else:
                print("Failed to generate response")
        
    def handle_back(self):
        """Handle back button click."""
        self.view.frame.pack_forget()  # Hide chats view
        self.accounts_controller.pack(expand=True, fill=tk.BOTH)  # Show accounts view
        
    def add_chat(self, chat: Chat):
        """Add a chat to the list and display."""
        print(f"Adding chat - Fan ID: {chat.fan.id}, Display Name: {self.get_display_name(chat)}")
        self.chats.append(chat)
        
        # Format display info
        display_info = {
            'display_name': self.get_display_name(chat),
            'last_message': chat.last_message.text,
            'last_message_time': self.format_time(chat.last_message.created_at)
        }
        print(f"Adding chat cell with display info: {display_info}")
        self.view.add_chat(display_info, lambda: self.handle_chat_click(chat))
            
    def fetch_and_display_chats(self):
        """Fetch and display chats for the current account."""
        print("Fetching and displaying chats...")
        # Clear existing chats
        self.chats = []
        self.view.clear_chats()
        
        # Fetch and display new chats
        chats = self.chat_service.get_chats_for_account(self.account_id)
        print(f"Found {len(chats) if chats else 0} chats")
        if chats:
            for chat in chats:
                self.add_chat(chat)
                
    def pack(self, **kwargs):
        """Pack the view into its parent and fetch chats."""
        # First pack the view
        self.view.pack(**kwargs)
        
        # Fetch and display chats
        self.fetch_and_display_chats() 