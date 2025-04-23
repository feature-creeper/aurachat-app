import os
from typing import Dict, Any, Optional
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

def get_mongodb_client() -> MongoClient:
    """Returns a MongoDB client instance."""
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set")
    
    return MongoClient(MONGODB_URI)

def get_message_by_chat_id(chat_id: str) -> Optional[Dict[str, Any]]:
    """Get a message from the telegram database messages collection by chat_id."""
    try:
        client = get_mongodb_client()
        db = client["telegram"]
        messages_collection = db["messages"]
        
        message = messages_collection.find_one({"chat_id": chat_id})
        return message
    except Exception as e:
        print(f"Error retrieving message by chat_id: {e}")
        return None
    finally:
        if 'client' in locals():
            client.close()
