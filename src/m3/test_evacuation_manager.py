from src.m3.evacuee import EvacueeGroup
from src.m3.evacuation_manager import EvacuationManager
from src.m3.storm import SevereStorm


def test_evacuation_manager():

    print("=" * 60)
    print("EVACUATION MANAGER INTEGRATION TEST")
    print("=" * 60)

    manager = EvacuationManager()

    # --------------------------------------------------
    # Create evacuation groups
    # --------------------------------------------------

    group1 = EvacueeGroup(
        group_id="G1",
        people_count=100,
        source="N1",
        priority=1,
        destination="S1",
        backup_shelter="S2",
        route=["N1", "N2", "S1"],
    )

    group2 = EvacueeGroup(
        group_id="G2",
        people_count=80,
        source="N3",
        priority=2,
        destination="S2",
        backup_shelter="S3",
        route=["N3", "N4", "S2"],
    )

    # --------------------------------------------------
    # Add groups
    # --------------------------------------------------

    manager.add_group(group1)
    manager.add_group(group2)

    assert len(manager.get_all_groups()) == 2
    assert manager.queue.size() == 2

    print("PASS: Evacuation groups added")

    # --------------------------------------------------
    # Check initial status
    # --------------------------------------------------

    status = manager.get_status()

    assert status["total_groups"] == 2
    assert status["waiting"] == 2
    assert status["on_route"] == 0
    assert status["arrived"] == 0

    print("PASS: Initial evacuation status")

    # --------------------------------------------------
    # Process first group
    # --------------------------------------------------

    processed = manager.process_next_group()

    assert processed.group_id == "G1"
    assert processed.status == "ON_ROUTE"

    print("PASS: Group moved to ON_ROUTE")

    # --------------------------------------------------
    # Mark first group arrived
    # --------------------------------------------------

    arrived = manager.mark_group_arrived("G1")

    assert arrived.status == "ARRIVED"

    print("PASS: Group marked ARRIVED")

    # --------------------------------------------------
    # Population distribution
    # --------------------------------------------------

    routes = [
        {
            "route_id": "R1",
            "capacity": 100
        },
        {
            "route_id": "R2",
            "capacity": 150
        },
        {
            "route_id": "R3",
            "capacity": 100
        }
    ]

    allocations = manager.distribute_population(
        300,
        routes
    )

    assigned = sum(
        item["assigned"]
        for item in allocations
    )

    assert assigned == 300

    print("PASS: Population distribution")

    # --------------------------------------------------
    # Severe storm
    # --------------------------------------------------

    storm = SevereStorm(
        wind_speed=100,
        rainfall=100,
        visibility=2,
        affected_radius=15,
        severity="HIGH",
    )

    storm_effects = manager.simulate_storm_impact(
        storm,
        base_travel_time=30
    )

    assert storm_effects["hazard_risk"] > 0
    assert storm_effects["travel_delay_minutes"] > 30

    print("PASS: Storm integration")

    # --------------------------------------------------
    # Complete simulation
    # --------------------------------------------------

    simulation = manager.simulate_evacuation(
        total_people=300,
        routes=routes,
        storm=storm,
        base_travel_time=30,
    )

    assert simulation["total_people"] == 300
    assert simulation["fully_distributed"] is True
    assert simulation["unassigned_people"] == 0
    assert simulation["storm_effects"] is not None

    print("PASS: Complete evacuation simulation")

    print("=" * 60)
    print("ALL EVACUATION MANAGER TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_evacuation_manager()