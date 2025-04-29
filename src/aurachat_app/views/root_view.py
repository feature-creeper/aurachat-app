import tkinter as tk
from tkinter import ttk

class RootView:
    """Root view class for handling the main application view."""
    
    def __init__(self):
        """Initialize the root view with a main window."""
        self.root = tk.Tk()
        self.root.title("AuraChat")
        self.root.geometry("800x600")
        self.root.attributes('-topmost', True)  # Keep window on top
        
        # Set dark theme
        self.root.configure(bg='#2b2b2b')
        
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Create File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
    def start(self):
        """Start the main event loop."""
        self.root.mainloop()
        
    def set_signout_command(self, command):
        """Set the command for the sign-out menu item."""
        self.file_menu.add_command(label="Sign Out", command=command) 