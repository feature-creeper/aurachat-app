import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class OnlyFansAPIClient:
    """Client for interacting with the OnlyFans API."""
    
    def __init__(self):
        """Initialize the client with an API token from environment variables."""
        load_dotenv()  # Load environment variables from .env file
        token = os.getenv('ONLYFANSAPI_KEY')
        if not token:
            raise ValueError("ONLYFANS_API_TOKEN not found in environment variables. Please add it to your .env file.")
            
        self.token = token
        self.base_url = "https://app.onlyfansapi.com/api"
        self.headers = {"Authorization": f"Bearer {token}"}
        
    def get_chats(self, account_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch chats for a specific OnlyFans account.
        
        Args:
            account_id: The ID of the OnlyFans account
            
        Returns:
            Dict containing the chat data or None if the request failed
        """
        try:
            url = f"{self.base_url}/{account_id}/chats"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise exception for bad status codes
            response_data = response.json()
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching chats: {e}")
            return None
            
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
            print("API Response:", response_data)  # Print the response
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching chat messages: {e}")
            return None
