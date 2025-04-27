import tkinter as tk
from tkinter import ttk
from .account_view import AccountView

# UI spacing configuration variables
MODEL_VERTICAL_SPACING = 0  # Controls vertical spacing around the model response section

# Create the root window
root = tk.Tk()
root.title("AuraChat")
root.geometry("450x350")  # Increased initial size
root.minsize(400, 300)  # Set minimum size to ensure buttons are visible
root.attributes('-topmost', True)  # Stay on top of other windows

# Use standard colors for macOS Dark Mode compatibility
root.configure(bg="#2c2f36")  # Standard background color

# Create the AccountView instance
account_view = AccountView(root, MODEL_VERTICAL_SPACING)

# Expose needed UI elements for external access
client_response_label = account_view.client_response_label
model_response_label = account_view.model_response_label

# Function to adjust window size based on content
def adjust_window_size():
    """Update window size to fit all contents."""
    # Update all idle tasks to get correct widget sizes
    root.update_idletasks()
    
    # Get the required width and height
    required_width = max(root.winfo_reqwidth(), 450)
    required_height = max(root.winfo_reqheight(), 350)
    
    # Set the window size
    root.geometry(f"{required_width}x{required_height}")

# Initialize UI function to be called externally
def initialize_ui():
    """Initialize and show the UI without starting mainloop."""
    # All UI elements are already initialized above
    
    # Adjust window size after initialization
    root.after(100, adjust_window_size)  # Small delay to ensure all widgets are ready
    
    return root

# Public functions to access the AccountView methods
def update_client_name(name):
    """Update the client name label with the provided name."""
    account_view.update_client_name(name)

def update_client_text(text):
    """Update client response text and adjust height."""
    account_view.update_client_text(text)

def update_model_text(text):
    """Update model response text and adjust height."""
    account_view.update_model_text(text)

# Set the button handlers
def set_button_handler(handler_function):
    """Set the handler function for the copy button."""
    account_view.set_button_handler(handler_function)

def set_issue_button_handler(handler_function):
    """Set the handler function for the issue button."""
    account_view.set_issue_button_handler(handler_function)

# Only start mainloop if this file is run directly
if __name__ == "__main__":
    root.mainloop()