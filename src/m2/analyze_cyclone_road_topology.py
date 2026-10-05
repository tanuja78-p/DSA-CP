from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact
)


def analyze_road_topology(
    graph,
    road_id
):
    """
    Analyze the graph connectivity around one road.
    """

    road_edges = []

    for node_id in graph.nodes:

        for edge in graph.get_neighbors(node_id):

            if edge.road_id == road_id:

                road_edges.append(
                    (node_id, edge)
                )

    unique_nodes = set()

    neighboring_roads = set()

    for node_id, edge in road_edges:

        unique_nodes.add(
            node_id
        )

        for neighbor in graph.get_neighbors(
            node_id
        ):

            if neighbor.road_id != road_id:

                neighboring_roads.add(
                    neighbor.road_id
                )

    return {
        "road_id": road_id,
        "edge_count": len(road_edges),
        "nodes": sorted(unique_nodes),
        "neighboring_roads": sorted(
            neighboring_roads
        )
    }


def test_cyclone_road_topology():

    print()
    print("==========================================")
    print(" CYCLONE ROAD TOPOLOGY ANALYSIS")
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

    affected_roads = impact[
        "affected_roads"
    ]

    print(
        "Affected roads:",
        len(affected_roads)
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print(
        "\nSTEP 4: ANALYZING AFFECTED ROAD TOPOLOGY"
    )

    road_results = []

    for road_id in affected_roads:

        result = analyze_road_topology(
            graph,
            road_id
        )

        road_results.append(
            result
        )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    road_results.sort(
        key=lambda item:
            len(
                item["neighboring_roads"]
            ),
        reverse=True
    )

    print(
        "\nTOP AFFECTED ROADS BY ALTERNATIVE"
        " CONNECTIVITY"
    )

    for result in road_results[:20]:

        print()
        print(
            "Road:",
            result["road_id"]
        )

        print(
            "Graph edges:",
            result["edge_count"]
        )

        print(
            "Road nodes:",
            len(
                result["nodes"]
            )
        )

        print(
            "Neighboring roads:",
            len(
                result["neighboring_roads"]
            )
        )

        print(
            "Neighbor road IDs:",
            result["neighboring_roads"][:15]
        )

    # ------------------------------------------
    # FINAL
    # ------------------------------------------

    print()
    print("==========================================")
    print(" TOPOLOGY ANALYSIS COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_road_topology()