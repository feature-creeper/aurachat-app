from pymongo import MongoClient
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv
import sys
import ssl
from datetime import datetime
from ..models.message import Message

load_dotenv()

class MongoDBClient:
    def __init__(self):
        print("MongoDBClient: Initializing connection...")
        try:
            # Add serverSelectionTimeoutMS to prevent hanging and disable SSL verification for development
            self.client = MongoClient(
                os.getenv("MONGODB_URI"),
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                tlsAllowInvalidCertificates=True  # Disable SSL verification for development
            )
            print("MongoDBClient: Connection established")
        except Exception as e:
            print(f"MongoDBClient: Connection failed: {e}")
            sys.exit(1)

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by their email address from the 'users' collection in 'aurachat' database"""
        try:
            print(f"MongoDBClient: Looking up user with email: {email}")
            db = self.client['aurachat']  # Explicitly use 'aurachat' database
            users = db['users']           # Explicitly use 'users' collection
            print("MongoDBClient: Executing find_one query")
            user = users.find_one({"email": email})
            print(f"MongoDBClient: Query result: {user}")  # Print the user object
            return user
        except Exception as e:
            print(f"MongoDBClient: Error looking up user: {e}")
            raise  # Re-raise the exception to see the full traceback

    def close(self):
        """Close the MongoDB connection"""
        print("MongoDBClient: Closing connection...")
        self.client.close()
        print("MongoDBClient: Connection closed")

    def get_chat_messages(self, account: str, chat_id: str) -> Optional[List[Message]]:
        """
        Fetch messages for a specific chat from the database.
        
        Args:
            account: The account identifier
            chat_id: The chat identifier
            
        Returns:
            List of Message objects if found, None if no document exists
        """
        document = self.client['onlyfans']['chats'].find_one({
            'account': account,
            'chat_id': chat_id
        })
        
        if not document or 'messages' not in document:
            return None
            
        messages = []
        for msg in document['messages']:
            messages.append(Message(
                content=msg.get('content', ''),
                timestamp=msg.get('timestamp', ''),
                sender=msg.get('sender', '')
            ))
            
        return messages

# Create a global instance
db_client = MongoDBClient() 