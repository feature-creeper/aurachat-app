from aurachat_helper_app.views.onlyfans_accounts_view import OnlyFansAccountsView
from aurachat_helper_app.views.components.onlyfans_account_cell_view import OnlyFansAccountCellView
from aurachat_helper_app.controllers.chats_controller import ChatsController
from aurachat_helper_app.managers.onlyfans_account_manager import OnlyFansAccountManager
from aurachat_helper_app.models.onlyfans_account import OnlyFansAccount
from aurachat_helper_app.utils.logger import get_logger
import tkinter.messagebox as messagebox
import tkinter as tk

logger = get_logger(__name__)

class OnlyFansAccountsController:
    """Controller class for managing OnlyFans accounts."""
    
    def __init__(self, parent, user_manager):
        """Initialize the OnlyFans accounts controller."""
        logger.info("Initializing OnlyFans accounts controller")
        self.parent = parent
        self.user_manager = user_manager
        self.view = OnlyFansAccountsView(parent)
        self.account_manager = OnlyFansAccountManager()
        
        # Add user's OnlyFans accounts
        current_user = self.user_manager.get_current_user()
        if current_user and current_user.onlyfans_account_ids:
            logger.debug(f"Loading accounts for user with {len(current_user.onlyfans_account_ids)} account IDs")
            self.account_manager.load_accounts_from_ids(current_user.onlyfans_account_ids)
            # Display loaded accounts
            accounts = self.account_manager.get_accounts()
            logger.info(f"Loaded {len(accounts)} accounts")
            for account in accounts:
                self.add_account(account)
        else:
            logger.warning("No accounts found for current user")
        
    def handle_account_click(self, account_info):
        """Handle account cell click event."""
        try:
            logger.info(f"Account clicked: {account_info}")
            self.view.frame.pack_forget()  # Hide accounts view
            logger.debug("Creating chats controller")
            self.chats_controller = ChatsController(self.parent, self, account_info['id'])
            logger.debug("Packing chats controller")
            self.chats_controller.pack(expand=True, fill=tk.BOTH)
        except Exception as e:
            logger.exception(f"Error handling account click for account {account_info}")
            messagebox.showerror("Error", f"An error occurred while loading chats: {str(e)}")
            # Try to recover by showing accounts view again
            self.view.pack(expand=True, fill=tk.BOTH)
        
    def add_account(self, account: OnlyFansAccount):
        """Add an account to the view."""
        try:
            logger.debug(f"Adding account to view: {account.account_id}")
            account_info = {'username': account.name, 'id': account.account_id}
            self.view.add_account(account_info, lambda: self.handle_account_click(account_info))
        except Exception as e:
            logger.exception(f"Error adding account {account.account_id} to view")
            
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        logger.debug("Packing accounts view")
        self.view.pack(**kwargs) 