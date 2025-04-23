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

def get_latest_client_message(chat_id: int) -> Optional[Dict[str, Any]]:
    
    try:
        client = get_mongodb_client()
        db = client["telegram"]
        messages_collection = db["messages"]
        
        # Get the document for the chat_id
        document = messages_collection.find_one({"chat_id": chat_id})
        
        if not document or "messages" not in document:
            return None
        
        # Filter for client messages only and sort by created_at in descending order
        client_messages = [
            msg for msg in document["messages"] 
            if msg.get("role") == "client" and "created_at" in msg
        ]
        
        if not client_messages:
            return None
            
        # Sort by created_at in descending order (newest first)
        sorted_messages = sorted(
            client_messages,
            key=lambda msg: msg["created_at"],
            reverse=True
        )
        
        # Return the most recent client message
        return sorted_messages[0] if sorted_messages else None
        
    except Exception as e:
        print(f"Error retrieving client message by chat_id: {e}")
        return None
    finally:
        if 'client' in locals():
            client.close()
