class EvacueeGroup:
    """
    Represents a group of people being evacuated.

    Status flow:
        WAITING -> ON_ROUTE -> ARRIVED
    """

    def __init__(
        self,
        group_id,
        people_count,
        source,
        priority,
        destination=None,
        backup_shelter=None,
        route=None,
        status="WAITING",
    ):
        self.group_id = group_id
        self.people_count = people_count
        self.source = source
        self.priority = priority
        self.destination = destination
        self.backup_shelter = backup_shelter
        self.route = route if route is not None else []
        self.status = status

    def start_route(self):
        """Mark the evacuation group as being on the way."""
        self.status = "ON_ROUTE"

    def mark_arrived(self):
        """Mark the evacuation group as arrived."""
        self.status = "ARRIVED"

    def to_dict(self):
        """Return the evacuation group as a dictionary."""
        return {
            "group_id": self.group_id,
            "people_count": self.people_count,
            "source": self.source,
            "priority": self.priority,
            "destination": self.destination,
            "backup_shelter": self.backup_shelter,
            "route": self.route,
            "status": self.status,
        }

    def __repr__(self):
        return (
            f"EvacueeGroup("
            f"group_id='{self.group_id}', "
            f"people_count={self.people_count}, "
            f"status='{self.status}'"
            f")"
        )