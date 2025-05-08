from typing import List
from ..db.db_client import db_client
from ..models.onlyfans_account import OnlyFansAccount

class OnlyFansAccountService:
    """Service for handling OnlyFans account operations."""
    
    def __init__(self):
        """Initialize the account service."""
        pass
        
    def get_accounts_by_ids(self, account_ids: List[str]) -> List[OnlyFansAccount]:
        """
        Fetch OnlyFans accounts from the database and create OnlyFansAccount objects.
        
        Args:
            account_ids: List of account identifiers to fetch
            
        Returns:
            List of OnlyFansAccount objects
        """
        accounts = []
        for account_id in account_ids:
            try:
                account_data = db_client.get_account_by_id(account_id)
                if account_data:
                    account = OnlyFansAccount.from_dict(account_data)
                    accounts.append(account)
            except Exception as e:
                print(f"Error fetching account {account_id}: {e}")
                continue
                
        return accounts 