from collections import deque
from typing import List, Set

from m1.graph import Graph


def bfs_reachable_nodes(
    graph: Graph,
    start_node: str
) -> List[str]:
    """
    Perform Breadth-First Search from a starting node.

    Only non-blocked roads are traversed.

    Returns:
        List of nodes reachable from start_node.
    """

    if start_node not in graph.nodes:
        return []

    queue = deque()

    visited: Set[str] = set()

    reachable_nodes = []

    queue.append(start_node)

    visited.add(start_node)

    while queue:

        current_node = queue.popleft()

        reachable_nodes.append(
            current_node
        )

        neighbors = graph.get_active_neighbors(
            current_node
        )

        for edge in neighbors:

            next_node = edge.destination

            if next_node not in visited:

                visited.add(next_node)

                queue.append(
                    next_node
                )

    return reachable_nodes


def bfs_affected_region(
    graph: Graph,
    start_nodes: List[str]
) -> List[str]:
    """
    Perform multi-source BFS.

    This is useful for disaster propagation.

    Multiple hazard-affected nodes can be supplied
    as starting points.

    The BFS explores all reachable non-blocked nodes.
    """

    queue = deque()

    visited: Set[str] = set()

    affected_region = []

    for start_node in start_nodes:

        if start_node not in graph.nodes:
            continue

        if start_node in visited:
            continue

        visited.add(start_node)

        queue.append(
            start_node
        )

    while queue:

        current_node = queue.popleft()

        affected_region.append(
            current_node
        )

        neighbors = graph.get_active_neighbors(
            current_node
        )

        for edge in neighbors:

            next_node = edge.destination

            if next_node not in visited:

                visited.add(next_node)

                queue.append(
                    next_node
                )

    return affected_region


def bfs_distance_from_source(
    graph: Graph,
    start_node: str
):
    """
    Calculate the number of road connections
    from start_node to every reachable node.

    This is an unweighted BFS distance.

    Returns:
        Dictionary:
            node_id -> number of edges from source
    """

    if start_node not in graph.nodes:
        return {}

    queue = deque()

    distances = {}

    queue.append(
        start_node
    )

    distances[start_node] = 0

    while queue:

        current_node = queue.popleft()

        for edge in graph.get_active_neighbors(
            current_node
        ):

            next_node = edge.destination

            if next_node not in distances:

                distances[next_node] = (
                    distances[current_node] + 1
                )

                queue.append(
                    next_node
                )

    return distances