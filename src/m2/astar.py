from math import inf

from m2.min_heap import MinHeap
from m2.route_utils import reconstruct_path
from m2.routing_cost import get_edge_cost
from m2.heuristic import geographic_heuristic


def astar(graph, source, destination):
    """
    Find a minimum-cost route between source and destination
    using the A* search algorithm.

    Cost model:

        SAFE       -> distance
        RESTRICTED -> distance * 1.5
        BLOCKED    -> not traversable

    Priority:

        f(n) = g(n) + h(n)

    where:

        g(n) = actual routing cost from source to n
        h(n) = Haversine distance from n to destination

    Returns:
        Dictionary containing:
            path
            distance
            reachable
            nodes_explored
    """

    if source not in graph.nodes or destination not in graph.nodes:
        return {
            "path": [],
            "distance": inf,
            "reachable": False,
            "nodes_explored": 0
        }

    # Actual cost from source to each node.
    g_cost = {
        node_id: inf
        for node_id in graph.nodes
    }

    # Parent map for route reconstruction.
    parent = {}

    # Source has zero accumulated cost.
    g_cost[source] = 0.0

    # Initial priority:
    # f(source) = g(source) + h(source)
    initial_heuristic = geographic_heuristic(
        graph,
        source,
        destination
    )

    heap = MinHeap()

    heap.insert(
        initial_heuristic,
        source
    )

    visited = set()

    nodes_explored = 0

    while not heap.is_empty():

        current_priority, current_node = heap.extract_min()

        if current_node in visited:
            continue

        visited.add(current_node)

        nodes_explored += 1

        if current_node == destination:
            break

        for edge in graph.get_active_neighbors(current_node):

            neighbor = edge.destination

            if neighbor in visited:
                continue

            edge_cost = get_edge_cost(edge)

            if edge_cost is None:
                continue

            tentative_g = (
                g_cost[current_node]
                + edge_cost
            )

            if tentative_g < g_cost[neighbor]:

                g_cost[neighbor] = tentative_g

                parent[neighbor] = current_node

                heuristic = geographic_heuristic(
                    graph,
                    neighbor,
                    destination
                )

                f_cost = (
                    tentative_g
                    + heuristic
                )

                heap.insert(
                    f_cost,
                    neighbor
                )

    if g_cost[destination] == inf:

        return {
            "path": [],
            "distance": inf,
            "reachable": False,
            "nodes_explored": nodes_explored
        }

    path = reconstruct_path(
        parent,
        source,
        destination
    )

    return {
        "path": path,
        "distance": g_cost[destination],
        "reachable": True,
        "nodes_explored": nodes_explored
    }