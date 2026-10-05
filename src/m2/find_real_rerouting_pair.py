import time

from m1.build_road_graph import build_chennai_graph
from m1.graph import haversine_distance

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact,
    apply_cyclone_impact
)

from m2.astar import astar


def get_route_road_ids(graph, path):
    """
    Extract road IDs used by a route.
    """

    road_ids = []

    for index in range(len(path) - 1):

        current_node = path[index]
        next_node = path[index + 1]

        for edge in graph.get_neighbors(
            current_node
        ):

            if edge.destination == next_node:

                road_ids.append(
                    edge.road_id
                )

                break

    return road_ids


def get_node_distance(
    graph,
    node_a,
    node_b
):
    """
    Geographic distance between two graph nodes.
    """

    a = graph.nodes[node_a]
    b = graph.nodes[node_b]

    return haversine_distance(
        a.latitude,
        a.longitude,
        b.latitude,
        b.longitude
    )


def find_rerouting_pair():

    print()
    print("==========================================")
    print(" REAL CYCLONE REROUTING PAIR SEARCH")
    print("==========================================")

    # ------------------------------------------
    # STEP 1
    # ------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # ------------------------------------------
    # STEP 2
    # ------------------------------------------

    print("\nSTEP 2: LOADING VARDah OBSERVATION")

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

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print("\nSTEP 3: CALCULATING CYCLONE IMPACT")

    impact = calculate_cyclone_impact(
        graph,
        cyclone,
        radius_meters=1000
    )

    affected_road_ids = set(
        impact["affected_roads"].keys()
    )

    affected_nodes = [
        item["node_id"]
        for item in impact["affected_nodes"]
    ]

    print(
        "Affected nodes:",
        len(affected_nodes)
    )

    print(
        "Affected roads:",
        len(affected_road_ids)
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print(
        "\nSTEP 4: CREATING OUTSIDE-ZONE CANDIDATES"
    )

    cyclone_lat = cyclone.latitude
    cyclone_lon = cyclone.longitude

    source_candidates = []
    destination_candidates = []

    # We deliberately choose nodes outside
    # the 1 km impact radius.
    #
    # Source:
    # approximately 2-3 km away
    #
    # Destination:
    # approximately 2-3 km away

    for node_id, node in graph.nodes.items():

        distance = haversine_distance(
            cyclone_lat,
            cyclone_lon,
            node.latitude,
            node.longitude
        )

        if 2000 <= distance <= 3000:

            source_candidates.append(
                node_id
            )

            destination_candidates.append(
                node_id
            )

    print(
        "Outside-zone candidates:",
        len(source_candidates)
    )

    # Limit candidate count to avoid excessive
    # A* searches.
    source_candidates = source_candidates[
        :30
    ]

    destination_candidates = destination_candidates[
        :30
    ]

    print(
        "Testing candidates:",
        len(source_candidates),
        "x",
        len(destination_candidates)
    )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print("\nSTEP 5: SEARCHING FOR ROUTE")

    found = False

    selected_source = None
    selected_destination = None
    selected_before = None
    selected_route_roads = None

    for source in source_candidates:

        for destination in destination_candidates:

            if source == destination:
                continue

            # Make sure source and destination
            # are geographically separated.
            endpoint_distance = get_node_distance(
                graph,
                source,
                destination
            )

            if endpoint_distance < 2000:
                continue

            before = astar(
                graph,
                source,
                destination
            )

            if not before["reachable"]:
                continue

            route_roads = get_route_road_ids(
                graph,
                before["path"]
            )

            affected_on_route = (
                set(route_roads)
                & affected_road_ids
            )

            if not affected_on_route:
                continue

            # ----------------------------------
            # Temporarily apply cyclone
            # ----------------------------------

            apply_cyclone_impact(
                graph,
                impact
            )

            after = astar(
                graph,
                source,
                destination
            )

            # Restore affected roads to SAFE
            # for testing the next pair.
            for road_id in affected_road_ids:

                graph.update_road_status(
                    road_id,
                    "SAFE"
                )

            if not after["reachable"]:
                continue

            new_route_roads = get_route_road_ids(
                graph,
                after["path"]
            )

            blocked_used = (
                set(new_route_roads)
                & affected_road_ids
            )

            if blocked_used:
                continue

            if before["path"] == after["path"]:
                continue

            selected_source = source
            selected_destination = destination
            selected_before = before
            selected_route_roads = route_roads

            print()
            print(
                "=========================================="
            )
            print(
                " SUCCESSFUL REROUTING PAIR FOUND"
            )
            print(
                "=========================================="
            )

            print(
                "Source:",
                selected_source
            )

            print(
                "Destination:",
                selected_destination
            )

            print(
                "Endpoint distance:",
                round(
                    endpoint_distance,
                    2
                ),
                "meters"
            )

            print(
                "Original route nodes:",
                len(
                    before["path"]
                )
            )

            print(
                "Original route distance:",
                before["distance"],
                "meters"
            )

            print(
                "Affected roads on original route:",
                sorted(
                    affected_on_route
                )
            )

            print(
                "Rerouted distance:",
                after["distance"],
                "meters"
            )

            print(
                "Rerouted nodes:",
                len(
                    after["path"]
                )
            )

            print(
                "Route changed:",
                before["path"] != after["path"]
            )

            print(
                "Blocked roads used after rerouting:",
                sorted(
                    blocked_used
                )
            )

            print(
                "Additional distance:",
                after["distance"]
                - before["distance"],
                "meters"
            )

            found = True
            break

        if found:
            break

    # ------------------------------------------
    # FINAL
    # ------------------------------------------

    if not found:

        print()
        print(
            "NO VALID REROUTING PAIR FOUND."
        )

        print(
            "The candidate search needs to be expanded."
        )

    print()
    print("==========================================")
    print(" SEARCH COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    find_rerouting_pair()