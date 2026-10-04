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
from m1.graph_update import count_road_statuses


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

        # Fallback to KML coordinates
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

        # Classify flood severity from inundation depth
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
    print(" M1 - FLOOD + CHENNAI GRAPH INTEGRATION")
    print("==========================================")
    print()

    # -------------------------------------------------
    # 1. Build the real Chennai road graph
    # -------------------------------------------------

    print("Loading Chennai road network...")

    graph = build_chennai_graph()

    print()
    print("Real Chennai graph created.")

    print(
        "Graph nodes :",
        graph.get_node_count()
    )

    print(
        "Graph edges :",
        graph.get_edge_count()
    )

    # -------------------------------------------------
    # 2. Load real Chennai flood observations
    # -------------------------------------------------

    print()
    print("Loading real Chennai flood data...")

    flood_records = load_flood_kml(
        str(FLOOD_KML)
    )

    print()
    print(
        "Flood records loaded:",
        len(flood_records)
    )

    # -------------------------------------------------
    # 3. Prepare FloodHazard objects
    # -------------------------------------------------

    hazards = prepare_flood_hazards(
        flood_records
    )

    print(
        "Flood hazards prepared:",
        len(hazards)
    )

    # -------------------------------------------------
    # 4. Build spatial index for road nodes
    # -------------------------------------------------

    print()
    print("Building flood spatial index...")

    spatial_index = SpatialIndex(
        cell_size=0.001
    )

    for node_id, node in graph.nodes.items():

        spatial_index.add_node(
            node
        )

    print(
        "Spatial index created."
    )

    # -------------------------------------------------
    # 5. Road status before flood
    # -------------------------------------------------

    print()
    print("Road status before flood:")

    before_status = count_road_statuses(
        graph
    )

    print(
        before_status
    )

    # -------------------------------------------------
    # 6. Apply real flood hazards
    # -------------------------------------------------

    print()
    print("Applying real flood hazards...")

    result = apply_flood_hazards(
        graph,
        spatial_index,
        hazards
    )

    affected_nodes = result[
        "affected_nodes"
    ]

    blocked_roads = result[
        "BLOCKED"
    ]

    restricted_roads = result[
        "RESTRICTED"
    ]

    # -------------------------------------------------
    # 7. Display flood impact
    # -------------------------------------------------

    print()
    print(
        "Flood impact applied successfully."
    )

    print(
        "Affected nodes  :",
        len(affected_nodes)
    )

    print(
        "Blocked roads   :",
        len(blocked_roads)
    )

    print(
        "Restricted roads:",
        len(restricted_roads)
    )

    # -------------------------------------------------
    # 8. Road status after flood
    # -------------------------------------------------

    print()
    print("Road status after flood:")

    after_status = count_road_statuses(
        graph
    )

    print(
        after_status
    )

    # -------------------------------------------------
    # 9. Verify integration
    # -------------------------------------------------

    assert len(hazards) > 0, (
        "No flood hazards were prepared."
    )

    assert len(affected_nodes) > 0, (
        "No graph nodes were affected."
    )

    assert (
        len(blocked_roads)
        + len(restricted_roads)
        > 0
    ), (
        "Flood hazards did not update "
        "any roads."
    )

    assert (
        after_status["BLOCKED"]
        + after_status["RESTRICTED"]
        > 0
    ), (
        "Road graph was not updated "
        "by flood hazards."
    )

    print()
    print("==========================================")
    print(" FLOOD + GRAPH INTEGRATION TEST PASSED")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()