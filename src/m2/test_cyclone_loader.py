from m2.cyclone_loader import (
    load_cyclone_track,
    get_cyclone_csv_path
)


def test_cyclone_loader():

    print()
    print("==========================================")
    print(" REAL CYCLONE DATASET LOADER TEST")
    print("==========================================")

    print("\nSTEP 1: DATASET PATH")

    print(
        "CSV:",
        get_cyclone_csv_path()
    )

    print("\nSTEP 2: LOADING CYCLONE DATASET")

    hazards = load_cyclone_track()

    print(
        "Cyclone observations loaded:",
        len(hazards)
    )

    print("\nSTEP 3: FIRST OBSERVATIONS")

    for index, hazard in enumerate(
        hazards[:5],
        start=1
    ):

        print()
        print("Observation", index)

        print(
            "Track point:",
            hazard.track_point_id
        )

        print(
            "Cyclone ID:",
            hazard.cyclone_id
        )

        print(
            "Cyclone:",
            hazard.cyclone_name
        )

        print(
            "Timestamp:",
            hazard.timestamp_utc
        )

        print(
            "Latitude:",
            hazard.latitude
        )

        print(
            "Longitude:",
            hazard.longitude
        )

        print(
            "Wind speed:",
            hazard.wind_speed
        )

        print(
            "Pressure:",
            hazard.pressure
        )

        print(
            "Distance from Chennai:",
            hazard.distance_from_chennai_km,
            "km"
        )

        print(
            "IMD category:",
            hazard.intensity_category
        )

    print()
    print("==========================================")
    print(" CYCLONE DATASET LOADER TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_loader()