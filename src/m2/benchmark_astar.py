import time

from m1.build_road_graph import build_chennai_graph

from m2.astar import astar


SOURCE = "80.26187_13.09112"
DESTINATION = "80.25126_13.09458"


def benchmark_astar():

    print()
    print("==========================================")
    print(" M2 - A* CHENNAI BENCHMARK")
    print("==========================================")

    print("\nBuilding Chennai graph...")

    graph = build_chennai_graph()

    print("\nUsing same benchmark pair as Dijkstra...")

    print("Source node      :", SOURCE)
    print("Destination node :", DESTINATION)

    if SOURCE not in graph.nodes:
        raise RuntimeError(
            f"Source node not found: {SOURCE}"
        )

    if DESTINATION not in graph.nodes:
        raise RuntimeError(
            f"Destination node not found: {DESTINATION}"
        )

    print("\nRunning A*...")

    start_time = time.perf_counter()

    result = astar(
        graph,
        SOURCE,
        DESTINATION
    )

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    )

    print()
    print("==========================================")
    print(" A* BENCHMARK RESULT")
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
        "Route node count :",
        len(result["path"])
    )

    print(
        "Nodes explored   :",
        result["nodes_explored"]
    )

    print(
        "Execution time   :",
        execution_time,
        "seconds"
    )

    print("==========================================")


if __name__ == "__main__":
    benchmark_astar()