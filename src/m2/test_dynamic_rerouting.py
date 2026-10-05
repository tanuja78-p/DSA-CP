from m1.graph import Graph

from m2.astar import astar


def build_test_graph():
    """
    Create a small road network containing
    a primary route and an alternate route.
    """

    graph = Graph()

    # Nodes
    graph.add_node(
        "A",
        13.0827,
        80.2707
    )

    graph.add_node(
        "B",
        13.0837,
        80.2717
    )

    graph.add_node(
        "C",
        13.0847,
        80.2727
    )

    graph.add_node(
        "D",
        13.0857,
        80.2737
    )

    graph.add_node(
        "E",
        13.0830,
        80.2740
    )

    # Primary route:
    #
    # A → B → C → D
    #
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

    # Alternate route:
    #
    # A → E → D
    #
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


def print_route(title, result):

    print()
    print(title)
    print("------------------------------------------")

    print(
        "Route:",
        " -> ".join(result["path"])
        if result["path"]
        else "No route"
    )

    print(
        "Cost:",
        result["distance"]
    )

    print(
        "Reachable:",
        result["reachable"]
    )

    print(
        "Nodes explored:",
        result["nodes_explored"]
    )


def test_dynamic_rerouting():

    print("==========================================")
    print(" DYNAMIC REROUTING TEST")
    print("==========================================")

    graph = build_test_graph()

    source = "A"
    destination = "D"

    # --------------------------------------------------
    # STEP 1: NORMAL ROUTING
    # --------------------------------------------------

    print("\nSTEP 1: NORMAL ROAD CONDITIONS")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "Primary route",
        result
    )

    # --------------------------------------------------
    # STEP 2: SIMULATE HAZARD
    # --------------------------------------------------

    print("\nSTEP 2: HAZARD DETECTED")

    print(
        "Simulating flood/cyclone blockage on road R2..."
    )

    graph.update_road_status(
        "R2",
        "BLOCKED"
    )

    print(
        "R2 status:",
        graph.get_road_status("R2")
    )

    # --------------------------------------------------
    # STEP 3: DYNAMIC REROUTING
    # --------------------------------------------------

    print("\nSTEP 3: DYNAMIC REROUTING")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "New evacuation route",
        result
    )

    print()
    print("==========================================")
    print(" DYNAMIC REROUTING COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_dynamic_rerouting()