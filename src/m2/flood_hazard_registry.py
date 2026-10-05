from m1.flood_engine import (
    SpatialIndex,
    apply_flood_hazards
)

from m2.hazard_registry import HazardRegistry


def build_flood_spatial_index(graph):
    """
    Build the same spatial index used by M1
    for mapping flood hazards to road nodes.
    """

    spatial_index = SpatialIndex(cell_size=0.001)

    for node in graph.get_all_nodes():
        spatial_index.add_node(node)

    return spatial_index


def apply_flood_to_registry(graph, flood_hazards, registry):
    """
    Apply M1 flood hazards to the graph and
    synchronize the resulting flood statuses
    with the M2 HazardRegistry.
    """

    # Build the spatial index required by M1.
    spatial_index = build_flood_spatial_index(graph)

    # Use M1's existing flood-to-road mapping logic.
    flood_result = apply_flood_hazards(
        graph,
        spatial_index,
        flood_hazards
    )

    # Store RESTRICTED flood roads in the M2 registry.
    for road_id in flood_result["RESTRICTED"]:
        registry.set_flood_status(
            road_id,
            "RESTRICTED"
        )

    # Store BLOCKED flood roads in the M2 registry.
    for road_id in flood_result["BLOCKED"]:
        registry.set_flood_status(
            road_id,
            "BLOCKED"
        )

    return flood_result