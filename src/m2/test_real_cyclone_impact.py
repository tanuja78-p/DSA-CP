from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)
from m2.cyclone_impact import (
    build_graph_spatial_index,
    find_cyclone_impact_node
)


def test_real_cyclone_impact():

    print()
    print("==========================================")
    print(" REAL CYCLONE -> CHENNAI GRAPH TEST")
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

    print("\nSTEP 2: LOADING CYCLONE DATA")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    cyclone = get_closest_observation(
        relevant
    )

    print(
        "Selected cyclone:",
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

    print("\nSTEP 3: BUILDING GRAPH SPATIAL INDEX")

    spatial_index = build_graph_spatial_index(
        graph
    )

    print("Spatial index created.")

    # ------------------------------------------------
    # STEP 4
    # ------------------------------------------------

    print("\nSTEP 4: FINDING NEAREST ROAD NODE")

    nearest_node = find_cyclone_impact_node(
        graph,
        spatial_index,
        cyclone
    )

    if nearest_node is None:

        print(
            "No nearby road node found."
        )

    else:

        print(
            "Nearest node:",
            nearest_node.node_id
        )

        print(
            "Node latitude:",
            nearest_node.latitude
        )

        print(
            "Node longitude:",
            nearest_node.longitude
        )

    print()
    print("==========================================")
    print(" REAL CYCLONE IMPACT TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_real_cyclone_impact()