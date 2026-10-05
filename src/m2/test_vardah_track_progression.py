from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    group_track_by_cyclone
)


def test_vardah_track_progression():

    print()
    print("==========================================")
    print(" VARDAH TRACK PROGRESSION")
    print("==========================================")

    # ------------------------------------------
    # STEP 1
    # ------------------------------------------

    print("\nSTEP 1: LOADING CYCLONE DATA")

    hazards = load_cyclone_track()

    print(
        "Total cyclone observations:",
        len(hazards)
    )

    # ------------------------------------------
    # STEP 2
    # ------------------------------------------

    print("\nSTEP 2: FILTERING CHENNAI-RELEVANT DATA")

    relevant = get_chennai_relevant_track(
        hazards
    )

    print(
        "Chennai-relevant observations:",
        len(relevant)
    )

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print("\nSTEP 3: GROUPING BY CYCLONE")

    grouped = group_track_by_cyclone(
        relevant
    )

    print(
        "Cyclones:",
        len(grouped)
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print("\nSTEP 4: VARDAH TRACK")

    vardah = grouped.get("vardah", [])

    print(
        "Vardah observations:",
        len(vardah)
    )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    # Sort by timestamp.
    vardah = sorted(
        vardah,
        key=lambda hazard:
            hazard.timestamp_utc
    )

    print()
    print(
        "TRACK POINT | TIMESTAMP | LAT | LON | "
        "WIND | PRESSURE | DISTANCE"
    )

    print(
        "-" * 90
    )

    for hazard in vardah:

        print(
            hazard.track_point_id,
            "|",
            hazard.timestamp_utc,
            "|",
            hazard.latitude,
            "|",
            hazard.longitude,
            "|",
            hazard.wind_speed,
            "|",
            hazard.pressure,
            "|",
            hazard.distance_from_chennai_km,
            "km"
        )

    # ------------------------------------------
    # FINAL
    # ------------------------------------------

    print()
    print("==========================================")
    print(" VARDAH TRACK ANALYSIS COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_vardah_track_progression()