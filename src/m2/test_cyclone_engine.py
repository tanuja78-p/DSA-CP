from m1.graph import Graph

from m2.cyclone_engine import (
    CycloneHazard,
    classify_cyclone_severity,
    cyclone_to_status,
    find_affected_nodes
)


def build_test_graph():

    graph = Graph()

    graph.add_node("A", 13.0827, 80.2707)
    graph.add_node("B", 13.0837, 80.2717)
    graph.add_node("C", 13.0847, 80.2727)
    graph.add_node("D", 13.0857, 80.2737)

    return graph


def test_cyclone_engine():

    print()
    print("==========================================")
    print(" M2 CYCLONE HAZARD ENGINE TEST")
    print("==========================================")

    print("\nSTEP 1: BUILDING TEST ROAD GRAPH")

    graph = build_test_graph()

    print("Nodes:", graph.get_node_count())

    print("\nSTEP 2: CREATING CYCLONE HAZARD")

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

    print("\nSTEP 3: CLASSIFYING CYCLONE SEVERITY")

    severity = classify_cyclone_severity(
        cyclone.wind_speed
    )

    print("Severity:", severity)

    print("\nSTEP 4: CONVERTING SEVERITY TO ROAD STATUS")

    status = cyclone_to_status(severity)

    print("Road status:", status)

    print("\nSTEP 5: FINDING AFFECTED ROAD NODES")

    affected_nodes = find_affected_nodes(
        graph,
        cyclone,
        influence_radius=0.0015
    )

    print("Affected nodes:", affected_nodes)

    print()
    print("==========================================")
    print(" CYCLONE ENGINE TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_engine()