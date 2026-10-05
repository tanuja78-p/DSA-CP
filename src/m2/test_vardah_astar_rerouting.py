from m1.build_road_graph import build_chennai_graph

from m2.astar import astar

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact,
    apply_cyclone_impact
)


SOURCE = "80.29048_13.09242"
DESTINATION = "80.29114_13.09609"


def get_route_road_ids(graph, path):

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


def test_vardah_astar_rerouting():

    print()
    print("==========================================")
    print(" REAL VARDAH + A* REROUTING TEST")
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

    print("\nSTEP 2: LOADING REAL VARDAH DATA")

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
        "Wind speed:",
        cyclone.wind_speed,
        "km/h"
    )

    print(
        "Pressure:",
        cyclone.pressure,
        "hPa"
    )

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print("\nSTEP 3: BASELINE A* ROUTE")

    baseline = astar(
        graph,
        SOURCE,
        DESTINATION
    )

    print(
        "Source:",
        SOURCE
    )

    print(
        "Destination:",
        DESTINATION
    )

    print(
        "Reachable:",
        baseline["reachable"]
    )

    print(
        "Distance:",
        baseline["distance"],
        "meters"
    )

    print(
        "Route nodes:",
        len(
            baseline["path"]
        )
    )

    print(
        "Nodes explored:",
        baseline["nodes_explored"]
    )

    baseline_roads = get_route_road_ids(
        graph,
        baseline["path"]
    )

    print(
        "Roads used:",
        sorted(
            set(baseline_roads)
        )
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print(
        "\nSTEP 4: CALCULATING REAL CYCLONE IMPACT"
    )

    impact = calculate_cyclone_impact(
        graph,
        cyclone,
        radius_meters=1000
    )

    affected_roads = set(
        impact["affected_roads"].keys()
    )

    print(
        "Severity:",
        impact["severity"]
    )

    print(
        "Status:",
        impact["status"]
    )

    print(
        "Impact radius:",
        impact["impact_radius_meters"],
        "meters"
    )

    print(
        "Affected nodes:",
        len(
            impact["affected_nodes"]
        )
    )

    print(
        "Affected roads:",
        len(
            affected_roads
        )
    )

    baseline_affected = (
        set(baseline_roads)
        & affected_roads
    )

    print(
        "Affected roads on baseline route:",
        sorted(
            baseline_affected
        )
    )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print(
        "\nSTEP 5: APPLYING REAL VARDAH IMPACT"
    )

    update_result = apply_cyclone_impact(
        graph,
        impact
    )

    print(
        "Updated roads:",
        update_result["updated_count"]
    )

    print(
        "Applied status:",
        update_result["status"]
    )

    # ------------------------------------------
    # STEP 6
    # ------------------------------------------

    print(
        "\nSTEP 6: RUNNING A* AFTER CYCLONE"
    )

    rerouted = astar(
        graph,
        SOURCE,
        DESTINATION
    )

    print(
        "Reachable:",
        rerouted["reachable"]
    )

    if rerouted["reachable"]:

        print(
            "New distance:",
            rerouted["distance"],
            "meters"
        )

        print(
            "New route nodes:",
            len(
                rerouted["path"]
            )
        )

        print(
            "Nodes explored:",
            rerouted["nodes_explored"]
        )

        rerouted_roads = get_route_road_ids(
            graph,
            rerouted["path"]
        )

        unique_rerouted_roads = set(
            rerouted_roads
        )

        print(
            "New route roads:",
            sorted(
                unique_rerouted_roads
            )
        )

        blocked_used = (
            unique_rerouted_roads
            & affected_roads
        )

        print(
            "Blocked cyclone roads used:",
            sorted(
                blocked_used
            )
        )

        print(
            "Route changed:",
            baseline["path"]
            != rerouted["path"]
        )

        print(
            "Additional distance:",
            rerouted["distance"]
            - baseline["distance"],
            "meters"
        )

    # ------------------------------------------
    # FINAL
    # ------------------------------------------

    print()
    print("==========================================")
    print(" REAL VARDAH + A* TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_vardah_astar_rerouting()