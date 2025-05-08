from typing import List
from ..models.onlyfans_account import OnlyFansAccount
from ..services.onlyfans_account_service import OnlyFansAccountService

class OnlyFansAccountManager:
    """Manager class for handling OnlyFans account operations."""
    
    def __init__(self):
        """Initialize the account manager with an empty list of accounts."""
        self._accounts: List[OnlyFansAccount] = []
        self._account_service = OnlyFansAccountService()
        
    def add_account(self, account: OnlyFansAccount) -> None:
        """
        Add an OnlyFans account to the manager.
        
        Args:
            account: The OnlyFansAccount object to add
        """
        self._accounts.append(account)
        
    def get_accounts(self) -> List[OnlyFansAccount]:
        """
        Get all stored OnlyFans accounts.
        
        Returns:
            List of OnlyFansAccount objects
        """
        return self._accounts.copy()  # Return a copy to prevent external modification
        
    def clear_accounts(self) -> None:
        """Clear all stored accounts."""
        self._accounts.clear()
        
    def load_accounts_from_ids(self, account_ids: List[str]) -> None:
        """
        Load accounts from the database using their IDs and add them to the manager.
        
        Args:
            account_ids: List of account identifiers to load
        """
        accounts = self._account_service.get_accounts_by_ids(account_ids)
        for account in accounts:
            self.add_account(account) 