import sys
from pathlib import Path

# Allow imports from src/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from m1.build_road_graph import build_chennai_graph
from m1.flood_loader import load_flood_kml
from m1.flood_engine import (
    FloodHazard,
    SpatialIndex,
    apply_flood_hazards
)
from m1.graph_export import export_road_status


FLOOD_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Inundation Points with Depth of Inundation.kml"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "flood_road_status.csv"
)


def prepare_flood_hazards(records):

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

        latitude = attributes.get(
            "F_LATITUDE"
        )

        longitude = attributes.get(
            "F_LONGITUDE"
        )

        depth = attributes.get(
            "DEPTH"
        )

        if (
            latitude is None
            or longitude is None
        ):

            if not coordinates:
                continue

            longitude = coordinates[0][0]
            latitude = coordinates[0][1]

        try:

            latitude = float(latitude)
            longitude = float(longitude)

        except (
            TypeError,
            ValueError
        ):

            continue

        try:

            depth = float(depth)

        except (
            TypeError,
            ValueError
        ):

            depth = 0.0

        if depth >= 5:

            severity = "CRITICAL"

        elif depth >= 3:

            severity = "HIGH"

        elif depth >= 1:

            severity = "MODERATE"

        else:

            severity = "LOW"

        hazards.append(
            FloodHazard(
                hazard_id=f"FLOOD_{index:03d}",
                latitude=latitude,
                longitude=longitude,
                severity=severity,
                depth=depth,
                source=(
                    "Chennai Inundation Points "
                    "with Depth of Inundation"
                )
            )
        )

    return hazards


def main():

    print()
    print("==========================================")
    print(" M1 - FLOOD GRAPH EXPORT TEST")
    print("==========================================")
    print()

    # -------------------------------------------------
    # 1. Build real Chennai graph
    # -------------------------------------------------

    print(
        "Building real Chennai road graph..."
    )

    graph = build_chennai_graph()

    print()
    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # -------------------------------------------------
    # 2. Load real flood data
    # -------------------------------------------------

    print()
    print(
        "Loading real Chennai flood data..."
    )

    records = load_flood_kml(
        str(FLOOD_KML)
    )

    hazards = prepare_flood_hazards(
        records
    )

    print(
        "Flood hazards:",
        len(hazards)
    )

    # -------------------------------------------------
    # 3. Build spatial index
    # -------------------------------------------------

    print()
    print(
        "Building spatial index..."
    )

    spatial_index = SpatialIndex(
        cell_size=0.001
    )

    for node_id, node in graph.nodes.items():

        spatial_index.add_node(
            node
        )

    # -------------------------------------------------
    # 4. Apply flood impact
    # -------------------------------------------------

    print(
        "Applying flood impact..."
    )

    result = apply_flood_hazards(
        graph,
        spatial_index,
        hazards
    )

    blocked_roads = result[
        "BLOCKED"
    ]

    restricted_roads = result[
        "RESTRICTED"
    ]

    print(
        "Blocked roads:",
        len(blocked_roads)
    )

    print(
        "Restricted roads:",
        len(restricted_roads)
    )

    # -------------------------------------------------
    # 5. Export updated road status
    # -------------------------------------------------

    print()
    print(
        "Exporting flood-updated road status..."
    )

    export_road_status(
        graph,
        str(OUTPUT_FILE)
    )

    # -------------------------------------------------
    # 6. Verify output
    # -------------------------------------------------

    assert OUTPUT_FILE.exists(), (
        "Flood road status file was not created."
    )

    with open(
        OUTPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    assert len(lines) > 1, (
        "Flood road status file is empty."
    )

    header = lines[0].strip()

    assert header == "road_id,status", (
        "Incorrect CSV header."
    )

    exported_statuses = []

    for line in lines[1:]:

        parts = line.strip().split(",")

        if len(parts) == 2:

            exported_statuses.append(
                parts[1]
            )

    assert "BLOCKED" in exported_statuses, (
        "No BLOCKED roads found in exported file."
    )

    print()
    print(
        "Exported road records:",
        len(exported_statuses)
    )

    print(
        "Flood-updated road status file:",
        OUTPUT_FILE
    )

    print()
    print("==========================================")
    print(" FLOOD GRAPH EXPORT TEST PASSED")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()