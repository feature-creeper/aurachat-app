from typing import List
from dataclasses import dataclass

@dataclass
class User:
    """User model representing a user in the system."""
    email: str
    onlyfans_account_ids: List[str] = None

    def __post_init__(self):
        """Initialize default values after dataclass initialization."""
        if self.onlyfans_account_ids is None:
            self.onlyfans_account_ids = []

    def to_dict(self) -> dict:
        """Convert the user object to a dictionary."""
        return {
            "email": self.email,
            "onlyfans_account_ids": self.onlyfans_account_ids
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create a User object from a dictionary."""
        return cls(
            email=data.get("email"),
            onlyfans_account_ids=data.get("onlyfans_account_ids", [])
        ) 