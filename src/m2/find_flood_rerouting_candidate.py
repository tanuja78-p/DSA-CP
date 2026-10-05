from m1.build_road_graph import build_chennai_graph

from m2.hazard_registry import HazardRegistry
from m2.hazard_astar import hazard_astar


SOURCE = "80.29048_13.09242"
DESTINATION = "80.29114_13.09609"


def get_route_road_ids(graph, path):
    """
    Return the unique road IDs used by a route.
    """

    road_ids = []

    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]

        for edge in graph.get_neighbors(current):
            if edge.destination == next_node:
                if edge.road_id not in road_ids:
                    road_ids.append(edge.road_id)
                break

    return road_ids


def test_candidate(graph, road_id):
    """
    Temporarily block one road and test whether
    A* can find an alternate route.
    """

    registry = HazardRegistry()

    # Block only the selected road in the hazard registry.
    registry.set_flood_status(
        road_id,
        "BLOCKED"
    )

    result = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    return result


def main():

    print()
    print("==========================================")
    print(" FLOOD REROUTING CANDIDATE SEARCH")
    print("==========================================")

    print()
    print("Building Chennai graph...")

    graph = build_chennai_graph()

    print()
    print("Graph nodes:", graph.get_node_count())
    print("Graph edges:", graph.get_edge_count())

    print()
    print("Calculating baseline route...")

    baseline_registry = HazardRegistry()

    baseline = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        baseline_registry
    )

    if not baseline["reachable"]:
        raise RuntimeError(
            "Baseline route is not reachable."
        )

    print()
    print("Baseline distance:", baseline["distance"])
    print("Baseline route nodes:", len(baseline["path"]))

    route_roads = get_route_road_ids(
        graph,
        baseline["path"]
    )

    print()
    print("Baseline route road IDs:")
    print(route_roads)

    print()
    print("Testing individual road blockages...")

    candidates = []

    for index, road_id in enumerate(route_roads, start=1):

        result = test_candidate(
            graph,
            road_id
        )

        print()
        print(
            f"[{index}/{len(route_roads)}] "
            f"Road {road_id}"
        )

        print(
            "Reachable:",
            result["reachable"]
        )

        if result["reachable"]:

            additional_distance = (
                result["distance"]
                - baseline["distance"]
            )

            print(
                "New distance:",
                result["distance"]
            )

            print(
                "Additional distance:",
                additional_distance
            )

            print(
                "New route nodes:",
                len(result["path"])
            )

            candidates.append(
                {
                    "road_id": road_id,
                    "distance": result["distance"],
                    "additional_distance": additional_distance,
                    "route": result["path"],
                    "nodes_explored": result["nodes_explored"]
                }
            )

    print()
    print("==========================================")
    print(" CANDIDATE SUMMARY")
    print("==========================================")

    if not candidates:

        print()
        print(
            "No single baseline road produced "
            "a reachable alternate route."
        )

    else:

        candidates.sort(
            key=lambda item: item["additional_distance"]
        )

        print()

        for candidate in candidates:

            print(
                "Road:",
                candidate["road_id"]
            )

            print(
                "New distance:",
                candidate["distance"]
            )

            print(
                "Additional distance:",
                candidate["additional_distance"]
            )

            print(
                "Nodes explored:",
                candidate["nodes_explored"]
            )

            print(
                "Route:"
            )

            print(
                " -> ".join(
                    candidate["route"]
                )
            )

            print("------------------------------------------")

    print()
    print("==========================================")
    print(" SEARCH COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    main()