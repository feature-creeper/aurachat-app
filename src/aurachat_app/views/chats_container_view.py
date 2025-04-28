import tkinter as tk
from tkinter import ttk
from .chat_view import ChatView

class ChatsContainerView:
    """A container view that manages multiple ChatView instances."""
    
    def __init__(self, parent):
        """
        Initialize the chats container view.
        
        Args:
            parent: The parent frame to pack this container into
        """
        self.parent = parent
        self.chat_views = []
        
        # Create main container frame
        self.container_frame = tk.Frame(parent, bg="#2c2f36")
        # Don't pack the frame immediately - it will be packed when shown
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.container_frame, bg="#2c2f36", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2c2f36")
        
        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a window inside the canvas to contain the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure scrollable_frame to update scroll region when its size changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
    
    def add_chat_view(self):
        """
        Add a new ChatView to the container.
        
        Returns:
            ChatView: The newly created chat view
        """
        new_chat_view = ChatView(self.scrollable_frame, 0)
        self.chat_views.append(new_chat_view)
        
        # Update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        return new_chat_view
    
    def get_chat_views(self):
        """
        Get all chat views in the container.
        
        Returns:
            list: List of ChatView instances
        """
        return self.chat_views
    
    def clear_chat_views(self):
        """Clear all chat views from the container."""
        # Destroy all children in scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Clear the chat views list
        self.chat_views.clear()
        
        # Update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all")) 