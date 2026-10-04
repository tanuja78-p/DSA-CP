from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from m1.graph import (
    Graph,
    make_node_id,
    haversine_distance
)

from m1.data_loader import (
    load_road_centerlines
)

from m1.flood_loader import (
    load_flood_kml
)

from m1.flood_engine import (
    FloodHazard,
    build_spatial_index,
    apply_flood_hazards,
    classify_flood_severity
)


ROAD_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Road centerline map.kml"
)


INUNDATION_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Inundation Points with Depth of Inundation.kml"
)


def build_chennai_graph():

    print(
        "Loading Chennai road network..."
    )

    roads = load_road_centerlines(
        str(ROAD_KML)
    )

    graph = Graph()

    for road in roads:

        road_id = road["road_id"]

        if not road_id:
            continue

        coordinates = road["coordinates"]

        for i in range(
            len(coordinates) - 1
        ):

            longitude1, latitude1 = (
                coordinates[i]
            )

            longitude2, latitude2 = (
                coordinates[i + 1]
            )

            node1 = make_node_id(
                longitude1,
                latitude1
            )

            node2 = make_node_id(
                longitude2,
                latitude2
            )

            if node1 == node2:

                continue

            graph.add_node(
                node1,
                latitude1,
                longitude1
            )

            graph.add_node(
                node2,
                latitude2,
                longitude2
            )

            distance = haversine_distance(
                latitude1,
                longitude1,
                latitude2,
                longitude2
            )

            graph.add_edge(
                node1,
                node2,
                road_id,
                distance
            )

    return graph


def load_inundation_hazards():

    records = load_flood_kml(
        str(INUNDATION_KML)
    )

    hazards = []

    for record in records:

        attributes = record[
            "attributes"
        ]

        coordinates = record[
            "coordinates"
        ]

        if not coordinates:

            continue

        longitude, latitude = (
            coordinates[0]
        )

        depth = None

        depth_text = attributes.get(
            "DEPTH"
        )

        if depth_text:

            try:

                depth = float(
                    depth_text
                )

            except ValueError:

                depth = None

        severity = classify_flood_severity(
            depth=depth
        )

        hazard = FloodHazard(
            hazard_id=str(
                record["record_id"]
            ),
            latitude=latitude,
            longitude=longitude,
            severity=severity,
            depth=depth,
            source=(
                "Chennai Inundation "
                "Points with Depth"
            )
        )

        hazards.append(
            hazard
        )

    return hazards


def main():

    print()
    print("==========================================")
    print(" M1 - FLOOD HAZARD ENGINE TEST")
    print("==========================================")
    print()

    graph = build_chennai_graph()

    print()
    print(
        f"Road graph nodes: "
        f"{graph.get_node_count()}"
    )

    print(
        f"Road graph edges: "
        f"{graph.get_edge_count()}"
    )

    print()
    print(
        "Building spatial index..."
    )

    spatial_index = build_spatial_index(
        graph
    )

    print(
        "Spatial index created."
    )

    print()
    print(
        "Loading real inundation dataset..."
    )

    hazards = load_inundation_hazards()

    print(
        f"Flood hazards loaded: "
        f"{len(hazards)}"
    )

    severity_counts = {}

    for hazard in hazards:

        severity_counts[
            hazard.severity
        ] = (
            severity_counts.get(
                hazard.severity,
                0
            ) + 1
        )

    print()
    print("Flood severity distribution:")

    for severity, count in (
        severity_counts.items()
    ):

        print(
            f"  {severity}: {count}"
        )

    print()
    print(
        "Applying flood hazards "
        "to road graph..."
    )

    result = apply_flood_hazards(
        graph,
        spatial_index,
        hazards
    )

    print()
    print("==========================================")
    print(" FLOOD IMPACT RESULT")
    print("==========================================")

    print(
        f"Affected nodes: "
        f"{len(result['affected_nodes'])}"
    )

    print(
        f"Restricted roads: "
        f"{len(result['RESTRICTED'])}"
    )

    print(
        f"Blocked roads: "
        f"{len(result['BLOCKED'])}"
    )

    print()

    print(
        "First 10 affected nodes:"
    )

    for node_id in (
        result["affected_nodes"][:10]
    ):

        print(
            f"  {node_id}"
        )

    print()
    print("==========================================")
    print(" FLOOD ENGINE TEST COMPLETE")
    print("==========================================")
    print()


if __name__ == "__main__":

    main()