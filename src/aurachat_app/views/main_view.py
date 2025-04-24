import tkinter as tk
from tkinter import ttk

# UI spacing configuration variables
MODEL_VERTICAL_SPACING = 0  # Controls vertical spacing around the model response section

# Create the root window
root = tk.Tk()
root.title("AuraChat Bot")
root.geometry("450x350")  # Increased initial size
root.minsize(400, 300)  # Set minimum size to ensure buttons are visible
root.attributes('-topmost', True)  # Stay on top of other windows

# Use standard colors for macOS Dark Mode compatibility
root.configure(bg="#2c2f36")  # Standard background color

# Frame for client message for better resizing
client_frame = tk.Frame(
    root,
    padx=5,
    pady=5,
    bg="#2c2f36"  # Match background
)
client_frame.pack(fill=tk.X, padx=5, pady=5)

# Create client name label (bold)
client_name_label = tk.Label(
    client_frame,
    text="Fetching client",
    font=("Arial", 15, "bold"),
    bg="#2c2f36",
    fg="#ffffff",
    anchor="w",
    padx=5
)
client_name_label.pack(fill=tk.X, padx=5, pady=(5, 2), anchor="w")

# Create a client response label that can adapt its height
client_response_label = tk.Text(
    client_frame,
    wrap=tk.WORD,
    font=("Arial", 13),
    width=35,  # Approximate width in characters
    height=1,  # Initial height (will adjust)
    padx=5,
    pady=5,
    bg="#2c2f36",
    relief=tk.FLAT,
    highlightthickness=0,
)
client_response_label.pack(fill=tk.X, padx=5, pady=5)
client_response_label.insert(tk.END, "Waiting for client message...")
client_response_label.config(state=tk.DISABLED)  # Make it read-only

# Create a model response section with auto-height
model_response_frame = tk.Frame(
    root,
    padx=5,
    pady=5,
    bg="#1e2129",  # Darker background for contrast
    highlightbackground="#4a5568",  # Border color
    highlightthickness=1  # Border thickness
)
model_response_frame.pack(pady=MODEL_VERTICAL_SPACING, padx=10, fill=tk.X)  # Only fill horizontally

# Create a model response text widget with dynamic height
model_response_label = tk.Text(
    model_response_frame,
    wrap=tk.WORD,
    font=("Arial", 13),
    width=38,  # Fixed width in characters
    height=3,  # Initial height (will adjust)
    padx=5,
    pady=5,
    bg="#1e2129",  # Dark background
    fg="#ffffff",  # White text
    relief=tk.FLAT,
    highlightthickness=0,
    cursor="arrow"  # Use arrow cursor to appear more like a label
)
model_response_label.pack(padx=5, pady=MODEL_VERTICAL_SPACING, fill=tk.BOTH)  # Fill both to allow expansion
model_response_label.insert(tk.END, "Waiting for input...")
model_response_label.config(state=tk.DISABLED)  # Make it read-only

# Function to update client name label
def update_client_name(name):
    """Update the client name label with the provided name."""
    if not name:
        client_name_label.config(text="Unknown Client")
    else:
        client_name_label.config(text=name)
    client_name_label.update_idletasks()

