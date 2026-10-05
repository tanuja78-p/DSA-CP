from m1.build_road_graph import build_chennai_graph

from m2.hazard_registry import HazardRegistry
from m2.hazard_astar import hazard_astar
from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.cyclone_hazard_registry import apply_cyclone_to_registry


SOURCE = "80.29048_13.09242"
DESTINATION = "80.29114_13.09609"

FLOOD_ROAD = "10529"


def get_vardah_observation():
    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(hazards)

    vardah = [
        hazard
        for hazard in relevant
        if hazard.cyclone_id == "vardah"
    ]

    if not vardah:
        raise RuntimeError(
            "No Chennai-relevant Vardah observations found."
        )

    return min(
        vardah,
        key=lambda hazard: hazard.distance_from_chennai_km
    )


def get_route_road_ids(graph, path):
    """
    Return the unique road IDs used by a route.
    """

    road_ids = []

    for index in range(len(path) - 1):

        current = path[index]
        next_node = path[index + 1]

        for edge in graph.get_neighbors(current):

            if edge.destination == next_node:

                if edge.road_id not in road_ids:
                    road_ids.append(edge.road_id)

                break

    return road_ids


def print_route(label, graph, result):

    print()
    print("------------------------------------------")
    print(label)
    print("------------------------------------------")

    print("Reachable:", result["reachable"])
    print("Distance:", result["distance"])
    print("Route nodes:", len(result["path"]))
    print("Nodes explored:", result["nodes_explored"])

    if result["path"]:

        print("Roads used:")

        roads = get_route_road_ids(
            graph,
            result["path"]
        )

        print(roads)


def main():

    print()
    print("==========================================")
    print(" CONTROLLED REAL MULTI-HAZARD REROUTING")
    print("==========================================")

    print()
    print("Building real Chennai graph...")

    graph = build_chennai_graph()

    print()
    print("Graph nodes:", graph.get_node_count())
    print("Graph edges:", graph.get_edge_count())

    registry = HazardRegistry()

    # --------------------------------------------------
    # TEST 1 — NORMAL CONDITIONS
    # --------------------------------------------------

    print()
    print("TEST 1: NORMAL CONDITIONS")

    baseline = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        "BASELINE A*",
        graph,
        baseline
    )

    # --------------------------------------------------
    # TEST 2 — CONTROLLED FLOOD
    # --------------------------------------------------

    print()
    print("TEST 2: CONTROLLED FLOOD")

    print(
        "Flood-blocking road:",
        FLOOD_ROAD
    )

    registry.set_flood_status(
        FLOOD_ROAD,
        "BLOCKED"
    )

    after_flood = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        "A* AFTER FLOOD",
        graph,
        after_flood
    )

    # --------------------------------------------------
    # TEST 3 — REAL VARDAH
    # --------------------------------------------------

    print()
    print("TEST 3: REAL VARDAH")

    cyclone = get_vardah_observation()

    print()
    print("Cyclone:", cyclone.cyclone_name)
    print("Track Point:", cyclone.track_point_id)
    print("Timestamp:", cyclone.timestamp_utc)
    print("Wind Speed:", cyclone.wind_speed)
    print("Pressure:", cyclone.pressure)
    print(
        "Distance from Chennai:",
        cyclone.distance_from_chennai_km,
        "km"
    )

    cyclone_result = apply_cyclone_to_registry(
        graph,
        cyclone,
        registry,
        radius_meters=1000
    )

    print()
    print("Cyclone severity:",
          cyclone_result["severity"])

    print(
        "Cyclone status:",
        cyclone_result["status"]
    )

    print(
        "Cyclone affected nodes:",
        len(cyclone_result["affected_nodes"])
    )

    print(
        "Cyclone affected roads:",
        len(cyclone_result["affected_roads"])
    )

    # --------------------------------------------------
    # TEST 4 — FLOOD + CYCLONE
    # --------------------------------------------------

    print()
    print("TEST 4: FLOOD + CYCLONE")

    final_result = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        "FINAL MULTI-HAZARD A*",
        graph,
        final_result
    )

    # --------------------------------------------------
    # FINAL COMPARISON
    # --------------------------------------------------

    print()
    print("==========================================")
    print(" FINAL COMPARISON")
    print("==========================================")

    print()
    print(
        "Baseline distance:",
        baseline["distance"]
    )

    print(
        "After flood distance:",
        after_flood["distance"]
    )

    print(
        "After flood + cyclone:",
        final_result["distance"]
    )

    if baseline["reachable"] and after_flood["reachable"]:

        print()
        print(
            "Flood additional distance:",
            after_flood["distance"]
            - baseline["distance"]
        )

    if after_flood["reachable"] and final_result["reachable"]:

        print()
        print(
            "Additional distance after cyclone:",
            final_result["distance"]
            - after_flood["distance"]
        )

    if baseline["reachable"] and final_result["reachable"]:

        print()
        print(
            "Total additional distance:",
            final_result["distance"]
            - baseline["distance"]
        )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    main()