from m2.road_hazard_state import RoadHazardState


def print_state(label, road):

    state = road.get_statuses()

    print()
    print(label)

    print(
        "Base:",
        state["base"]
    )

    print(
        "Flood:",
        state["flood"]
    )

    print(
        "Cyclone:",
        state["cyclone"]
    )

    print(
        "Effective:",
        state["effective"]
    )


def test_road_hazard_state():

    print()
    print("==========================================")
    print(" ROAD HAZARD STATE TEST")
    print("==========================================")

    road = RoadHazardState()

    # --------------------------------------------------
    # INITIAL
    # --------------------------------------------------

    print_state(
        "INITIAL ROAD",
        road
    )

    # --------------------------------------------------
    # FLOOD ARRIVES
    # --------------------------------------------------

    road.set_flood_status(
        "BLOCKED"
    )

    print_state(
        "AFTER FLOOD",
        road
    )

    # --------------------------------------------------
    # CYCLONE ARRIVES
    # --------------------------------------------------

    road.set_cyclone_status(
        "BLOCKED"
    )

    print_state(
        "AFTER CYCLONE",
        road
    )

    # --------------------------------------------------
    # CYCLONE LEAVES
    # --------------------------------------------------

    road.set_cyclone_status(
        "SAFE"
    )

    print_state(
        "AFTER CYCLONE LEAVES",
        road
    )

    # --------------------------------------------------
    # FLOOD LEAVES
    # --------------------------------------------------

    road.set_flood_status(
        "SAFE"
    )

    print_state(
        "AFTER FLOOD LEAVES",
        road
    )

    # --------------------------------------------------
    # DIFFERENT COMBINATION
    # --------------------------------------------------

    road.set_flood_status(
        "RESTRICTED"
    )

    road.set_cyclone_status(
        "RESTRICTED"
    )

    print_state(
        "FLOOD + CYCLONE RESTRICTED",
        road
    )

    # --------------------------------------------------
    # FINAL
    # --------------------------------------------------

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_road_hazard_state()