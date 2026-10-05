from m1.graph import haversine_distance

from m2.cyclone_engine import (
    classify_cyclone_severity,
    cyclone_to_status
)


DEFAULT_IMPACT_RADIUS_METERS = 1000


def find_cyclone_affected_nodes(
    graph,
    cyclone,
    radius_meters=DEFAULT_IMPACT_RADIUS_METERS
):
    """
    Find all Chennai road nodes located within the
    physical cyclone impact radius.
    """

    affected_nodes = []

    for node_id, node in graph.nodes.items():

        distance = haversine_distance(
            cyclone.latitude,
            cyclone.longitude,
            node.latitude,
            node.longitude
        )

        if distance <= radius_meters:

            affected_nodes.append(
                {
                    "node_id": node_id,
                    "distance_meters": distance
                }
            )

    return affected_nodes


def find_affected_roads(
    graph,
    affected_nodes
):
    """
    Convert affected road nodes into unique
    affected road IDs.
    """

    affected_roads = {}

    for affected_node in affected_nodes:

        node_id = affected_node["node_id"]

        if node_id not in graph.nodes:
            continue

        node_distance = affected_node[
            "distance_meters"
        ]

        for edge in graph.get_neighbors(node_id):

            road_id = edge.road_id

            if road_id not in affected_roads:

                affected_roads[road_id] = {
                    "road_id": road_id,
                    "minimum_distance_meters":
                        node_distance,
                    "affected_nodes": set(),
                    "current_status": edge.status
                }

            affected_roads[
                road_id
            ]["affected_nodes"].add(node_id)

            if node_distance < affected_roads[
                road_id
            ]["minimum_distance_meters"]:

                affected_roads[
                    road_id
                ]["minimum_distance_meters"] = (
                    node_distance
                )

    return affected_roads


def calculate_cyclone_impact(
    graph,
    cyclone,
    radius_meters=DEFAULT_IMPACT_RADIUS_METERS
):
    """
    Complete cyclone impact analysis.

    Returns:
        cyclone severity
        road status
        affected nodes
        affected roads
    """

    severity = classify_cyclone_severity(
        cyclone.wind_speed
    )

    status = cyclone_to_status(
        severity
    )

    affected_nodes = find_cyclone_affected_nodes(
        graph,
        cyclone,
        radius_meters
    )

    affected_roads = find_affected_roads(
        graph,
        affected_nodes
    )

    return {
        "cyclone_name": cyclone.cyclone_name,
        "track_point_id": cyclone.track_point_id,
        "timestamp_utc": cyclone.timestamp_utc,
        "latitude": cyclone.latitude,
        "longitude": cyclone.longitude,
        "wind_speed": cyclone.wind_speed,
        "pressure": cyclone.pressure,
        "severity": severity,
        "status": status,
        "impact_radius_meters": radius_meters,
        "affected_nodes": affected_nodes,
        "affected_roads": affected_roads
    }


def apply_cyclone_impact(
    graph,
    impact_result
):
    """
    Apply the calculated cyclone road status
    to the dynamic graph.
    """

    status = impact_result["status"]

    affected_roads = impact_result[
        "affected_roads"
    ]

    updated_roads = []

    for road_id in affected_roads:

        graph.update_road_status(
            road_id,
            status
        )

        updated_roads.append(
            road_id
        )

    return {
        "status": status,
        "updated_roads": sorted(
            updated_roads
        ),
        "updated_count": len(
            updated_roads
        )
    }