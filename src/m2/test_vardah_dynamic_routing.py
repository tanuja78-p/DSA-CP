from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.real_cyclone_impact import calculate_cyclone_impact
from m2.cyclone_graph_state import CycloneGraphStateManager
from m2.astar import astar


IMPACT_RADIUS_METERS = 1000

SOURCE = "80.29048_13.09242"
DESTINATION = "80.29114_13.09609"


def get_route_roads(graph, path):

    roads = []

    for index in range(len(path) - 1):

        current = path[index]
        next_node = path[index + 1]

        for edge in graph.get_neighbors(current):

            if edge.destination == next_node:

                roads.append(edge.road_id)
                break

    return roads


def print_route(label, result, graph):

    print()
    print("------------------------------------------")
    print(label)
    print("------------------------------------------")

    print(
        "Reachable:",
        result["reachable"]
    )

    print(
        "Distance:",
        result["distance"]
    )

    print(
        "Route nodes:",
        len(result["path"])
    )

    print(
        "Nodes explored:",
        result["nodes_explored"]
    )

    if result["reachable"]:

        print(
            "Roads used:",
            get_route_roads(
                graph,
                result["path"]
            )
        )


def test_vardah_dynamic_routing():

    print()
    print("======================================================")
    print(" REAL VARDAH DYNAMIC A* ROUTING")
    print("======================================================")

    # --------------------------------------------------
    # STEP 1: BUILD REAL CHENNAI GRAPH
    # --------------------------------------------------

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

    # --------------------------------------------------
    # STEP 2: LOAD VARDAH TRACK
    # --------------------------------------------------

    print("\nSTEP 2: LOADING REAL VARDAH TRACK")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    vardah = [
        hazard
        for hazard in relevant
        if hazard.cyclone_name.lower() == "vardah"
    ]

    vardah = sorted(
        vardah,
        key=lambda hazard:
            hazard.timestamp_utc
    )

    selected_track_ids = {
        "TP0157",
        "TP0158",
        "TP0159",
        "TP0160"
    }

    vardah = [
        hazard
        for hazard in vardah
        if hazard.track_point_id in selected_track_ids
    ]

    print(
        "Selected track points:",
        len(vardah)
    )

    # --------------------------------------------------
    # STEP 3: CREATE CYCLONE GRAPH STATE MANAGER
    # --------------------------------------------------

    cyclone_manager = (
        CycloneGraphStateManager()
    )

    # --------------------------------------------------
    # STEP 4: BASELINE ROUTE
    # --------------------------------------------------

    print("\nSTEP 3: BASELINE A* ROUTE")

    baseline = astar(
        graph,
        SOURCE,
        DESTINATION
    )

    print_route(
        "BASELINE BEFORE CYCLONE",
        baseline,
        graph
    )

    baseline_distance = baseline["distance"]
    baseline_path = baseline["path"]

    # --------------------------------------------------
    # STEP 5: PROCESS EACH CYCLONE OBSERVATION
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" CYCLONE TRACK SIMULATION")
    print("======================================================")

    current_route = baseline

    for hazard in vardah:

        print()
        print("==========================================")
        print(
            "TRACK POINT:",
            hazard.track_point_id
        )
        print(
            "TIME:",
            hazard.timestamp_utc
        )
        print("==========================================")

        print(
            "Cyclone distance:",
            hazard.distance_from_chennai_km,
            "km"
        )

        print(
            "Wind speed:",
            hazard.wind_speed,
            "km/h"
        )

        # --------------------------------------------------
        # CALCULATE IMPACT
        # --------------------------------------------------

        impact = calculate_cyclone_impact(
            graph,
            hazard,
            radius_meters=IMPACT_RADIUS_METERS
        )

        affected_roads = set(
            impact["affected_roads"].keys()
        )

        print(
            "Severity:",
            impact["severity"]
        )

        print(
            "Affected nodes:",
            len(
                impact["affected_nodes"]
            )
        )

        print(
            "Affected roads:",
            len(affected_roads)
        )

        # --------------------------------------------------
        # UPDATE CYCLONE GRAPH STATE
        # --------------------------------------------------

        changes = cyclone_manager.update_graph(
            graph,
            affected_roads
        )

        print(
            "Newly affected:",
            len(
                changes["newly_affected"]
            )
        )

        print(
            "Still affected:",
            len(
                changes["still_affected"]
            )
        )

        print(
            "No longer affected:",
            len(
                changes["no_longer_affected"]
            )
        )

        # --------------------------------------------------
        # ONLY REROUTE IF GRAPH CHANGED
        # --------------------------------------------------

        graph_changed = (
            len(changes["newly_affected"]) > 0
            or
            len(changes["no_longer_affected"]) > 0
        )

        if graph_changed:

            current_route = astar(
                graph,
                SOURCE,
                DESTINATION
            )

            print_route(
                "A* AFTER GRAPH UPDATE",
                current_route,
                graph
            )

        else:

            print(
                "No graph change."
            )

            print(
                "A* rerouting skipped."
            )

    # --------------------------------------------------
    # STEP 6: FINAL COMPARISON
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" FINAL ROUTING COMPARISON")
    print("======================================================")

    print(
        "Baseline distance:",
        baseline_distance
    )

    print(
        "Final distance:",
        current_route["distance"]
    )

    if baseline_distance is not None:
        print(
            "Additional distance:",
            current_route["distance"]
            - baseline_distance
        )

    print(
        "Route changed:",
        baseline_path != current_route["path"]
    )

    print()
    print("======================================================")
    print(" REAL VARDAH DYNAMIC ROUTING COMPLETE")
    print("======================================================")


if __name__ == "__main__":
    test_vardah_dynamic_routing()