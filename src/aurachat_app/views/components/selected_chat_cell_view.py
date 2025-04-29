import tkinter as tk
from tkinter import ttk

class SelectedChatCellView:
    """Component view for displaying the selected chat cell."""
    
    def __init__(self, parent, chat_info):
        """Initialize the selected chat cell view."""
        self.frame = tk.Frame(parent, bg='#2b2b2b')
        self.chat_info = chat_info
        self.parent = parent  # Store parent for clipboard access
        
        # Main container with padding
        container = tk.Frame(self.frame, bg='#2b2b2b')
        container.pack(fill=tk.X, padx=10, pady=10)
        
        # Username with larger font
        tk.Label(container, 
                text=chat_info['username'], 
                font=('Helvetica', 12, 'bold'),
                bg='#2b2b2b',
                fg='white').pack(side=tk.LEFT, padx=5)
        
        # Client message section
        tk.Label(self.frame, 
                text="Client message", 
                font=('Helvetica', 10),
                bg='#2b2b2b',
                fg='white').pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Text field for generated response
        self.response_text = tk.Text(self.frame, 
                                   height=3, 
                                   wrap=tk.WORD,
                                   font=('Helvetica', 10),
                                   bg='#2b2b2b',
                                   fg='white',
                                   insertbackground='white')
        self.response_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.response_text.insert('1.0', 'Generated response')
        self.response_text.config(state='disabled')  # Make it read-only
        
        # Action container
        action_frame = tk.Frame(self.frame, bg='#2b2b2b')
        action_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Generate action (green)
        self.generate_frame = tk.Frame(action_frame, bg='#4CAF50')
        self.generate_frame.pack(side=tk.LEFT, padx=5)
        self.generate_label = tk.Label(self.generate_frame,
                                     text="Generate",
                                     bg='#4CAF50',
                                     fg='white',
                                     font=('Helvetica', 10),
                                     padx=10,
                                     pady=5)
        self.generate_label.pack()
        self.generate_frame.bind('<Button-1>', lambda e: self._on_generate_click())
        self.generate_label.bind('<Button-1>', lambda e: self._on_generate_click())
        
        # Issue action (red)
        self.issue_frame = tk.Frame(action_frame, bg='#F44336')
        self.issue_frame.pack(side=tk.LEFT, padx=5)
        self.issue_label = tk.Label(self.issue_frame,
                                  text="Issue",
                                  bg='#F44336',
                                  fg='white',
                                  font=('Helvetica', 10),
                                  padx=10,
                                  pady=5)
        self.issue_label.pack()
        self.issue_frame.bind('<Button-1>', lambda e: self._on_issue_click())
        self.issue_label.bind('<Button-1>', lambda e: self._on_issue_click())
        
        # Copy text action (blue)
        self.copy_frame = tk.Frame(action_frame, bg='#2196F3')
        self.copy_frame.pack(side=tk.LEFT, padx=5)
        self.copy_label = tk.Label(self.copy_frame,
                                 text="Copy text",
                                 bg='#2196F3',
                                 fg='white',
                                 font=('Helvetica', 10),
                                 padx=10,
                                 pady=5)
        self.copy_label.pack()
        self.copy_frame.bind('<Button-1>', lambda e: self._on_copy_click())
        self.copy_label.bind('<Button-1>', lambda e: self._on_copy_click())
        
    def _on_generate_click(self):
        """Handle generate click."""
        if hasattr(self, 'generate_command'):
            self.generate_command()
            
    def _on_issue_click(self):
        """Handle issue click."""
        if hasattr(self, 'issue_command'):
            self.issue_command()
            
    def _on_copy_click(self):
        """Handle copy click."""
        # Enable text widget temporarily to get content
        self.response_text.config(state='normal')
        text = self.response_text.get('1.0', tk.END).strip()
        self.response_text.config(state='disabled')
        
        # Clear clipboard and add new text
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
        
        # Execute any additional copy command if set
        if hasattr(self, 'copy_command'):
            self.copy_command()
        
    def pack(self, **kwargs):
        """Pack the cell into its parent."""
        self.frame.pack(fill=tk.X, **kwargs)
        
    def update_response(self, text):
        """Update the response text."""
        self.response_text.config(state='normal')
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert('1.0', text)
        self.response_text.config(state='disabled')
        
    def set_generate_command(self, command):
        """Set the command for the generate action."""
        self.generate_command = command
        
    def set_issue_command(self, command):
        """Set the command for the issue action."""
        self.issue_command = command
        
    def set_copy_command(self, command):
        """Set the command for the copy action."""
        self.copy_command = command 