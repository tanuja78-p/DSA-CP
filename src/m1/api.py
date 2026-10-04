from pathlib import Path
import csv

from fastapi import FastAPI, HTTPException


# -------------------------------------------------
# Project paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

ROAD_NODES_FILE = (
    PROCESSED_DATA
    / "road_nodes.csv"
)

ROAD_EDGES_FILE = (
    PROCESSED_DATA
    / "road_edges.csv"
)

ROAD_STATUS_FILE = (
    PROCESSED_DATA
    / "flood_road_status.csv"
)

FLOOD_HAZARDS_FILE = (
    PROCESSED_DATA
    / "flood_hazards.csv"
)


# -------------------------------------------------
# FastAPI application
# -------------------------------------------------

app = FastAPI(
    title=(
        "M1 - Dynamic Road Graph "
        "and Urban Flood API"
    ),
    description=(
        "API for the Dynamic Graph-Based Framework "
        "for Emergency Evacuation and Disaster "
        "Decision Support."
    ),
    version="1.0.0"
)


# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def read_csv_file(filename: Path):

    if not filename.exists():
        raise FileNotFoundError(
            f"Required file not found: {filename}"
        )

    with open(
        filename,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def get_road_status_counts():

    records = read_csv_file(
        ROAD_STATUS_FILE
    )

    counts = {
        "SAFE": 0,
        "RESTRICTED": 0,
        "BLOCKED": 0
    }

    for record in records:

        status = record.get(
            "status",
            "UNKNOWN"
        ).upper()

        if status in counts:
            counts[status] += 1

    return counts


# -------------------------------------------------
# Root endpoint
# -------------------------------------------------

@app.get("/")
def root():

    return {
        "project": (
            "A Dynamic Graph-Based Framework for "
            "Emergency Evacuation and Disaster "
            "Decision Support"
        ),
        "module": "M1",
        "module_name": (
            "Dynamic Road Graph + Urban Flood"
        ),
        "status": "running"
    }


# -------------------------------------------------
# Graph summary
# -------------------------------------------------

@app.get("/api/m1/graph/summary")
def graph_summary():

    try:

        nodes = read_csv_file(
            ROAD_NODES_FILE
        )

        edges = read_csv_file(
            ROAD_EDGES_FILE
        )

        road_status = read_csv_file(
            ROAD_STATUS_FILE
        )

        status_counts = {
            "SAFE": 0,
            "RESTRICTED": 0,
            "BLOCKED": 0
        }

        for record in road_status:

            status = record.get(
                "status",
                "UNKNOWN"
            ).upper()

            if status in status_counts:
                status_counts[status] += 1

        return {
            "module": "M1",
            "graph_type": (
                "Dynamic weighted road graph"
            ),
            "nodes": len(nodes),
            "physical_roads": len(edges),
            "road_status": status_counts
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -------------------------------------------------
# Road status endpoint
# -------------------------------------------------

@app.get("/api/m1/roads/status")
def road_status():

    try:

        records = read_csv_file(
            ROAD_STATUS_FILE
        )

        return {
            "module": "M1",
            "count": len(records),
            "roads": records
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -------------------------------------------------
# Flood hazards endpoint
# -------------------------------------------------

@app.get("/api/m1/flood/hazards")
def flood_hazards():

    try:

        records = read_csv_file(
            FLOOD_HAZARDS_FILE
        )

        return {
            "module": "M1",
            "hazard_type": "Urban Flood",
            "count": len(records),
            "hazards": records
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -------------------------------------------------
# Flood summary endpoint
# -------------------------------------------------

@app.get("/api/m1/flood/summary")
def flood_summary():

    try:

        records = read_csv_file(
            FLOOD_HAZARDS_FILE
        )

        severity_counts = {}

        for record in records:

            severity = record.get(
                "severity",
                "UNKNOWN"
            ).upper()

            severity_counts[severity] = (
                severity_counts.get(
                    severity,
                    0
                ) + 1
            )

        road_status = get_road_status_counts()

        return {
            "module": "M1",
            "hazard_type": "Urban Flood",
            "flood_hazards": len(records),
            "severity_distribution": severity_counts,
            "affected_road_status": road_status
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )