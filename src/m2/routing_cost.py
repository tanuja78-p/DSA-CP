def get_edge_cost(edge):
    """
    Calculate the routing cost of an edge.

    SAFE roads:
        Normal physical distance.

    RESTRICTED roads:
        Distance multiplied by a 1.5 penalty.

    BLOCKED roads:
        Not traversable.
    """

    if edge.status == "BLOCKED":
        return None

    if edge.status == "RESTRICTED":
        return edge.distance * 1.5

    return edge.distance