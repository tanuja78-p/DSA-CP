import csv
from pathlib import Path
from typing import List

from m1.flood_engine import FloodHazard


def export_flood_hazards(
    hazards: List[FloodHazard],
    filename: str
):
    """
    Export processed flood hazard observations to CSV.

    Each row represents one flood hazard observation.

    Columns:
        hazard_id
        latitude
        longitude
        severity
        depth
        source
    """

    output_path = Path(filename)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "hazard_id",
                "latitude",
                "longitude",
                "severity",
                "depth",
                "source"
            ]
        )

        for hazard in hazards:

            writer.writerow(
                [
                    hazard.hazard_id,
                    hazard.latitude,
                    hazard.longitude,
                    hazard.severity,
                    hazard.depth,
                    hazard.source
                ]
            )

    print(
        f"Flood hazards exported: {len(hazards)}"
    )

    print(
        f"Output file: {output_path}"
    )