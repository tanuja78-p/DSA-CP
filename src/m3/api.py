from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .shelter import Shelter
from .shelter_manager import ShelterManager
from .m2_client import M2Client
from .evacuee import EvacueeGroup
from .evacuation_manager import EvacuationManager
from .storm import SevereStorm


# ============================================================
# CONFIGURATION
# ============================================================

M2_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="DEEDSF Member 3 - Evacuation, Shelter & Storm API",
    description=(
        "Member 3 API for evacuation management, shelter "
        "allocation and severe storm handling."
    ),
    version="2.0.0",
)


# ============================================================
# CORS
# ============================================================

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


# ============================================================
# MANAGERS
# ============================================================

manager = ShelterManager(SHELTERS)

evacuation_manager = EvacuationManager()

latest_storm: Optional[SevereStorm] = None


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


# ------------------------------------------------------------
# Evacuation models
# ------------------------------------------------------------

class EvacuationGroupRequest(BaseModel):
    group_id: str
    people_count: int
    source: str
    priority: int
    destination: Optional[str] = None
    backup_shelter: Optional[str] = None
    route: List[str] = []


class RouteInput(BaseModel):
    route_id: str
    capacity: int
    cost: float = 0.0


class StormRequest(BaseModel):
    wind_speed: float
    rainfall: float
    visibility: float
    affected_radius: float
    severity: str


class EvacuationSimulationRequest(BaseModel):
    total_people: int
    routes: List[RouteInput]
    base_travel_time: float = 30.0
    storm: Optional[StormRequest] = None


class ShelterAllocationRequest(BaseModel):
    source: str
    people: int = 1


# ============================================================
# HELPERS
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


def create_storm(request: StormRequest):
    return SevereStorm(
        wind_speed=request.wind_speed,
        rainfall=request.rainfall,
        visibility=request.visibility,
        affected_radius=request.affected_radius,
        severity=request.severity,
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "module": "M3",
        "module_name": "Evacuation + Shelter + Severe Storm",
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
        "shelter_count": len(manager.get_all_shelters()),
        "evacuation_groups": len(
            evacuation_manager.get_all_groups()
        ),
        "storm_active": latest_storm is not None,
    }


# ============================================================
# GET ALL SHELTERS
# ============================================================

@app.get("/api/m3/shelters")
def get_shelters():

    return {
        "module": "M3",
        "count": len(manager.get_all_shelters()),
        "shelters": [
            shelter_to_dict(shelter)
            for shelter in manager.get_all_shelters()
        ],
    }


# ============================================================
# NEW ASSIGNMENT ENDPOINT
# GET /shelters
# ============================================================

@app.get("/shelters")
def get_shelters_short():

    return {
        "count": len(manager.get_all_shelters()),
        "shelters": [
            shelter_to_dict(shelter)
            for shelter in manager.get_all_shelters()
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

    result = manager.assign_shelter(
        distances,
        request.people,
    )

    result["source"] = request.source
    result["people"] = request.people
    result["distances"] = distances

    return result


# ============================================================
# NEW ASSIGNMENT ENDPOINT
# POST /shelters/allocate
# ============================================================

@app.post("/shelters/allocate")
def allocate_shelter(
    request: ShelterAllocationRequest
):

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
            "reason": "No reachable shelters",
            "primary": None,
            "backup": None,
        }

    result = manager.assign_shelter(
        distances,
        request.people,
    )

    return {
        "success": True,
        "source": request.source,
        "people": request.people,
        "distances": distances,
        "allocation": result,
    }


# ============================================================
# M3 VERSION OF SHELTER ALLOCATION
# ============================================================

@app.post("/api/m3/shelters/allocate")
def allocate_shelter_m3(
    request: ShelterAllocationRequest
):

    return allocate_shelter(request)


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


# ============================================================
# EVACUATION GROUPS
# ============================================================

@app.post("/api/m3/evacuation/groups")
def add_evacuation_group(
    request: EvacuationGroupRequest
):

    if request.people_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="people_count must be greater than zero",
        )

    if request.priority < 1:
        raise HTTPException(
            status_code=400,
            detail="priority must be at least 1",
        )

    if evacuation_manager.get_group(
        request.group_id
    ) is not None:

        raise HTTPException(
            status_code=409,
            detail=f"Group already exists: {request.group_id}",
        )

    group = EvacueeGroup(
        group_id=request.group_id,
        people_count=request.people_count,
        source=request.source,
        priority=request.priority,
        destination=request.destination,
        backup_shelter=request.backup_shelter,
        route=request.route,
    )

    evacuation_manager.add_group(group)

    return {
        "success": True,
        "group": group.to_dict(),
    }


