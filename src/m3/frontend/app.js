// ============================================================
// M3 FRONTEND
// Evacuation + Shelter Management + Severe Storm
// ============================================================

const API_BASE = "http://127.0.0.1:8001";


// ============================================================
// GLOBAL STATE
// ============================================================

let map = null;

let shelterMarkers = {};

let currentShelters = [];

let currentStorm = null;


// ============================================================
// DOM HELPERS
// ============================================================

function getElement(id) {
    return document.getElementById(id);
}


function setText(id, value) {
    const element = getElement(id);

    if (element) {
        element.textContent = value;
    }
}


function escapeHtml(value) {
    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ============================================================
// SYSTEM LOG
// ============================================================

function addLog(message, type = "info") {

    const log = getElement("system-log");

    if (!log) {
        return;
    }

    const now = new Date();

    const time = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });

    const entry = document.createElement("div");

    entry.className = "log-entry";

    entry.innerHTML = `
        <span class="log-time">${time}</span>
        <span>${escapeHtml(message)}</span>
    `;

    log.prepend(entry);
}


function clearLog() {

    const log = getElement("system-log");

    if (!log) {
        return;
    }

    log.innerHTML = `
        <div class="log-entry">
            <span class="log-time">--:--:--</span>
            <span>System log cleared.</span>
        </div>
    `;
}


// ============================================================
// API HELPER
// ============================================================

async function apiRequest(endpoint, options = {}) {

    const response = await fetch(
        `${API_BASE}${endpoint}`,
        {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        }
    );

    let data = null;

    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok) {

        let message = `HTTP ${response.status}`;

        if (data && data.detail) {
            message = data.detail;
        }

        throw new Error(message);
    }

    return data;
}


// ============================================================
// M3 HEALTH
// ============================================================

async function checkHealth() {

    const dot = getElement("system-status-dot");
    const text = getElement("system-status-text");

    try {

        const data = await apiRequest("/api/m3/health");

        if (dot) {
            dot.className = "status-dot online";
        }

        if (text) {
            text.textContent = "M3 ONLINE";
        }

        setText(
            "shelter-count",
            data.shelter_count ?? 0
        );

        setText(
            "group-count",
            data.evacuation_groups ?? 0
        );

        setText(
            "storm-status",
            data.storm_active
                ? "ACTIVE"
                : "INACTIVE"
        );

        addLog("Connected to M3 backend.");

        return data;

    } catch (error) {

        if (dot) {
            dot.className = "status-dot offline";
        }

        if (text) {
            text.textContent = "M3 OFFLINE";
        }

        addLog(
            `M3 connection failed: ${error.message}`,
            "error"
        );

        return null;
    }
}


// ============================================================
// MAP INITIALIZATION
// ============================================================

function initializeMap() {

    const mapElement = getElement("map");

    if (!mapElement) {
        return;
    }

    map = L.map("map").setView(
        [13.09114, 80.26176],
        16
    );


    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution:
                '&copy; OpenStreetMap contributors'
        }
    ).addTo(map);


    addLog("Emergency shelter map initialized.");
}


// ============================================================
// SHELTER MAP MARKER
// ============================================================

function getMarkerColor(status) {

    const normalized =
        String(status || "").toUpperCase();

    if (normalized === "CLOSED") {
        return "#dc2626";
    }

    if (
        normalized === "FULL" ||
        normalized === "LIMITED"
    ) {
        return "#f59e0b";
    }

    if (normalized === "RESTRICTED") {
        return "#f97316";
    }

    return "#16a34a";
}


