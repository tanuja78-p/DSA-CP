import time

from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact,
    apply_cyclone_impact
)

from m2.astar import astar


def get_route_road_ids(graph, path):
    """
    Extract the road IDs used by a route.

    The graph is bidirectional, so we inspect the
    consecutive nodes in the returned path.
    """

    road_ids = []

    for index in range(len(path) - 1):

        current_node = path[index]
        next_node = path[index + 1]

        edges = graph.get_neighbors(
            current_node
        )

        for edge in edges:

            if edge.destination == next_node:

                road_ids.append(
                    edge.road_id
                )

                break

    return road_ids


def find_candidate_nodes(
    graph,
    affected_nodes,
    maximum_candidates=20
):
    """
    Select a limited set of affected nodes
    for route-pair testing.
    """

    sorted_nodes = sorted(
        affected_nodes,
        key=lambda item: item["distance_meters"]
    )

    candidates = []

    for item in sorted_nodes:

        node_id = item["node_id"]

        if node_id not in candidates:

            candidates.append(
                node_id
            )

        if len(candidates) >= maximum_candidates:
            break

    return candidates


def test_cyclone_rerouting_pair():

    print()
    print("==========================================")
    print(" CYCLONE REROUTING PAIR SEARCH")
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

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print("\nSTEP 3: CALCULATING CYCLONE IMPACT")

    impact = calculate_cyclone_impact(
        graph,
        cyclone,
        radius_meters=1000
    )

    affected_road_ids = set(
        impact["affected_roads"].keys()
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
            affected_road_ids
        )
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print("\nSTEP 4: SELECTING ROUTE CANDIDATES")

    candidates = find_candidate_nodes(
        graph,
        impact["affected_nodes"],
        maximum_candidates=20
    )

    print(
        "Candidate nodes:",
        len(candidates)
    )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print("\nSTEP 5: SEARCHING FOR AFFECTED ROUTE")

    found = False

    selected_source = None
    selected_destination = None
    selected_path = None
    selected_distance = None
    selected_road_ids = None

    # Try pairs among candidate nodes.
    for source in candidates:

        for destination in candidates:

            if source == destination:
                continue

            result = astar(
                graph,
                source,
                destination
            )

            if not result["reachable"]:
                continue

            path = result["path"]

            route_roads = get_route_road_ids(
                graph,
                path
            )

            route_affected_roads = (
                set(route_roads)
                & affected_road_ids
            )

            if route_affected_roads:

                selected_source = source
                selected_destination = destination
                selected_path = path
                selected_distance = (
                    result["distance"]
                )
                selected_road_ids = (
                    route_roads
                )

                print()
                print(
                    "FOUND CANDIDATE ROUTE"
                )

                print(
                    "Source:",
                    selected_source
                )

                print(
                    "Destination:",
                    selected_destination
                )

                print(
                    "Route nodes:",
                    len(selected_path)
                )

                print(
                    "Route distance:",
                    selected_distance,
                    "meters"
                )

                print(
                    "Route affected roads:",
                    sorted(
                        route_affected_roads
                    )
                )

                found = True

                break

        if found:
            break

    # ------------------------------------------
    # STEP 6
    # ------------------------------------------

    if not found:

        print()
        print(
            "NO SUITABLE ROUTE FOUND"
        )

        print(
            "Try a larger candidate set."
        )

        print()
        print("==========================================")
        print(
            " ROUTE PAIR SEARCH COMPLETE"
        )
        print("==========================================")

        return

    # ------------------------------------------
    # STEP 7
    # ------------------------------------------

    print("\nSTEP 6: APPLYING CYCLONE BLOCKAGE")

    apply_result = apply_cyclone_impact(
        graph,
        impact
    )

    print(
        "Blocked roads:",
        apply_result["updated_count"]
    )

    # ------------------------------------------
    # STEP 8
    # ------------------------------------------

    print("\nSTEP 7: TESTING POST-CYCLONE ROUTE")

    start_time = time.perf_counter()

    rerouted = astar(
        graph,
        selected_source,
        selected_destination
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    print(
        "Reachable after cyclone:",
        rerouted["reachable"]
    )

    if rerouted["reachable"]:

        print(
            "New route nodes:",
            len(rerouted["path"])
        )

        print(
            "New route distance:",
            rerouted["distance"],
            "meters"
        )

        print(
            "Nodes explored:",
            rerouted["nodes_explored"]
        )

        print(
            "Routing time:",
            elapsed,
            "seconds"
        )

        new_route_roads = get_route_road_ids(
            graph,
            rerouted["path"]
        )

        blocked_roads_used = (
            set(new_route_roads)
            & affected_road_ids
        )

        print(
            "Blocked roads used:",
            sorted(
                blocked_roads_used
            )
        )

        print(
            "Route changed:",
            selected_path != rerouted["path"]
        )

    # ------------------------------------------
    # FINAL
    # ------------------------------------------

    print()
    print("==========================================")
    print(" CYCLONE REROUTING PAIR SEARCH COMPLETE")
    print("==========================================")

    print(
        "Source:",
        selected_source
    )

    print(
        "Destination:",
        selected_destination
    )

    print(
        "Original distance:",
        selected_distance,
        "meters"
    )

    if rerouted["reachable"]:

        print(
            "New distance:",
            rerouted["distance"],
            "meters"
        )

    print("==========================================")


if __name__ == "__main__":
    test_cyclone_rerouting_pair()