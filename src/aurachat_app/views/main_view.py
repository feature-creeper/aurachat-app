import tkinter as tk


# Create the root window
root = tk.Tk()
root.title("AuraChat Bot")
root.geometry("400x300")
root.attributes('-topmost', True)  # Stay on top of other windows

# Use standard colors for macOS Dark Mode compatibility
root.configure(bg="#2c2f36")  # Standard background color


# Create a title label with system colors and border
title_label = tk.Label(
    root,  # Added parent root
    text="AuraChat Bot Interface",
    font=("Arial", 16, "bold"),
)
title_label.pack(pady=5, padx=5)

# Create a status section with visible border
status_frame = tk.Frame(
    root,
    padx=5,
    pady=5,
)
status_frame.pack(fill=tk.X, pady=10, padx=10)

# Create a status label with emphasis
status_label = tk.Label(
    status_frame,
    text="Status: Ready",
    font=("Arial", 12),
)
status_label.pack(pady=5, padx=5, fill=tk.X)

# Create a model response section
model_response_frame = tk.Frame(
    root,
    padx=5,
    pady=5,
    bg="#1e2129",  # Darker background for contrast
    highlightbackground="#4a5568",  # Border color
    highlightthickness=1  # Border thickness
)
model_response_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

# Create a model response label
model_response_label = tk.Label(
    model_response_frame,
    text="Model Response: Waiting for input...",
    font=("Arial", 11),
    justify=tk.LEFT,
    anchor="nw",
    wraplength=360,  # Allow text wrapping
    bg="#1e2129",  # Match frame background
    fg="#ffffff"   # White text for better readability
)
model_response_label.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

# Create a button (function will be set by the controller)
button_handler = None

def button_clicked():
    if button_handler:
        button_handler()

# Create button frame with border
button_frame = tk.Frame(
    root,
    padx=5,
    pady=5,
)
button_frame.pack(pady=10, padx=10)

action_button = tk.Button(
    button_frame,
    text="COPY RESPONSE",
    font=("Arial", 14, "bold"),
    command=button_clicked
)
action_button.pack(pady=10, padx=10)

# Initialize UI function to be called externally
def initialize_ui():
    """Initialize and show the UI without starting mainloop."""
    # All UI elements are already initialized above
    return root

# Set the button handler
def set_button_handler(handler_function):
    """Set the handler function for the button."""
    global button_handler
    button_handler = handler_function

# Only start mainloop if this file is run directly
if __name__ == "__main__":
    root.mainloop()