function createShelterMarker(shelter) {

    if (!map) {
        return;
    }

    const latitude =
        Number(shelter.latitude);

    const longitude =
        Number(shelter.longitude);

    if (
        Number.isNaN(latitude) ||
        Number.isNaN(longitude)
    ) {
        return;
    }


    const color =
        getMarkerColor(shelter.status);


    const icon = L.divIcon({

        className: "",

        html: `
            <div
                style="
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    background: ${color};
                    border: 3px solid white;
                    box-shadow: 0 2px 7px rgba(0,0,0,0.35);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                "
            >
                🏠
            </div>
        `,

        iconSize: [30, 30],

        iconAnchor: [15, 15]

    });


    const popup = `
        <div style="min-width: 210px">

            <strong>
                ${escapeHtml(shelter.name)}
            </strong>

            <br>

            <span>
                ID: ${escapeHtml(shelter.shelter_id)}
            </span>

            <hr>

            <div>
                Capacity:
                <strong>${shelter.capacity}</strong>
            </div>

            <div>
                Occupied:
                <strong>${shelter.occupied}</strong>
            </div>

            <div>
                Available:
                <strong>${shelter.available_capacity}</strong>
            </div>

            <div>
                Status:
                <strong>${escapeHtml(shelter.status)}</strong>
            </div>

            <div>
                Accessible:
                <strong>
                    ${shelter.accessible ? "YES" : "NO"}
                </strong>
            </div>

        </div>
    `;


    const marker = L.marker(
        [latitude, longitude],
        { icon }
    )
        .addTo(map)
        .bindPopup(popup);


    shelterMarkers[shelter.shelter_id] =
        marker;
}


// ============================================================
// LOAD SHELTERS
// ============================================================

async function loadShelters() {

    const container =
        getElement("shelter-list");


    if (container) {

        container.innerHTML = `
            <div class="loading">
                Loading shelters...
            </div>
        `;
    }


    try {

        const data =
            await apiRequest("/api/m3/shelters");


        currentShelters =
            data.shelters || [];


        setText(
            "shelter-count",
            data.count || currentShelters.length
        );


        renderShelters(
            currentShelters
        );


        updateMap(
            currentShelters
        );


        addLog(
            `Loaded ${currentShelters.length} shelters.`
        );


        return currentShelters;


    } catch (error) {

        if (container) {

            container.innerHTML = `
                <div class="empty-state">
                    Unable to load shelters.
                    <br>
                    ${escapeHtml(error.message)}
                </div>
            `;
        }


        addLog(
            `Shelter loading failed: ${error.message}`,
            "error"
        );

        return [];
    }
}


// ============================================================
// UPDATE MAP
// ============================================================

function updateMap(shelters) {

    if (!map) {
        return;
    }


    Object.values(shelterMarkers)
        .forEach(marker => {

            map.removeLayer(marker);

        });


    shelterMarkers = {};


    shelters.forEach(
        createShelterMarker
    );


    if (shelters.length > 0) {

        const validShelters =
            shelters.filter(
                shelter =>
                    !Number.isNaN(
                        Number(shelter.latitude)
                    ) &&
                    !Number.isNaN(
                        Number(shelter.longitude)
                    )
            );


        if (validShelters.length > 0) {

            const bounds =
                L.latLngBounds(
                    validShelters.map(
                        shelter => [
                            Number(shelter.latitude),
                            Number(shelter.longitude)
                        ]
                    )
                );


            map.fitBounds(
                bounds.pad(0.25)
            );
        }
    }
}


// ============================================================
// SHELTER STATUS CLASS
// ============================================================

function getStatusClass(status) {

    const normalized =
        String(status || "").toUpperCase();


    if (normalized === "CLOSED") {
        return "badge-closed";
    }


    if (
        normalized === "FULL"
    ) {
        return "badge-full";
    }


    if (
        normalized === "LIMITED" ||
        normalized === "RESTRICTED"
    ) {
        return "badge-limited";
    }


    return "badge-safe";
}


// ============================================================
// RENDER SHELTERS
// ============================================================

