from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact
)


TARGET_ROAD_ID = "10529"


def inspect_road(graph, road_id):

    road_nodes = set()
    neighboring_roads = {}

    # ------------------------------------------
    # Find every graph node belonging to the road
    # ------------------------------------------

    for node_id in graph.nodes:

        for edge in graph.get_neighbors(node_id):

            if edge.road_id == road_id:

                road_nodes.add(node_id)

    # ------------------------------------------
    # Inspect connections from those nodes
    # ------------------------------------------

    for node_id in road_nodes:

        connections = []

        for edge in graph.get_neighbors(node_id):

            if edge.road_id != road_id:

                connections.append(
                    (
                        edge.road_id,
                        edge.destination
                    )
                )

        if connections:

            neighboring_roads[node_id] = connections

    return road_nodes, neighboring_roads


def test_candidate():

    print()
    print("==========================================")
    print(" CYCLONE CANDIDATE ROAD INSPECTION")
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
        "Affected roads:",
        len(
            impact["affected_roads"]
        )
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print(
        "\nSTEP 4: INSPECTING ROAD",
        TARGET_ROAD_ID
    )

    if TARGET_ROAD_ID not in impact[
        "affected_roads"
    ]:

        print(
            "ERROR: Target road is not "
            "cyclone affected."
        )

        return

    road_nodes, neighboring_roads = (
        inspect_road(
            graph,
            TARGET_ROAD_ID
        )
    )

    print(
        "Road:",
        TARGET_ROAD_ID
    )

    print(
        "Road node count:",
        len(road_nodes)
    )

    print(
        "Connection nodes:",
        len(neighboring_roads)
    )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print(
        "\nSTEP 5: ROAD NODE CONNECTIONS"
    )

    for node_id in sorted(
        neighboring_roads
    ):

        print()
        print(
            "Node:",
            node_id
        )

        for road_id, destination in (
            neighboring_roads[node_id]
        ):

            print(
                "   -> Road:",
                road_id,
                "| Destination:",
                destination
            )

    # ------------------------------------------
    # STEP 6
    # ------------------------------------------

    print()
    print("==========================================")
    print(" CANDIDATE INSPECTION COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_candidate()