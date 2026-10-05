import time

from m1.build_road_graph import build_chennai_graph

from m2.dijkstra import dijkstra
from m2.astar import astar


SOURCE = "80.26187_13.09112"
DESTINATION = "80.25126_13.09458"


def compare_routing():

    print()
    print("==========================================")
    print(" DIJKSTRA VS A* COMPARISON")
    print("==========================================")

    print("\nBuilding Chennai graph once...")

    graph = build_chennai_graph()

    print("\nSource node      :", SOURCE)
    print("Destination node :", DESTINATION)

    # --------------------------------------------------
    # DIJKSTRA
    # --------------------------------------------------

    print("\nRunning Dijkstra...")

    start = time.perf_counter()

    dijkstra_result = dijkstra(
        graph,
        SOURCE,
        DESTINATION
    )

    dijkstra_time = (
        time.perf_counter() - start
    )

    # --------------------------------------------------
    # A*
    # --------------------------------------------------

    print("Running A*...")

    start = time.perf_counter()

    astar_result = astar(
        graph,
        SOURCE,
        DESTINATION
    )

    astar_time = (
        time.perf_counter() - start
    )

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    print()
    print("==========================================")
    print(" COMPARISON RESULTS")
    print("==========================================")

    print("\nDijkstra")
    print("------------------------------------------")
    print(
        "Reachable       :",
        dijkstra_result["reachable"]
    )
    print(
        "Distance        :",
        dijkstra_result["distance"],
        "meters"
    )
    print(
        "Route nodes     :",
        len(dijkstra_result["path"])
    )
    print(
        "Nodes explored  :",
        dijkstra_result["nodes_explored"]
    )
    print(
        "Execution time  :",
        dijkstra_time,
        "seconds"
    )

    print("\nA*")
    print("------------------------------------------")
    print(
        "Reachable       :",
        astar_result["reachable"]
    )
    print(
        "Distance        :",
        astar_result["distance"],
        "meters"
    )
    print(
        "Route nodes     :",
        len(astar_result["path"])
    )
    print(
        "Nodes explored  :",
        astar_result["nodes_explored"]
    )
    print(
        "Execution time  :",
        astar_time,
        "seconds"
    )

    # --------------------------------------------------
    # CORRECTNESS CHECK
    # --------------------------------------------------

    distance_difference = abs(
        dijkstra_result["distance"]
        - astar_result["distance"]
    )

    same_route_cost = (
        distance_difference < 0.000001
    )

    # --------------------------------------------------
    # NODE REDUCTION
    # --------------------------------------------------

    if dijkstra_result["nodes_explored"] > 0:

        node_reduction = (
            (
                dijkstra_result["nodes_explored"]
                - astar_result["nodes_explored"]
            )
            /
            dijkstra_result["nodes_explored"]
        ) * 100

    else:

        node_reduction = 0.0

    # --------------------------------------------------
    # TIME COMPARISON
    # --------------------------------------------------

    if dijkstra_time > 0:

        time_change = (
            (
                astar_time
                - dijkstra_time
            )
            /
            dijkstra_time
        ) * 100

    else:

        time_change = 0.0

    print()
    print("==========================================")
    print(" ANALYSIS")
    print("==========================================")

    print(
        "Same route cost:",
        same_route_cost
    )

    print(
        "Node reduction :",
        node_reduction,
        "%"
    )

    print(
        "A* time change :",
        time_change,
        "%"
    )

    print("==========================================")


if __name__ == "__main__":
    compare_routing()