from m2.hazard_status import calculate_effective_status


class RoadHazardState:

    def __init__(
        self,
        base_status="SAFE",
        flood_status="SAFE",
        cyclone_status="SAFE"
    ):
        self.base_status = base_status
        self.flood_status = flood_status
        self.cyclone_status = cyclone_status

    def get_effective_status(self):

        return calculate_effective_status(
            base_status=self.base_status,
            flood_status=self.flood_status,
            cyclone_status=self.cyclone_status
        )

    def set_flood_status(self, status):

        self.flood_status = status

    def set_cyclone_status(self, status):

        self.cyclone_status = status

    def set_base_status(self, status):

        self.base_status = status

    def get_statuses(self):

        return {
            "base": self.base_status,
            "flood": self.flood_status,
            "cyclone": self.cyclone_status,
            "effective": self.get_effective_status()
        }