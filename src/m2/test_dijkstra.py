from m1.graph import Graph

from m2.dijkstra import dijkstra


def build_test_graph():
    """
    Build a small test graph for congestion-aware routing.
    """

    graph = Graph()

    graph.add_node("A", 18.5204, 73.8567)
    graph.add_node("B", 18.5210, 73.8570)
    graph.add_node("C", 18.5220, 73.8580)
    graph.add_node("D", 18.5230, 73.8590)

    # Short route:
    # A -> B -> D
    graph.add_edge("A", "B", "R1", 100)
    graph.add_edge("B", "D", "R2", 100)

    # Slightly longer safe route:
    # A -> C -> D
    graph.add_edge("A", "C", "R3", 120)
    graph.add_edge("C", "D", "R4", 120)

    return graph


def test_congestion_aware_routing():

    print("=== CONGESTION-AWARE DIJKSTRA TEST ===")

    graph = build_test_graph()

    source = "A"
    destination = "D"

    # --------------------------------------------------
    # TEST 1: NORMAL ROAD CONDITIONS
    # --------------------------------------------------

    print("\n--- BEFORE RESTRICTION ---")

    result = dijkstra(
        graph,
        source,
        destination
    )

    print("Route:", " -> ".join(result["path"]))
    print("Cost:", result["distance"])
    print("Reachable:", result["reachable"])
    print("Nodes explored:", result["nodes_explored"])

    # --------------------------------------------------
    # MAKE SHORTER ROUTE RESTRICTED
    # --------------------------------------------------

    print("\nMaking shorter route restricted...")

    graph.update_road_status(
        "R1",
        "RESTRICTED"
    )

    graph.update_road_status(
        "R2",
        "RESTRICTED"
    )

    print(
        "R1 status:",
        graph.get_road_status("R1")
    )

    print(
        "R2 status:",
        graph.get_road_status("R2")
    )

    # --------------------------------------------------
    # TEST 2: RESTRICTED ROAD CONDITIONS
    # --------------------------------------------------

    print("\n--- AFTER RESTRICTION ---")

    result = dijkstra(
        graph,
        source,
        destination
    )

    print("Route:", " -> ".join(result["path"]))
    print("Cost:", result["distance"])
    print("Reachable:", result["reachable"])
    print("Nodes explored:", result["nodes_explored"])


if __name__ == "__main__":
    test_congestion_aware_routing()