class CycloneStateManager:
    """
    Tracks which roads are currently affected by the cyclone.

    This allows the system to distinguish:
        - newly affected roads
        - roads still affected
        - roads no longer affected
    """

    def __init__(self):
        self.affected_roads = set()

    def get_current_roads(self):
        return set(self.affected_roads)

    def update(self, new_affected_roads):
        new_affected_roads = set(new_affected_roads)

        newly_affected = (
            new_affected_roads
            - self.affected_roads
        )

        no_longer_affected = (
            self.affected_roads
            - new_affected_roads
        )

        still_affected = (
            self.affected_roads
            & new_affected_roads
        )

        self.affected_roads = new_affected_roads

        return {
            "newly_affected": newly_affected,
            "still_affected": still_affected,
            "no_longer_affected": no_longer_affected
        }