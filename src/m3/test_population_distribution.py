from src.m3.population_distribution import PopulationDistributor


def test_population_distribution():

    print("=" * 60)
    print("POPULATION DISTRIBUTION TEST")
    print("=" * 60)

    distributor = PopulationDistributor()

    routes = [
        {
            "route_id": "R1",
            "capacity": 200
        },
        {
            "route_id": "R2",
            "capacity": 180
        },
        {
            "route_id": "R3",
            "capacity": 250
        }
    ]

    total_people = 500

    allocations = distributor.distribute(
        total_people,
        routes
    )

    # Route 1
    assert allocations[0]["route_id"] == "R1"
    assert allocations[0]["assigned"] == 200

    # Route 2
    assert allocations[1]["route_id"] == "R2"
    assert allocations[1]["assigned"] == 180

    # Route 3
    assert allocations[2]["route_id"] == "R3"
    assert allocations[2]["assigned"] == 120

    print("PASS: Population distribution")

    # Total assigned
    total_assigned = sum(
        item["assigned"]
        for item in allocations
    )

    assert total_assigned == 500

    print("PASS: Total population assigned")

    # No one left unassigned
    unassigned = distributor.get_unassigned_people(
        total_people,
        allocations
    )

    assert unassigned == 0

    print("PASS: No unassigned population")

    # Full distribution check
    assert distributor.is_fully_distributed(
        total_people,
        allocations
    )

    print("PASS: Fully distributed")

    print("=" * 60)
    print("ALL POPULATION DISTRIBUTION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_population_distribution()