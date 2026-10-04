import csv
from pathlib import Path

from m1.graph import Graph


def export_nodes(
    graph: Graph,
    filename: str
):
    """
    Export all graph nodes to a CSV file.

    Columns:
        node_id
        latitude
        longitude
    """

    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "node_id",
            "latitude",
            "longitude"
        ])

        for node in graph.get_all_nodes():

            writer.writerow([
                node.node_id,
                node.latitude,
                node.longitude
            ])

    print(
        f"Nodes exported: {graph.get_node_count()}"
    )


def export_edges(
    graph: Graph,
    filename: str
):
    """
    Export every physical road segment once.

    Columns:
        source
        destination
        road_id
        distance
    """

    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    edges = graph.get_all_edges()

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "source",
            "destination",
            "road_id",
            "distance"
        ])

        for edge in edges:

            writer.writerow([
                edge.source,
                edge.destination,
                edge.road_id,
                edge.distance
            ])

    print(
        f"Edges exported: {len(edges)}"
    )


def export_road_status(
    graph: Graph,
    filename: str
):
    """
    Export the current status of every road.

    This file will later be updated by the
    Flood Hazard Engine.

    Columns:
        road_id
        status
    """

    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    roads = {}

    for edge in graph.get_all_edges():

        if edge.road_id not in roads:

            roads[edge.road_id] = edge.status

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "road_id",
            "status"
        ])

        for road_id, status in roads.items():

            writer.writerow([
                road_id,
                status
            ])

    print(
        f"Road statuses exported: {len(roads)}"
    )


def export_graph(
    graph: Graph,
    output_directory: str
):
    """
    Export the complete processed road graph.

    Files created:

        road_nodes.csv
        road_edges.csv
        road_status.csv
    """

    output_path = Path(output_directory)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("==========================================")
    print(" EXPORTING PROCESSED CHENNAI ROAD GRAPH")
    print("==========================================")
    print()

    nodes_file = (
        output_path / "road_nodes.csv"
    )

    edges_file = (
        output_path / "road_edges.csv"
    )

    status_file = (
        output_path / "road_status.csv"
    )

    export_nodes(
        graph,
        str(nodes_file)
    )

    export_edges(
        graph,
        str(edges_file)
    )

    export_road_status(
        graph,
        str(status_file)
    )

    print()
    print("==========================================")
    print(" GRAPH EXPORT COMPLETE")
    print("==========================================")
    print()
    print(f"Output directory: {output_path}")
    print(f"Nodes file      : {nodes_file}")
    print(f"Edges file      : {edges_file}")
    print(f"Status file     : {status_file}")
    print()