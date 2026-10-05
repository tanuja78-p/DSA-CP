from m2.graph_loader import load_chennai_graph
from m2.astar import astar


SOURCE = "80.26187_13.09112"
DESTINATION = "80.25126_13.09458"


def main():

    print()
    print("==========================================")
    print(" LOADED GRAPH A* ROUTING TEST")
    print("==========================================")

    graph = load_chennai_graph()

    print()
    print("Graph:")
    print("Nodes:", graph.get_node_count())
    print("Edges:", graph.get_edge_count())

    print()
    print("Routing:")
    print("Source:", SOURCE)
    print("Destination:", DESTINATION)

    result = astar(
        graph,
        SOURCE,
        DESTINATION
    )

    print()
    print("Reachable:", result["reachable"])
    print("Distance:", result["distance"])
    print("Route nodes:", len(result["path"]))
    print("Nodes explored:", result["nodes_explored"])

    print()
    print("Route:")
    print(result["path"])

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    main()