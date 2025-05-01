from typing import Optional, Dict, Any, List
from aurachat_helper_app.api.onlyfansapi_client import OnlyFansAPIClient
from aurachat_helper_app.models.message import Message
import re

class MessageService:
    """Service for handling message-related operations."""
    
    def __init__(self):
        """Initialize the message service with an API client."""
        self.api_client = OnlyFansAPIClient()
        
    def get_last_fan_message(self, messages: List[Message], fan_id: str) -> Optional[Message]:
        """
        Get the last message from a fan with HTML tags removed.
        
        Args:
            messages: List of Message objects
            fan_id: The fan's ID to match against
            
        Returns:
            The last Message from the fan with cleaned content, or None if not found
        """
        # Find the last message from the fan
        last_fan_message = None
        for msg in reversed(messages):
            if msg.sender == str(fan_id):
                last_fan_message = msg
                break
                
        if last_fan_message:
            # Remove HTML tags from the message content
            last_fan_message.content = self._remove_html_tags(last_fan_message.content)
            
        return last_fan_message
        
    def _remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text."""
        if not text:
            return text
            
        # Remove <p> and </p> tags
        text = text.replace('<p>', '').replace('</p>', '')
        
        # Remove any remaining HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
        
    def get_most_recent_message_text(self, account_id: str, chat_id: str) -> Optional[str]:
        """
        Get the most recent message text from a chat.
        
        Args:
            account_id: The ID of the OnlyFans account
            chat_id: The ID of the chat
            
        Returns:
            The text of the most recent message, or None if no messages found
        """
        try:
            response = self.api_client.get_chat_messages(account_id, chat_id)
            if not response or 'data' not in response or 'list' not in response['data']:
                return None
                
            messages = response['data']['list']
            if not messages:
                return None
                
            # Get the most recent message
            most_recent = messages[0]
            text = most_recent.get('text', '')
            
            # Clean HTML from message if present
            if text.startswith('<p>') and text.endswith('</p>'):
                text = text[3:-4]  # Remove <p> and </p>
                
            return text
            
        except Exception as e:
            print(f"Error getting most recent message: {e}")
            return None 