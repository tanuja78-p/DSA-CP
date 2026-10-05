import time
from collections import deque

from m1.build_road_graph import build_chennai_graph

from m2.dijkstra import dijkstra


def select_far_test_nodes(graph, hop_distance=100):
    """
    Select two nodes that are approximately hop_distance
    graph edges apart using BFS.

    This is only used to create a meaningful benchmark pair.
    """

    source = next(iter(graph.adjacency))

    queue = deque([(source, 0)])
    visited = {source}

    while queue:

        current, depth = queue.popleft()

        if depth >= hop_distance:
            return source, current

        for edge in graph.get_active_neighbors(current):

            neighbor = edge.destination

            if neighbor in visited:
                continue

            visited.add(neighbor)

            queue.append(
                (neighbor, depth + 1)
            )

    raise RuntimeError(
        "Could not find a sufficiently distant test node."
    )


def benchmark_dijkstra():

    print()
    print("==========================================")
    print(" M2 - DIJKSTRA CHENNAI BENCHMARK")
    print("==========================================")

    print("\nBuilding Chennai graph...")

    graph = build_chennai_graph()

    print("\nSelecting benchmark nodes...")

    source, destination = select_far_test_nodes(
        graph,
        hop_distance=100
    )

    print("Source node      :", source)
    print("Destination node :", destination)

    print("\nRunning Dijkstra...")

    start_time = time.perf_counter()

    result = dijkstra(
        graph,
        source,
        destination
    )

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    )

    print()
    print("==========================================")
    print(" DIJKSTRA BENCHMARK RESULT")
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
    benchmark_dijkstra()