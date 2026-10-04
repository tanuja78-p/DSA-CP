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
from m1.graph_update import (
    recover_roads,
    count_road_statuses
)


FLOOD_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Inundation Points with Depth of Inundation.kml"
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
    print(" M1 - FLOOD RECOVERY TEST")
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
    # 2. Check initial state
    # -------------------------------------------------

    initial_status = count_road_statuses(
        graph
    )

    print()
    print(
        "Road status before flood:"
    )

    print(
        initial_status
    )

    assert initial_status["BLOCKED"] == 0, (
        "Graph should initially have no blocked roads."
    )

    # -------------------------------------------------
    # 3. Load real flood data
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
    # 4. Build spatial index
    # -------------------------------------------------

    print()
    print(
        "Building flood spatial index..."
    )

    spatial_index = SpatialIndex(
        cell_size=0.001
    )

    for node_id, node in graph.nodes.items():

        spatial_index.add_node(
            node
        )

    # -------------------------------------------------
    # 5. Apply flood
    # -------------------------------------------------

    print()
    print(
        "Applying flood impact..."
    )

    result = apply_flood_hazards(
        graph,
        spatial_index,
        hazards
    )

    blocked_roads = set(
        result["BLOCKED"]
    )

    restricted_roads = set(
        result["RESTRICTED"]
    )

    print(
        "Blocked roads:",
        len(blocked_roads)
    )

    print(
        "Restricted roads:",
        len(restricted_roads)
    )

    flood_status = count_road_statuses(
        graph
    )

    print()
    print(
        "Road status after flood:"
    )

    print(
        flood_status
    )

    assert flood_status["BLOCKED"] > 0, (
        "Flood should block at least one road."
    )

    # -------------------------------------------------
    # 6. Recover blocked roads
    # -------------------------------------------------

    print()
    print(
        "Recovering flood-affected roads..."
    )

    recovered = recover_roads(
        graph,
        blocked_roads
    )

    print(
        "Roads recovered:",
        recovered
    )

    # -------------------------------------------------
    # 7. Verify recovery
    # -------------------------------------------------

    recovered_status = count_road_statuses(
        graph
    )

    print()
    print(
        "Road status after recovery:"
    )

    print(
        recovered_status
    )

    assert recovered == len(
        blocked_roads
    ), (
        "Not all blocked roads were recovered."
    )

    assert recovered_status["BLOCKED"] == 0, (
        "Blocked roads should be zero after recovery."
    )

    assert recovered_status["SAFE"] == (
        initial_status["SAFE"]
    ), (
        "All recovered roads should return to SAFE."
    )

    print()
    print("==========================================")
    print(" FLOOD RECOVERY TEST PASSED")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()