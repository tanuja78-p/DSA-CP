from m1.graph import Graph

from m2.hazard_registry import HazardRegistry
from m2.hazard_astar import hazard_astar


def build_test_graph():

    graph = Graph()

    # --------------------------------------------------
    # NODES
    # --------------------------------------------------

    graph.add_node(
        "A",
        13.0000,
        80.0000
    )

    graph.add_node(
        "B",
        13.0010,
        80.0000
    )

    graph.add_node(
        "C",
        13.0020,
        80.0000
    )

    graph.add_node(
        "D",
        13.0030,
        80.0000
    )

    graph.add_node(
        "E",
        13.0010,
        80.0010
    )

    # --------------------------------------------------
    # PRIMARY ROUTE
    # A → B → C → D
    # --------------------------------------------------

    graph.add_edge(
        "A",
        "B",
        "R1",
        100
    )

    graph.add_edge(
        "B",
        "C",
        "R2",
        100
    )

    graph.add_edge(
        "C",
        "D",
        "R3",
        100
    )

    # --------------------------------------------------
    # ALTERNATE ROUTE
    # A → E → D
    # --------------------------------------------------

    graph.add_edge(
        "A",
        "E",
        "R4",
        180
    )

    graph.add_edge(
        "E",
        "D",
        "R5",
        180
    )

    return graph


def print_result(
    label,
    result
):

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
        "Path:",
        result["path"]
    )

    print(
        "Nodes explored:",
        result["nodes_explored"]
    )


def test_hazard_astar():

    print()
    print("==========================================")
    print(" MULTI-HAZARD A* TEST")
    print("==========================================")

    graph = build_test_graph()

    registry = HazardRegistry()

    # --------------------------------------------------
    # TEST 1: NO HAZARDS
    # --------------------------------------------------

    result1 = hazard_astar(
        graph,
        "A",
        "D",
        registry
    )

    print_result(
        "TEST 1: ALL ROADS SAFE",
        result1
    )

    # --------------------------------------------------
    # TEST 2: FLOOD BLOCKS PRIMARY ROUTE
    # --------------------------------------------------

    registry.set_flood_status(
        "R2",
        "BLOCKED"
    )

    result2 = hazard_astar(
        graph,
        "A",
        "D",
        registry
    )

    print_result(
        "TEST 2: FLOOD BLOCKS R2",
        result2
    )

    # --------------------------------------------------
    # TEST 3: CYCLONE ALSO AFFECTS ALTERNATE
    # --------------------------------------------------

    registry.set_cyclone_status(
        "R4",
        "BLOCKED"
    )

    result3 = hazard_astar(
        graph,
        "A",
        "D",
        registry
    )

    print_result(
        "TEST 3: FLOOD + CYCLONE",
        result3
    )

    # --------------------------------------------------
    # TEST 4: CYCLONE LEAVES
    # --------------------------------------------------

    registry.set_cyclone_status(
        "R4",
        "SAFE"
    )

    result4 = hazard_astar(
        graph,
        "A",
        "D",
        registry
    )

    print_result(
        "TEST 4: CYCLONE LEAVES",
        result4
    )

    # --------------------------------------------------
    # FINAL
    # --------------------------------------------------

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_hazard_astar()