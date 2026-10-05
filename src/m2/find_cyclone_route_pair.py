from m1.build_road_graph import build_chennai_graph
from m1.graph import haversine_distance

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact
)


def find_nearest_affected_nodes(
    graph,
    impact
):
    """
    Return affected nodes sorted by their
    distance from the cyclone center.
    """

    nodes = impact["affected_nodes"]

    return sorted(
        nodes,
        key=lambda item: item["distance_meters"]
    )


def find_farthest_affected_nodes(
    graph,
    impact
):
    """
    Return affected nodes sorted from
    nearest to farthest.
    """

    nodes = impact["affected_nodes"]

    return sorted(
        nodes,
        key=lambda item: item["distance_meters"],
        reverse=True
    )


def test_route_pair_selection():

    print()
    print("==========================================")
    print(" CYCLONE ROUTE PAIR SELECTION")
    print("==========================================")

    # ------------------------------------------
    # STEP 1
    # ------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # ------------------------------------------
    # STEP 2
    # ------------------------------------------

    print("\nSTEP 2: LOADING VARDah OBSERVATION")

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
        "Location:",
        cyclone.latitude,
        cyclone.longitude
    )

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print("\nSTEP 3: CALCULATING CYCLONE IMPACT")

    impact = calculate_cyclone_impact(
        graph,
        cyclone,
        radius_meters=1000
    )

    print(
        "Severity:",
        impact["severity"]
    )

    print(
        "Status:",
        impact["status"]
    )

    print(
        "Affected nodes:",
        len(
            impact["affected_nodes"]
        )
    )

    print(
        "Affected roads:",
        len(
            impact["affected_roads"]
        )
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print("\nSTEP 4: SELECTING ROUTE CANDIDATES")

    nearest = find_nearest_affected_nodes(
        graph,
        impact
    )

    farthest = find_farthest_affected_nodes(
        graph,
        impact
    )

    print(
        "\nNearest affected nodes:"
    )

    for item in nearest[:10]:

        print(
            item["node_id"],
            "|",
            round(
                item["distance_meters"],
                2
            ),
            "m"
        )

    print(
        "\nFarthest affected nodes:"
    )

    for item in farthest[:10]:

        print(
            item["node_id"],
            "|",
            round(
                item["distance_meters"],
                2
            ),
            "m"
        )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print()
    print("==========================================")
    print(" ROUTE PAIR SELECTION COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_route_pair_selection()