function renderShelters(shelters) {

    const container =
        getElement("shelter-list");


    if (!container) {
        return;
    }


    if (!shelters.length) {

        container.innerHTML = `
            <div class="empty-state">
                No shelters available.
            </div>
        `;

        return;
    }


    container.innerHTML =
        shelters.map(shelter => {

            const capacity =
                Number(shelter.capacity || 0);

            const occupied =
                Number(shelter.occupied || 0);

            const percentage =
                capacity > 0
                    ? Math.min(
                        100,
                        Math.round(
                            occupied / capacity * 100
                        )
                    )
                    : 0;


            return `

                <div class="shelter-card">

                    <div class="shelter-card-header">

                        <div>

                            <div class="shelter-name">
                                ${escapeHtml(shelter.name)}
                            </div>

                            <div class="shelter-id">
                                ${escapeHtml(shelter.shelter_id)}
                            </div>

                        </div>

                        <span
                            class="badge ${getStatusClass(
                                shelter.status
                            )}"
                        >
                            ${escapeHtml(
                                shelter.status
                            )}
                        </span>

                    </div>


                    <div class="shelter-details">

                        <div class="shelter-detail">

                            <div class="shelter-detail-label">
                                Capacity
                            </div>

                            <div class="shelter-detail-value">
                                ${capacity}
                            </div>

                        </div>


                        <div class="shelter-detail">

                            <div class="shelter-detail-label">
                                Occupied
                            </div>

                            <div class="shelter-detail-value">
                                ${occupied}
                            </div>

                        </div>


                        <div class="shelter-detail">

                            <div class="shelter-detail-label">
                                Available
                            </div>

                            <div class="shelter-detail-value">
                                ${shelter.available_capacity}
                            </div>

                        </div>


                        <div class="shelter-detail">

                            <div class="shelter-detail-label">
                                Accessible
                            </div>

                            <div class="shelter-detail-value">
                                ${shelter.accessible ? "YES" : "NO"}
                            </div>

                        </div>

                    </div>


                    <div
                        style="
                            margin-top: 12px;
                            height: 7px;
                            background: #e2e8f0;
                            border-radius: 999px;
                            overflow: hidden;
                        "
                    >

                        <div
                            style="
                                width: ${percentage}%;
                                height: 100%;
                                background: ${
                                    percentage >= 100
                                        ? "#dc2626"
                                        : percentage >= 80
                                            ? "#f59e0b"
                                            : "#16a34a"
                                };
                            "
                        ></div>

                    </div>


                    <div
                        style="
                            margin-top: 5px;
                            text-align: right;
                            font-size: 11px;
                            color: #64748b;
                        "
                    >
                        ${percentage}% occupied
                    </div>

                </div>

            `;

        }).join("");
}


// ============================================================
// EVACUATION SIMULATION
// ============================================================

async function simulateEvacuation() {

    const people =
        Number(
            getElement("people-input")?.value
        );


    const route1Capacity =
        Number(
            getElement("route1-capacity")?.value
        );


    const route2Capacity =
        Number(
            getElement("route2-capacity")?.value
        );


    if (
        !people ||
        people <= 0
    ) {

        alert(
            "Affected population must be greater than zero."
        );

        return;
    }


    const payload = {

        total_people: people,

        routes: [

            {
                route_id: "R1",
                capacity: route1Capacity,
                cost: 10
            },

            {
                route_id: "R2",
                capacity: route2Capacity,
                cost: 20
            }

        ],

        base_travel_time: 30

    };


    const resultContainer =
        getElement("evacuation-result");


    if (resultContainer) {

        resultContainer.innerHTML = `
            <div class="loading">
                Running evacuation simulation...
            </div>
        `;
    }


    try {

        const data =
            await apiRequest(
                "/api/m3/evacuation/simulate",
                {
                    method: "POST",
                    body: JSON.stringify(payload)
                }
            );


        const simulation =
            data.simulation || {};


        renderEvacuationResult(
            simulation
        );


        setText(
            "affected-people",
            simulation.total_people ?? people
        );


        const rerouting =
            Boolean(
                simulation.rerouting_required
            );


        updateReroutingStatus(
            rerouting
        );


        addLog(
            `Evacuation simulation completed for ${people} people.`
        );


    } catch (error) {

        if (resultContainer) {

            resultContainer.innerHTML = `
                <div class="empty-state">
                    Evacuation simulation failed.
                    <br>
                    ${escapeHtml(error.message)}
                </div>
            `;
        }


        addLog(
            `Evacuation simulation failed: ${error.message}`,
            "error"
        );
    }
}


