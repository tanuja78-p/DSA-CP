from pathlib import Path
import csv

from m1.graph import Graph


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

ROAD_NODES_FILE = PROCESSED_DATA / "road_nodes.csv"
ROAD_EDGES_FILE = PROCESSED_DATA / "road_edges.csv"
ROAD_STATUS_FILE = PROCESSED_DATA / "flood_road_status.csv"


def load_chennai_graph():
    graph = Graph()

    # ---------------------------------------------
    # Load nodes
    # ---------------------------------------------

    with open(
        ROAD_NODES_FILE,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            graph.add_node(
                row["node_id"],
                float(row["latitude"]),
                float(row["longitude"])
            )

    # ---------------------------------------------
    # Load road edges
    # ---------------------------------------------

    with open(
        ROAD_EDGES_FILE,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            graph.add_edge(
                row["source"],
                row["destination"],
                row["road_id"],
                float(row["distance"])
            )

    # ---------------------------------------------
    # Load road statuses into a dictionary
    # ---------------------------------------------

    road_statuses = {}

    if ROAD_STATUS_FILE.exists():

        with open(
            ROAD_STATUS_FILE,
            "r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                road_statuses[row["road_id"]] = (
                    row["status"].upper()
                )

    # ---------------------------------------------
    # Apply statuses in ONE graph traversal
    # ---------------------------------------------

    for edges in graph.adjacency.values():

        for edge in edges:

            status = road_statuses.get(
                edge.road_id
            )

            if status is not None:
                edge.status = status

    return graph