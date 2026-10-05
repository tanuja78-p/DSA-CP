from m1.graph import Graph
from m1.flood_engine import (
    FloodHazard,
    SpatialIndex,
    apply_flood_hazards
)

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
    graph.add_node("F", 13.0860, 80.2700)

    # Primary route
    graph.add_edge("A", "B", "R1", 100)
    graph.add_edge("B", "C", "R2", 100)
    graph.add_edge("C", "D", "R3", 100)

    # First alternate route
    graph.add_edge("A", "E", "R4", 180)
    graph.add_edge("E", "D", "R5", 180)

    # Second alternate route
    graph.add_edge("A", "F", "R6", 220)
    graph.add_edge("F", "D", "R7", 220)

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


def test_multi_hazard_routing():

    print()
    print("==========================================")
    print(" MULTI-HAZARD ROUTING INTEGRATION TEST")
    print("==========================================")

    graph = build_test_graph()

    source = "A"
    destination = "D"

    # ------------------------------------------------
    # STEP 1
    # ------------------------------------------------

    print("\nSTEP 1: INITIAL ROUTING")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "Initial evacuation route",
        result
    )

    # ------------------------------------------------
    # STEP 2
    # ------------------------------------------------

    print("\nSTEP 2: FLOOD HAZARD")

    spatial_index = SpatialIndex(
        cell_size=0.001
    )

    for node in graph.get_all_nodes():
        spatial_index.add_node(node)

    flood = FloodHazard(
        hazard_id="FLOOD-001",
        latitude=13.0837,
        longitude=80.2717,
        severity="HIGH",
        depth=4.0,
        source="TEST"
    )

    flood_result = apply_flood_hazards(
        graph,
        spatial_index,
        [flood]
    )

    print("Flood affected nodes:",
          flood_result["affected_nodes"])

    print("Flood blocked roads:",
          flood_result["BLOCKED"])

    # ------------------------------------------------
    # STEP 3
    # ------------------------------------------------

    print("\nSTEP 3: ROUTING AFTER FLOOD")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "Route after flood",
        result
    )

    # ------------------------------------------------
    # STEP 4
    # ------------------------------------------------

    print("\nSTEP 4: CYCLONE HAZARD")

    cyclone = CycloneHazard(
        latitude=13.0830,
        longitude=80.2740,
        wind_speed=130,
        pressure=950,
        cyclone_name="TEST-CYCLONE"
    )

    cyclone_severity = classify_cyclone_severity(
        cyclone.wind_speed
    )

    cyclone_status = cyclone_to_status(
        cyclone_severity
    )

    print("Cyclone:", cyclone.cyclone_name)
    print("Wind speed:", cyclone.wind_speed)
    print("Severity:", cyclone_severity)
    print("Road status:", cyclone_status)

    # ------------------------------------------------
    # STEP 5
    # ------------------------------------------------

    print("\nSTEP 5: APPLYING CYCLONE TO SAME GRAPH")

    cyclone_affected_nodes = find_affected_nodes(
        graph,
        cyclone,
        influence_radius=0.0006
    )

    print(
        "Cyclone affected nodes:",
        cyclone_affected_nodes
    )

    cyclone_result = apply_cyclone_hazard(
        graph,
        cyclone_affected_nodes,
        cyclone_status
    )

    print(
        "Cyclone updated roads:",
        cyclone_result["updated_roads"]
    )

    # ------------------------------------------------
    # STEP 6
    # ------------------------------------------------

    print("\nSTEP 6: FINAL ROAD STATUS")

    for road_id in [
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
        "R7"
    ]:
        print(
            road_id,
            "status:",
            graph.get_road_status(road_id)
        )

    # ------------------------------------------------
    # STEP 7
    # ------------------------------------------------

    print("\nSTEP 7: FINAL MULTI-HAZARD REROUTING")

    result = astar(
        graph,
        source,
        destination
    )

    print_route(
        "Final evacuation route",
        result
    )

    print()
    print("==========================================")
    print(" MULTI-HAZARD TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_multi_hazard_routing()