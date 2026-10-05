from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.real_cyclone_impact import calculate_cyclone_impact
from m2.cyclone_graph_state import CycloneGraphStateManager


IMPACT_RADIUS_METERS = 1000


def test_vardah_restoration():

    print()
    print("======================================================")
    print(" VARDAH DEPARTURE AND ROAD RESTORATION TEST")
    print("======================================================")

    # --------------------------------------------------
    # STEP 1: BUILD REAL CHENNAI GRAPH
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
    # STEP 2: LOAD VARDAH TRACK
    # --------------------------------------------------

    print("\nSTEP 2: LOADING REAL VARDAH TRACK")

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
    # SELECT REAL TRACK OBSERVATIONS
    # --------------------------------------------------

    selected_track_ids = {
        "TP0160",
        "TP0162",
        "TP0163",
        "TP0164",
        "TP0165",
        "TP0166",
        "TP0167"
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
    # STEP 3: CREATE CYCLONE STATE MANAGER
    # --------------------------------------------------

    cyclone_manager = (
        CycloneGraphStateManager()
    )

    # --------------------------------------------------
    # STEP 4: PROCESS TRACK
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" CYCLONE DEPARTURE / RESTORATION")
    print("======================================================")

    for hazard in vardah:

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
            "Distance from Chennai:",
            hazard.distance_from_chennai_km,
            "km"
        )

        print(
            "Wind speed:",
            hazard.wind_speed,
            "km/h"
        )

        # --------------------------------------------------
        # CALCULATE CURRENT IMPACT
        # --------------------------------------------------

        impact = calculate_cyclone_impact(
            graph,
            hazard,
            radius_meters=IMPACT_RADIUS_METERS
        )

        affected_roads = set(
            impact["affected_roads"].keys()
        )

        print(
            "Severity:",
            impact["severity"]
        )

        print(
            "Affected roads:",
            len(affected_roads)
        )

        # --------------------------------------------------
        # UPDATE GRAPH
        # --------------------------------------------------

        changes = cyclone_manager.update_graph(
            graph,
            affected_roads
        )

        print(
            "Newly affected:",
            len(
                changes["newly_affected"]
            )
        )

        print(
            "Still affected:",
            len(
                changes["still_affected"]
            )
        )

        print(
            "No longer affected:",
            len(
                changes["no_longer_affected"]
            )
        )

        # --------------------------------------------------
        # CURRENT CYCLONE STATE
        # --------------------------------------------------

        current_roads = (
            cyclone_manager.state
            .get_current_roads()
        )

        print(
            "Currently cyclone-affected:",
            len(current_roads)
        )

        # --------------------------------------------------
        # SAMPLE STATUS CHECK
        # --------------------------------------------------

        if changes["newly_affected"]:

            sample_road = (
                changes["newly_affected"][0]
            )

            print(
                "Sample newly affected road:",
                sample_road
            )

            print(
                "Sample road status:",
                graph.get_road_status(
                    sample_road
                )
            )

        if changes["no_longer_affected"]:

            sample_road = (
                changes["no_longer_affected"][0]
            )

            print(
                "Sample restored road:",
                sample_road
            )

            print(
                "Restored road status:",
                graph.get_road_status(
                    sample_road
                )
            )

    # --------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" FINAL CYCLONE STATE")
    print("======================================================")

    final_roads = (
        cyclone_manager.state
        .get_current_roads()
    )

    print(
        "Currently cyclone-affected roads:",
        len(final_roads)
    )

    print(
        "Cyclone-affected road IDs:",
        sorted(final_roads)
    )

    print()
    print("======================================================")
    print(" VARDAH RESTORATION TEST COMPLETE")
    print("======================================================")


if __name__ == "__main__":
    test_vardah_restoration()