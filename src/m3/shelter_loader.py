import csv
import json

from .shelter import Shelter


class ShelterLoader:
    """Loads shelter records from external datasets."""

    @staticmethod
    def _to_bool(value):
        if isinstance(value, bool):
            return value

        return str(value).strip().lower() not in {
            "false",
            "0",
            "no",
            "closed",
        }

    @staticmethod
    def from_csv(file_path):
        """
        Load shelters from CSV.

        Expected columns:

        shelter_id
        name
        latitude
        longitude
        capacity

        Optional:

        occupied
        status
        accessible
        """

        shelters = []

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                shelter_id = (
                    row.get("shelter_id")
                    or row.get("id")
                    or row.get("ID")
                )

                name = (
                    row.get("name")
                    or row.get("shelter_name")
                    or f"Shelter {shelter_id}"
                )

                latitude = float(
                    row.get("latitude")
                    or row.get("lat")
                    or 0
                )

                longitude = float(
                    row.get("longitude")
                    or row.get("lon")
                    or row.get("lng")
                    or 0
                )

                capacity = int(
                    float(
                        row.get("capacity")
                        or row.get("total_capacity")
                        or 0
                    )
                )

                occupied = int(
                    float(
                        row.get("occupied")
                        or row.get("current_occupancy")
                        or 0
                    )
                )

                status = (
                    row.get("status")
                    or "SAFE"
                ).upper()

                accessible = ShelterLoader._to_bool(
                    row.get("accessible", True)
                )

                shelter = Shelter(
                    shelter_id=str(shelter_id),
                    name=str(name),
                    latitude=latitude,
                    longitude=longitude,
                    capacity=capacity,
                    occupied=occupied,
                    status=status,
                    accessible=accessible,
                )

                shelters.append(shelter)

        return shelters

    @staticmethod
    def from_json(file_path):
        """Load shelters from JSON."""

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            data = data.get("shelters", [])

        shelters = []

        for row in data:

            shelter = Shelter(
                shelter_id=str(
                    row.get("shelter_id", row.get("id"))
                ),
                name=row.get(
                    "name",
                    "Unnamed Shelter",
                ),
                latitude=float(
                    row.get("latitude", 0)
                ),
                longitude=float(
                    row.get("longitude", 0)
                ),
                capacity=int(
                    row.get("capacity", 0)
                ),
                occupied=int(
                    row.get("occupied", 0)
                ),
                status=row.get(
                    "status",
                    "SAFE",
                ).upper(),
                accessible=bool(
                    row.get(
                        "accessible",
                        True,
                    )
                ),
            )

            shelters.append(shelter)

        return shelters