from src.m3.shelter import Shelter
from src.m3.hash_map import ShelterHashMap
from src.m3.bst import ShelterBST
from src.m3.priority_queue import ShelterPriorityQueue
from src.m3.shelter_manager import ShelterManager
from src.m3.resource import Resource
from src.m3.resource_manager import ResourceManager


# ============================================================
# TEST 1: SHELTER MODEL
# ============================================================

def test_shelter():
    shelter = Shelter(
        shelter_id="S1",
        name="Test Shelter",
        latitude=13.0,
        longitude=80.0,
        capacity=500,
        occupied=100,
    )

    assert shelter.available_capacity == 400
    assert shelter.occupancy_percentage == 20.0
    assert shelter.is_available()

    shelter.add_occupants(50)

    assert shelter.occupied == 150
    assert shelter.available_capacity == 350

    shelter.remove_occupants(20)

    assert shelter.occupied == 130
    assert shelter.available_capacity == 370

    print("PASS: Shelter model")


# ============================================================
# TEST 2: CUSTOM HASH MAP
# ============================================================

def test_hash_map():
    hash_map = ShelterHashMap()

    shelter1 = Shelter(
        shelter_id="S1",
        name="Shelter 1",
        latitude=13.0,
        longitude=80.0,
        capacity=500,
        occupied=100,
    )

    shelter2 = Shelter(
        shelter_id="S2",
        name="Shelter 2",
        latitude=13.1,
        longitude=80.1,
        capacity=300,
        occupied=50,
    )

    hash_map.put("S1", shelter1)
    hash_map.put("S2", shelter2)

    assert hash_map.get("S1") == shelter1
    assert hash_map.get("S2") == shelter2
    assert hash_map.contains("S1")
    assert hash_map.contains("S2")
    assert len(hash_map) == 2

    hash_map.remove("S1")

    assert not hash_map.contains("S1")
    assert len(hash_map) == 1

    print("PASS: Custom HashMap")


# ============================================================
# TEST 3: BST
# ============================================================

def test_bst():
    bst = ShelterBST()

    shelters = [
        Shelter(
            shelter_id="S1",
            name="Shelter 1",
            latitude=13.0,
            longitude=80.0,
            capacity=500,
            occupied=100,
        ),
        Shelter(
            shelter_id="S2",
            name="Shelter 2",
            latitude=13.1,
            longitude=80.1,
            capacity=300,
            occupied=50,
        ),
        Shelter(
            shelter_id="S3",
            name="Shelter 3",
            latitude=13.2,
            longitude=80.2,
            capacity=700,
            occupied=100,
        ),
    ]

    for shelter in shelters:
        bst.insert(shelter)

    ordered = bst.inorder()

    assert len(ordered) == 3
    assert ordered[0].available_capacity <= ordered[1].available_capacity
    assert ordered[1].available_capacity <= ordered[2].available_capacity

    print("PASS: BST")


# ============================================================
# TEST 4: PRIORITY QUEUE
# ============================================================

def test_priority_queue():
    queue = ShelterPriorityQueue()

    queue.push(5, "Low Priority")
    queue.push(1, "High Priority")
    queue.push(3, "Medium Priority")

    first = queue.pop()
    second = queue.pop()
    third = queue.pop()

    assert first.shelter == "High Priority"
    assert second.shelter == "Medium Priority"
    assert third.shelter == "Low Priority"

    assert len(queue) == 0

    print("PASS: Priority Queue")


# ============================================================
# TEST 5: SHELTER MANAGER
# ============================================================

def test_manager():
    manager = ShelterManager()

    shelters = [
        Shelter(
            shelter_id="S1",
            name="Shelter 1",
            latitude=13,
            longitude=80,
            capacity=500,
            occupied=100,
        ),
        Shelter(
            shelter_id="S2",
            name="Shelter 2",
            latitude=13,
            longitude=80,
            capacity=200,
            occupied=190,
        ),
        Shelter(
            shelter_id="S3",
            name="Shelter 3",
            latitude=13,
            longitude=80,
            capacity=300,
            occupied=50,
        ),
    ]

    manager.add_shelters(shelters)

    distances = {
        "S1": 3.0,
        "S2": 1.0,
        "S3": 2.0,
    }

    result = manager.assign_shelter(
        distances,
        people=50,
    )

    assert result["success"]
    assert result["primary"] is not None
    assert result["backup"] is not None

    print("PASS: Shelter Manager")


# ============================================================
# TEST 6: RESOURCE MANAGER
# ============================================================

def test_resource_manager():
    manager = ResourceManager()

    resources = [
        Resource(
            resource_id="R1",
            name="Drinking Water",
            category="Water",
            quantity=1000,
            priority=5,
        ),
        Resource(
            resource_id="R2",
            name="Food Packets",
            category="Food",
            quantity=500,
            priority=4,
        ),
        Resource(
            resource_id="R3",
            name="First Aid Kits",
            category="Medical",
            quantity=100,
            priority=10,
        ),
    ]

    # Add resources
    manager.add_resources(resources)

    # Check resource storage
    assert manager.get_resource("R1") is not None
    assert manager.get_resource("R2") is not None
    assert manager.get_resource("R3") is not None

    # Add stock
    manager.add_stock("R1", 200)

    water = manager.get_resource("R1")

    assert water.quantity == 1200

    # Create first request
    request1 = manager.request_resource(
        resource_id="R1",
        quantity=100,
        requester="Shelter S1",
        priority=5,
    )

    # Create second request with higher priority
    request2 = manager.request_resource(
        resource_id="R3",
        quantity=20,
        requester="Shelter S2",
        priority=10,
    )

    assert request1["success"]
    assert request2["success"]

    assert manager.pending_request_count() == 2

    # Highest priority should be processed first
    result = manager.process_next_request()

    assert result["success"]
    assert result["resource_id"] == "R3"
    assert result["quantity_allocated"] == 20
    assert result["requester"] == "Shelter S2"

    # Process second request
    result = manager.process_next_request()

    assert result["success"]
    assert result["resource_id"] == "R1"
    assert result["quantity_allocated"] == 100

    # Check remaining quantities
    assert manager.get_resource("R3").quantity == 80
    assert manager.get_resource("R1").quantity == 1100

    print("PASS: Resource Manager")


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_all_tests():
    print("=" * 60)
    print("MEMBER 3 TEST SUITE")
    print("=" * 60)

    test_shelter()
    test_hash_map()
    test_bst()
    test_priority_queue()
    test_manager()
    test_resource_manager()

    print("=" * 60)
    print("ALL MEMBER 3 TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()