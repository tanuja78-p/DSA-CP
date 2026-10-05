from dataclasses import dataclass


@dataclass
class Shelter:
    """
    Represents one emergency shelter.

    shelter_id:
        Unique shelter identifier.

    name:
        Shelter name.

    latitude / longitude:
        Geographic coordinates.

    capacity:
        Maximum number of people the shelter can hold.

    occupied:
        Current number of people inside.

    status:
        SAFE / CONGESTED / BLOCKED / CLOSED

    accessible:
        Whether evacuees can currently reach the shelter.
    """

    shelter_id: str
    name: str
    latitude: float
    longitude: float
    capacity: int
    occupied: int = 0
    status: str = "SAFE"
    accessible: bool = True

    @property
    def available_capacity(self) -> int:
        """Return remaining capacity."""
        return max(0, self.capacity - self.occupied)

    @property
    def occupancy_percentage(self) -> float:
        """Return occupancy percentage."""
        if self.capacity <= 0:
            return 100.0

        return (self.occupied / self.capacity) * 100

    def is_available(self) -> bool:
        """Check whether shelter can accept evacuees."""
        return (
            self.status == "SAFE"
            and self.accessible
            and self.available_capacity > 0
        )

    def add_occupants(self, count: int) -> bool:
        """
        Add evacuees to shelter.

        Returns True if successful.
        Returns False if there is insufficient capacity.
        """
        if count <= 0:
            return False

        if self.occupied + count > self.capacity:
            return False

        self.occupied += count

        if self.available_capacity == 0:
            self.status = "CONGESTED"

        return True

    def remove_occupants(self, count: int) -> bool:
        """Remove evacuees from shelter."""
        if count <= 0:
            return False

        if count > self.occupied:
            return False

        self.occupied -= count

        if self.status == "CONGESTED" and self.available_capacity > 0:
            self.status = "SAFE"

        return True

    def to_dict(self) -> dict:
        """Convert shelter to dictionary for JSON/API output."""
        return {
            "shelter_id": self.shelter_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "capacity": self.capacity,
            "occupied": self.occupied,
            "available_capacity": self.available_capacity,
            "occupancy_percentage": round(
                self.occupancy_percentage, 2
            ),
            "status": self.status,
            "accessible": self.accessible,
        }