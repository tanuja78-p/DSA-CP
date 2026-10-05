from m1.graph import Graph
from m2.flood_hazard_registry import apply_flood_to_registry
from m2.hazard_registry import HazardRegistry
from m1.flood_engine import FloodHazard


def build_test_graph():
    graph = Graph()

    graph.add_node("A", 13.0000, 80.0000)
    graph.add_node("B", 13.0010, 80.0000)
    graph.add_node("C", 13.0020, 80.0000)
    graph.add_node("D", 13.0030, 80.0000)
    graph.add_node("E", 13.0010, 80.0010)

    graph.add_edge("A", "B", "R1", 100)
    graph.add_edge("B", "C", "R2", 100)
    graph.add_edge("C", "D", "R3", 100)
    graph.add_edge("A", "E", "R4", 180)
    graph.add_edge("E", "D", "R5", 180)

    return graph


def test_flood_hazard_registry():

    print()
    print("==========================================")
    print(" FLOOD → HAZARD REGISTRY TEST")
    print("==========================================")

    graph = build_test_graph()
    registry = HazardRegistry()

    flood = FloodHazard(
        hazard_id="TEST_FLOOD_001",
        latitude=13.0010,
        longitude=80.0000,
        severity="HIGH",
        depth=2.0,
        source="TEST"
    )

    print()
    print("Applying flood hazard...")

    result = apply_flood_to_registry(
        graph,
        [flood],
        registry
    )

    print()
    print("M1 flood result:")
    print(result)

    print()
    print("Hazard Registry:")

    for road_id in ["R1", "R2", "R3", "R4", "R5"]:
        print(
            road_id,
            "→",
            registry.get_road_statuses(road_id)
        )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_flood_hazard_registry()