from m1.flood_engine import (
    SpatialIndex,
    find_nearest_node
)


def build_graph_spatial_index(graph):
    """
    Build the same type of spatial index used
    by M1's flood engine.
    """

    spatial_index = SpatialIndex(
        cell_size=0.001
    )

    for node in graph.get_all_nodes():
        spatial_index.add_node(node)

    return spatial_index


def find_cyclone_impact_node(
    graph,
    spatial_index,
    cyclone
):
    """
    Find the Chennai road-graph node nearest
    to a cyclone track observation.
    """

    return find_nearest_node(
        graph,
        spatial_index,
        cyclone.latitude,
        cyclone.longitude
    )