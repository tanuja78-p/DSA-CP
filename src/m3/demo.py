from .shelter import Shelter
from .shelter_manager import ShelterManager


def print_shelter(shelter):
    print(
        f"{shelter.shelter_id:<8}"
        f"{shelter.name:<25}"
        f"Capacity: {shelter.capacity:<5}"
        f"Occupied: {shelter.occupied:<5}"
        f"Available: {shelter.available_capacity:<5}"
        f"Status: {shelter.status}"
    )


def main():

    print("=" * 70)
    print("MEMBER 3 - SHELTER MANAGEMENT DEMO")
    print("=" * 70)

    manager = ShelterManager()

    # -------------------------------------------------
    # Shelter dataset
    # -------------------------------------------------

    shelters = [
        Shelter(
            shelter_id="S101",
            name="Chennai Central Shelter",
            latitude=13.0827,
            longitude=80.2707,
            capacity=500,
            occupied=200,
            status="SAFE",
            accessible=True,
        ),

        Shelter(
            shelter_id="S102",
            name="Marina Emergency Shelter",
            latitude=13.0475,
            longitude=80.2824,
            capacity=300,
            occupied=290,
            status="SAFE",
            accessible=True,
        ),

        Shelter(
            shelter_id="S103",
            name="Adyar Relief Center",
            latitude=13.0067,
            longitude=80.2206,
            capacity=700,
            occupied=100,
            status="SAFE",
            accessible=True,
        ),

        Shelter(
            shelter_id="S104",
            name="Velachery Emergency Shelter",
            latitude=12.9815,
            longitude=80.2180,
            capacity=450,
            occupied=150,
            status="CONGESTED",
            accessible=True,
        ),

        Shelter(
            shelter_id="S105",
            name="Tambaram Relief Center",
            latitude=12.9249,
            longitude=80.1000,
            capacity=600,
            occupied=50,
            status="SAFE",
            accessible=True,
        ),
    ]

    manager.add_shelters(shelters)

    # -------------------------------------------------
    # Show HashMap
    # -------------------------------------------------

    print("\n1. SHELTER HASHMAP")
    print("-" * 70)

    for shelter in manager.all_shelters():
        print_shelter(shelter)

    # -------------------------------------------------
    # Show BST
    # -------------------------------------------------

    print("\n2. BST - CAPACITY ORDER")
    print("-" * 70)

    for shelter in manager.get_capacity_order():
        print(
            f"{shelter.shelter_id} -> "
            f"{shelter.available_capacity} spaces available"
        )

    # -------------------------------------------------
    # Mock M2 distance information
    # -------------------------------------------------

    print("\n3. DISTANCES FROM MEMBER 2")
    print("-" * 70)

    distances = {
        "S101": 2.1,
        "S102": 1.0,
        "S103": 2.8,
        "S104": 3.2,
        "S105": 6.5,
    }

    for shelter_id, distance in distances.items():
        print(
            f"{shelter_id} -> {distance} km"
        )

    # -------------------------------------------------
    # Priority Queue ranking
    # -------------------------------------------------

    print("\n4. PRIORITY QUEUE RANKING")
    print("-" * 70)

    ranked = manager.rank_shelters(
        distances
    )

    for index, item in enumerate(
        ranked,
        start=1,
    ):
        shelter = item["shelter"]

        print(
            f"{index}. "
            f"{shelter.name} | "
            f"Distance: {item['distance']} km | "
            f"Available: {shelter.available_capacity} | "
            f"Score: {item['score']}"
        )

    # -------------------------------------------------
    # Assign primary + backup
    # -------------------------------------------------

    print("\n5. SHELTER ASSIGNMENT")
    print("-" * 70)

    result = manager.assign_shelter(
        distances,
        people=50,
    )

    print(
        f"Success: {result['success']}"
    )

    print(
        f"Primary: {result['primary']}"
    )

    print(
        f"Backup: {result['backup']}"
    )

    # -------------------------------------------------
    # Dynamic occupancy
    # -------------------------------------------------

    print("\n6. OCCUPANCY UPDATE")
    print("-" * 70)

    primary_id = result["primary"][
        "shelter_id"
    ]

    print(
        "After admitting 50 people:"
    )

    print(
        manager.get_shelter_load(
            primary_id
        )
    )

    # -------------------------------------------------
    # Simulate shelter becoming inaccessible
    # -------------------------------------------------

    print("\n7. DYNAMIC SHELTER FAILURE")
    print("-" * 70)

    manager.update_shelter_status(
        primary_id,
        status="BLOCKED",
        accessible=False,
    )

    print(
        f"{primary_id} is now BLOCKED."
    )

    new_result = manager.assign_shelter(
        distances,
        people=25,
    )

    print(
        f"New Primary: "
        f"{new_result['primary']}"
    )

    print(
        f"New Backup: "
        f"{new_result['backup']}"
    )

    print("\n" + "=" * 70)
    print("MEMBER 3 DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()