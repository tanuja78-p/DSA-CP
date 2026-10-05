from math import inf

from m2.min_heap import MinHeap
from m2.route_utils import reconstruct_path
from m2.routing_cost import get_edge_cost


def dijkstra(graph, source, destination):
    """
    Find the minimum-cost route between source and destination
    using Dijkstra's shortest-path algorithm.

    The routing cost depends on the current road status:

        SAFE       -> distance
        RESTRICTED -> distance * 1.5
        BLOCKED    -> not traversable

    Parameters:
        graph: M1 Graph object.
        source: Starting node ID.
        destination: Destination node ID.

    Returns:
        Dictionary containing:
            path
            distance
            reachable
            nodes_explored
    """

    # Check whether source and destination exist.
    if source not in graph.nodes or destination not in graph.nodes:
        return {
            "path": [],
            "distance": inf,
            "reachable": False,
            "nodes_explored": 0
        }

    # Initially, every node has infinite cost.
    distances = {
        node_id: inf
        for node_id in graph.nodes
    }

    # Parent dictionary is used to reconstruct the final route.
    parent = {}

    # Distance from source to itself is zero.
    distances[source] = 0.0

    # Insert source into the Min Heap.
    heap = MinHeap()
    heap.insert(0.0, source)

    # Keep track of nodes whose minimum cost is finalized.
    visited = set()

    # Number of nodes actually explored.
    nodes_explored = 0

    # Main Dijkstra loop.
    while not heap.is_empty():

        # Extract node with the smallest current cost.
        current_distance, current_node = heap.extract_min()

        # Ignore duplicate heap entries.
        if current_node in visited:
            continue

        visited.add(current_node)
        nodes_explored += 1

        # Destination reached.
        if current_node == destination:
            break

        # Get roads that are not BLOCKED.
        for edge in graph.get_active_neighbors(current_node):

            neighbor = edge.destination

            # Ignore already finalized nodes.
            if neighbor in visited:
                continue

            # Calculate cost according to road status.
            edge_cost = get_edge_cost(edge)

            # BLOCKED road.
            if edge_cost is None:
                continue

            # Calculate new total route cost.
            new_distance = current_distance + edge_cost

            # Relaxation step.
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance

                parent[neighbor] = current_node

                # Add updated cost to Min Heap.
                heap.insert(
                    new_distance,
                    neighbor
                )

    # No route exists.
    if distances[destination] == inf:
        return {
            "path": [],
            "distance": inf,
            "reachable": False,
            "nodes_explored": nodes_explored
        }

    # Reconstruct source -> destination route.
    path = reconstruct_path(
        parent,
        source,
        destination
    )

    return {
        "path": path,
        "distance": distances[destination],
        "reachable": True,
        "nodes_explored": nodes_explored
    }