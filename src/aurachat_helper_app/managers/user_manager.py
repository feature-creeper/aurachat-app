from typing import Optional, Dict, Any
from ..db.db_client import db_client
from ..models.user import User

class UserManager:
    """Manager class for handling user authentication state and operations."""
    
    def __init__(self):
        """Initialize the user manager."""
        self._current_user = None
        
    def sign_in(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        print(f"UserManager: Attempting to sign in with email: {email}")
        user = db_client.get_user_by_email(email)
        print(f"UserManager: User lookup result: {user is not None}")
        return user is not None
        
    def sign_out(self):
        """Sign out the current user."""
        self._current_user = None
        
    def get_current_user(self) -> Optional[User]:
        """Get the currently signed in user."""
        return self._current_user
        
    def is_signed_in(self) -> bool:
        """Check if a user is currently signed in."""
        return self._current_user is not None 