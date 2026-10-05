import time

from m1.build_road_graph import build_chennai_graph

from m2.hazard_registry import HazardRegistry
from m2.dijkstra import dijkstra
from m2.astar import astar


ROUTE_PAIRS = [
    (
        "80.26187_13.09112",
        "80.25126_13.09458"
    ),
    (
        "80.29048_13.09242",
        "80.29114_13.09609"
    ),
    (
        "80.29525_13.10277",
        "80.29518_13.10300"
    ),
    (
        "80.26187_13.09112",
        "80.29048_13.09242"
    ),
    (
        "80.25126_13.09458",
        "80.29114_13.09609"
    )
]


def run_dijkstra(graph, source, destination):

    start = time.perf_counter()

    result = dijkstra(
        graph,
        source,
        destination
    )

    elapsed = time.perf_counter() - start

    return result, elapsed


def run_astar(graph, source, destination):

    start = time.perf_counter()

    result = astar(
        graph,
        source,
        destination
    )

    elapsed = time.perf_counter() - start

    return result, elapsed


def calculate_node_reduction(
    dijkstra_nodes,
    astar_nodes
):

    if dijkstra_nodes == 0:
        return 0.0

    return (
        (dijkstra_nodes - astar_nodes)
        / dijkstra_nodes
    ) * 100.0


def calculate_time_change(
    dijkstra_time,
    astar_time
):

    if dijkstra_time == 0:
        return 0.0

    return (
        (astar_time - dijkstra_time)
        / dijkstra_time
    ) * 100.0


def main():

    print()
    print("==========================================")
    print(" MULTI-PAIR DIJKSTRA vs A* BENCHMARK")
    print("==========================================")

    print()
    print("Building Chennai graph...")

    graph = build_chennai_graph()

    print()
    print("Graph nodes:", graph.get_node_count())
    print("Graph edges:", graph.get_edge_count())

    results = []

    for index, (source, destination) in enumerate(
        ROUTE_PAIRS,
        start=1
    ):

        print()
        print("==========================================")
        print(f"ROUTE PAIR {index}")
        print("==========================================")

        print("Source:", source)
        print("Destination:", destination)

        if source not in graph.nodes:
            print("SKIPPED: source node not found.")
            continue

        if destination not in graph.nodes:
            print("SKIPPED: destination node not found.")
            continue

        # Fresh graph-status registry is not needed here because
        # this benchmark compares the existing Dijkstra and A*
        # implementations under normal SAFE conditions.

        dijkstra_result, dijkstra_time = run_dijkstra(
            graph,
            source,
            destination
        )

        astar_result, astar_time = run_astar(
            graph,
            source,
            destination
        )

        dijkstra_distance = dijkstra_result["distance"]
        astar_distance = astar_result["distance"]

        dijkstra_nodes = dijkstra_result["nodes_explored"]
        astar_nodes = astar_result["nodes_explored"]

        node_reduction = calculate_node_reduction(
            dijkstra_nodes,
            astar_nodes
        )

        time_change = calculate_time_change(
            dijkstra_time,
            astar_time
        )

        same_distance = (
            dijkstra_distance == astar_distance
        )

        print()
        print("Dijkstra:")
        print(
            "  Reachable:",
            dijkstra_result["reachable"]
        )
        print(
            "  Distance:",
            dijkstra_distance
        )
        print(
            "  Route nodes:",
            len(dijkstra_result["path"])
        )
        print(
            "  Nodes explored:",
            dijkstra_nodes
        )
        print(
            "  Time:",
            dijkstra_time
        )

        print()
        print("A*:")
        print(
            "  Reachable:",
            astar_result["reachable"]
        )
        print(
            "  Distance:",
            astar_distance
        )
        print(
            "  Route nodes:",
            len(astar_result["path"])
        )
        print(
            "  Nodes explored:",
            astar_nodes
        )
        print(
            "  Time:",
            astar_time
        )

        print()
        print(
            "Same route cost:",
            same_distance
        )

        print(
            "Node reduction:",
            node_reduction,
            "%"
        )

        print(
            "A* time change:",
            time_change,
            "%"
        )

        results.append(
            {
                "dijkstra_time": dijkstra_time,
                "astar_time": astar_time,
                "dijkstra_nodes": dijkstra_nodes,
                "astar_nodes": astar_nodes,
                "node_reduction": node_reduction,
                "time_change": time_change,
                "same_distance": same_distance
            }
        )

    print()
    print("==========================================")
    print(" OVERALL BENCHMARK SUMMARY")
    print("==========================================")

    if not results:
        print("No valid route pairs were tested.")
        return

    average_dijkstra_time = (
        sum(
            item["dijkstra_time"]
            for item in results
        )
        / len(results)
    )

    average_astar_time = (
        sum(
            item["astar_time"]
            for item in results
        )
        / len(results)
    )

    average_dijkstra_nodes = (
        sum(
            item["dijkstra_nodes"]
            for item in results
        )
        / len(results)
    )

    average_astar_nodes = (
        sum(
            item["astar_nodes"]
            for item in results
        )
        / len(results)
    )

    average_node_reduction = (
        sum(
            item["node_reduction"]
            for item in results
        )
        / len(results)
    )

    same_cost_count = sum(
        1
        for item in results
        if item["same_distance"]
    )

    print()
    print(
        "Valid route pairs:",
        len(results)
    )

    print(
        "Average Dijkstra time:",
        average_dijkstra_time
    )

    print(
        "Average A* time:",
        average_astar_time
    )

    print(
        "Average Dijkstra nodes explored:",
        average_dijkstra_nodes
    )

    print(
        "Average A* nodes explored:",
        average_astar_nodes
    )

    print(
        "Average node reduction:",
        average_node_reduction,
        "%"
    )

    print(
        "Pairs with same route cost:",
        same_cost_count,
        "/",
        len(results)
    )

    print()
    print("==========================================")
    print(" BENCHMARK COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    main()