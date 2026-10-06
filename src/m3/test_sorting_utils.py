from src.m3.sorting_utils import SortingUtils


def test_shelter_sorting():

    shelters = [
        {
            "shelter_id": "S1",
            "score": 8.5
        },
        {
            "shelter_id": "S2",
            "score": 3.2
        },
        {
            "shelter_id": "S3",
            "score": 5.7
        }
    ]

    result = SortingUtils.sort_shelters(shelters)

    assert result[0]["shelter_id"] == "S2"
    assert result[1]["shelter_id"] == "S3"
    assert result[2]["shelter_id"] == "S1"

    print("PASS: Shelter sorting")


def test_route_sorting():

    routes = [
        {
            "route_id": "R1",
            "cost": 25
        },
        {
            "route_id": "R2",
            "cost": 10
        },
        {
            "route_id": "R3",
            "cost": 18
        }
    ]

    result = SortingUtils.sort_routes(routes)

    assert result[0]["route_id"] == "R2"
    assert result[1]["route_id"] == "R3"
    assert result[2]["route_id"] == "R1"

    print("PASS: Route sorting")


def test_destination_sorting():

    destinations = [
        {
            "destination": "S1",
            "priority": 3
        },
        {
            "destination": "S2",
            "priority": 1
        },
        {
            "destination": "S3",
            "priority": 2
        }
    ]

    result = SortingUtils.sort_destinations(
        destinations
    )

    assert result[0]["destination"] == "S2"
    assert result[1]["destination"] == "S3"
    assert result[2]["destination"] == "S1"

    print("PASS: Destination sorting")


def run_all_tests():

    print("=" * 60)
    print("SORTING TEST")
    print("=" * 60)

    test_shelter_sorting()
    test_route_sorting()
    test_destination_sorting()

    print("=" * 60)
    print("ALL SORTING TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()