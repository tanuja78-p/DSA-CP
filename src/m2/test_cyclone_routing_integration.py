from m1.graph import Graph

from m2.astar import astar
from m2.cyclone_engine import (
    CycloneHazard,
    classify_cyclone_severity,
    cyclone_to_status,
    find_affected_nodes
)
from m2.cyclone_graph_update import apply_cyclone_hazard


def build_test_graph():

    graph = Graph()

    graph.add_node("A", 13.0827, 80.2707)
    graph.add_node("B", 13.0837, 80.2717)
    graph.add_node("C", 13.0847, 80.2727)
    graph.add_node("D", 13.0857, 80.2737)
    graph.add_node("E", 13.0830, 80.2740)

    # Primary route
    graph.add_edge("A", "B", "R1", 100)
    graph.add_edge("B", "C", "R2", 100)
    graph.add_edge("C", "D", "R3", 100)

    # Alternate route
    graph.add_edge("A", "E", "R4", 180)
    graph.add_edge("E", "D", "R5", 180)

    return graph


def print_route(title, result):

    print()
    print(title)
    print("------------------------------------------")

    if result["path"]:
        print("Route:", " -> ".join(result["path"]))
    else:
        print("Route: No route")

    print("Cost:", result["distance"])
    print("Reachable:", result["reachable"])
    print("Nodes explored:", result["nodes_explored"])


def test_cyclone_routing_integration():

    print()
    print("==========================================")
    print(" CYCLONE -> GRAPH -> A* INTEGRATION TEST")
    print("==========================================")

    graph = build_test_graph()

    source = "A"
    destination = "D"

    # ------------------------------------------------
    # STEP 1
    # ------------------------------------------------

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

    # ------------------------------------------------
    # STEP 2
    # ------------------------------------------------

    print("\nSTEP 2: CYCLONE DETECTED")

    cyclone = CycloneHazard(
        latitude=13.0837,
        longitude=80.2717,
        wind_speed=130,
        pressure=950,
        cyclone_name="TEST-CYCLONE"
    )

    print("Cyclone:", cyclone.cyclone_name)
    print("Wind speed:", cyclone.wind_speed)
    print("Pressure:", cyclone.pressure)

    # ------------------------------------------------
    # STEP 3
    # ------------------------------------------------

    print("\nSTEP 3: CLASSIFYING CYCLONE")

    severity = classify_cyclone_severity(
        cyclone.wind_speed
    )

    status = cyclone_to_status(
        severity
    )

    print("Severity:", severity)
    print("Road status:", status)

    # ------------------------------------------------
    # STEP 4
    # ------------------------------------------------

    print("\nSTEP 4: FINDING AFFECTED NODES")

    affected_nodes = find_affected_nodes(
        graph,
        cyclone,
        influence_radius=0.0006
    )

    print("Affected nodes:", affected_nodes)

    # ------------------------------------------------
    # STEP 5
    # ------------------------------------------------

    print("\nSTEP 5: UPDATING ROAD GRAPH")

    update_result = apply_cyclone_hazard(
        graph,
        affected_nodes,
        status
    )

    print(
        "Updated roads:",
        update_result["updated_roads"]
    )

    # ------------------------------------------------
    # STEP 6
    # ------------------------------------------------

    print("\nSTEP 6: CHECKING ROAD STATUS")

    for road_id in update_result["updated_roads"]:
        print(
            road_id,
            "status:",
            graph.get_road_status(road_id)
        )

    # ------------------------------------------------
    # STEP 7
    # ------------------------------------------------

    print("\nSTEP 7: DYNAMIC A* REROUTING")

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
    print(" CYCLONE ROUTING INTEGRATION COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_routing_integration()