from m1.graph import Graph

from m2.cyclone_graph_state import (
    CycloneGraphStateManager
)


def build_test_graph():

    graph = Graph()

    # --------------------------------------------------
    # CREATE NODES FIRST
    # --------------------------------------------------
    # M1 Graph requires nodes to exist before
    # edges can be added.

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

    # --------------------------------------------------
    # CREATE ROADS
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

    return graph


def test_cyclone_graph_state():

    print()
    print("==========================================")
    print(" CYCLONE GRAPH STATE TEST")
    print("==========================================")

    # --------------------------------------------------
    # BUILD TEST GRAPH
    # --------------------------------------------------

    graph = build_test_graph()

    manager = CycloneGraphStateManager()

    # --------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------

    print("\nINITIAL ROAD STATUS")

    print(
        "R1:",
        graph.get_road_status("R1")
    )

    print(
        "R2:",
        graph.get_road_status("R2")
    )

    print(
        "R3:",
        graph.get_road_status("R3")
    )

    # --------------------------------------------------
    # CYCLONE UPDATE 1
    # R1 AND R2 ARE AFFECTED
    # --------------------------------------------------

    print("\nCYCLONE UPDATE 1")

    result1 = manager.update_graph(
        graph,
        {
            "R1",
            "R2"
        }
    )

    print(
        "New:",
        result1["newly_affected"]
    )

    print(
        "Still:",
        result1["still_affected"]
    )

    print(
        "Removed:",
        result1["no_longer_affected"]
    )

    print(
        "R1:",
        graph.get_road_status("R1")
    )

    print(
        "R2:",
        graph.get_road_status("R2")
    )

    print(
        "R3:",
        graph.get_road_status("R3")
    )

    # --------------------------------------------------
    # CYCLONE UPDATE 2
    # R1 IS NO LONGER AFFECTED
    # R2 REMAINS AFFECTED
    # R3 BECOMES AFFECTED
    # --------------------------------------------------

    print("\nCYCLONE UPDATE 2")

    result2 = manager.update_graph(
        graph,
        {
            "R2",
            "R3"
        }
    )

    print(
        "New:",
        result2["newly_affected"]
    )

    print(
        "Still:",
        result2["still_affected"]
    )

    print(
        "Removed:",
        result2["no_longer_affected"]
    )

    print(
        "R1:",
        graph.get_road_status("R1")
    )

    print(
        "R2:",
        graph.get_road_status("R2")
    )

    print(
        "R3:",
        graph.get_road_status("R3")
    )

    # --------------------------------------------------
    # CYCLONE UPDATE 3
    # R2 IS NO LONGER AFFECTED
    # R3 REMAINS AFFECTED
    # --------------------------------------------------

    print("\nCYCLONE UPDATE 3")

    result3 = manager.update_graph(
        graph,
        {
            "R3"
        }
    )

    print(
        "New:",
        result3["newly_affected"]
    )

    print(
        "Still:",
        result3["still_affected"]
    )

    print(
        "Removed:",
        result3["no_longer_affected"]
    )

    print(
        "R1:",
        graph.get_road_status("R1")
    )

    print(
        "R2:",
        graph.get_road_status("R2")
    )

    print(
        "R3:",
        graph.get_road_status("R3")
    )

    # --------------------------------------------------
    # CYCLONE UPDATE 4
    # CYCLONE HAS LEFT THE AREA
    # --------------------------------------------------

    print("\nCYCLONE UPDATE 4")

    result4 = manager.update_graph(
        graph,
        set()
    )

    print(
        "New:",
        result4["newly_affected"]
    )

    print(
        "Still:",
        result4["still_affected"]
    )

    print(
        "Removed:",
        result4["no_longer_affected"]
    )

    print(
        "R1:",
        graph.get_road_status("R1")
    )

    print(
        "R2:",
        graph.get_road_status("R2")
    )

    print(
        "R3:",
        graph.get_road_status("R3")
    )

    # --------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------

    print("\nFINAL ROAD STATUS")

    print(
        "R1:",
        graph.get_road_status("R1")
    )

    print(
        "R2:",
        graph.get_road_status("R2")
    )

    print(
        "R3:",
        graph.get_road_status("R3")
    )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_graph_state()