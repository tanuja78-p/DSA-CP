from pathlib import Path
import xml.etree.ElementTree as ET


KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


def parse_coordinates(coordinate_text):
    """
    Parse a KML coordinate string.

    KML normally stores coordinates as:

        longitude,latitude,altitude

    Returns:

        [
            (longitude, latitude),
            ...
        ]
    """

    if not coordinate_text:
        return []

    coordinates = []

    coordinate_text = coordinate_text.strip()

    raw_coordinates = coordinate_text.split()

    for item in raw_coordinates:

        parts = item.split(",")

        if len(parts) < 2:
            continue

        try:

            longitude = float(parts[0])
            latitude = float(parts[1])

            coordinates.append(
                (longitude, latitude)
            )

        except ValueError:

            continue

    return coordinates


def extract_element_text(parent, tag):
    """
    Return the text of the first matching
    element under parent.
    """

    element = parent.find(
        f".//kml:{tag}",
        KML_NAMESPACE
    )

    if element is None:
        return None

    if element.text is None:
        return None

    return element.text.strip()


def load_flood_kml(filename):
    """
    Load flood-related geographic information
    from a KML file.

    Each Placemark is returned as a dictionary.

    The loader supports:

        Point
        LineString
        Polygon

    The exact geometry can be inspected later
    by the Flood Hazard Engine.
    """

    path = Path(filename)

    if not path.exists():

        raise FileNotFoundError(
            f"Flood KML not found: {filename}"
        )

    tree = ET.parse(path)

    root = tree.getroot()

    flood_records = []

    placemarks = root.findall(
        ".//kml:Placemark",
        KML_NAMESPACE
    )

    for index, placemark in enumerate(
        placemarks,
        start=1
    ):

        record = {
            "record_id": index,
            "name": None,
            "description": None,
            "geometry_type": None,
            "coordinates": [],
            "attributes": {}
        }

        name = placemark.find(
            "kml:name",
            KML_NAMESPACE
        )

        if name is not None and name.text:

            record["name"] = name.text.strip()

        description = placemark.find(
            "kml:description",
            KML_NAMESPACE
        )

        if (
            description is not None
            and description.text
        ):

            record["description"] = (
                description.text.strip()
            )

        # --------------------------------------------------
        # Read ExtendedData / SimpleData attributes
        # --------------------------------------------------

        simple_data_elements = placemark.findall(
            ".//kml:SimpleData",
            KML_NAMESPACE
        )

        for element in simple_data_elements:

            field_name = element.get("name")

            if not field_name:
                continue

            value = ""

            if element.text:

                value = element.text.strip()

            record["attributes"][
                field_name
            ] = value

        # --------------------------------------------------
        # Point geometry
        # --------------------------------------------------

        point_coordinates = placemark.find(
            ".//kml:Point/kml:coordinates",
            KML_NAMESPACE
        )

        if (
            point_coordinates is not None
            and point_coordinates.text
        ):

            coordinates = parse_coordinates(
                point_coordinates.text
            )

            if coordinates:

                record["geometry_type"] = "Point"

                record["coordinates"] = coordinates

        # --------------------------------------------------
        # LineString geometry
        # --------------------------------------------------

        if not record["coordinates"]:

            line_coordinates = placemark.find(
                ".//kml:LineString/kml:coordinates",
                KML_NAMESPACE
            )

            if (
                line_coordinates is not None
                and line_coordinates.text
            ):

                coordinates = parse_coordinates(
                    line_coordinates.text
                )

                if coordinates:

                    record["geometry_type"] = (
                        "LineString"
                    )

                    record["coordinates"] = (
                        coordinates
                    )

        # --------------------------------------------------
        # Polygon geometry
        # --------------------------------------------------

        if not record["coordinates"]:

            polygon_coordinates = placemark.find(
                ".//kml:Polygon"
                "//kml:coordinates",
                KML_NAMESPACE
            )

            if (
                polygon_coordinates is not None
                and polygon_coordinates.text
            ):

                coordinates = parse_coordinates(
                    polygon_coordinates.text
                )

                if coordinates:

                    record["geometry_type"] = (
                        "Polygon"
                    )

                    record["coordinates"] = (
                        coordinates
                    )

        flood_records.append(record)

    return flood_records


def print_flood_summary(records, filename):
    """
    Print a readable summary of a flood KML file.
    """

    print()
    print("==========================================")
    print(" FLOOD DATASET SUMMARY")
    print("==========================================")

    print(
        f"File: {Path(filename).name}"
    )

    print(
        f"Placemark records: {len(records)}"
    )

    geometry_counts = {}

    records_with_coordinates = 0

    for record in records:

        geometry_type = (
            record["geometry_type"]
            or "Unknown"
        )

        geometry_counts[
            geometry_type
        ] = (
            geometry_counts.get(
                geometry_type,
                0
            ) + 1
        )

        if record["coordinates"]:

            records_with_coordinates += 1

    print(
        f"Records with coordinates: "
        f"{records_with_coordinates}"
    )

    print()
    print("Geometry types:")

    for geometry_type, count in (
        geometry_counts.items()
    ):

        print(
            f"  {geometry_type}: {count}"
        )

    print()
    print("First 5 records:")

    for record in records[:5]:

        print(
            f"Record ID    : "
            f"{record['record_id']}"
        )

        print(
            f"Name         : "
            f"{record['name']}"
        )

        print(
            f"Geometry     : "
            f"{record['geometry_type']}"
        )

        print(
            f"Coordinates   : "
            f"{len(record['coordinates'])}"
        )

        print(
            f"Attributes   : "
            f"{len(record['attributes'])}"
        )

        if record["attributes"]:

            print(
                f"Attribute data: "
                f"{record['attributes']}"
            )

        print("------------------------------------------")


def load_and_print_flood_kml(filename):
    """
    Convenience function used for testing.
    """

    records = load_flood_kml(
        filename
    )

    print_flood_summary(
        records,
        filename
    )

    return records