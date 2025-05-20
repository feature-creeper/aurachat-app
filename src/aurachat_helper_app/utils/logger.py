import logging
import os
from datetime import datetime

def setup_logger():
    """Set up logging configuration with file output in user's home directory."""
    # Create logs directory in user's home directory
    log_dir = os.path.expanduser('~/aurachat_logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create a new log file with timestamp
    log_file = os.path.join(log_dir, f'aurachat_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also print to console for development
        ]
    )
    
    # Log the start of the application and log file location
    logging.info(f"Application started - Log file: {log_file}")
    
# Create logger instances for different parts of the application
def get_logger(name):
    """Get a logger instance for a specific module."""
    return logging.getLogger(name) 