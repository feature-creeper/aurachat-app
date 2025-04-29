from views.onlyfans_accounts_view import OnlyFansAccountsView
from controllers.chats_controller import ChatsController
import tkinter.messagebox as messagebox
import tkinter as tk

class OnlyFansAccountsController:
    """Controller class for managing OnlyFans accounts."""
    
    def __init__(self, parent):
        """Initialize the OnlyFans accounts controller."""
        self.parent = parent
        self.view = OnlyFansAccountsView(parent)
        self.accounts = []
        
        # Add sample accounts
        self.add_account({'username': 'sample_account1'})
        self.add_account({'username': 'sample_account2'})
        
    def handle_account_click(self, account_info):
        """Handle account cell click event."""
        self.view.frame.pack_forget()  # Hide accounts view
        self.chats_controller = ChatsController(self.parent, self)
        self.chats_controller.pack(expand=True, fill=tk.BOTH)
        
    def add_account(self, account_info):
        """Add an account to the list and display."""
        self.accounts.append(account_info)
        self.view.add_account(account_info, lambda: self.handle_account_click(account_info))
            
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        self.view.pack(**kwargs) 