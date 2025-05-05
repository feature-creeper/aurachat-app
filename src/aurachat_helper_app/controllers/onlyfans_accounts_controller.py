from aurachat_helper_app.views.onlyfans_accounts_view import OnlyFansAccountsView
from aurachat_helper_app.views.components.onlyfans_account_cell_view import OnlyFansAccountCellView
from aurachat_helper_app.controllers.chats_controller import ChatsController
import tkinter.messagebox as messagebox
import tkinter as tk

class OnlyFansAccountsController:
    """Controller class for managing OnlyFans accounts."""
    
    def __init__(self, parent, user_manager):
        """Initialize the OnlyFans accounts controller."""
        self.parent = parent
        self.user_manager = user_manager
        self.view = OnlyFansAccountsView(parent)
        self.accounts = []
        
        # Add user's OnlyFans accounts
        current_user = self.user_manager.get_current_user()
        if current_user and current_user.onlyfans_account_ids:
            for account_id in current_user.onlyfans_account_ids:
                self.add_account({'username': account_id, 'id': account_id})
        
    def handle_account_click(self, account_info):
        """Handle account cell click event."""
        self.view.frame.pack_forget()  # Hide accounts view
        self.chats_controller = ChatsController(self.parent, self, account_info['id'])
        self.chats_controller.pack(expand=True, fill=tk.BOTH)
        
    def add_account(self, account_info):
        """Add an account to the list and display."""
        self.accounts.append(account_info)
        self.view.add_account(account_info, lambda: self.handle_account_click(account_info))
            
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        self.view.pack(**kwargs) 