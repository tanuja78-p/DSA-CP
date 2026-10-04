from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from m1.flood_loader import (
    load_and_print_flood_kml
)


FLOOD_DATASETS = [

    PROJECT_ROOT
    / "data"
    / "Chennai Flood Hazard Zones Map.kml",

    PROJECT_ROOT
    / "data"
    / "Chennai Flooding Points in 2015.kml",

    PROJECT_ROOT
    / "data"
    / "Chennai Inundation Points with Depth of Inundation.kml",

    PROJECT_ROOT
    / "data"
    / "Flood hotspots in Chennai in 2020 from Cyclone Nivar..kml"
]


def main():

    print()
    print("==========================================")
    print(" M1 - CHENNAI FLOOD DATA LOADER TEST")
    print("==========================================")

    for dataset in FLOOD_DATASETS:

        print()
        print()
        print(
            "Loading:"
        )

        print(
            dataset.name
        )

        print("------------------------------------------")

        if not dataset.exists():

            print(
                "WARNING: File not found."
            )

            continue

        try:

            load_and_print_flood_kml(
                str(dataset)
            )

        except Exception as error:

            print(
                f"ERROR: {error}"
            )

    print()
    print("==========================================")
    print(" FLOOD LOADER TEST COMPLETE")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()