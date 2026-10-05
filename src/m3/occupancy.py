class OccupancyManager:
    """Handles dynamic shelter occupancy updates."""

    def __init__(self, shelter_map):
        self.shelter_map = shelter_map

    def admit(self, shelter_id, people):
        """Add evacuees to a shelter."""
        shelter = self.shelter_map.get(shelter_id)

        if shelter is None:
            return {
                "success": False,
                "reason": "Shelter not found",
            }

        if shelter.add_occupants(people):
            return {
                "success": True,
                "shelter_id": shelter_id,
                "occupied": shelter.occupied,
                "available_capacity": shelter.available_capacity,
            }

        return {
            "success": False,
            "reason": "Insufficient shelter capacity",
            "shelter_id": shelter_id,
            "available_capacity": shelter.available_capacity,
        }

    def release(self, shelter_id, people):
        """Remove evacuees from a shelter."""
        shelter = self.shelter_map.get(shelter_id)

        if shelter is None:
            return {
                "success": False,
                "reason": "Shelter not found",
            }

        if shelter.remove_occupants(people):
            return {
                "success": True,
                "shelter_id": shelter_id,
                "occupied": shelter.occupied,
                "available_capacity": shelter.available_capacity,
            }

        return {
            "success": False,
            "reason": "Invalid release amount",
            "shelter_id": shelter_id,
        }

    def update_status(
        self,
        shelter_id,
        status=None,
        accessible=None,
    ):
        """Update shelter safety/accessibility."""
        shelter = self.shelter_map.get(shelter_id)

        if shelter is None:
            return False

        if status is not None:
            shelter.status = status.upper()

        if accessible is not None:
            shelter.accessible = accessible

        return True