# ============================================================
# GET EVACUATION GROUPS
# ============================================================

@app.get("/evacuation/groups")
def get_evacuation_groups():

    groups = evacuation_manager.get_all_groups()

    return {
        "count": len(groups),
        "groups": [
            group.to_dict()
            for group in groups
        ],
        "status": evacuation_manager.get_status(),
    }


# M3-prefixed version
@app.get("/api/m3/evacuation/groups")
def get_evacuation_groups_m3():

    return get_evacuation_groups()


# ============================================================
# PROCESS NEXT EVACUATION GROUP
# ============================================================

@app.post("/api/m3/evacuation/process-next")
def process_next_evacuation_group():

    group = evacuation_manager.process_next_group()

    if group is None:
        return {
            "success": False,
            "message": "No groups waiting for evacuation",
        }

    return {
        "success": True,
        "group": group.to_dict(),
    }


# ============================================================
# MARK GROUP ARRIVED
# ============================================================

@app.post(
    "/api/m3/evacuation/groups/{group_id}/arrive"
)
def mark_group_arrived(group_id: str):

    try:
        group = evacuation_manager.mark_group_arrived(
            group_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return {
        "success": True,
        "group": group.to_dict(),
    }


# ============================================================
# EVACUATION SIMULATION
# ============================================================

@app.post("/evacuation/simulate")
def simulate_evacuation(
    request: EvacuationSimulationRequest
):

    if request.total_people <= 0:
        raise HTTPException(
            status_code=400,
            detail="total_people must be greater than zero",
        )

    if not request.routes:
        raise HTTPException(
            status_code=400,
            detail="At least one route is required",
        )

    routes = [
        {
            "route_id": route.route_id,
            "capacity": route.capacity,
            "cost": route.cost,
        }
        for route in request.routes
    ]

    storm = None

    if request.storm is not None:
        try:
            storm = create_storm(request.storm)

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            )

    result = evacuation_manager.simulate_evacuation(
        total_people=request.total_people,
        routes=routes,
        storm=storm,
        base_travel_time=request.base_travel_time,
    )

    return {
        "success": True,
        "simulation": result,
    }


# M3-prefixed version
@app.post("/api/m3/evacuation/simulate")
def simulate_evacuation_m3(
    request: EvacuationSimulationRequest
):

    return simulate_evacuation(request)


# ============================================================
# STORM
# ============================================================

@app.post("/hazards/storm")
def create_storm_event(
    request: StormRequest
):

    global latest_storm

    try:
        latest_storm = create_storm(request)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return {
        "success": True,
        "hazard": "SEVERE_STORM",
        "storm": latest_storm.to_dict(),
    }


# M3-prefixed version
@app.post("/api/m3/hazards/storm")
def create_storm_event_m3(
    request: StormRequest
):

    return create_storm_event(request)


# ============================================================
# GET CURRENT STORM
# ============================================================

@app.get("/api/m3/hazards/storm")
def get_current_storm():

    if latest_storm is None:
        return {
            "active": False,
            "storm": None,
        }

    return {
        "active": True,
        "storm": latest_storm.to_dict(),
    }


# ============================================================
# RUNNING DIRECTLY
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.m3.api:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )