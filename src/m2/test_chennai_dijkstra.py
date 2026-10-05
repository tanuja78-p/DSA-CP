from m1.build_road_graph import build_chennai_graph

from m2.dijkstra import dijkstra


def select_test_nodes(graph):
    """
    Select two connected nodes from the real Chennai graph.

    The first edge found is used so that the destination
    is guaranteed to be directly reachable from the source.
    """

    for source, edges in graph.adjacency.items():

        if edges:

            destination = edges[0].destination

            return source, destination

    raise RuntimeError(
        "Could not find connected nodes in Chennai graph."
    )


def test_chennai_dijkstra():

    print()
    print("==========================================")
    print(" M2 - CHENNAI DIJKSTRA TEST")
    print("==========================================")

    print("\nBuilding Chennai graph...")

    graph = build_chennai_graph()

    print("\nSelecting connected test nodes...")

    source, destination = select_test_nodes(graph)

    print("Source node      :", source)
    print("Destination node :", destination)

    print("\nRunning Dijkstra...")

    result = dijkstra(
        graph,
        source,
        destination
    )

    print()
    print("==========================================")
    print(" DIJKSTRA RESULT")
    print("==========================================")

    print(
        "Reachable        :",
        result["reachable"]
    )

    print(
        "Route distance   :",
        result["distance"],
        "meters"
    )

    print(
        "Nodes explored   :",
        result["nodes_explored"]
    )

    print(
        "Route node count :",
        len(result["path"])
    )

    print()

    if result["reachable"]:

        print("Route:")

        print(
            " -> ".join(result["path"])
        )

    else:

        print("No route available.")

    print()
    print("==========================================")


if __name__ == "__main__":
    test_chennai_dijkstra()