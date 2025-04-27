# User state management module

# Global sign-in state for the application
_user_signed_in = False

# Current user ID (set upon successful sign-in)
_current_user_id = None

def user_signedin():
    """
    Check if a user is currently signed in.
    
    Returns:
        bool: True if user is signed in, False otherwise
    """
    global _user_signed_in
    return _user_signed_in

def set_user_signed_in(state):
    """
    Set the user's sign-in state.
    
    Args:
        state: Boolean indicating if the user is signed in
    """
    global _user_signed_in
    _user_signed_in = state
    
    # If signing out, clear the user ID
    if not state:
        set_current_user_id(None)

def get_current_user_id():
    """
    Get the current user ID.
    
    Returns:
        The current user ID or None if not signed in
    """
    global _current_user_id
    return _current_user_id

def set_current_user_id(user_id):
    """
    Set the current user ID.
    
    Args:
        user_id: The user ID to set
    """
    global _current_user_id
    _current_user_id = user_id 