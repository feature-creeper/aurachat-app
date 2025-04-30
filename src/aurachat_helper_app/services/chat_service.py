from typing import List, Dict, Any
from aurachat_helper_app.api.onlyfansapi_client import OnlyFansAPIClient
from aurachat_helper_app.models.chat import Chat
import re

class ChatService:
    """Service class for handling chat-related operations."""
    
    def __init__(self):
        """Initialize the chat service."""
        self.api_client = OnlyFansAPIClient()
        
    def clean_html(self, text: str) -> str:
        """
        Remove HTML tags from a string.
        
        Args:
            text: The string containing HTML tags
            
        Returns:
            The cleaned string without HTML tags
        """
        if not text:
            return ''
            
        # Remove <p> and </p> tags
        text = text.replace('<p>', '').replace('</p>', '')
        
        # Remove any remaining HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
        
    def get_chats_for_account(self, account_id: str) -> List[Chat]:
        """
        Get chats for a specific account and process the response.
        
        Args:
            account_id: The ID of the OnlyFans account
            
        Returns:
            List of Chat objects
        """
        response = self.api_client.get_chats(account_id)
        if not response or 'data' not in response:
            print("No chat data in response")
            return []
            
        # Extract the data array from the response and convert to Chat objects
        chats_data = response['data']
        if not isinstance(chats_data, list):
            print(f"Expected list of chats, got {type(chats_data)}")
            return []
            
        chats = []
        for chat_data in chats_data:
            try:
                # Clean HTML from last message before creating Chat object
                if 'lastMessage' in chat_data and 'text' in chat_data['lastMessage']:
                    chat_data['lastMessage']['text'] = self.clean_html(chat_data['lastMessage']['text'])
                    
                chat = Chat.from_dict(chat_data)
                chats.append(chat)
            except Exception as e:
                print(f"Error converting chat data: {e}")
                continue
                
        print(f"Successfully converted {len(chats)} chats")
        return chats 