// ============================================================
// REROUTING STATUS
// ============================================================

function updateReroutingStatus(required) {

    const badge =
        getElement("rerouting-badge");


    if (!badge) {
        return;
    }


    if (required) {

        badge.className =
            "badge badge-storm";

        badge.textContent =
            "⚠ REROUTING REQUIRED";

    } else {

        badge.className =
            "badge badge-safe";

        badge.textContent =
            "ROUTES NORMAL";
    }
}


// ============================================================
// RENDER EVACUATION RESULT
// ============================================================

function renderEvacuationResult(simulation) {

    const container =
        getElement("evacuation-result");


    if (!container) {
        return;
    }


    const allocations =
        simulation.route_allocations || [];


    const totalPeople =
        simulation.total_people || 0;


    const unassigned =
        simulation.unassigned_people || 0;


    const fullyDistributed =
        Boolean(
            simulation.fully_distributed
        );


    const reroutingRequired =
        Boolean(
            simulation.rerouting_required
        );


    let rows = "";


    allocations.forEach(route => {

        rows += `

            <tr>

                <td>
                    <strong>
                        ${escapeHtml(route.route_id)}
                    </strong>
                </td>

                <td>
                    ${route.capacity}
                </td>

                <td>
                    ${route.assigned}
                </td>

                <td>
                    ${route.remaining_capacity}
                </td>

                <td>
                    <span class="badge ${
                        route.assigned > 0
                            ? "badge-safe"
                            : "badge-limited"
                    }">
                        ${
                            route.assigned > 0
                                ? "USED"
                                : "UNUSED"
                        }
                    </span>
                </td>

            </tr>

        `;
    });


    const stormEffects =
        simulation.storm_effects;


    let stormInfo = "";


    if (stormEffects) {

        stormInfo = `

            <div
                style="
                    margin-top: 15px;
                    padding: 12px;
                    border-radius: 8px;
                    background: #fff7ed;
                    border: 1px solid #fed7aa;
                "
            >

                <strong>
                    ⛈️ Storm impact detected
                </strong>

                <br>

                Hazard risk:
                ${stormEffects.hazard_risk}%

                &nbsp; | &nbsp;

                Road:
                ${escapeHtml(
                    stormEffects.road_restriction
                )}

                &nbsp; | &nbsp;

                Delay:
                ${stormEffects.travel_delay_minutes}
                min

            </div>

        `;
    }


    container.innerHTML = `

        <div class="evacuation-summary">

            <div class="result-card">

                <div class="result-card-label">
                    TOTAL PEOPLE
                </div>

                <div class="result-card-value">
                    ${totalPeople}
                </div>

            </div>


            <div class="result-card">

                <div class="result-card-label">
                    ASSIGNED
                </div>

                <div class="result-card-value">
                    ${totalPeople - unassigned}
                </div>

            </div>


            <div class="result-card">

                <div class="result-card-label">
                    UNASSIGNED
                </div>

                <div class="result-card-value">
                    ${unassigned}
                </div>

            </div>


            <div class="result-card">

                <div class="result-card-label">
                    STATUS
                </div>

                <div class="result-card-value">
                    ${
                        fullyDistributed
                            ? "COMPLETE"
                            : "PARTIAL"
                    }
                </div>

            </div>

        </div>


        <table class="route-table">

            <thead>

                <tr>
                    <th>Route</th>
                    <th>Capacity</th>
                    <th>Assigned</th>
                    <th>Remaining</th>
                    <th>Status</th>
                </tr>

            </thead>

            <tbody>

                ${
                    rows ||
                    `
                    <tr>
                        <td colspan="5">
                            No route allocations.
                        </td>
                    </tr>
                    `
                }

            </tbody>

        </table>


        ${stormInfo}


        <div
            style="
                margin-top: 12px;
                font-size: 13px;
                color: #475569;
            "
        >
            Rerouting:
            <strong>
                ${
                    reroutingRequired
                        ? "REQUIRED"
                        : "NOT REQUIRED"
                }
            </strong>
        </div>

    `;
}


