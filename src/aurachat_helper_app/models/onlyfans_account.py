from dataclasses import dataclass

@dataclass
class OnlyFansAccount:
    """Model representing an OnlyFans account in the system."""
    account_id: str
    name: str

    def to_dict(self) -> dict:
        """Convert the account object to a dictionary."""
        return {
            "account": self.account_id,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'OnlyFansAccount':
        """Create an OnlyFansAccount object from a dictionary."""
        return cls(
            account_id=data.get("account"),
            name=data.get("name", "")
        ) 