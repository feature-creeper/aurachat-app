from typing import List, Dict, Any
from aurachat_helper_app.api.onlyfansapi_client import OnlyFansAPIClient

class ChatService:
    """Service class for handling chat-related operations."""
    
    def __init__(self):
        """Initialize the chat service."""
        self.api_client = OnlyFansAPIClient()
        
    def get_chats_for_account(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Get chats for a specific account and process the response.
        
        Args:
            account_id: The ID of the OnlyFans account
            
        Returns:
            List of chat objects from the data field
        """
        response = self.api_client.get_chats(account_id)
        if not response:
            return []
            
        # Extract the data array from the response
        return response.get('data', []) 