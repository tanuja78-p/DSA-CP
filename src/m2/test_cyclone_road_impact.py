from m1.build_road_graph import build_chennai_graph
from m1.graph import haversine_distance

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)


IMPACT_RADIUS_METERS = 1000


def find_affected_nodes(
    graph,
    latitude,
    longitude,
    radius_meters
):
    """
    Find all Chennai road nodes within the
    physical cyclone impact radius.
    """

    affected_nodes = []

    for node_id, node in graph.nodes.items():

        distance = haversine_distance(
            latitude,
            longitude,
            node.latitude,
            node.longitude
        )

        if distance <= radius_meters:

            affected_nodes.append(
                (node_id, distance)
            )

    return affected_nodes


def analyze_affected_roads(
    graph,
    affected_nodes
):
    """
    Find all unique roads connected to
    cyclone-affected nodes.
    """

    affected_roads = {}

    for node_id, node_distance in affected_nodes:

        if node_id not in graph.nodes:
            continue

        neighbors = graph.get_neighbors(
            node_id
        )

        for edge in neighbors:

            road_id = edge.road_id

            if road_id not in affected_roads:

                affected_roads[road_id] = {
                    "road_id": road_id,
                    "affected_nodes": set(),
                    "minimum_distance": node_distance,
                    "current_status": edge.status
                }

            affected_roads[road_id][
                "affected_nodes"
            ].add(node_id)

            if node_distance < affected_roads[
                road_id
            ]["minimum_distance"]:

                affected_roads[
                    road_id
                ]["minimum_distance"] = node_distance

    return affected_roads


def test_cyclone_road_impact():

    print()
    print("==========================================")
    print(" CYCLONE ROAD IMPACT ANALYSIS")
    print("==========================================")

    # ------------------------------------------------
    # STEP 1
    # ------------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI ROAD GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # ------------------------------------------------
    # STEP 2
    # ------------------------------------------------

    print("\nSTEP 2: SELECTING REAL CYCLONE OBSERVATION")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    cyclone = get_closest_observation(
        relevant
    )

    print(
        "Cyclone:",
        cyclone.cyclone_name
    )

    print(
        "Track point:",
        cyclone.track_point_id
    )

    print(
        "Timestamp:",
        cyclone.timestamp_utc
    )

    print(
        "Latitude:",
        cyclone.latitude
    )

    print(
        "Longitude:",
        cyclone.longitude
    )

    print(
        "Wind speed:",
        cyclone.wind_speed,
        "km/h"
    )

    print(
        "Pressure:",
        cyclone.pressure,
        "hPa"
    )

    print(
        "Distance from Chennai:",
        cyclone.distance_from_chennai_km,
        "km"
    )

    # ------------------------------------------------
    # STEP 3
    # ------------------------------------------------

    print("\nSTEP 3: FINDING AFFECTED ROAD NODES")

    affected_nodes = find_affected_nodes(
        graph,
        cyclone.latitude,
        cyclone.longitude,
        IMPACT_RADIUS_METERS
    )

    print(
        "Impact radius:",
        IMPACT_RADIUS_METERS,
        "meters"
    )

    print(
        "Affected nodes:",
        len(affected_nodes)
    )

    # ------------------------------------------------
    # STEP 4
    # ------------------------------------------------

    print("\nSTEP 4: FINDING AFFECTED ROADS")

    affected_roads = analyze_affected_roads(
        graph,
        affected_nodes
    )

    print(
        "Unique affected roads:",
        len(affected_roads)
    )

    # ------------------------------------------------
    # STEP 5
    # ------------------------------------------------

    print("\nSTEP 5: ROAD STATUS SUMMARY")

    status_counts = {}

    for road_id, road_data in affected_roads.items():

        status = road_data["current_status"]

        if status not in status_counts:
            status_counts[status] = 0

        status_counts[status] += 1

    for status, count in status_counts.items():

        print(
            status,
            ":",
            count
        )

    # ------------------------------------------------
    # STEP 6
    # ------------------------------------------------

    print("\nSTEP 6: SAMPLE AFFECTED ROADS")

    sorted_roads = sorted(
        affected_roads.values(),
        key=lambda road: road["minimum_distance"]
    )

    for road in sorted_roads[:20]:

        print(
            "Road:",
            road["road_id"],
            "| Distance:",
            round(
                road["minimum_distance"],
                2
            ),
            "m",
            "| Nodes:",
            len(
                road["affected_nodes"]
            ),
            "| Status:",
            road["current_status"]
        )

    # ------------------------------------------------
    # FINAL SUMMARY
    # ------------------------------------------------

    print()
    print("==========================================")
    print(" CYCLONE ROAD IMPACT ANALYSIS COMPLETE")
    print("==========================================")

    print(
        "Cyclone:",
        cyclone.cyclone_name
    )

    print(
        "Impact radius:",
        IMPACT_RADIUS_METERS,
        "m"
    )

    print(
        "Affected nodes:",
        len(affected_nodes)
    )

    print(
        "Affected roads:",
        len(affected_roads)
    )

    print("==========================================")


if __name__ == "__main__":
    test_cyclone_road_impact()