# Function to update client response text and adjust height
def update_client_text(text):
    client_response_label.config(state=tk.NORMAL)  # Make it editable
    client_response_label.delete('1.0', tk.END)  # Clear current text
    client_response_label.insert(tk.END, text)  # Insert new text
    
    # Count number of lines needed for the text
    line_count = text.count('\n') + 1
    # Estimate additional line wraps (approximation)
    estimated_lines = max(1, len(text) // 50)  # Approx 50 chars per line
    needed_height = max(1, line_count + estimated_lines)
    
    # Update height (max 5 lines to avoid taking too much space)
    client_response_label.config(height=min(5, needed_height))
    client_response_label.config(state=tk.DISABLED)  # Make it read-only again
    
    # Force update to ensure size changes take effect
    client_response_label.update_idletasks()

# Function to update model response text and adjust height
def update_model_text(text):
    model_response_label.config(state=tk.NORMAL)  # Make it editable
    model_response_label.delete('1.0', tk.END)  # Clear current text
    model_response_label.insert(tk.END, text)  # Insert new text
    
    # Get the actual height needed in pixels
    text_height = model_response_label.count('1.0', 'end', 'displaylines')[0]
    
    # Set the height to show all lines (min 3, max 15)
    new_height = min(15, max(3, text_height))
    model_response_label.config(height=new_height)
    
    # Update the widget to ensure proper rendering
    model_response_label.update_idletasks()
    
    model_response_label.config(state=tk.DISABLED)  # Make it read-only again
    model_response_label.see("1.0")  # Scroll to the beginning

# Initial setup
update_client_text("Waiting for client message...")
update_model_text("Waiting for input...")

# Create button handlers (functions will be set by the controller)
button_handler = None
issue_button_handler = None

def button_clicked():
    if button_handler:
        button_handler()

def issue_button_clicked():
    if issue_button_handler:
        issue_button_handler()
    else:
        # Default behavior if no handler is set
        print("Issue detected")

style = ttk.Style()
style.theme_use("default")  # Use a consistent base theme

# Style for Copy button - increased vertical padding
style.configure("Copy.TButton",
    font=("Arial", 14),
    foreground="white",
    background="#007aff",
    padding=(20, 0),  # Significantly increased padding
    relief="flat"
)

# Apply the same look to all states for Copy button
style.map("Copy.TButton",
    foreground=[("active", "white"), ("pressed", "white"), ("disabled", "white"), ("focus", "white")],
    background=[("active", "#007aff"), ("pressed", "#007aff"), ("disabled", "#007aff"), ("focus", "#007aff")]
)

# Style for Issue button - increased vertical padding
style.configure("Issue.TButton",
    font=("Arial", 14),
    foreground="white",
    background="#900404",  # Red color as specified
    padding=(20, 0),  # Significantly increased padding
    relief="flat"
)

# Apply the same look to all states for Issue button
style.map("Issue.TButton",
    foreground=[("active", "white"), ("pressed", "white"), ("disabled", "white"), ("focus", "white")],
    background=[("active", "#900404"), ("pressed", "#900404"), ("disabled", "#900404"), ("focus", "#900404")]
)

# Create button frame with border - fixed height and no pack_propagate
button_frame = tk.Frame(
    root,
    bg="#2c2f36",  # Match background color
    height=80  # Increased fixed height for more space
)
button_frame.pack(fill=tk.X, padx=10, pady=(MODEL_VERTICAL_SPACING, 20))  # Top padding controlled by variable
button_frame.pack_propagate(False)  # Prevent frame from shrinking

# Create a container to right-align the buttons
button_container = tk.Frame(
    button_frame,
    bg="#2c2f36",  # Match background color
    height=80  # Increased height to match parent
)
button_container.pack(side=tk.RIGHT, pady=15)  # Increased padding

# Create Issue button
issue_button = ttk.Button(
    button_container,
    text="Issue",
    style="Issue.TButton",
    command=issue_button_clicked
)
issue_button.pack(pady=5, padx=10, side=tk.LEFT, ipady=8)  # Increased internal y-padding and horizontal spacing

# Create Copy button
action_button = ttk.Button(
    button_container,
    text="Copy",
    style="Copy.TButton",
    command=button_clicked
)
action_button.pack(pady=5, padx=10, side=tk.LEFT, ipady=8)  # Increased internal y-padding and horizontal spacing

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

# Set the button handlers
def set_button_handler(handler_function):
    """Set the handler function for the copy button."""
    global button_handler
    button_handler = handler_function

def set_issue_button_handler(handler_function):
    """Set the handler function for the issue button."""
    global issue_button_handler
    issue_button_handler = handler_function

# Only start mainloop if this file is run directly
if __name__ == "__main__":
    root.mainloop()