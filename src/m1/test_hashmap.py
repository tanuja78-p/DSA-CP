from pathlib import Path
import sys


# Find the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Add the src directory to Python's import path.
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from m1.hashmap import HashMap


def main():

    print()
    print("==========================================")
    print(" M1 - HASHMAP TEST")
    print("==========================================")
    print()

    hashmap = HashMap()

    print("Adding road information...")

    hashmap.put(
        "ROAD_11196",
        {
            "road_id": "11196",
            "road_name": "Raghava Street",
            "status": "SAFE"
        }
    )

    hashmap.put(
        "ROAD_90_New45",
        {
            "road_id": "90_New45",
            "road_name": "Santham Colony 10th Street",
            "status": "SAFE"
        }
    )

    print(
        f"HashMap size: {len(hashmap)}"
    )

    print()
    print("Looking up ROAD_11196...")

    road = hashmap.get(
        "ROAD_11196"
    )

    print(
        f"Road ID   : {road['road_id']}"
    )

    print(
        f"Road Name : {road['road_name']}"
    )

    print(
        f"Status    : {road['status']}"
    )

    print()
    print("Checking key existence...")

    print(
        "ROAD_11196:",
        hashmap.contains("ROAD_11196")
    )

    print(
        "ROAD_UNKNOWN:",
        hashmap.contains("ROAD_UNKNOWN")
    )

    print()
    print("Updating road status...")

    hashmap.put(
        "ROAD_11196",
        {
            "road_id": "11196",
            "road_name": "Raghava Street",
            "status": "BLOCKED"
        }
    )

    updated_road = hashmap.get(
        "ROAD_11196"
    )

    print(
        f"Updated status: "
        f"{updated_road['status']}"
    )

    print()
    print("==========================================")
    print(" HASHMAP TEST COMPLETE")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()