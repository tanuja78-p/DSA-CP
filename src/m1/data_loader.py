import xml.etree.ElementTree as ET
from typing import List, Dict


KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


def parse_coordinates(
    coordinate_text: str
):
    """
    Convert KML coordinate text into:

        [(longitude, latitude), ...]

    KML normally stores coordinates as:

        longitude,latitude,altitude
    """

    coordinates = []

    if not coordinate_text:
        return coordinates

    coordinate_items = (
        coordinate_text.strip().split()
    )

    for item in coordinate_items:

        parts = item.split(",")

        if len(parts) < 2:
            continue

        try:

            longitude = float(parts[0])
            latitude = float(parts[1])

        except ValueError:
            continue

        coordinates.append(
            (longitude, latitude)
        )

    return coordinates


def load_road_centerlines(
    filename: str
) -> List[Dict]:
    """
    Load the Chennai Road Centerline KML dataset.

    Each returned dictionary represents one road geometry.
    """

    tree = ET.parse(filename)

    root = tree.getroot()

    roads = []

    placemarks = root.findall(
        ".//kml:Placemark",
        KML_NAMESPACE
    )

    for placemark in placemarks:

        data = {}

        simple_data_elements = (
            placemark.findall(
                ".//kml:SimpleData",
                KML_NAMESPACE
            )
        )

        for simple_data in simple_data_elements:

            field_name = (
                simple_data.attrib.get("name")
            )

            field_value = simple_data.text

            data[field_name] = field_value

        coordinate_element = (
            placemark.find(
                ".//kml:LineString/kml:coordinates",
                KML_NAMESPACE
            )
        )

        if coordinate_element is None:
            continue

        coordinates = parse_coordinates(
            coordinate_element.text
        )

        if len(coordinates) < 2:
            continue

        road = {
            "road_id": data.get("road_id"),
            "road_name": data.get("road_name"),
            "objectid": data.get("objectid"),
            "length": data.get(
                "st_length(shape)"
            ),
            "coordinates": coordinates
        }

        roads.append(road)

    return roads


def print_road_sample(
    roads: List[Dict],
    count: int = 5
):
    """
    Print a few roads so we can verify
    that the real dataset was loaded correctly.
    """

    print()
    print("========== ROAD DATA SAMPLE ==========")

    for road in roads[:count]:

        print(
            f"Road ID   : {road['road_id']}"
        )

        print(
            f"Road Name : {road['road_name']}"
        )

        print(
            f"Length    : {road['length']}"
        )

        print(
            f"Points    : {len(road['coordinates'])}"
        )

        print(
            f"First Point: {road['coordinates'][0]}"
        )

        print("--------------------------------------")

    print()