from m1.graph import Graph

from m2.astar import astar


def build_test_graph():

    graph = Graph()

    graph.add_node(
        "A",
        18.5204,
        73.8567
    )

    graph.add_node(
        "B",
        18.5210,
        73.8570
    )

    graph.add_node(
        "C",
        18.5220,
        73.8580
    )

    graph.add_node(
        "D",
        18.5230,
        73.8590
    )

    graph.add_edge(
        "A",
        "B",
        "R1",
        100
    )

    graph.add_edge(
        "B",
        "D",
        "R2",
        100
    )

    graph.add_edge(
        "A",
        "C",
        "R3",
        120
    )

    graph.add_edge(
        "C",
        "D",
        "R4",
        120
    )

    return graph


def test_astar():

    print("=== A* TEST ===")

    graph = build_test_graph()

    source = "A"
    destination = "D"

    result = astar(
        graph,
        source,
        destination
    )

    print("Source:", source)
    print("Destination:", destination)

    print(
        "Route:",
        " -> ".join(result["path"])
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


if __name__ == "__main__":
    test_astar()