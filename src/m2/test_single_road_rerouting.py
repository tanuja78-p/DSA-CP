from m1.build_road_graph import build_chennai_graph

from m2.astar import astar


TARGET_ROAD_ID = "10529"


def get_route_road_ids(graph, path):

    road_ids = []

    for index in range(len(path) - 1):

        current_node = path[index]
        next_node = path[index + 1]

        for edge in graph.get_neighbors(
            current_node
        ):

            if edge.destination == next_node:

                road_ids.append(
                    edge.road_id
                )

                break

    return road_ids


def get_connection_nodes(
    graph,
    road_id
):

    connection_nodes = []

    for node_id in graph.nodes:

        for edge in graph.get_neighbors(
            node_id
        ):

            if edge.road_id == road_id:

                for neighbor in graph.get_neighbors(
                    node_id
                ):

                    if neighbor.road_id != road_id:

                        connection_nodes.append(
                            (
                                node_id,
                                neighbor.road_id,
                                neighbor.destination
                            )
                        )

    return connection_nodes


def test_single_road_rerouting():

    print()
    print("==========================================")
    print(" SINGLE ROAD REROUTING TEST")
    print("==========================================")

    # ------------------------------------------
    # STEP 1
    # ------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # ------------------------------------------
    # STEP 2
    # ------------------------------------------

    print(
        "\nSTEP 2: FINDING ROAD CONNECTIONS"
    )

    connections = get_connection_nodes(
        graph,
        TARGET_ROAD_ID
    )

    print(
        "Road:",
        TARGET_ROAD_ID
    )

    print(
        "Connection points:",
        len(connections)
    )

    for connection in connections[:20]:

        print(
            "Node:",
            connection[0],
            "| Road:",
            connection[1],
            "| Next:",
            connection[2]
        )

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print(
        "\nSTEP 3: TESTING CONNECTION PAIRS"
    )

    # Use distinct connection nodes.
    candidate_nodes = []

    for node_id, road_id, destination in connections:

        if node_id not in candidate_nodes:

            candidate_nodes.append(
                node_id
            )

    print(
        "Candidate nodes:",
        len(candidate_nodes)
    )

    found = False

    selected_source = None
    selected_destination = None
    selected_before = None
    selected_after = None

    for i in range(
        len(candidate_nodes)
    ):

        for j in range(
            i + 1,
            len(candidate_nodes)
        ):

            source = candidate_nodes[i]
            destination = candidate_nodes[j]

            if source == destination:
                continue

            # ----------------------------------
            # BEFORE BLOCKAGE
            # ----------------------------------

            before = astar(
                graph,
                source,
                destination
            )

            if not before["reachable"]:
                continue

            before_roads = get_route_road_ids(
                graph,
                before["path"]
            )

            if TARGET_ROAD_ID not in before_roads:
                continue

            # ----------------------------------
            # BLOCK ROAD
            # ----------------------------------

            graph.update_road_status(
                TARGET_ROAD_ID,
                "BLOCKED"
            )

            # ----------------------------------
            # AFTER BLOCKAGE
            # ----------------------------------

            after = astar(
                graph,
                source,
                destination
            )

            # ----------------------------------
            # RESTORE ROAD
            # ----------------------------------

            graph.update_road_status(
                TARGET_ROAD_ID,
                "SAFE"
            )

            if not after["reachable"]:
                continue

            after_roads = get_route_road_ids(
                graph,
                after["path"]
            )

            if TARGET_ROAD_ID in after_roads:
                continue

            if before["path"] == after["path"]:
                continue

            selected_source = source
            selected_destination = destination
            selected_before = before
            selected_after = after

            found = True

            break

        if found:
            break

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    if not found:

        print()
        print(
            "NO ALTERNATE ROUTE FOUND"
        )

        print(
            "Road 10529 may not provide a usable"
        )

        print(
            "alternate route for these connection"
        )

        print(
            "nodes."
        )

        return

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print()
    print(
        "=========================================="
    )

    print(
        " SUCCESSFUL REROUTING FOUND"
    )

    print(
        "=========================================="
    )

    print(
        "Source:",
        selected_source
    )

    print(
        "Destination:",
        selected_destination
    )

    print()
    print(
        "BEFORE BLOCKAGE"
    )

    print(
        "Reachable:",
        selected_before["reachable"]
    )

    print(
        "Distance:",
        selected_before["distance"],
        "meters"
    )

    print(
        "Nodes:",
        len(
            selected_before["path"]
        )
    )

    print(
        "Explored:",
        selected_before["nodes_explored"]
    )

    print(
        "Roads:",
        get_route_road_ids(
            graph,
            selected_before["path"]
        )
    )

    print()
    print(
        "AFTER BLOCKAGE"
    )

    print(
        "Reachable:",
        selected_after["reachable"]
    )

    print(
        "Distance:",
        selected_after["distance"],
        "meters"
    )

    print(
        "Nodes:",
        len(
            selected_after["path"]
        )
    )

    print(
        "Explored:",
        selected_after["nodes_explored"]
    )

    print(
        "Roads:",
        get_route_road_ids(
            graph,
            selected_after["path"]
        )
    )

    print()
    print(
        "Additional distance:",
        selected_after["distance"]
        - selected_before["distance"],
        "meters"
    )

    print(
        "Route changed:",
        selected_before["path"]
        != selected_after["path"]
    )

    print(
        "=========================================="
    )


if __name__ == "__main__":
    test_single_road_rerouting()