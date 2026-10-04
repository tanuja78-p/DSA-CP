from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from m1.graph import Graph

from m1.graph_update import (
    update_roads_from_flood_nodes,
    count_road_statuses,
    recover_roads
)


def build_test_graph():

    graph = Graph()

    graph.add_node(
        "NODE_A",
        13.0000,
        80.2000
    )

    graph.add_node(
        "NODE_B",
        13.0010,
        80.2010
    )

    graph.add_node(
        "NODE_C",
        13.0020,
        80.2020
    )

    graph.add_node(
        "NODE_D",
        13.0030,
        80.2030
    )

    graph.add_edge(
        source="NODE_A",
        destination="NODE_B",
        road_id="ROAD_001",
        distance=100
    )

    graph.add_edge(
        source="NODE_B",
        destination="NODE_C",
        road_id="ROAD_002",
        distance=150
    )

    graph.add_edge(
        source="NODE_C",
        destination="NODE_D",
        road_id="ROAD_003",
        distance=200
    )

    return graph


def main():

    print()
    print("==========================================")
    print(" M1 - DYNAMIC GRAPH UPDATE TEST")
    print("==========================================")
    print()

    graph = build_test_graph()

    print("Initial road status:")

    print(
        count_road_statuses(graph)
    )

    print()

    print(
        "Applying flood impact to NODE_B..."
    )

    result = update_roads_from_flood_nodes(
        graph,
        ["NODE_B"],
        status="BLOCKED"
    )

    print(
        f"Nodes processed : {result['nodes_processed']}"
    )

    print(
        f"Roads updated   : {result['roads_updated']}"
    )

    print()

    print("Road status after flood:")

    after_flood = count_road_statuses(
        graph
    )

    print(after_flood)

    print()

    assert after_flood["BLOCKED"] == 2

    assert after_flood["SAFE"] == 1

    print(
        "Flood road update verified."
    )

    print()

    print(
        "Recovering affected roads..."
    )

    recovered = recover_roads(
        graph,
        [
            "ROAD_001",
            "ROAD_002"
        ]
    )

    print(
        f"Roads recovered: {recovered}"
    )

    print()

    after_recovery = count_road_statuses(
        graph
    )

    print(
        "Road status after recovery:"
    )

    print(after_recovery)

    assert after_recovery["SAFE"] == 3

    assert after_recovery["BLOCKED"] == 0

    print()

    print("==========================================")
    print(" DYNAMIC GRAPH UPDATE TEST PASSED")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()