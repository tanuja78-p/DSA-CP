from math import sqrt

from m1.build_road_graph import build_chennai_graph
from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)


def calculate_distance_degrees(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):
    """
    Calculate approximate coordinate-space distance.
    """

    return sqrt(
        (latitude1 - latitude2) ** 2 +
        (longitude1 - longitude2) ** 2
    )


def find_nodes_within_radius(
    graph,
    latitude,
    longitude,
    radius_degrees
):
    """
    Find Chennai road nodes within the specified
    coordinate-space radius.
    """

    affected_nodes = []

    for node_id, node in graph.nodes.items():

        distance = calculate_distance_degrees(
            latitude,
            longitude,
            node.latitude,
            node.longitude
        )

        if distance <= radius_degrees:
            affected_nodes.append(
                (node_id, distance)
            )

    return affected_nodes


def test_cyclone_impact_radius():

    print()
    print("==========================================")
    print(" CYCLONE IMPACT RADIUS ANALYSIS")
    print("==========================================")

    # ------------------------------------------------
    # STEP 1
    # ------------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI ROAD GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # ------------------------------------------------
    # STEP 2
    # ------------------------------------------------

    print("\nSTEP 2: SELECTING REAL CYCLONE OBSERVATION")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    cyclone = get_closest_observation(
        relevant
    )

    print(
        "Cyclone:",
        cyclone.cyclone_name
    )

    print(
        "Track point:",
        cyclone.track_point_id
    )

    print(
        "Timestamp:",
        cyclone.timestamp_utc
    )

    print(
        "Latitude:",
        cyclone.latitude
    )

    print(
        "Longitude:",
        cyclone.longitude
    )

    print(
        "Distance from Chennai:",
        cyclone.distance_from_chennai_km,
        "km"
    )

    # ------------------------------------------------
    # STEP 3
    # ------------------------------------------------

    print("\nSTEP 3: TESTING IMPACT RADII")

    # Coordinate-space radii.
    #
    # These are deliberately small because this
    # test is measuring local road-network coverage.
    radii = [
        0.001,
        0.002,
        0.003,
        0.005,
        0.010
    ]

    for radius in radii:

        affected = find_nodes_within_radius(
            graph,
            cyclone.latitude,
            cyclone.longitude,
            radius
        )

        print()
        print(
            "Radius:",
            radius,
            "coordinate degrees"
        )

        print(
            "Affected nodes:",
            len(affected)
        )

        if affected:

            nearest = min(
                affected,
                key=lambda item: item[1]
            )

            print(
                "Nearest affected node:",
                nearest[0]
            )

            print(
                "Coordinate distance:",
                nearest[1]
            )

    print()
    print("==========================================")
    print(" IMPACT RADIUS ANALYSIS COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_impact_radius()