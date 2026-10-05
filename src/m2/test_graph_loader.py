from m2.graph_loader import load_chennai_graph


def main():
    print()
    print("==========================================")
    print(" M2 CHENNAI GRAPH LOADER TEST")
    print("==========================================")

    graph = load_chennai_graph()

    print()
    print("Graph loaded successfully")
    print("Nodes:", graph.get_node_count())
    print("Edges:", graph.get_edge_count())

    print()
    print("Known road status checks:")

    for road_id in ["11196", "7075", "9113", "90_New45"]:
        print(
            road_id,
            "->",
            graph.get_road_status(road_id)
        )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    main()