from m2.hazard_status import (
    combine_statuses,
    calculate_effective_status
)


def test_hazard_status():

    print()
    print("==========================================")
    print(" MULTI-HAZARD STATUS TEST")
    print("==========================================")

    # ------------------------------------------
    # TEST 1
    # ------------------------------------------

    print("\nTEST 1: SAFE + SAFE")

    result = combine_statuses(
        "SAFE",
        "SAFE"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 2
    # ------------------------------------------

    print("\nTEST 2: RESTRICTED + SAFE")

    result = combine_statuses(
        "RESTRICTED",
        "SAFE"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 3
    # ------------------------------------------

    print("\nTEST 3: SAFE + BLOCKED")

    result = combine_statuses(
        "SAFE",
        "BLOCKED"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 4
    # ------------------------------------------

    print("\nTEST 4: RESTRICTED + BLOCKED")

    result = combine_statuses(
        "RESTRICTED",
        "BLOCKED"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 5
    # ------------------------------------------

    print("\nTEST 5: BLOCKED + RESTRICTED")

    result = combine_statuses(
        "BLOCKED",
        "RESTRICTED"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 6
    # ------------------------------------------

    print("\nTEST 6: ALL THREE HAZARDS")

    result = calculate_effective_status(
        base_status="SAFE",
        flood_status="RESTRICTED",
        cyclone_status="BLOCKED"
    )

    print(
        "Base:",
        "SAFE"
    )

    print(
        "Flood:",
        "RESTRICTED"
    )

    print(
        "Cyclone:",
        "BLOCKED"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 7
    # ------------------------------------------

    print("\nTEST 7: FLOOD BLOCKED + CYCLONE SAFE")

    result = calculate_effective_status(
        base_status="SAFE",
        flood_status="BLOCKED",
        cyclone_status="SAFE"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 8
    # ------------------------------------------

    print("\nTEST 8: FLOOD SAFE + CYCLONE RESTRICTED")

    result = calculate_effective_status(
        base_status="SAFE",
        flood_status="SAFE",
        cyclone_status="RESTRICTED"
    )

    print(
        "Effective:",
        result
    )

    # ------------------------------------------
    # TEST 9
    # ------------------------------------------

    print("\nTEST 9: ALL SAFE")

    result = calculate_effective_status(
        base_status="SAFE",
        flood_status="SAFE",
        cyclone_status="SAFE"
    )

    print(
        "Effective:",
        result
    )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_hazard_status()