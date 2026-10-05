from m2.cyclone_loader import load_cyclone_track

from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    group_track_by_cyclone,
    get_closest_observation
)


def test_chennai_cyclone_track():

    print()
    print("==========================================")
    print(" CHENNAI CYCLONE TRACK FILTER TEST")
    print("==========================================")

    print("\nSTEP 1: LOADING REAL CYCLONE DATA")

    hazards = load_cyclone_track()

    print(
        "Total observations:",
        len(hazards)
    )

    print("\nSTEP 2: FILTERING CHENNAI TRACK")

    relevant = get_chennai_relevant_track(
        hazards
    )

    print(
        "Chennai-relevant observations:",
        len(relevant)
    )

    print("\nSTEP 3: GROUPING BY CYCLONE")

    grouped = group_track_by_cyclone(
        relevant
    )

    print(
        "Cyclones found:",
        len(grouped)
    )

    for cyclone_id, track in grouped.items():

        print()
        print(
            "Cyclone:",
            cyclone_id
        )

        print(
            "Cyclone name:",
            track[0].cyclone_name
        )

        print(
            "Track observations:",
            len(track)
        )

    print("\nSTEP 4: CLOSEST OBSERVATION")

    closest = get_closest_observation(
        relevant
    )

    if closest is not None:

        print(
            "Track point:",
            closest.track_point_id
        )

        print(
            "Cyclone:",
            closest.cyclone_name
        )

        print(
            "Timestamp:",
            closest.timestamp_utc
        )

        print(
            "Latitude:",
            closest.latitude
        )

        print(
            "Longitude:",
            closest.longitude
        )

        print(
            "Wind speed:",
            closest.wind_speed,
            "km/h"
        )

        print(
            "Pressure:",
            closest.pressure,
            "hPa"
        )

        print(
            "Distance:",
            closest.distance_from_chennai_km,
            "km"
        )

        print(
            "IMD category:",
            closest.intensity_category
        )

    print()
    print("==========================================")
    print(" CHENNAI CYCLONE TRACK TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_chennai_cyclone_track()