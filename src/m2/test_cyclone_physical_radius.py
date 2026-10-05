from m1.build_road_graph import build_chennai_graph
from m1.graph import haversine_distance

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)


def find_nodes_within_radius(
    graph,
    latitude,
    longitude,
    radius_meters
):
    """
    Find actual Chennai road nodes within a
    physical geographic radius using Haversine distance.
    """

    affected_nodes = []

    for node_id, node in graph.nodes.items():

        distance = haversine_distance(
            latitude,
            longitude,
            node.latitude,
            node.longitude
        )

        if distance <= radius_meters:

            affected_nodes.append(
                (node_id, distance)
            )

    return affected_nodes


def test_cyclone_physical_radius():

    print()
    print("==========================================")
    print(" CYCLONE PHYSICAL IMPACT RADIUS ANALYSIS")
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

    print("\nSTEP 3: TESTING PHYSICAL IMPACT RADII")

    radii = [
        500,
        1000,
        2000,
        3000,
        5000,
        10000
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
            "meters"
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

            farthest = max(
                affected,
                key=lambda item: item[1]
            )

            print(
                "Nearest node:",
                nearest[0]
            )

            print(
                "Nearest distance:",
                round(nearest[1], 2),
                "meters"
            )

            print(
                "Farthest included node:",
                farthest[0]
            )

            print(
                "Farthest included distance:",
                round(farthest[1], 2),
                "meters"
            )

    print()
    print("==========================================")
    print(" PHYSICAL RADIUS ANALYSIS COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_physical_radius()