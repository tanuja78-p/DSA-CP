from src.m3.evacuee import EvacueeGroup
from src.m3.evacuation_queue import EvacuationQueue


def test_evacuation_queue():
    print("=" * 60)
    print("EVACUATION QUEUE TEST")
    print("=" * 60)

    queue = EvacuationQueue()

    group1 = EvacueeGroup(
        group_id="G1",
        people_count=50,
        source="N1",
        priority=1,
        destination="S1",
        backup_shelter="S2",
        route=["N1", "N2", "S1"],
    )

    group2 = EvacueeGroup(
        group_id="G2",
        people_count=30,
        source="N3",
        priority=2,
        destination="S2",
        backup_shelter="S3",
        route=["N3", "N4", "S2"],
    )

    # Test initial status
    assert group1.status == "WAITING"
    assert group2.status == "WAITING"

    print("PASS: EvacueeGroup")

    # Add groups to queue
    queue.enqueue(group1)
    queue.enqueue(group2)

    assert queue.size() == 2

    print("PASS: Enqueue")

    # Check first group
    first = queue.peek()

    assert first is not None
    assert first.group_id == "G1"
    assert first.status == "WAITING"

    print("PASS: Peek")

    # Remove first group
    first = queue.dequeue()

    assert first.group_id == "G1"
    assert first.status == "ON_ROUTE"

    print("PASS: Dequeue + ON_ROUTE")

    # Mark first group as arrived
    queue.mark_arrived(first)

    assert first.status == "ARRIVED"

    print("PASS: ARRIVED status")

    # Process second group
    second = queue.dequeue()

    assert second.group_id == "G2"
    assert second.status == "ON_ROUTE"

    print("PASS: Second group")

    # Queue should now be empty
    assert queue.is_empty()
    assert queue.size() == 0

    print("PASS: Queue empty")

    print("=" * 60)
    print("ALL EVACUATION QUEUE TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_evacuation_queue()