from typing import Dict, Any
import logging
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OnlyFansAPIClient:
    """Client for interacting with the OnlyFans API."""
    
    def __init__(self, auth_token: str = None):
        """Initialize the OnlyFans API client.
        
        Args:
            auth_token: Authentication token for API access (optional)
        """
        self.auth_token = auth_token or os.getenv("ONLYFANSAPI_KEY")
        if not self.auth_token:
            raise ValueError("No API key found. Please set ONLYFANSAPI_KEY in .env file.")
        
    def get_chats(self, account: str) -> Dict[str, Any]:
        """Get chats for a specific account.
        
        Args:
            account: The account identifier to get chats for
            
        Returns:
            Dict containing chat information
        """
        # Try with the account ID directly first
        url = f"https://app.onlyfansapi.com/api/{account}/chats"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            response = requests.request("GET", url, headers=headers)
            print(f"Request URL: {url}")
            print(f"Request Headers: {headers}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Text: {response.text}")
            
            # If we get a 403, try with the account ID without the 'acct_' prefix
            if response.status_code == 403:
                account_id = account.replace('acct_', '')
                url = f"https://app.onlyfansapi.com/api/{account_id}/chats"
                print(f"Trying alternative URL: {url}")
                response = requests.request("GET", url, headers=headers)
                print(f"Alternative Response Status Code: {response.status_code}")
                print(f"Alternative Response Text: {response.text}")
            
            response.raise_for_status()
            response_data = response.json()
            print(f"API Response: {response_data}")
            return response_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get chats: {str(e)}")
            if hasattr(e.response, 'text'):
                logging.error(f"Error response: {e.response.text}")
            return {}