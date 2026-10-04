from pathlib import Path
import sys


# Find project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Add src folder to Python import path
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))


from m1.flood_loader import load_flood_kml
from m1.flood_engine import (
    FloodHazard,
    classify_flood_severity
)
from m1.flood_export import export_flood_hazards


INUNDATION_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Inundation Points with Depth of Inundation.kml"
)

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    PROCESSED_DATA
    / "flood_hazards.csv"
)


def build_flood_hazards():

    records = load_flood_kml(
        str(INUNDATION_KML)
    )

    hazards = []

    for index, record in enumerate(
        records,
        start=1
    ):

        attributes = record.get(
            "attributes",
            {}
        )

        coordinates = record.get(
            "coordinates",
            []
        )

        # Use the actual latitude/longitude fields
        # from the Chennai flood dataset.
        latitude_text = attributes.get(
            "F_LATITUDE"
        )

        longitude_text = attributes.get(
            "F_LONGITUDE"
        )

        depth_text = attributes.get(
            "DEPTH"
        )

        # Fall back to geometry coordinates
        # if latitude/longitude attributes are missing.
        if latitude_text is not None:
            latitude = float(latitude_text)
        elif coordinates:
            latitude = float(coordinates[0][1])
        else:
            continue

        if longitude_text is not None:
            longitude = float(longitude_text)
        elif coordinates:
            longitude = float(coordinates[0][0])
        else:
            continue

        depth = None

        if depth_text not in (None, ""):
            depth = float(depth_text)

        severity = classify_flood_severity(
            depth=depth
        )

        hazard = FloodHazard(
            hazard_id=f"FLOOD_{index:03d}",
            latitude=latitude,
            longitude=longitude,
            severity=severity,
            depth=depth,
            source="Chennai Inundation Points with Depth of Inundation"
        )

        hazards.append(hazard)

    return hazards


def main():

    print()
    print("==========================================")
    print(" M1 - FLOOD DATA EXPORT TEST")
    print("==========================================")
    print()

    print(
        "Loading real inundation dataset..."
    )

    hazards = build_flood_hazards()

    print(
        f"Flood hazards prepared: {len(hazards)}"
    )

    print()

    print(
        "Exporting processed flood data..."
    )

    export_flood_hazards(
        hazards,
        str(OUTPUT_FILE)
    )

    print()

    print("==========================================")
    print(" FLOOD EXPORT COMPLETE")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()