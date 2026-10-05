from m2.hazard_registry import HazardRegistry


def test_hazard_registry():

    print()
    print("==========================================")
    print(" MULTI-HAZARD ROAD REGISTRY TEST")
    print("==========================================")

    registry = HazardRegistry()

    # --------------------------------------------------
    # ROAD 1
    # --------------------------------------------------

    registry.set_flood_status(
        "R1",
        "BLOCKED"
    )

    registry.set_cyclone_status(
        "R1",
        "SAFE"
    )

    print("\nROAD R1")

    print(
        registry.get_road_statuses("R1")
    )

    # --------------------------------------------------
    # ROAD 2
    # --------------------------------------------------

    registry.set_flood_status(
        "R2",
        "SAFE"
    )

    registry.set_cyclone_status(
        "R2",
        "BLOCKED"
    )

    print("\nROAD R2")

    print(
        registry.get_road_statuses("R2")
    )

    # --------------------------------------------------
    # ROAD 3
    # --------------------------------------------------

    registry.set_flood_status(
        "R3",
        "RESTRICTED"
    )

    registry.set_cyclone_status(
        "R3",
        "RESTRICTED"
    )

    print("\nROAD R3")

    print(
        registry.get_road_statuses("R3")
    )

    # --------------------------------------------------
    # ROAD 4
    # --------------------------------------------------

    registry.set_flood_status(
        "R4",
        "BLOCKED"
    )

    registry.set_cyclone_status(
        "R4",
        "BLOCKED"
    )

    print("\nROAD R4")

    print(
        registry.get_road_statuses("R4")
    )

    # --------------------------------------------------
    # CYCLONE LEAVES R4
    # --------------------------------------------------

    registry.set_cyclone_status(
        "R4",
        "SAFE"
    )

    print("\nR4 AFTER CYCLONE LEAVES")

    print(
        registry.get_road_statuses("R4")
    )

    # --------------------------------------------------
    # FINAL ROAD IDS
    # --------------------------------------------------

    print("\nREGISTERED ROADS")

    print(
        sorted(
            registry.get_all_road_ids()
        )
    )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_hazard_registry()