// ============================================================
// SHELTER ASSIGNMENT
// ============================================================

async function assignShelter() {

    const source =
        getElement("source-node")?.value.trim();


    const people =
        Number(
            getElement("assignment-people")?.value
        );


    if (!source) {

        alert(
            "Please enter an evacuation source node."
        );

        return;
    }


    if (
        !people ||
        people <= 0
    ) {

        alert(
            "People must be greater than zero."
        );

        return;
    }


    const container =
        getElement("assignment-result");


    if (container) {

        container.innerHTML = `
            <div class="loading">
                Contacting M2 and ranking shelters...
            </div>
        `;
    }


    try {

        const data =
            await apiRequest(
                "/api/m3/assign",
                {
                    method: "POST",
                    body: JSON.stringify({
                        source: source,
                        people: people
                    })
                }
            );


        renderAssignmentResult(
            data
        );


        addLog(
            "Shelter assignment completed using M2 route distances."
        );


    } catch (error) {

        if (container) {

            container.innerHTML = `
                <div class="empty-state">
                    Shelter assignment failed.
                    <br>
                    ${escapeHtml(error.message)}
                    <br><br>
                    Make sure M2 is running on port 8000.
                </div>
            `;
        }


        addLog(
            `Shelter assignment failed: ${error.message}`,
            "error"
        );
    }
}


// ============================================================
// RENDER SHELTER ASSIGNMENT
// ============================================================

function renderAssignmentResult(data) {

    const container =
        getElement("assignment-result");


    if (!container) {
        return;
    }


    if (
        data.success === false
    ) {

        container.innerHTML = `

            <div class="empty-state">

                No feasible shelter assignment.

                <br><br>

                ${
                    escapeHtml(
                        data.reason ||
                        "No reachable shelters."
                    )
                }

            </div>

        `;

        return;
    }


    const primary =
        data.primary;


    const backup =
        data.backup;


    const distanceText =
        primary &&
        primary.distance !== undefined
            ? `${Number(primary.distance).toFixed(2)} m`
            : "N/A";


    container.innerHTML = `

        <div class="assignment-grid">

            <div class="assignment-card primary">

                <div class="assignment-title">
                    PRIMARY SHELTER
                </div>

                <div class="assignment-name">

                    ${
                        primary
                            ? escapeHtml(primary.name)
                            : "None"
                    }

                </div>

                ${
                    primary
                        ? `
                            <div class="assignment-meta">

                                Shelter ID:
                                <strong>
                                    ${escapeHtml(
                                        primary.shelter_id
                                    )}
                                </strong>

                                <br>

                                Distance:
                                <strong>
                                    ${distanceText}
                                </strong>

                                <br>

                                Available:
                                <strong>
                                    ${primary.available_capacity}
                                </strong>

                            </div>
                        `
                        : `
                            <div class="assignment-meta">
                                No primary shelter available.
                            </div>
                        `
                }

            </div>


            <div class="assignment-card backup">

                <div class="assignment-title">
                    BACKUP SHELTER
                </div>

                <div class="assignment-name">

                    ${
                        backup
                            ? escapeHtml(backup.name)
                            : "None"
                    }

                </div>

                ${
                    backup
                        ? `
                            <div class="assignment-meta">

                                Shelter ID:
                                <strong>
                                    ${escapeHtml(
                                        backup.shelter_id
                                    )}
                                </strong>

                                <br>

                                Distance:
                                <strong>
                                    ${Number(
                                        backup.distance
                                    ).toFixed(2)} m
                                </strong>

                                <br>

                                Available:
                                <strong>
                                    ${backup.available_capacity}
                                </strong>

                            </div>
                        `
                        : `
                            <div class="assignment-meta">
                                No backup shelter available.
                            </div>
                        `
                }

            </div>

        </div>


        <div
            style="
                margin-top: 15px;
                padding: 12px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 13px;
            "
        >

            Source:
            <strong>
                ${escapeHtml(data.source || "")}
            </strong>

            &nbsp; | &nbsp;

            People:
            <strong>
                ${data.people || 0}
            </strong>

        </div>

    `;
}


