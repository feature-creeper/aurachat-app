import tkinter as tk
from tkinter import ttk
from .components.onlyfans_account_cell_view import OnlyFansAccountCellView

class OnlyFansAccountsView:
    """View class for displaying and managing OnlyFans accounts."""
    
    def __init__(self, parent):
        """Initialize the OnlyFans accounts view."""
        self.frame = ttk.Frame(parent)
        self.frame.configure(style='Dark.TFrame')
        
        # Configure dark theme
        style = ttk.Style()
        style.configure('Dark.TFrame', background='#2b2b2b')
        style.configure('Dark.TLabel', background='#2b2b2b', foreground='white')
        
        # Header
        header_frame = ttk.Frame(self.frame, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(header_frame, 
                 text="OnlyFans Accounts", 
                 font=('Helvetica', 14, 'bold'),
                 style='Dark.TLabel').pack(side=tk.LEFT, padx=5)
        
        # Accounts list
        self.accounts_frame = ttk.Frame(self.frame, style='Dark.TFrame')
        self.accounts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def pack(self, **kwargs):
        """Pack the view into its parent."""
        self.frame.pack(**kwargs)
        
    def add_account(self, account_info, click_command):
        """Add an account to the display."""
        cell = OnlyFansAccountCellView(self.accounts_frame, account_info)
        cell.set_click_command(click_command)
        cell.pack(pady=2)
        
    def clear_accounts(self):
        """Clear all displayed accounts."""
        for widget in self.accounts_frame.winfo_children():
            widget.destroy() 