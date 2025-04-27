import tkinter as tk
import platform
import sys

def add_signout_menu_option(root, signout_callback):
    """
    Add a Sign out option to the application menu bar.
    
    Args:
        root: The tkinter root window
        signout_callback: Function to call when Sign out is selected
    """
    # Store the callback on the root for later reuse (e.g., after sign out)
    root._signout_callback = signout_callback
    
    # Get the operating system
    system = platform.system()
    
    # Create menubar if it doesn't exist
    if not hasattr(root, 'menubar'):
        root.menubar = tk.Menu(root)
        root.config(menu=root.menubar)
    
    # Handle macOS differently
    if system == 'Darwin':  # macOS
        # On macOS, use the system menu bar
        # First check if App menu already exists
        app_menu_exists = False
        for i in range(root.menubar.index('end') + 1 if root.menubar.index('end') is not None else 0):
            if root.menubar.entrycget(i, 'label') == 'AuraChat':
                app_menu_exists = True
                app_menu = root.menubar.nametowidget(root.menubar.entrycget(i, 'menu'))
                break
        
        if not app_menu_exists:
            # Create App menu (appears with application name on macOS)
            app_menu = tk.Menu(root.menubar, name='apple')
            root.menubar.add_cascade(label='AuraChat', menu=app_menu)
            
            # Add About option (standard on macOS)
            app_menu.add_command(label='About AuraChat', command=lambda: show_about_dialog(root))
        
        # Add separator before Sign out if there are items in the menu
        if app_menu.index('end') is not None:
            app_menu.add_separator()
            
        # Add Sign out option
        app_menu.add_command(label='Sign Out', command=signout_callback)
        
    else:  # Windows/Linux
        # Create or get File menu
        file_menu_exists = False
        for i in range(root.menubar.index('end') + 1 if root.menubar.index('end') is not None else 0):
            if root.menubar.entrycget(i, 'label') == 'File':
                file_menu_exists = True
                file_menu = root.menubar.nametowidget(root.menubar.entrycget(i, 'menu'))
                break
        
        if not file_menu_exists:
            # Create File menu
            file_menu = tk.Menu(root.menubar, tearoff=0)
            root.menubar.add_cascade(label='File', menu=file_menu)
        
        # Add separator before Sign out if there are items in the menu
        if file_menu.index('end') is not None:
            file_menu.add_separator()
            
        # Add Sign out option
        file_menu.add_command(label='Sign Out', command=signout_callback)
        
        # Add Exit option if it doesn't exist
        # Check if Exit already exists in the menu
        exit_exists = False
        if file_menu.index('end') is not None:
            for i in range(file_menu.index('end') + 1):
                try:
                    if file_menu.entrycget(i, 'label') == 'Exit':
                        exit_exists = True
                        break
                except:
                    pass
                
        if not exit_exists:
            file_menu.add_separator()
            file_menu.add_command(label='Exit', command=root.quit)

def show_about_dialog(root):
    """Show an About dialog with application information."""
    about_window = tk.Toplevel(root)
    about_window.title("About AuraChat")
    about_window.geometry("300x200")
    about_window.resizable(False, False)
    
    # Center the window
    about_window.update_idletasks()
    width = about_window.winfo_width()
    height = about_window.winfo_height()
    x = (about_window.winfo_screenwidth() // 2) - (width // 2)
    y = (about_window.winfo_screenheight() // 2) - (height // 2)
    about_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Add content
    tk.Label(
        about_window, 
        text="AuraChat", 
        font=("Arial", 16, "bold")
    ).pack(pady=(20, 5))
    
    tk.Label(
        about_window, 
        text="Version 1.0.0", 
        font=("Arial", 10)
    ).pack(pady=5)
    
    tk.Label(
        about_window, 
        text="© 2023 AuraChat", 
        font=("Arial", 10)
    ).pack(pady=5)
    
    # Close button
    tk.Button(
        about_window, 
        text="Close", 
        command=about_window.destroy
    ).pack(pady=20) 