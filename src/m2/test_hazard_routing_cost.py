from m1.graph import Graph

from m2.hazard_registry import HazardRegistry
from m2.hazard_routing_cost import (
    get_effective_edge_status,
    get_hazard_edge_cost
)


def build_test_graph():

    graph = Graph()

    graph.add_node(
        "A",
        13.0000,
        80.0000
    )

    graph.add_node(
        "B",
        13.0010,
        80.0000
    )

    graph.add_edge(
        "A",
        "B",
        "R1",
        100
    )

    return graph


def test_hazard_routing_cost():

    print()
    print("==========================================")
    print(" MULTI-HAZARD ROUTING COST TEST")
    print("==========================================")

    graph = build_test_graph()

    registry = HazardRegistry()

    edge = graph.get_neighbors("A")[0]

    # --------------------------------------------------
    # TEST 1: SAFE
    # --------------------------------------------------

    print("\nTEST 1: SAFE")

    status = get_effective_edge_status(
        edge,
        registry
    )

    cost = get_hazard_edge_cost(
        edge,
        registry
    )

    print(
        "Effective status:",
        status
    )

    print(
        "Cost:",
        cost
    )

    # --------------------------------------------------
    # TEST 2: FLOOD RESTRICTED
    # --------------------------------------------------

    print("\nTEST 2: FLOOD RESTRICTED")

    registry.set_flood_status(
        "R1",
        "RESTRICTED"
    )

    status = get_effective_edge_status(
        edge,
        registry
    )

    cost = get_hazard_edge_cost(
        edge,
        registry
    )

    print(
        "Effective status:",
        status
    )

    print(
        "Cost:",
        cost
    )

    # --------------------------------------------------
    # TEST 3: CYCLONE BLOCKED
    # --------------------------------------------------

    print("\nTEST 3: CYCLONE BLOCKED")

    registry.set_cyclone_status(
        "R1",
        "BLOCKED"
    )

    status = get_effective_edge_status(
        edge,
        registry
    )

    cost = get_hazard_edge_cost(
        edge,
        registry
    )

    print(
        "Effective status:",
        status
    )

    print(
        "Cost:",
        cost
    )

    # --------------------------------------------------
    # TEST 4: CYCLONE LEAVES
    # --------------------------------------------------

    print("\nTEST 4: CYCLONE LEAVES")

    registry.set_cyclone_status(
        "R1",
        "SAFE"
    )

    status = get_effective_edge_status(
        edge,
        registry
    )

    cost = get_hazard_edge_cost(
        edge,
        registry
    )

    print(
        "Effective status:",
        status
    )

    print(
        "Cost:",
        cost
    )

    # --------------------------------------------------
    # TEST 5: FLOOD ALSO LEAVES
    # --------------------------------------------------

    print("\nTEST 5: FLOOD LEAVES")

    registry.set_flood_status(
        "R1",
        "SAFE"
    )

    status = get_effective_edge_status(
        edge,
        registry
    )

    cost = get_hazard_edge_cost(
        edge,
        registry
    )

    print(
        "Effective status:",
        status
    )

    print(
        "Cost:",
        cost
    )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_hazard_routing_cost()