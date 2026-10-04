from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from m1.graph import Graph
from m1.data_loader import load_road_centerlines
from m1.graph import (
    make_node_id,
    haversine_distance
)

from m1.bfs import (
    bfs_reachable_nodes,
    bfs_distance_from_source
)


ROAD_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Road centerline map.kml"
)


def build_test_graph():

    print(
        "Loading real Chennai road dataset..."
    )

    roads = load_road_centerlines(
        str(ROAD_KML)
    )

    graph = Graph()

    for road in roads:

        road_id = road["road_id"]

        if not road_id:
            continue

        coordinates = road["coordinates"]

        for i in range(
            len(coordinates) - 1
        ):

            longitude1, latitude1 = (
                coordinates[i]
            )

            longitude2, latitude2 = (
                coordinates[i + 1]
            )

            node1 = make_node_id(
                longitude1,
                latitude1
            )

            node2 = make_node_id(
                longitude2,
                latitude2
            )

            if node1 == node2:
                continue

            graph.add_node(
                node1,
                latitude1,
                longitude1
            )

            graph.add_node(
                node2,
                latitude2,
                longitude2
            )

            distance = haversine_distance(
                latitude1,
                longitude1,
                latitude2,
                longitude2
            )

            graph.add_edge(
                node1,
                node2,
                road_id,
                distance
            )

    return graph


def main():

    print()
    print("==========================================")
    print(" M1 - BFS REAL CHENNAI GRAPH TEST")
    print("==========================================")
    print()

    graph = build_test_graph()

    print()
    print(
        f"Graph nodes: {graph.get_node_count()}"
    )

    print(
        f"Graph edges: {graph.get_edge_count()}"
    )

    all_nodes = graph.get_all_nodes()

    if not all_nodes:

        print("No graph nodes found.")

        return

    start_node = all_nodes[0].node_id

    print()
    print(
        f"BFS starting node: {start_node}"
    )

    reachable = bfs_reachable_nodes(
        graph,
        start_node
    )

    print()
    print(
        f"Reachable nodes: {len(reachable)}"
    )

    distances = bfs_distance_from_source(
        graph,
        start_node
    )

    print(
        f"BFS distance entries: "
        f"{len(distances)}"
    )

    print()
    print("First 10 reachable nodes:")

    for node in reachable[:10]:

        print(
            f"  {node}"
        )

    print()
    print("==========================================")
    print(" BFS TEST COMPLETE")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()