from m1.graph import Graph
from m1.flood_engine import (
    FloodHazard,
    SpatialIndex,
    apply_flood_hazards
)

from m2.astar import astar


def build_test_graph():
    """
    Build a small road network containing:
    
        Primary route:
        A -> B -> C -> D
        
        Alternate route:
        A -> E -> D
    """

    graph = Graph()

    # --------------------------------------------------
    # NODES
    # --------------------------------------------------

    graph.add_node(
        "A",
        13.0827,
        80.2707
    )

    graph.add_node(
        "B",
        13.0837,
        80.2717
    )

    graph.add_node(
        "C",
        13.0847,
        80.2727
    )

    graph.add_node(
        "D",
        13.0857,
        80.2737
    )

    graph.add_node(
        "E",
        13.0830,
        80.2740
    )

    # --------------------------------------------------
    # PRIMARY ROUTE
    # --------------------------------------------------

    graph.add_edge(
        "A",
        "B",
        "R1",
        100
    )

    graph.add_edge(
        "B",
        "C",
        "R2",
        100
    )

    graph.add_edge(
        "C",
        "D",
        "R3",
        100
    )

    # --------------------------------------------------
    # ALTERNATE ROUTE
    # --------------------------------------------------

    graph.add_edge(
        "A",
        "E",
        "R4",
        180
    )

    graph.add_edge(
        "E",
        "D",
        "R5",
        180
    )

    return graph


def print_route(title, result):

    print()
    print(title)
    print("------------------------------------------")

    if result["path"]:

        print(
            "Route:",
            " -> ".join(result["path"])
        )

    else:

        print("Route: No route")

    print(
        "Cost:",
        result["distance"]
    )

    print(
        "Reachable:",
        result["reachable"]
    )

    print(
        "Nodes explored:",
        result["nodes_explored"]
    )


def test_flood_routing_integration():

    print()
    print("==========================================")
    print(" M1 FLOOD -> M2 A* INTEGRATION TEST")
    print("==========================================")

    graph = build_test_graph()

    source = "A"
    destination = "D"

    # --------------------------------------------------
    # STEP 1
    # NORMAL ROUTING
    # --------------------------------------------------

    print("\nSTEP 1: NORMAL ROUTING")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "Primary evacuation route",
        result
    )

    # --------------------------------------------------
    # STEP 2
    # BUILD M1 SPATIAL INDEX
    # --------------------------------------------------

    print("\nSTEP 2: BUILDING M1 SPATIAL INDEX")

    spatial_index = SpatialIndex(
        cell_size=0.001
    )

    for node in graph.get_all_nodes():

        spatial_index.add_node(
            node
        )

    print("Spatial index created.")

    # --------------------------------------------------
    # STEP 3
    # CREATE M1 FLOOD HAZARD
    # --------------------------------------------------

    print("\nSTEP 3: FLOOD HAZARD DETECTED")

    # Flood hazard is placed at node B.
    hazard = FloodHazard(
        hazard_id="FLOOD-001",
        latitude=13.0837,
        longitude=80.2717,
        severity="HIGH",
        depth=4.0,
        source="TEST"
    )

    print(
        "Hazard ID:",
        hazard.hazard_id
    )

    print(
        "Severity:",
        hazard.severity
    )

    print(
        "Depth:",
        hazard.depth,
        "m"
    )

    # --------------------------------------------------
    # STEP 4
    # APPLY M1 FLOOD ENGINE
    # --------------------------------------------------

    print("\nSTEP 4: APPLYING FLOOD HAZARD")

    flood_result = apply_flood_hazards(
        graph,
        spatial_index,
        [hazard]
    )

    print(
        "Affected nodes:",
        flood_result["affected_nodes"]
    )

    print(
        "Restricted roads:",
        flood_result["RESTRICTED"]
    )

    print(
        "Blocked roads:",
        flood_result["BLOCKED"]
    )

    # --------------------------------------------------
    # STEP 5
    # CHECK ROAD STATUS
    # --------------------------------------------------

    print("\nSTEP 5: CHECKING UPDATED ROAD STATUS")

    print(
        "R1 status:",
        graph.get_road_status("R1")
    )

    print(
        "R2 status:",
        graph.get_road_status("R2")
    )

    print(
        "R3 status:",
        graph.get_road_status("R3")
    )

    # --------------------------------------------------
    # STEP 6
    # RUN M2 A* AGAIN
    # --------------------------------------------------

    print("\nSTEP 6: DYNAMIC REROUTING")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "New evacuation route",
        result
    )

    print()
    print("==========================================")
    print(" FLOOD -> ROUTING INTEGRATION COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_flood_routing_integration()