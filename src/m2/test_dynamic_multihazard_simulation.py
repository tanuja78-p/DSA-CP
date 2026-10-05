from m1.graph import Graph

from m2.hazard_registry import HazardRegistry
from m2.hazard_astar import hazard_astar


SOURCE = "A"
DESTINATION = "D"


def build_test_graph():
    graph = Graph()

    graph.add_node("A", 13.0000, 80.0000)
    graph.add_node("B", 13.0010, 80.0000)
    graph.add_node("C", 13.0020, 80.0000)
    graph.add_node("D", 13.0030, 80.0000)

    graph.add_node("E", 13.0010, 80.0010)
    graph.add_node("F", 13.0020, 80.0010)

    graph.add_edge("A", "B", "R1", 100)
    graph.add_edge("B", "C", "R2", 100)
    graph.add_edge("C", "D", "R3", 100)

    graph.add_edge("A", "E", "R4", 180)
    graph.add_edge("E", "F", "R5", 100)
    graph.add_edge("F", "D", "R6", 180)

    return graph


def print_route(label, result):

    print()
    print("------------------------------------------")
    print(label)
    print("------------------------------------------")

    print("Reachable:", result["reachable"])
    print("Distance:", result["distance"])
    print("Route:", result["path"])
    print("Nodes explored:", result["nodes_explored"])


def print_statuses(registry):

    print()
    print("Road hazard states:")

    for road_id in [
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6"
    ]:
        print(
            road_id,
            "→",
            registry.get_road_statuses(road_id)
        )


def run_route(graph, registry, label):

    result = hazard_astar(
        graph,
        SOURCE,
        DESTINATION,
        registry
    )

    print_route(
        label,
        result
    )

    return result


def main():

    print()
    print("==========================================")
    print(" DYNAMIC MULTI-HAZARD SIMULATION")
    print("==========================================")

    graph = build_test_graph()
    registry = HazardRegistry()

    # --------------------------------------------------
    # STATE 1 — NORMAL
    # --------------------------------------------------

    print()
    print("STATE 1: NORMAL CONDITIONS")

    result_normal = run_route(
        graph,
        registry,
        "NORMAL A*"
    )

    print_statuses(registry)

    # --------------------------------------------------
    # STATE 2 — FLOOD APPEARS
    # --------------------------------------------------

    print()
    print("STATE 2: FLOOD APPEARS")

    registry.set_flood_status(
        "R2",
        "BLOCKED"
    )

    result_flood = run_route(
        graph,
        registry,
        "A* AFTER FLOOD"
    )

    print_statuses(registry)

    # --------------------------------------------------
    # STATE 3 — CYCLONE APPEARS
    # --------------------------------------------------

    print()
    print("STATE 3: CYCLONE APPEARS")

    registry.set_cyclone_status(
        "R4",
        "BLOCKED"
    )

    result_both = run_route(
        graph,
        registry,
        "A* AFTER FLOOD + CYCLONE"
    )

    print_statuses(registry)

    # --------------------------------------------------
    # STATE 4 — CYCLONE MOVES AWAY
    # --------------------------------------------------

    print()
    print("STATE 4: CYCLONE LEAVES")

    registry.set_cyclone_status(
        "R4",
        "SAFE"
    )

    result_cyclone_gone = run_route(
        graph,
        registry,
        "A* AFTER CYCLONE LEAVES"
    )

    print_statuses(registry)

    # --------------------------------------------------
    # STATE 5 — FLOOD CLEARS
    # --------------------------------------------------

    print()
    print("STATE 5: FLOOD CLEARS")

    registry.set_flood_status(
        "R2",
        "SAFE"
    )

    result_all_clear = run_route(
        graph,
        registry,
        "A* AFTER ALL HAZARDS CLEAR"
    )

    print_statuses(registry)

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    print()
    print("==========================================")
    print(" DYNAMIC SIMULATION VALIDATION")
    print("==========================================")

    print()
    print(
        "Normal route:",
        result_normal["path"]
    )

    print(
        "Flood route:",
        result_flood["path"]
    )

    print(
        "Flood + cyclone route:",
        result_both["path"]
    )

    print(
        "After cyclone leaves:",
        result_cyclone_gone["path"]
    )

    print(
        "After all hazards clear:",
        result_all_clear["path"]
    )

    print()
    print("Flood status after cyclone leaves:")

    print(
        "R2 →",
        registry.get_road_statuses("R2")
    )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    main()