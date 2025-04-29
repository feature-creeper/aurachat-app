from pymongo import MongoClient
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
import sys
import ssl

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
            # Test the connection
            self.client.server_info()
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
            user = users.find_one({"email": email})
            print(f"MongoDBClient: Found user: {user}")  # Print the user object
            return user
        except Exception as e:
            print(f"MongoDBClient: Error looking up user: {e}")
            return None

    def close(self):
        """Close the MongoDB connection"""
        print("MongoDBClient: Closing connection...")
        self.client.close()
        print("MongoDBClient: Connection closed")

# Create a global instance
db_client = MongoDBClient() 