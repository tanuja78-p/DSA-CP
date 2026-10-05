from dataclasses import dataclass


@dataclass
class Resource:
    """
    Represents a disaster-management resource.

    Examples:
    - Water
    - Food
    - Medicine
    - Blankets
    - First Aid Kits
    """

    resource_id: str
    name: str
    category: str
    quantity: int
    priority: int = 1

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Resource quantity cannot be negative")

        if self.priority < 1:
            raise ValueError("Resource priority must be at least 1")

    def is_available(self):
        """Return True if at least one unit is available."""
        return self.quantity > 0

    def add_quantity(self, amount):
        """Add resource units."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self.quantity += amount

    def remove_quantity(self, amount):
        """Remove resource units."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        if amount > self.quantity:
            raise ValueError(
                f"Insufficient {self.name}. "
                f"Available: {self.quantity}, requested: {amount}"
            )

        self.quantity -= amount

    def to_dict(self):
        """Return resource information as a dictionary."""
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "priority": self.priority,
        }