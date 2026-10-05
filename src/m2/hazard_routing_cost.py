from m2.hazard_registry import HazardRegistry


def get_effective_edge_status(
    edge,
    registry
):
    """
    Return the effective hazard status
    for an edge using its road ID.
    """

    return registry.get_effective_status(
        edge.road_id
    )


def get_hazard_edge_cost(
    edge,
    registry
):
    """
    Calculate routing cost using the
    effective multi-hazard road status.

    SAFE       -> normal distance
    RESTRICTED -> 1.5x distance
    BLOCKED    -> unavailable
    """

    status = get_effective_edge_status(
        edge,
        registry
    )

    if status == "BLOCKED":
        return None

    if status == "RESTRICTED":
        return edge.distance * 1.5

    return edge.distance