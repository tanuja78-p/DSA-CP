from typing import Dict, Iterable

from m1.graph import Graph


VALID_STATUSES = {
    "SAFE",
    "RESTRICTED",
    "BLOCKED"
}


def _get_all_graph_edges(graph: Graph):
    """
    Return every edge stored in the graph
    through its adjacency list.
    """

    for node_id in graph.adjacency:

        for edge in graph.adjacency[node_id]:

            yield edge


def update_road_status(
    graph: Graph,
    road_id: str,
    new_status: str
) -> bool:
    """
    Update all edges belonging to a road.

    Returns True if the road was found.
    """

    new_status = new_status.upper()

    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid road status: {new_status}"
        )

    updated = False

    for edge in _get_all_graph_edges(graph):

        if edge.road_id == road_id:

            graph.update_road_status(
                edge.road_id,
                new_status
            )

            updated = True

    return updated


def update_roads_from_flood_nodes(
    graph: Graph,
    affected_nodes: Iterable[str],
    status: str = "BLOCKED"
) -> Dict[str, int]:
    """
    Update roads connected to flood-affected nodes.

    Returns:
        roads_updated
        nodes_processed
    """

    status = status.upper()

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid road status: {status}"
        )

    affected_nodes = set(
        affected_nodes
    )

    roads_updated = set()

    for node_id in affected_nodes:

        neighbors = graph.get_neighbors(
            node_id
        )

        for edge in neighbors:

            graph.update_road_status(
                edge.road_id,
                status
            )

            roads_updated.add(
                edge.road_id
            )

    return {
        "roads_updated": len(roads_updated),
        "nodes_processed": len(affected_nodes)
    }


def recover_roads(graph: Graph, road_ids: Iterable[str]) -> int:
    """
    Recover the specified roads by setting their status to SAFE.

    The graph stores each physical road in both directions.
    We scan the adjacency list once and recover all requested
    roads together.
    """

    road_ids = set(road_ids)

    if not road_ids:
        return 0

    recovered_roads = set()

    for node_id in graph.adjacency:

        for edge in graph.adjacency[node_id]:

            if edge.road_id in road_ids:

                edge.status = "SAFE"
                recovered_roads.add(
                    edge.road_id
                )

    return len(recovered_roads)

def count_road_statuses(
    graph: Graph
) -> Dict[str, int]:
    """
    Count unique roads by their current status.
    """

    road_statuses = {}

    for edge in _get_all_graph_edges(graph):

        road_statuses[
            edge.road_id
        ] = edge.status

    counts = {
        "SAFE": 0,
        "RESTRICTED": 0,
        "BLOCKED": 0
    }

    for status in road_statuses.values():

        if status in counts:
            counts[status] += 1

    return counts