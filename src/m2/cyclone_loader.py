import csv
from pathlib import Path

from m2.cyclone_engine import CycloneHazard


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CYCLONE_CSV = (
    PROJECT_ROOT
    / "data"
    / "DEEDSF_Cyclone_Best_Track_Final.csv"
)


def load_cyclone_track(csv_path=CYCLONE_CSV):
    """
    Load the project's real cyclone best-track CSV.

    Every CSV observation is converted into a
    CycloneHazard object.

    Important source metadata is preserved so that
    later stages can use the real cyclone track
    information.
    """

    hazards = []

    with open(
        csv_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            hazard = CycloneHazard(
                latitude=row["latitude_deg_n"],
                longitude=row["longitude_deg_e"],
                wind_speed=row[
                    "max_sustained_wind_kmh_approx"
                ],
                pressure=row[
                    "estimated_central_pressure_hpa"
                ],
                cyclone_name=row["cyclone_name"],

                track_point_id=row[
                    "track_point_id"
                ],

                cyclone_id=row[
                    "cyclone_id"
                ],

                timestamp_utc=row[
                    "timestamp_utc"
                ],

                distance_from_chennai_km=row[
                    "distance_from_chennai_km_approx"
                ],

                intensity_category=row[
                    "intensity_category_imd"
                ]
            )

            hazards.append(hazard)

    return hazards


def get_cyclone_csv_path():
    """
    Return the default cyclone dataset path.
    """

    return CYCLONE_CSV