import sys
from pathlib import Path

# Allow imports from src/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from fastapi.testclient import TestClient

from m1.api import app


client = TestClient(app)


def main():

    print()
    print("==========================================")
    print(" M1 - API TEST")
    print("==========================================")
    print()

    # -------------------------------------------------
    # Root endpoint
    # -------------------------------------------------

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["module"] == "M1"
    assert data["status"] == "running"

    print("Root endpoint: PASSED")

    # -------------------------------------------------
    # Graph summary
    # -------------------------------------------------

    response = client.get(
        "/api/m1/graph/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["nodes"] == 288442
    assert data["physical_roads"] == 287615
    print(
        "Graph summary endpoint: PASSED"
    )

    print(
        "Nodes:",
        data["nodes"]
    )

    print(
        "Physical roads:",
        data["physical_roads"]
    )

    print(
        "Road status:",
        data["road_status"]
    )

    # -------------------------------------------------
    # Road status
    # -------------------------------------------------

    response = client.get(
        "/api/m1/roads/status"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 33404

    print(
        "Road status endpoint: PASSED"
    )

    # -------------------------------------------------
    # Flood hazards
    # -------------------------------------------------

    response = client.get(
        "/api/m1/flood/hazards"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["hazard_type"] == "Urban Flood"
    assert data["count"] == 192

    print(
        "Flood hazards endpoint: PASSED"
    )

    print(
        "Flood hazards:",
        data["count"]
    )

    # -------------------------------------------------
    # Flood summary
    # -------------------------------------------------

    response = client.get(
        "/api/m1/flood/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["flood_hazards"] == 192

    print(
        "Flood summary endpoint: PASSED"
    )

    print(
        "Severity distribution:",
        data["severity_distribution"]
    )

    print(
        "Affected road status:",
        data["affected_road_status"]
    )

    # -------------------------------------------------
    # Final result
    # -------------------------------------------------

    print()
    print("==========================================")
    print(" M1 - API TEST PASSED")
    print("==========================================")
    print()


if __name__ == "__main__":
    main()