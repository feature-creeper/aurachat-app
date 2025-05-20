import requests
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from ..utils.logger import get_logger
from ..env_config import ONLYFANSAPI_KEY as CONFIG_KEY

logger = get_logger(__name__)

class OnlyFansAPIClient:
    """Client for interacting with the OnlyFans API."""
    
    def __init__(self):
        """Initialize the client with an API token from environment variables."""
        load_dotenv()  # Load environment variables from .env file
        # Try config value first, then environment variable
        token = CONFIG_KEY or os.getenv('ONLYFANSAPI_KEY')
        if not token:
            logger.error("ONLYFANSAPI_KEY not found in configuration or environment variables")
            raise ValueError("ONLYFANSAPI_KEY not found in configuration or environment variables. Please add it to your .env file.")
            
        self.token = token
        self.base_url = "https://app.onlyfansapi.com/api"
        self.headers = {"Authorization": f"Bearer {token}"}
        logger.debug("OnlyFansAPI client initialized successfully")
        
    def get_chats(self, account_id: str, order: str = 'recent') -> List[Dict[str, Any]]:
        """
        Get chats for an account.
        
        Args:
            account_id: The account ID
            order: Sort order for chats ('recent' or 'oldest')
            
        Returns:
            List of chat data
        """
        try:
            url = f"{self.base_url}/{account_id}/chats/"
            print(f"Fetching chats from: {url}")
            response = requests.get(
                url,
                params={'order': order},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error getting chats: {e}")
            return []
            
    def get_chat_messages(self, account_id: str, chat_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch messages for a specific chat.
        
        Args:
            account_id: The ID of the OnlyFans account
            chat_id: The ID of the chat
            
        Returns:
            Dict containing the messages data or None if the request failed
        """
        try:
            url = f"{self.base_url}/{account_id}/chats/{chat_id}/messages"
            print("URL:", url)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise exception for bad status codes
            response_data = response.json()
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching chat messages: {e}")
            return None
