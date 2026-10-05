from m2.road_hazard_state import RoadHazardState


class HazardRegistry:

    def __init__(self):
        self.roads = {}

    def get_or_create(self, road_id):

        if road_id not in self.roads:

            self.roads[road_id] = (
                RoadHazardState()
            )

        return self.roads[road_id]

    def set_flood_status(
        self,
        road_id,
        status
    ):

        road = self.get_or_create(
            road_id
        )

        road.set_flood_status(
            status
        )

    def set_cyclone_status(
        self,
        road_id,
        status
    ):

        road = self.get_or_create(
            road_id
        )

        road.set_cyclone_status(
            status
        )

    def set_base_status(
        self,
        road_id,
        status
    ):

        road = self.get_or_create(
            road_id
        )

        road.set_base_status(
            status
        )

    def get_effective_status(
        self,
        road_id
    ):

        road = self.get_or_create(
            road_id
        )

        return road.get_effective_status()

    def get_road_statuses(
        self,
        road_id
    ):

        road = self.get_or_create(
            road_id
        )

        return road.get_statuses()

    def get_all_road_ids(self):

        return list(
            self.roads.keys()
        )