from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.real_cyclone_impact import calculate_cyclone_impact


IMPACT_RADIUS_METERS = 1000


def test_vardah_dynamic_changes():

    print()
    print("======================================================")
    print(" VARDAH DYNAMIC ROAD IMPACT CHANGES")
    print("======================================================")

    # --------------------------------------------------
    # STEP 1: BUILD GRAPH
    # --------------------------------------------------

    print("\nSTEP 1: BUILDING CHENNAI ROAD GRAPH")

    graph = build_chennai_graph()

    print(
        "Graph nodes:",
        graph.get_node_count()
    )

    print(
        "Graph edges:",
        graph.get_edge_count()
    )

    # --------------------------------------------------
    # STEP 2: LOAD CYCLONE DATA
    # --------------------------------------------------

    print("\nSTEP 2: LOADING VARDAH TRACK")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    vardah = [
        hazard
        for hazard in relevant
        if hazard.cyclone_name.lower() == "vardah"
    ]

    vardah = sorted(
        vardah,
        key=lambda hazard:
            hazard.timestamp_utc
    )

    # --------------------------------------------------
    # STEP 3: SELECT APPROACHING TRACK
    # --------------------------------------------------

    selected_track_ids = {
        "TP0157",
        "TP0158",
        "TP0159",
        "TP0160"
    }

    vardah = [
        hazard
        for hazard in vardah
        if hazard.track_point_id in selected_track_ids
    ]

    print(
        "Selected track points:",
        len(vardah)
    )

    # --------------------------------------------------
    # STEP 4: PREVIOUS ROAD SET
    # --------------------------------------------------

    previous_roads = set()

    # --------------------------------------------------
    # STEP 5: PROCESS EACH TRACK POINT
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" DYNAMIC CHANGES")
    print("======================================================")

    for hazard in vardah:

        impact = calculate_cyclone_impact(
            graph,
            hazard,
            radius_meters=IMPACT_RADIUS_METERS
        )

        current_roads = set(
            impact["affected_roads"].keys()
        )

        newly_affected = (
            current_roads - previous_roads
        )

        no_longer_affected = (
            previous_roads - current_roads
        )

        still_affected = (
            current_roads & previous_roads
        )

        print()
        print("------------------------------------------")

        print(
            "Track point:",
            hazard.track_point_id
        )

        print(
            "Timestamp:",
            hazard.timestamp_utc
        )

        print(
            "Cyclone distance:",
            hazard.distance_from_chennai_km,
            "km"
        )

        print(
            "Wind speed:",
            hazard.wind_speed,
            "km/h"
        )

        print(
            "Severity:",
            impact["severity"]
        )

        print(
            "Affected roads:",
            len(current_roads)
        )

        print(
            "Newly affected:",
            len(newly_affected)
        )

        print(
            "Still affected:",
            len(still_affected)
        )

        print(
            "No longer affected:",
            len(no_longer_affected)
        )

        # ------------------------------------------
        # Update previous state
        # ------------------------------------------

        previous_roads = current_roads

    # --------------------------------------------------
    # FINAL
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" DYNAMIC CHANGE ANALYSIS COMPLETE")
    print("======================================================")


if __name__ == "__main__":
    test_vardah_dynamic_changes()