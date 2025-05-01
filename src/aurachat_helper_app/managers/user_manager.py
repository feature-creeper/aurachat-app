from typing import Optional, Dict, Any
from ..db.db_client import db_client
from ..models.user import User
import asyncio

class UserManager:
    """Manager class for handling user authentication state and operations."""
    
    def __init__(self):
        """Initialize the user manager."""
        self._current_user = None
        
    def sign_in(self, email: str) -> bool:
        """Check if a user exists with the given email and set the current user."""
        user_data = asyncio.run(db_client.get_user_by_email(email))
        if user_data:
            self._current_user = User.from_dict(user_data)
            return True
        return False
        
    def sign_out(self):
        """Sign out the current user."""
        self._current_user = None
        
    def get_current_user(self) -> Optional[User]:
        """Get the currently signed in user."""
        return self._current_user
        
    def is_signed_in(self) -> bool:
        """Check if a user is currently signed in."""
        return self._current_user is not None 