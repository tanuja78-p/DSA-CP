from math import sqrt


class CycloneHazard:
    """
    Represents one cyclone track observation.

    Core hazard information:
        latitude
        longitude
        wind_speed
        pressure
        cyclone_name

    Real-dataset metadata:
        track_point_id
        cyclone_id
        timestamp_utc
        distance_from_chennai_km
        intensity_category
    """

    def __init__(
        self,
        latitude,
        longitude,
        wind_speed,
        pressure,
        cyclone_name="UNKNOWN",
        track_point_id=None,
        cyclone_id=None,
        timestamp_utc=None,
        distance_from_chennai_km=None,
        intensity_category=None
    ):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.wind_speed = float(wind_speed)
        self.pressure = float(pressure)

        self.cyclone_name = cyclone_name

        self.track_point_id = track_point_id
        self.cyclone_id = cyclone_id
        self.timestamp_utc = timestamp_utc

        if distance_from_chennai_km is not None:
            self.distance_from_chennai_km = float(
                distance_from_chennai_km
            )
        else:
            self.distance_from_chennai_km = None

        self.intensity_category = intensity_category


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate approximate geographic distance
    in coordinate space.

    Used for local cyclone influence testing.
    """

    return sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )


def classify_cyclone_severity(wind_speed):
    """
    Classify cyclone severity using wind speed.

    Thresholds used by the current M2 routing model:

        >= 120 km/h -> CRITICAL
        >= 90 km/h  -> HIGH
        >= 60 km/h  -> MODERATE
        < 60 km/h   -> LOW
    """

    if wind_speed >= 120:
        return "CRITICAL"

    if wind_speed >= 90:
        return "HIGH"

    if wind_speed >= 60:
        return "MODERATE"

    return "LOW"


def cyclone_to_status(severity):
    """
    Convert cyclone severity into a road status.

        CRITICAL -> BLOCKED
        HIGH     -> BLOCKED
        MODERATE -> RESTRICTED
        LOW      -> RESTRICTED
    """

    if severity == "CRITICAL":
        return "BLOCKED"

    if severity == "HIGH":
        return "BLOCKED"

    if severity == "MODERATE":
        return "RESTRICTED"

    return "RESTRICTED"


def find_affected_nodes(
    graph,
    cyclone,
    influence_radius=0.002
):
    """
    Find graph nodes located inside the cyclone's
    local influence radius.

    Returns:
        List of affected node IDs.
    """

    affected_nodes = []

    for node_id, node in graph.nodes.items():

        distance = calculate_distance(
            cyclone.latitude,
            cyclone.longitude,
            node.latitude,
            node.longitude
        )

        if distance <= influence_radius:
            affected_nodes.append(node_id)

    return affected_nodes