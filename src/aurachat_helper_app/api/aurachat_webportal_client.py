"""Client for interacting with the AuraChat web portal API."""
import requests
from typing import Optional, Dict, Any

class AuraChatWebPortalClient:
    """Client for interacting with the AuraChat web portal API."""
    
    def __init__(self, base_url: str = "https://aurachat-webportal.vercel.app"):
        """Initialize the web portal client."""
        self.base_url = base_url
        
    def sync_messages(self, account_id: str, chat_id: str) -> Optional[dict]:
        """
        Sync messages for a specific chat.
        
        Args:
            account_id: The account ID
            chat_id: The chat ID
            
        Returns:
            Response data from the API or None if the request failed
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/sync-messages/{account_id}/{chat_id}"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error syncing messages: {e}")
            return None 

    def generate_response(self, account_id: str, chat_id: str) -> Optional[Dict[str, Any]]:
        """
        Generate a response for a chat.
        
        Args:
            account_id: The ID of the OnlyFans account
            chat_id: The ID of the chat
            
        Returns:
            The JSON response from the server, or None if the request fails
        """
        try:
            response = requests.post(f"{self.base_url}/api/generate-response/{account_id}/{chat_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error generating response: {e}")
            return None 