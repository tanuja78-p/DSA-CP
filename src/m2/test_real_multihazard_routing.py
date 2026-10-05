from m1.build_road_graph import build_chennai_graph
from m1.flood_engine import FloodHazard

from m2.hazard_registry import HazardRegistry
from m2.flood_hazard_registry import apply_flood_to_registry
from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.cyclone_hazard_registry import apply_cyclone_to_registry
from m2.hazard_astar import hazard_astar


SOURCE = "80.29048_13.09242"
DESTINATION = "80.29114_13.09609"


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


def print_route(label, result):
    print()
    print("------------------------------------------")
    print(label)
    print("------------------------------------------")
    print("Reachable:", result["reachable"])
    print("Distance:", result["distance"])
    print("Route nodes:", len(result["path"]))
    print("Nodes explored:", result["nodes_explored"])

    if result["path"]:
        print("Path:")
        print(" -> ".join(result["path"]))


def test_real_multihazard_routing():

    print()
    print("==========================================")
    print(" REAL MULTI-HAZARD A* TEST")
    print("==========================================")

    print()
    print("Building real Chennai road graph...")

    graph = build_chennai_graph()

    print("Graph nodes:", graph.get_node_count())
    print("Graph edges:", graph.get_edge_count())

    if SOURCE not in graph.nodes:
        raise RuntimeError(
            f"Source node {SOURCE} not found."
        )

    if DESTINATION not in graph.nodes:
        raise RuntimeError(
            f"Destination node {DESTINATION} not found."
        )

    registry = HazardRegistry()

    # --------------------------------------------------
    # TEST 1: BASELINE
    # --------------------------------------------------

    print()
    print("TEST 1: BASELINE — NO HAZARDS")

    baseline = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        "BASELINE A*",
        baseline
    )

    # --------------------------------------------------
    # TEST 2: FLOOD
    # --------------------------------------------------

    print()
    print("TEST 2: APPLYING FLOOD")

    flood = FloodHazard(
        hazard_id="TEST_FLOOD_001",
        latitude=13.09242,
        longitude=80.29048,
        severity="HIGH",
        depth=2.0,
        source="TEST"
    )

    flood_result = apply_flood_to_registry(
        graph,
        [flood],
        registry
    )

    print()
    print("Flood affected nodes:",
          len(flood_result["affected_nodes"]))

    print(
        "Flood BLOCKED roads:",
        len(flood_result["BLOCKED"])
    )

    print(
        "Flood RESTRICTED roads:",
        len(flood_result["RESTRICTED"])
    )

    after_flood = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        "A* AFTER FLOOD",
        after_flood
    )

    # --------------------------------------------------
    # TEST 3: CYCLONE
    # --------------------------------------------------

    print()
    print("TEST 3: APPLYING REAL VARDAH")

    cyclone = get_vardah_observation()

    print()
    print("Cyclone:")
    print("Name:", cyclone.cyclone_name)
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

    after_cyclone = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        "A* AFTER FLOOD + CYCLONE",
        after_cyclone
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
        "After flood + cyclone distance:",
        after_cyclone["distance"]
    )

    if (
        baseline["reachable"]
        and after_cyclone["reachable"]
    ):
        print()
        print(
            "Additional distance:",
            after_cyclone["distance"]
            - baseline["distance"]
        )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_real_multihazard_routing()