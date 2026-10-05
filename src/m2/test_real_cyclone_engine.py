from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import (
    get_chennai_relevant_track,
    get_closest_observation
)

from m2.real_cyclone_impact import (
    calculate_cyclone_impact,
    apply_cyclone_impact
)


def test_real_cyclone_engine():

    print()
    print("==========================================")
    print(" REAL CYCLONE IMPACT ENGINE TEST")
    print("==========================================")

    # ------------------------------------------
    # STEP 1
    # ------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # ------------------------------------------
    # STEP 2
    # ------------------------------------------

    print("\nSTEP 2: LOADING REAL CYCLONE DATA")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    cyclone = get_closest_observation(
        relevant
    )

    print(
        "Cyclone:",
        cyclone.cyclone_name
    )

    print(
        "Track point:",
        cyclone.track_point_id
    )

    print(
        "Timestamp:",
        cyclone.timestamp_utc
    )

    print(
        "Wind speed:",
        cyclone.wind_speed,
        "km/h"
    )

    print(
        "Pressure:",
        cyclone.pressure,
        "hPa"
    )

    print(
        "Distance from Chennai:",
        cyclone.distance_from_chennai_km,
        "km"
    )

    # ------------------------------------------
    # STEP 3
    # ------------------------------------------

    print("\nSTEP 3: CALCULATING CYCLONE IMPACT")

    impact = calculate_cyclone_impact(
        graph,
        cyclone,
        radius_meters=1000
    )

    print(
        "Severity:",
        impact["severity"]
    )

    print(
        "Road status:",
        impact["status"]
    )

    print(
        "Impact radius:",
        impact["impact_radius_meters"],
        "meters"
    )

    print(
        "Affected nodes:",
        len(
            impact["affected_nodes"]
        )
    )

    print(
        "Affected roads:",
        len(
            impact["affected_roads"]
        )
    )

    # ------------------------------------------
    # STEP 4
    # ------------------------------------------

    print("\nSTEP 4: APPLYING CYCLONE IMPACT")

    update_result = apply_cyclone_impact(
        graph,
        impact
    )

    print(
        "Applied status:",
        update_result["status"]
    )

    print(
        "Updated roads:",
        update_result["updated_count"]
    )

    # ------------------------------------------
    # STEP 5
    # ------------------------------------------

    print("\nSTEP 5: VERIFYING ROAD STATUSES")

    blocked_count = 0
    restricted_count = 0
    safe_count = 0

    for road_id in impact["affected_roads"]:

        status = graph.get_road_status(
            road_id
        )

        if status == "BLOCKED":
            blocked_count += 1

        elif status == "RESTRICTED":
            restricted_count += 1

        else:
            safe_count += 1

    print(
        "BLOCKED:",
        blocked_count
    )

    print(
        "RESTRICTED:",
        restricted_count
    )

    print(
        "SAFE:",
        safe_count
    )

    # ------------------------------------------
    # FINAL
    # ------------------------------------------

    print()
    print("==========================================")
    print(" REAL CYCLONE ENGINE TEST COMPLETE")
    print("==========================================")


if __name__ == "__main__":
    test_real_cyclone_engine()