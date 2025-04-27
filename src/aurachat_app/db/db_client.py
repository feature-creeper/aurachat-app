import os
import certifi
from typing import Dict, Any, Optional, List, Union
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

def get_mongodb_client() -> MongoClient:
    """Returns a MongoDB client instance with SSL certificate verification configured."""
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set")
    
    # Use certifi to provide a trusted CA bundle
    # This solves the SSL certificate verification issue
    return MongoClient(
        MONGODB_URI,
        tlsCAFile=certifi.where(),
        # Add connect timeout to avoid hanging forever
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )

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

def fetch_connected_accounts(user_identifier: Union[int, str]) -> Optional[List[str]]:
    """
    Retrieves the 'accounts' array from the user object in the 'users' collection.
    The accounts are stored as an array of strings.
    
    Args:
        user_identifier: Either a chat_id (int) or MongoDB _id (str)
        
    Returns:
        A list of account strings if found, None otherwise
    """
    try:
        print(f"Fetching connected accounts for user_identifier: {user_identifier} (type: {type(user_identifier)})")
        
        client = get_mongodb_client()
        db = client["aurachat"]
        users_collection = db["users"]
        
        # Determine query based on identifier type
        if isinstance(user_identifier, str):
            # Use MongoDB ObjectId for string identifiers
            try:
                object_id = ObjectId(user_identifier)
                print(f"Using ObjectId: {object_id}")
                user_document = users_collection.find_one({"_id": object_id})
            except Exception as e:
                print(f"Error converting to ObjectId: {e}, trying to query as string")
                user_document = users_collection.find_one({"_id": user_identifier})
        else:
            # Use chat_id for integer identifiers
            print(f"Using chat_id: {user_identifier}")
            user_document = users_collection.find_one({"chat_id": user_identifier})
        
        print(f"User document found: {user_document is not None}")
        
        if not user_document:
            print("No user document found")
            return None
            
        if "accounts" not in user_document:
            print("User document does not have 'accounts' field")
            # Print the keys in the document to help debugging
            print(f"Available keys: {list(user_document.keys())}")
            return None
        
        accounts = user_document["accounts"]
        print(f"Found accounts: {accounts} (type: {type(accounts)})")
        
        return accounts
        
    except Exception as e:
        print(f"Error retrieving connected accounts for identifier {user_identifier}: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if 'client' in locals():
            client.close()

def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Find a user by email in the 'users' collection of the 'aurachat' database.
    
    Args:
        email: The email address to search for
        
    Returns:
        The user document if found, None otherwise
    """
    try:
        client = get_mongodb_client()
        db = client["aurachat"]
        users_collection = db["users"]
        
        # Query by email (using case-insensitive search)
        user_document = users_collection.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
        
        return user_document
        
    except Exception as e:
        print(f"Error finding user by email: {e}")
        return None
    finally:
        if 'client' in locals():
            client.close()

def list_mongodb_info():
    """Print MongoDB database and collection information for debugging."""
    try:
        client = get_mongodb_client()
        print("\n=== MongoDB INFO ===")
        
        # List all databases
        databases = client.list_database_names()
        print(f"Available databases: {databases}")
        
        # Check aurachat database
        if "aurachat" in databases:
            db = client["aurachat"]
            collections = db.list_collection_names()
            print(f"Collections in 'aurachat' database: {collections}")
            
            # Check users collection
            if "users" in collections:
                users_count = db["users"].count_documents({})
                print(f"Number of documents in users collection: {users_count}")
                
                # Get a sample user
                sample_user = db["users"].find_one({})
                if sample_user:
                    print(f"Sample user keys: {list(sample_user.keys())}")
                    if "accounts" in sample_user:
                        print(f"Sample user has {len(sample_user['accounts'])} accounts")
                        print(f"Sample accounts: {sample_user['accounts']}")
            else:
                print("No 'users' collection found in aurachat database")
        else:
            print("No 'aurachat' database found")
            
        print("===================\n")
    except Exception as e:
        print(f"Error listing MongoDB info: {e}")
    finally:
        if 'client' in locals():
            client.close()