// ============================================================
// ACTIVATE STORM
// ============================================================

async function activateStorm() {

    const windSpeed =
        Number(
            getElement("wind-speed")?.value
        );


    const rainfall =
        Number(
            getElement("rainfall")?.value
        );


    const visibility =
        Number(
            getElement("visibility")?.value
        );


    const affectedRadius =
        Number(
            getElement("affected-radius")?.value
        );


    const severity =
        getElement("severity")?.value;


    const payload = {

        wind_speed: windSpeed,

        rainfall: rainfall,

        visibility: visibility,

        affected_radius: affectedRadius,

        severity: severity

    };


    const container =
        getElement("storm-result");


    if (container) {

        container.innerHTML = `
            <div class="loading">
                Activating severe storm...
            </div>
        `;
    }


    try {

        const data =
            await apiRequest(
                "/api/m3/hazards/storm",
                {
                    method: "POST",
                    body: JSON.stringify(payload)
                }
            );


        currentStorm =
            data.storm;


        renderStormResult(
            data.storm
        );


        updateStormHeader(
            data.storm
        );


        addLog(
            `Severe storm activated: ${severity}.`
        );


        /*
         * Refresh shelter information because
         * storm state may affect later allocation.
         */
        await loadShelters();


    } catch (error) {

        if (container) {

            container.innerHTML = `
                <div class="empty-state">
                    Storm activation failed.
                    <br>
                    ${escapeHtml(error.message)}
                </div>
            `;
        }


        addLog(
            `Storm activation failed: ${error.message}`,
            "error"
        );
    }
}


// ============================================================
// RENDER STORM
// ============================================================

function renderStormResult(storm) {

    const container =
        getElement("storm-result");


    if (!container) {
        return;
    }


    if (!storm) {

        container.innerHTML = `
            <div class="empty-state">
                No storm data available.
            </div>
        `;

        return;
    }


    const effects =
        storm.effects || {};


    container.innerHTML = `

        <div class="storm-metrics">

            <div class="storm-metric">

                <div class="storm-metric-label">
                    SEVERITY
                </div>

                <div class="storm-metric-value">
                    ${escapeHtml(
                        storm.severity
                    )}
                </div>

            </div>


            <div class="storm-metric">

                <div class="storm-metric-label">
                    WIND
                </div>

                <div class="storm-metric-value">
                    ${storm.wind_speed}
                </div>

            </div>


            <div class="storm-metric">

                <div class="storm-metric-label">
                    RAINFALL
                </div>

                <div class="storm-metric-value">
                    ${storm.rainfall}
                </div>

            </div>


            <div class="storm-metric">

                <div class="storm-metric-label">
                    VISIBILITY
                </div>

                <div class="storm-metric-value">
                    ${storm.visibility}
                </div>

            </div>


            <div class="storm-metric">

                <div class="storm-metric-label">
                    HAZARD RISK
                </div>

                <div class="storm-metric-value">
                    ${effects.hazard_risk ?? 0}%
                </div>

            </div>


            <div class="storm-metric">

                <div class="storm-metric-label">
                    ROAD STATUS
                </div>

                <div class="storm-metric-value">
                    ${escapeHtml(
                        effects.road_restriction ||
                        "OPEN"
                    )}
                </div>

            </div>

        </div>


        <div
            style="
                margin-top: 15px;
                padding: 13px;
                border-radius: 8px;
                background: #fef2f2;
                border: 1px solid #fecaca;
                color: #991b1b;
                font-size: 13px;
            "
        >

            <strong>
                Storm Effects
            </strong>

            <br><br>

            Speed reduction:
            ${effects.speed_reduction_percentage ?? 0}%

            &nbsp; | &nbsp;

            Travel delay:
            ${effects.travel_delay_minutes ?? 0} min

            &nbsp; | &nbsp;

            Rerouting:
            ${
                effects.requires_rerouting
                    ? "REQUIRED"
                    : "NOT REQUIRED"
            }

        </div>

    `;
}


