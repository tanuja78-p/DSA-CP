from m1.graph import Edge

from m2.routing_cost import get_edge_cost


def test_routing_cost():

    print("=== ROUTING COST TEST ===")

    safe_edge = Edge(
        source="A",
        destination="B",
        road_id="R1",
        distance=100
    )

    restricted_edge = Edge(
        source="A",
        destination="C",
        road_id="R2",
        distance=100,
        status="RESTRICTED"
    )

    blocked_edge = Edge(
        source="A",
        destination="D",
        road_id="R3",
        distance=100,
        status="BLOCKED"
    )

    print("SAFE cost:", get_edge_cost(safe_edge))
    print("RESTRICTED cost:", get_edge_cost(restricted_edge))
    print("BLOCKED cost:", get_edge_cost(blocked_edge))


if __name__ == "__main__":
    test_routing_cost()