import tkinter as tk
from tkinter import ttk

class ChatView:
    """Class representing the client and model response view components."""
    
    def __init__(self, parent, model_vertical_spacing):
        """Initialize the ChatView with all UI elements."""
        self.parent = parent
        self.model_vertical_spacing = model_vertical_spacing
        
        # Button handler callbacks
        self.button_handler = None
        self.issue_button_handler = None
        
        # Create main container frame for the entire ChatView
        self.container_frame = tk.Frame(
            self.parent,
            bg="#2c2f36",  # Match background
            padx=0,
            pady=0
        )
        self.container_frame.pack(fill=tk.X, padx=0, pady=0)
        
        self._create_client_section()
        self._create_model_section()
        self._setup_button_styles()
        self._create_button_section()
        self._create_separator_line()
        
        # Initial setup
        self.update_client_text("Waiting for client message...")
        self.update_model_text("Waiting for input...")
    
    def _create_client_section(self):
        """Create the client name and response section."""
        # Frame for client message for better resizing
        self.client_frame = tk.Frame(
            self.container_frame,  # Use container_frame instead of parent
            padx=5,
            pady=5,
            bg="#2c2f36"  # Match background
        )
        self.client_frame.pack(fill=tk.X, padx=5, pady=(5, 0))  # Removed bottom padding
        
        # Create client name label (bold)
        self.client_name_label = tk.Label(
            self.client_frame,
            text="Fetching client",
            font=("Arial", 15, "bold"),
            bg="#2c2f36",
            fg="#ffffff",
            anchor="w",
            padx=5
        )
        self.client_name_label.pack(fill=tk.X, padx=5, pady=(5, 2), anchor="w")
        
        # Create a client response label that can adapt its height
        self.client_response_label = tk.Text(
            self.client_frame,
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
        self.client_response_label.pack(fill=tk.X, padx=5, pady=(5, 0))  # Reduced bottom padding
        self.client_response_label.insert(tk.END, "Waiting for client message...")
        self.client_response_label.config(state=tk.DISABLED)  # Make it read-only
    
    def _create_model_section(self):
        """Create the model response section."""
        # Create a model response section with auto-height
        self.model_response_frame = tk.Frame(
            self.container_frame,  # Use container_frame instead of parent
            padx=5,
            pady=0,  # Removed vertical padding inside the frame
            bg="#1e2129",  # Darker background for contrast
            highlightbackground="#4a5568",  # Border color
            highlightthickness=1  # Border thickness
        )
        self.model_response_frame.pack(pady=(2, 0), padx=10, fill=tk.X)  # Minimal top padding
        
        # Create a model response text widget with dynamic height
        self.model_response_label = tk.Text(
            self.model_response_frame,
            wrap=tk.WORD,
            font=("Arial", 13),
            width=38,  # Fixed width in characters
            height=3,  # Initial height (will adjust)
            padx=5,
            pady=5,  # Use single value for the widget constructor
            bg="#1e2129",  # Dark background
            fg="#ffffff",  # White text
            relief=tk.FLAT,
            highlightthickness=0,
            cursor="arrow"  # Use arrow cursor to appear more like a label
        )
        self.model_response_label.pack(padx=5, pady=(5, 0), fill=tk.BOTH)  # Remove bottom padding
        self.model_response_label.insert(tk.END, "Waiting for input...")
        self.model_response_label.config(state=tk.DISABLED)  # Make it read-only
    
    def _setup_button_styles(self):
        """Set up the button styles."""
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
    
    def _create_button_section(self):
        """Create buttons section with action and issue buttons."""
        # Create button frame with border - fixed height and no pack_propagate
        self.button_frame = tk.Frame(
            self.container_frame,  # Use container_frame instead of parent
            bg="#2c2f36",  # Match background color
            height=50,  # Further reduced height
            bd=0,  # No border
            highlightthickness=0  # No highlight border
        )
        # Use negative padding to pull the frame up slightly, eliminating any gap
        self.button_frame.pack(fill=tk.X, padx=10, pady=0, ipady=0)
        self.button_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create a container to right-align the buttons
        self.button_container = tk.Frame(
            self.button_frame,
            bg="#2c2f36",  # Match background color
            height=50,  # Reduced height to match parent
            bd=0  # No border
        )
        self.button_container.pack(side=tk.RIGHT, pady=0)  # No vertical padding
        
        # Create Issue button
        self.issue_button = ttk.Button(
            self.button_container,
            text="Issue",
            style="Issue.TButton",
            command=self._issue_button_clicked
        )
        self.issue_button.pack(pady=5, padx=10, side=tk.LEFT, ipady=8)  # Increased internal y-padding and horizontal spacing
        
        # Create Copy button
        self.action_button = ttk.Button(
            self.button_container,
            text="Copy",
            style="Copy.TButton",
            command=self._button_clicked
        )
        self.action_button.pack(pady=5, padx=10, side=tk.LEFT, ipady=8)  # Increased internal y-padding and horizontal spacing
    
    def update_client_name(self, name):
        """Update the client name label with the provided name."""
        if not name:
            self.client_name_label.config(text="Unknown Client")
        else:
            # Handle if name is a simple string or a complex object
            if isinstance(name, dict) and 'name' in name:
                display_name = name['name']
            else:
                display_name = str(name)  # Convert to string to be safe
                
            self.client_name_label.config(text=display_name)
            
        self.client_name_label.update_idletasks()
    
    def update_client_text(self, text):
        """Update client response text and adjust height."""
        self.client_response_label.config(state=tk.NORMAL)  # Make it editable
        self.client_response_label.delete('1.0', tk.END)  # Clear current text
        self.client_response_label.insert(tk.END, text)  # Insert new text
        
        # Count number of lines needed for the text
        line_count = text.count('\n') + 1
        # Estimate additional line wraps (approximation)
        estimated_lines = max(1, len(text) // 50)  # Approx 50 chars per line
        needed_height = max(1, line_count + estimated_lines)
        
        # Update height (max 5 lines to avoid taking too much space)
        self.client_response_label.config(height=min(5, needed_height))
        self.client_response_label.config(state=tk.DISABLED)  # Make it read-only again
        
        # Force update to ensure size changes take effect
        self.client_response_label.update_idletasks()
    
    def update_model_text(self, text):
        """Update model response text and adjust height."""
        self.model_response_label.config(state=tk.NORMAL)  # Make it editable
        self.model_response_label.delete('1.0', tk.END)  # Clear current text
        self.model_response_label.insert(tk.END, text)  # Insert new text
        
        # Get the actual height needed in pixels
        text_height = self.model_response_label.count('1.0', 'end', 'displaylines')[0]
        
        # Set the height to show all lines (min 3, max 15)
        new_height = min(15, max(3, text_height))
        self.model_response_label.config(height=new_height)
        
        # Update the widget to ensure proper rendering
        self.model_response_label.update_idletasks()
        
        self.model_response_label.config(state=tk.DISABLED)  # Make it read-only again
        self.model_response_label.see("1.0")  # Scroll to the beginning
        
        # Force immediate update to remove any lag in UI updates
        self.parent.update_idletasks()
    
    def _button_clicked(self):
        """Handle action button click."""
        if self.button_handler:
            self.button_handler()
    
    def _issue_button_clicked(self):
        """Handle issue button click."""
        if self.issue_button_handler:
            self.issue_button_handler()
        else:
            # Default behavior if no handler is set
            print("Issue detected")
    
    def set_button_handler(self, handler_function):
        """Set the handler function for the action button."""
        self.button_handler = handler_function
    
    def set_issue_button_handler(self, handler_function):
        """Set the handler function for the issue button."""
        self.issue_button_handler = handler_function
    
    def _create_separator_line(self):
        """Create a separator line between chat views."""
        separator = tk.Frame(
            self.container_frame,
            height=1,
            bg="#4a5568",  # Border color
            highlightthickness=0
        )
        separator.pack(fill=tk.X, padx=10, pady=5) 