from m1.build_road_graph import build_chennai_graph

from m2.cyclone_loader import load_cyclone_track
from m2.chennai_cyclone_track import get_chennai_relevant_track
from m2.real_cyclone_impact import calculate_cyclone_impact


def test_vardah_dynamic_impact():

    print()
    print("======================================================")
    print(" VARDAH DYNAMIC IMPACT ANALYSIS")
    print("======================================================")

    # --------------------------------------------------
    # STEP 1: BUILD REAL CHENNAI ROAD GRAPH
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

    print("\nSTEP 2: LOADING CYCLONE DATA")

    hazards = load_cyclone_track()

    relevant = get_chennai_relevant_track(
        hazards
    )

    # Select Vardah observations.
    vardah = [
        hazard
        for hazard in relevant
        if hazard.cyclone_name.lower() == "vardah"
    ]

    # Sort chronologically.
    vardah = sorted(
        vardah,
        key=lambda hazard: hazard.timestamp_utc
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

    vardah_approach = [
        hazard
        for hazard in vardah
        if hazard.track_point_id in selected_track_ids
    ]

    print(
        "\nSelected Vardah observations:",
        len(vardah_approach)
    )

    # --------------------------------------------------
    # STEP 4: CALCULATE IMPACT FOR EACH TRACK POINT
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" TRACK IMPACT RESULTS")
    print("======================================================")

    print(
        "\nTRACK | TIME | DIST | WIND | SEVERITY | "
        "NODES | ROADS"
    )

    print("-" * 85)

    for hazard in vardah_approach:

        impact = calculate_cyclone_impact(
            graph,
            hazard,
            radius_meters=1000
        )

        affected_nodes = impact[
            "affected_nodes"
        ]

        affected_roads = impact[
            "affected_roads"
        ]

        print(
            hazard.track_point_id,
            "|",
            hazard.timestamp_utc,
            "|",
            hazard.distance_from_chennai_km,
            "km |",
            hazard.wind_speed,
            "km/h |",
            impact["severity"],
            "|",
            len(affected_nodes),
            "|",
            len(affected_roads)
        )

    # --------------------------------------------------
    # FINAL
    # --------------------------------------------------

    print()
    print("======================================================")
    print(" DYNAMIC IMPACT ANALYSIS COMPLETE")
    print("======================================================")


if __name__ == "__main__":
    test_vardah_dynamic_impact()