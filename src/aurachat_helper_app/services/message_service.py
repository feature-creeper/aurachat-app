from typing import Optional, Dict, Any
from aurachat_helper_app.api.onlyfansapi_client import OnlyFansAPIClient

class MessageService:
    """Service for handling message-related operations."""
    
    def __init__(self):
        """Initialize the message service with an API client."""
        self.api_client = OnlyFansAPIClient()
        
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