// ============================================================
// STORM HEADER
// ============================================================

function updateStormHeader(storm) {

    const badge =
        getElement("storm-severity-badge");


    if (!badge) {
        return;
    }


    if (!storm) {

        badge.className =
            "badge badge-safe";

        badge.textContent =
            "NO ACTIVE STORM";

        return;
    }


    badge.className =
        "badge badge-storm";


    badge.textContent =
        `⛈ ${storm.severity}`;


    setText(
        "storm-status",
        "ACTIVE"
    );


    const effects =
        storm.effects || {};


    setText(
        "impact-storm",
        storm.severity || "ACTIVE"
    );


    setText(
        "impact-risk",
        `${effects.hazard_risk ?? 0}%`
    );


    setText(
        "impact-road",
        effects.road_restriction || "OPEN"
    );


    setText(
        "impact-rerouting",
        effects.requires_rerouting
            ? "REQUIRED"
            : "NOT REQUIRED"
    );
}


// ============================================================
// LOAD CURRENT STORM
// ============================================================

async function loadCurrentStorm() {

    try {

        const data =
            await apiRequest(
                "/api/m3/hazards/storm"
            );


        if (
            data &&
            data.active &&
            data.storm
        ) {

            currentStorm =
                data.storm;


            renderStormResult(
                currentStorm
            );


            updateStormHeader(
                currentStorm
            );

        } else {

            currentStorm = null;

            updateStormHeader(
                null
            );
        }


    } catch (error) {

        addLog(
            `Unable to load storm state: ${error.message}`,
            "error"
        );
    }
}


// ============================================================
// REFRESH DASHBOARD
// ============================================================

async function refreshDashboard() {

    addLog(
        "Refreshing M3 dashboard..."
    );


    await checkHealth();

    await loadShelters();

    await loadCurrentStorm();


    addLog(
        "M3 dashboard refresh completed."
    );
}


// ============================================================
// BUTTON EVENTS
// ============================================================

function setupEventListeners() {

    const simulateButton =
        getElement("simulate-btn");


    if (simulateButton) {

        simulateButton.addEventListener(
            "click",
            simulateEvacuation
        );
    }


    const assignButton =
        getElement("assign-btn");


    if (assignButton) {

        assignButton.addEventListener(
            "click",
            assignShelter
        );
    }


    const stormButton =
        getElement("storm-btn");


    if (stormButton) {

        stormButton.addEventListener(
            "click",
            activateStorm
        );
    }


    const refreshButton =
        getElement("refresh-map-btn");


    if (refreshButton) {

        refreshButton.addEventListener(
            "click",
            refreshDashboard
        );
    }


    const clearLogButton =
        getElement("clear-log-btn");


    if (clearLogButton) {

        clearLogButton.addEventListener(
            "click",
            clearLog
        );
    }
}


// ============================================================
// START APPLICATION
// ============================================================

async function initializeM3() {

    addLog(
        "Starting M3 frontend..."
    );


    initializeMap();


    setupEventListeners();


    await refreshDashboard();


    addLog(
        "M3 dashboard ready."
    );
}


// ============================================================
// START
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    initializeM3
);