from m2.cyclone_loader import load_cyclone_track


CHENNAI_TRACK_RADIUS_KM = 250.0


def get_chennai_relevant_track(
    hazards=None,
    max_distance_km=CHENNAI_TRACK_RADIUS_KM
):
    """
    Return cyclone observations within the
    Chennai-relevant track corridor.

    The current dataset defines the Chennai
    track corridor as less than 250 km.
    """

    if hazards is None:
        hazards = load_cyclone_track()

    relevant_hazards = []

    for hazard in hazards:

        if (
            hazard.distance_from_chennai_km
            is not None
            and hazard.distance_from_chennai_km
            <= max_distance_km
        ):
            relevant_hazards.append(hazard)

    return relevant_hazards


def group_track_by_cyclone(hazards):
    """
    Group cyclone observations by cyclone ID.

    Returns:
        Dictionary:
            cyclone_id -> list of observations
    """

    grouped = {}

    for hazard in hazards:

        cyclone_id = hazard.cyclone_id

        if cyclone_id not in grouped:
            grouped[cyclone_id] = []

        grouped[cyclone_id].append(hazard)

    return grouped


def get_closest_observation(hazards):
    """
    Return the observation closest to Chennai.
    """

    if not hazards:
        return None

    return min(
        hazards,
        key=lambda hazard:
        hazard.distance_from_chennai_km
    )