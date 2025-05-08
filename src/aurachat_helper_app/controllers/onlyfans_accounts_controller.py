from aurachat_helper_app.views.onlyfans_accounts_view import OnlyFansAccountsView
from aurachat_helper_app.views.components.onlyfans_account_cell_view import OnlyFansAccountCellView
from aurachat_helper_app.controllers.chats_controller import ChatsController
from aurachat_helper_app.managers.onlyfans_account_manager import OnlyFansAccountManager
from aurachat_helper_app.models.onlyfans_account import OnlyFansAccount
import tkinter.messagebox as messagebox
import tkinter as tk

class OnlyFansAccountsController:
    """Controller class for managing OnlyFans accounts."""
    
    def __init__(self, parent, user_manager):
        """Initialize the OnlyFans accounts controller."""
        self.parent = parent
        self.user_manager = user_manager
        self.view = OnlyFansAccountsView(parent)
        self.account_manager = OnlyFansAccountManager()
        
        # Add user's OnlyFans accounts
        current_user = self.user_manager.get_current_user()
        if current_user and current_user.onlyfans_account_ids:
            self.account_manager.load_accounts_from_ids(current_user.onlyfans_account_ids)
            # Display loaded accounts
            for account in self.account_manager.get_accounts():
                self.add_account(account)
        
    def handle_account_click(self, account_info):
        """Handle account cell click event."""
        self.view.frame.pack_forget()  # Hide accounts view
        self.chats_controller = ChatsController(self.parent, self, account_info['id'])
        self.chats_controller.pack(expand=True, fill=tk.BOTH)
        
    def add_account(self, account: OnlyFansAccount):
        """Add an account to the view."""
        account_info = {'username': account.name, 'id': account.account_id}
        self.view.add_account(account_info, lambda: self.handle_account_click(account_info))
            
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        self.view.pack(**kwargs) 