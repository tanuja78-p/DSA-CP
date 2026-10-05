def apply_cyclone_hazard(graph, affected_nodes, status):
    """
    Apply a cyclone hazard to roads connected to affected nodes.

    Parameters:
        graph: M1 Graph object.
        affected_nodes: Node IDs affected by the cyclone.
        status: Road status to apply.
                SAFE / RESTRICTED / BLOCKED

    Returns:
        Dictionary containing:
            affected_nodes
            updated_roads
    """

    updated_roads = set()

    for node_id in affected_nodes:

        if node_id not in graph.nodes:
            continue

        for edge in graph.get_neighbors(node_id):

            graph.update_road_status(
                edge.road_id,
                status
            )

            updated_roads.add(edge.road_id)

    return {
        "affected_nodes": affected_nodes,
        "updated_roads": sorted(updated_roads)
    }