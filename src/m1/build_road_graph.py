from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from m1.data_loader import (
    load_road_centerlines,
    print_road_sample
)

from m1.graph import (
    Graph,
    make_node_id,
    haversine_distance
)

from m1.graph_export import (
    export_graph
)


ROAD_KML = (
    PROJECT_ROOT
    / "data"
    / "Chennai Road centerline map.kml"
)


PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


def build_chennai_graph():

    print()
    print("==========================================")
    print(" M1 - CHENNAI DYNAMIC ROAD GRAPH")
    print("==========================================")
    print()

    print(
        "Loading Chennai Road Centerline KML..."
    )

    roads = load_road_centerlines(
        str(ROAD_KML)
    )

    print(
        f"Road geometries loaded: {len(roads)}"
    )

    print_road_sample(
        roads,
        count=5
    )

    graph = Graph()

    print(
        "Building adjacency-list graph..."
    )

    for index, road in enumerate(
        roads,
        start=1
    ):

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
                source=node1,
                destination=node2,
                road_id=road_id,
                distance=distance
            )

        if index % 5000 == 0:

            print(
                f"Processed "
                f"{index}/{len(roads)} roads..."
            )

    print()
    print("==========================================")
    print(" GRAPH BUILD COMPLETE")
    print("==========================================")

    print(
        f"Road geometries : {len(roads)}"
    )

    print(
        f"Graph nodes     : "
        f"{graph.get_node_count()}"
    )

    print(
        f"Graph edges     : "
        f"{graph.get_edge_count()}"
    )

    print("==========================================")

    return graph


if __name__ == "__main__":

    graph = build_chennai_graph()

    export_graph(
        graph,
        str(PROCESSED_DATA)
    )