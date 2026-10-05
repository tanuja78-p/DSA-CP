from m1.graph import Graph
from m2.hazard_registry import HazardRegistry
from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.cyclone_hazard_registry import apply_cyclone_to_registry


def build_test_graph():
    graph = Graph()

    graph.add_node("A", 13.0000, 80.0000)
    graph.add_node("B", 13.0010, 80.0000)
    graph.add_node("C", 13.0020, 80.0000)
    graph.add_node("D", 13.0030, 80.0000)
    graph.add_node("E", 13.0010, 80.0010)

    graph.add_edge("A", "B", "R1", 100)
    graph.add_edge("B", "C", "R2", 100)
    graph.add_edge("C", "D", "R3", 100)
    graph.add_edge("A", "E", "R4", 180)
    graph.add_edge("E", "D", "R5", 180)

    return graph


def get_vardah_observation():
    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(hazards)

    vardah = [
        hazard
        for hazard in relevant
        if hazard.cyclone_id == "vardah"
    ]

    if not vardah:
        raise RuntimeError("No Chennai-relevant Vardah observations found.")

    # Use the closest Vardah observation to Chennai.
    return min(
        vardah,
        key=lambda hazard: hazard.distance_from_chennai_km
    )


def test_cyclone_hazard_registry():

    print()
    print("==========================================")
    print(" CYCLONE → HAZARD REGISTRY TEST")
    print("==========================================")

    graph = build_test_graph()
    registry = HazardRegistry()

    cyclone = get_vardah_observation()

    print()
    print("Selected cyclone observation:")
    print("Track Point:", cyclone.track_point_id)
    print("Cyclone:", cyclone.cyclone_name)
    print("Timestamp:", cyclone.timestamp_utc)
    print("Latitude:", cyclone.latitude)
    print("Longitude:", cyclone.longitude)
    print("Wind Speed:", cyclone.wind_speed)
    print("Pressure:", cyclone.pressure)
    print("Distance from Chennai:", cyclone.distance_from_chennai_km)

    print()
    print("Applying cyclone hazard...")

    result = apply_cyclone_to_registry(
        graph,
        cyclone,
        registry,
        radius_meters=1000
    )

    print()
    print("Cyclone impact result:")
    print("Severity:", result["severity"])
    print("Status:", result["status"])
    print("Impact Radius:", result["impact_radius_meters"], "meters")
    print("Affected Nodes:", len(result["affected_nodes"]))
    print("Affected Roads:", len(result["affected_roads"]))

    print()
    print("Hazard Registry:")

    for road_id in ["R1", "R2", "R3", "R4", "R5"]:
        print(
            road_id,
            "→",
            registry.get_road_statuses(road_id)
        )

    print()
    print("==========================================")
    print(" TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_cyclone_hazard_registry()