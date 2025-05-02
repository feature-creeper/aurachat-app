from typing import Optional, Dict, Any
from aurachat_helper_app.api.aurachat_webportal_client import AuraChatWebPortalClient

class GenerateMessageService:
    """Service for handling message generation operations."""
    
    def __init__(self):
        """Initialize the message generation service with a web portal client."""
        self.webportal_client = AuraChatWebPortalClient()
        
    def generate_response(self, account_id: str, chat_id: str) -> str:
        """
        Generate a response for a chat.
        
        Args:
            account_id: The ID of the OnlyFans account
            chat_id: The ID of the chat
            
        Returns:
            The generated response content, or 'Generate response error' if generation fails
        """
        try:
            response = self.webportal_client.generate_response(account_id, chat_id)
            print("Generate response:", response)
            if response and 'content' in response:
                return response['content']
            return 'Generate response error'
        except Exception as e:
            print(f"Error generating message: {e}")
            return 'Generate response error' 