from src.m3.evacuation_manager import EvacuationManager


def test_route_ranking_and_feasibility():
    manager = EvacuationManager()

    routes = [
        {
            "route_id": "R1",
            "capacity": 100,
            "cost": 10,
            "congestion": 0.9,
            "traffic_flow": 80,
            "feasible": True,
        },
        {
            "route_id": "R2",
            "capacity": 150,
            "cost": 15,
            "congestion": 0.1,
            "traffic_flow": 20,
            "feasible": True,
        },
        {
            "route_id": "R3",
            "capacity": 200,
            "cost": 5,
            "congestion": 0.2,
            "traffic_flow": 10,
            "feasible": False,
        },
    ]

    ranked = manager.rank_routes(routes)

    assert len(ranked) == 2

    assert ranked[0]["route_id"] == "R2"
    assert ranked[1]["route_id"] == "R1"

    assert ranked[0]["score"] < ranked[1]["score"]

    print("PASS: Route ranking")
    print("PASS: Infeasible route removed")


def test_capacity_aware_route_distribution():
    manager = EvacuationManager()

    routes = [
        {
            "route_id": "R1",
            "capacity": 100,
            "cost": 10,
            "congestion": 0.9,
            "traffic_flow": 80,
            "feasible": True,
        },
        {
            "route_id": "R2",
            "capacity": 150,
            "cost": 15,
            "congestion": 0.1,
            "traffic_flow": 20,
            "feasible": True,
        },
        {
            "route_id": "R3",
            "capacity": 200,
            "cost": 5,
            "congestion": 0.2,
            "traffic_flow": 10,
            "feasible": False,
        },
    ]

    allocations = manager.distribute_population(
        200,
        routes
    )

    assert allocations[0]["route_id"] == "R2"
    assert allocations[0]["assigned"] == 150

    assert allocations[1]["route_id"] == "R1"
    assert allocations[1]["assigned"] == 50

    total_assigned = sum(
        item["assigned"]
        for item in allocations
    )

    assert total_assigned == 200

    print("PASS: Capacity-aware distribution")


def test_infeasible_routes_are_not_used():
    manager = EvacuationManager()

    routes = [
        {
            "route_id": "BLOCKED",
            "capacity": 500,
            "cost": 1,
            "congestion": 0.0,
            "traffic_flow": 0,
            "feasible": False,
        },
        {
            "route_id": "OPEN",
            "capacity": 100,
            "cost": 20,
            "congestion": 0.2,
            "traffic_flow": 10,
            "feasible": True,
        },
    ]

    allocations = manager.distribute_population(
        50,
        routes
    )

    assert len(allocations) == 1
    assert allocations[0]["route_id"] == "OPEN"
    assert allocations[0]["assigned"] == 50

    print("PASS: Infeasible routes excluded")


if __name__ == "__main__":
    print("=" * 60)
    print("ROUTE MANAGEMENT TEST")
    print("=" * 60)

    test_route_ranking_and_feasibility()
    test_capacity_aware_route_distribution()
    test_infeasible_routes_are_not_used()

    print("=" * 60)
    print("ALL ROUTE MANAGEMENT TESTS PASSED")
    print("=" * 60)