from m2.real_cyclone_impact import calculate_cyclone_impact
from m2.hazard_registry import HazardRegistry


def apply_cyclone_to_registry(
    graph,
    cyclone,
    registry,
    radius_meters=1000
):
    """
    Calculate the real cyclone impact on the road graph
    and synchronize cyclone road statuses with the
    M2 HazardRegistry.

    Cyclone status is stored separately from flood status.
    """

    # Calculate cyclone severity, affected nodes,
    # and affected roads using the existing M2 engine.
    impact_result = calculate_cyclone_impact(
        graph,
        cyclone,
        radius_meters=radius_meters
    )

    # Store the cyclone status independently
    # in the HazardRegistry.
    for road_id in impact_result["affected_roads"]:
        registry.set_cyclone_status(
            road_id,
            impact_result["status"]
        )

    return impact_result