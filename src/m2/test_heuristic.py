from m1.graph import Graph

from m2.heuristic import geographic_heuristic


def test_geographic_heuristic():

    print("=== A* HEURISTIC TEST ===")

    graph = Graph()

    graph.add_node(
        "A",
        18.5204,
        73.8567
    )

    graph.add_node(
        "B",
        18.5304,
        73.8567
    )

    distance = geographic_heuristic(
        graph,
        "A",
        "B"
    )

    print("Current node:", "A")
    print("Destination node:", "B")
    print("Estimated distance:", distance, "meters")

    print("\nHeuristic calculation successful.")


if __name__ == "__main__":
    test_geographic_heuristic()