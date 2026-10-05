from m1.graph import haversine_distance


def geographic_heuristic(graph, current_node, destination_node):
    """
    Estimate the remaining distance between the current node
    and destination node using Haversine distance.

    This is the heuristic function used by A*.

    Parameters:
        graph: M1 Graph object.
        current_node: Current node ID.
        destination_node: Destination node ID.

    Returns:
        Estimated geographic distance in meters.
    """

    current = graph.nodes[current_node]
    destination = graph.nodes[destination_node]

    return haversine_distance(
        current.latitude,
        current.longitude,
        destination.latitude,
        destination.longitude
    )