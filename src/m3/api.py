from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .shelter import Shelter
from .shelter_manager import ShelterManager
from .m2_client import M2Client


# ============================================================
# CONFIGURATION
# ============================================================

M2_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="DEEDSF Member 3 - Shelter Management API",
    description="Shelter assignment and resource management API.",
    version="1.0.0",
)


# Allow the M3 frontend to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# M2 CLIENT
# ============================================================

m2_client = M2Client(M2_BASE_URL)


# ============================================================
# M3 SHELTER DATA
# ============================================================
#
# These node IDs are real M2 graph nodes that we already
# successfully tested.
#
# Later, these can be replaced by the project's real
# Chennai shelter dataset without changing the API contract.
# ============================================================

SHELTERS = [
    Shelter(
        "S1",
        "Chennai Central Relief Shelter",
        13.09112,
        80.26185,
        100,
        20,
    ),
    Shelter(
        "S2",
        "Egmore Emergency Shelter",
        13.09114,
        80.26176,
        50,
        10,
    ),
    Shelter(
        "S3",
        "Harbour Relief Shelter",
        13.09115,
        80.26166,
        200,
        150,
    ),
]


# M2 graph node corresponding to each shelter.
SHELTER_NODES: Dict[str, str] = {
    "S1": "80.26185_13.09112",
    "S2": "80.26176_13.09114",
    "S3": "80.26166_13.09115",
}


# Create the Member 3 manager.
manager = ShelterManager(SHELTERS)


# ============================================================
# REQUEST MODELS
# ============================================================

class AssignmentRequest(BaseModel):
    source: str
    people: int = 1


class AdmitRequest(BaseModel):
    people: int


class StatusRequest(BaseModel):
    status: str | None = None
    accessible: bool | None = None


# ============================================================
# HELPER
# ============================================================

def shelter_to_dict(shelter):
    return {
        "shelter_id": shelter.shelter_id,
        "name": shelter.name,
        "latitude": shelter.latitude,
        "longitude": shelter.longitude,
        "capacity": shelter.capacity,
        "occupied": shelter.occupied,
        "available_capacity": shelter.available_capacity,
        "status": shelter.status,
        "accessible": shelter.accessible,
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "module": "M3",
        "module_name": "Shelter Management",
        "status": "running",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/m3/health")
def health():
    return {
        "module": "M3",
        "status": "running",
        "m2_base_url": M2_BASE_URL,
        "shelter_count": len(manager.all_shelters()),
    }


# ============================================================
# GET ALL SHELTERS
# ============================================================

@app.get("/api/m3/shelters")
def get_shelters():

    return {
        "module": "M3",
        "count": len(manager.all_shelters()),
        "shelters": [
            shelter_to_dict(shelter)
            for shelter in manager.all_shelters()
        ],
    }


# ============================================================
# GET ONE SHELTER
# ============================================================

@app.get("/api/m3/shelters/{shelter_id}")
def get_shelter(shelter_id: str):

    shelter = manager.get_shelter(shelter_id)

    if shelter is None:
        raise HTTPException(
            status_code=404,
            detail=f"Shelter not found: {shelter_id}",
        )

    return shelter_to_dict(shelter)


# ============================================================
# SHELTER ASSIGNMENT
# ============================================================

@app.post("/api/m3/assign")
def assign_shelter(request: AssignmentRequest):

    if request.people <= 0:
        raise HTTPException(
            status_code=400,
            detail="people must be greater than zero",
        )

    if not request.source.strip():
        raise HTTPException(
            status_code=400,
            detail="source node is required",
        )

    # Ask M2 for real safe-route distances.
    try:
        distances = m2_client.get_distances_to_shelters(
            request.source,
            SHELTER_NODES,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to contact M2: {exc}",
        )

    if not distances:
        return {
            "success": False,
            "reason": "M2 returned no reachable shelters",
            "source": request.source,
            "distances": {},
            "primary": None,
            "backup": None,
        }

    # M3 Priority Queue ranks the shelters.
    result = manager.assign_shelter(
        distances,
        request.people,
    )

    result["source"] = request.source
    result["people"] = request.people
    result["distances"] = distances

    return result


# ============================================================
# GET SHELTER LOAD
# ============================================================

@app.get("/api/m3/shelters/{shelter_id}/load")
def get_shelter_load(shelter_id: str):

    result = manager.get_shelter_load(shelter_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Shelter not found: {shelter_id}",
        )

    return result


# ============================================================
# ADMIT PEOPLE MANUALLY
# ============================================================

@app.post("/api/m3/shelters/{shelter_id}/admit")
def admit_people(
    shelter_id: str,
    request: AdmitRequest,
):

    if request.people <= 0:
        raise HTTPException(
            status_code=400,
            detail="people must be greater than zero",
        )

    result = manager.admit_people(
        shelter_id,
        request.people,
    )

    return result


# ============================================================
# RELEASE PEOPLE
# ============================================================

@app.post("/api/m3/shelters/{shelter_id}/release")
def release_people(
    shelter_id: str,
    request: AdmitRequest,
):

    if request.people <= 0:
        raise HTTPException(
            status_code=400,
            detail="people must be greater than zero",
        )

    result = manager.release_people(
        shelter_id,
        request.people,
    )

    return result


# ============================================================
# UPDATE SHELTER STATUS
# ============================================================

@app.post("/api/m3/shelters/{shelter_id}/status")
def update_shelter_status(
    shelter_id: str,
    request: StatusRequest,
):

    result = manager.update_shelter_status(
        shelter_id,
        request.status,
        request.accessible,
    )

    return result