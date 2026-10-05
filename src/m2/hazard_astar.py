from m2.min_heap import MinHeap
from m2.route_utils import reconstruct_path
from m2.heuristic import geographic_heuristic
from m2.hazard_routing_cost import get_hazard_edge_cost


def hazard_astar(
    graph,
    source,
    destination,
    registry
):
    """
    A* routing using multi-hazard road status.

    SAFE:
        normal distance

    RESTRICTED:
        1.5 x distance

    BLOCKED:
        unavailable
    """

    if source not in graph.nodes:
        return {
            "path": [],
            "distance": None,
            "reachable": False,
            "nodes_explored": 0
        }

    if destination not in graph.nodes:
        return {
            "path": [],
            "distance": None,
            "reachable": False,
            "nodes_explored": 0
        }

    if source == destination:
        return {
            "path": [source],
            "distance": 0.0,
            "reachable": True,
            "nodes_explored": 1
        }

    open_set = MinHeap()

    g_score = {
        source: 0.0
    }

    parent = {}

    open_set.insert(
        0.0,
        source
    )

    nodes_explored = 0

    while not open_set.is_empty():

        current_f, current = (
            open_set.extract_min()
        )

        nodes_explored += 1

        current_g = g_score.get(
            current,
            float("inf")
        )

        expected_f = (
            current_g
            + geographic_heuristic(
                graph,
                current,
                destination
            )
        )

        # Ignore stale heap entries.
        if current_f > expected_f + 1e-9:
            continue

        if current == destination:

            path = reconstruct_path(
                parent,
                source,
                destination
            )

            return {
                "path": path,
                "distance": current_g,
                "reachable": True,
                "nodes_explored": nodes_explored
            }

        for edge in graph.get_neighbors(
            current
        ):

            cost = get_hazard_edge_cost(
                edge,
                registry
            )

            if cost is None:
                continue

            neighbor = edge.destination

            tentative_g = (
                current_g + cost
            )

            if tentative_g < g_score.get(
                neighbor,
                float("inf")
            ):

                g_score[neighbor] = (
                    tentative_g
                )

                parent[neighbor] = (
                    current
                )

                heuristic = (
                    geographic_heuristic(
                        graph,
                        neighbor,
                        destination
                    )
                )

                f_score = (
                    tentative_g
                    + heuristic
                )

                open_set.insert(
                    f_score,
                    neighbor
                )

    return {
        "path": [],
        "distance": None,
        "reachable": False,
        "nodes_explored": nodes_explored
    }