from m2.cyclone_state import CycloneStateManager


class CycloneGraphStateManager:
    """
    Connects cyclone state tracking with graph road statuses.

    This manager tracks the roads whose status was changed
    specifically by the cyclone.
    """

    def __init__(self):
        self.state = CycloneStateManager()

        # Stores the road status before the cyclone changed it.
        self.previous_status = {}

    def update_graph(self, graph, affected_roads):

        affected_roads = set(affected_roads)

        changes = self.state.update(
            affected_roads
        )

        newly_affected = changes[
            "newly_affected"
        ]

        no_longer_affected = changes[
            "no_longer_affected"
        ]

        still_affected = changes[
            "still_affected"
        ]

        # ------------------------------------------
        # NEWLY AFFECTED
        # ------------------------------------------

        for road_id in newly_affected:

            current_status = graph.get_road_status(
                road_id
            )

            if current_status is not None:

                self.previous_status[
                    road_id
                ] = current_status

                graph.update_road_status(
                    road_id,
                    "BLOCKED"
                )

        # ------------------------------------------
        # NO LONGER AFFECTED
        # ------------------------------------------

        for road_id in no_longer_affected:

            if road_id in self.previous_status:

                original_status = (
                    self.previous_status[
                        road_id
                    ]
                )

                graph.update_road_status(
                    road_id,
                    original_status
                )

                del self.previous_status[
                    road_id
                ]

        return {
            "newly_affected": sorted(
                newly_affected
            ),
            "still_affected": sorted(
                still_affected
            ),
            "no_longer_affected": sorted(
                no_longer_affected
            )
        }