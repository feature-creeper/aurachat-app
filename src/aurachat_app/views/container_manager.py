import tkinter as tk

# Global references
chats_container = None
accounts_container = None
root_window = None
navbar = None

def set_containers(chats, accounts, root, nav):
    """Set the global container references."""
    global chats_container, accounts_container, root_window, navbar
    chats_container = chats
    accounts_container = accounts
    root_window = root
    navbar = nav

def show_chats_container():
    """Show the chats container and hide the accounts container."""
    if chats_container and accounts_container and root_window:
        # Hide accounts container first
        accounts_container.container_frame.pack_forget()
        # Show chats container
        chats_container.container_frame.pack(fill=tk.BOTH, expand=True)
        # Update the window
        root_window.update_idletasks()
        # Force a redraw
        root_window.update()
        # Update navbar visibility
        if navbar:
            navbar.update_visibility(True)
        # Print debug info
        print("Showing chats container")

def show_accounts_container():
    """Show the accounts container and hide the chats container."""
    if chats_container and accounts_container and root_window:
        # Hide chats container first
        chats_container.container_frame.pack_forget()
        # Show accounts container
        accounts_container.container_frame.pack(fill=tk.BOTH, expand=True)
        # Update the window
        root_window.update_idletasks()
        # Force a redraw
        root_window.update()
        # Update navbar visibility
        if navbar:
            navbar.update_visibility(False)
        # Print debug info
        print("Showing accounts container") 