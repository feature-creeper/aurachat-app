from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    """Represents a message in the database."""
    content: str
    timestamp: datetime
    sender: str 