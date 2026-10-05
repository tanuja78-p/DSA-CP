from m2.cyclone_state import CycloneStateManager


def test_cyclone_state_manager():

    print()
    print("==========================================")
    print(" CYCLONE STATE MANAGER TEST")
    print("==========================================")

    manager = CycloneStateManager()

    # ------------------------------------------
    # FIRST UPDATE
    # ------------------------------------------

    result1 = manager.update({
        "R1",
        "R2",
        "R3"
    })

    print("\nFIRST UPDATE")

    print(
        "New:",
        sorted(result1["newly_affected"])
    )

    print(
        "Still:",
        sorted(result1["still_affected"])
    )

    print(
        "Removed:",
        sorted(result1["no_longer_affected"])
    )

    # ------------------------------------------
    # SECOND UPDATE
    # ------------------------------------------

    result2 = manager.update({
        "R2",
        "R3",
        "R4"
    })

    print("\nSECOND UPDATE")

    print(
        "New:",
        sorted(result2["newly_affected"])
    )

    print(
        "Still:",
        sorted(result2["still_affected"])
    )

    print(
        "Removed:",
        sorted(result2["no_longer_affected"])
    )

    # ------------------------------------------
    # THIRD UPDATE
    # ------------------------------------------

    result3 = manager.update({
        "R4"
    })

    print("\nTHIRD UPDATE")

    print(
        "New:",
        sorted(result3["newly_affected"])
    )

    print(
        "Still:",
        sorted(result3["still_affected"])
    )

    print(
        "Removed:",
        sorted(result3["no_longer_affected"])
    )

    # ------------------------------------------
    # FINAL STATE
    # ------------------------------------------

    print("\nFINAL CYCLONE STATE")

    print(
        "Affected roads:",
        sorted(manager.get_current_roads())
    )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_state_manager()