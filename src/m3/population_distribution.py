class PopulationDistributor:
    """
    Distributes an evacuation population across routes
    according to route capacity.
    """

    def distribute(self, total_people, routes):
        """
        Distribute people across routes.

        routes format:
        [
            {"route_id": "R1", "capacity": 200},
            {"route_id": "R2", "capacity": 180},
            {"route_id": "R3", "capacity": 250}
        ]
        """

        if total_people < 0:
            raise ValueError("total_people cannot be negative")

        if not routes:
            return []

        remaining_people = total_people
        allocations = []

        for route in routes:
            route_id = route["route_id"]
            capacity = route["capacity"]

            if capacity < 0:
                raise ValueError(
                    f"Capacity for route {route_id} cannot be negative"
                )

            assigned = min(remaining_people, capacity)

            allocations.append(
                {
                    "route_id": route_id,
                    "capacity": capacity,
                    "assigned": assigned,
                    "remaining_capacity": capacity - assigned,
                }
            )

            remaining_people -= assigned

            if remaining_people == 0:
                break

        return allocations

    def get_unassigned_people(self, total_people, allocations):
        """Return people who could not be assigned."""

        assigned = sum(
            item["assigned"]
            for item in allocations
        )

        return total_people - assigned

    def is_fully_distributed(self, total_people, allocations):
        """Return True if everyone was assigned."""

        return self.get_unassigned_people(
            total_people,
            allocations
        ) == 0