let map;

let roadLayer;
let floodLayer;


/* ---------------------------------------------
   Initialize map
--------------------------------------------- */

function initializeMap() {

    map = L.map("map");

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                '&copy; OpenStreetMap contributors'
        }
    ).addTo(map);

    /*
     * Chennai approximate center.
     */
    map.setView(
        [13.0827, 80.2707],
        11
    );
}


/* ---------------------------------------------
   Create road layers
--------------------------------------------- */

async function loadRoadStatus() {

    const response = await fetch(
        "/api/m1/roads/status"
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load road status."
        );
    }

    const data = await response.json();

    /*
     * The API returns road status records.
     *
     * At this stage the frontend uses the
     * road-status information for statistics.
     *
     * Actual road geometry can be integrated
     * with the final combined dashboard.
     */

    const roads = data.roads || [];

    let safe = 0;
    let restricted = 0;
    let blocked = 0;

    roads.forEach(
        road => {

            const status =
                (road.status || "")
                .toUpperCase();

            if (status === "SAFE") {
                safe++;
            }

            else if (status === "RESTRICTED") {
                restricted++;
            }

            else if (status === "BLOCKED") {
                blocked++;
            }

        }
    );

    document.getElementById(
        "safeCount"
    ).textContent = safe.toLocaleString();

    document.getElementById(
        "restrictedCount"
    ).textContent =
        restricted.toLocaleString();

    document.getElementById(
        "blockedCount"
    ).textContent =
        blocked.toLocaleString();
}


/* ---------------------------------------------
   Load flood hazards
--------------------------------------------- */

async function loadFloodHazards() {

    const response = await fetch(
        "/api/m1/flood/hazards"
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load flood hazards."
        );
    }

    const data = await response.json();

    document.getElementById(
        "floodCount"
    ).textContent =
        data.count.toLocaleString();

    if (floodLayer) {
        map.removeLayer(floodLayer);
    }

    floodLayer = L.layerGroup();

    const hazards =
        data.hazards || [];

    hazards.forEach(
        hazard => {

            const latitude =
                parseFloat(hazard.latitude);

            const longitude =
                parseFloat(hazard.longitude);

            if (
                Number.isNaN(latitude)
                ||
                Number.isNaN(longitude)
            ) {
                return;
            }

            const severity =
                hazard.severity || "UNKNOWN";

            const depth =
                hazard.depth || "0";

            const marker =
                L.circleMarker(
                    [latitude, longitude],
                    {
                        radius: 6,
                        weight: 2,
                        fillOpacity: 0.75
                    }
                );

            marker.bindPopup(
                `
                <strong>Urban Flood Hazard</strong>
                <br>
                Hazard ID:
                ${hazard.hazard_id}
                <br>
                Severity:
                ${severity}
                <br>
                Depth:
                ${depth} m
                <br>
                Source:
                ${hazard.source}
                `
            );

            marker.addTo(
                floodLayer
            );

        }
    );

    floodLayer.addTo(map);


    /*
     * Automatically fit map around
     * flood observations.
     */

    if (hazards.length > 0) {

        const points = [];

        hazards.forEach(
            hazard => {

                const lat =
                    parseFloat(
                        hazard.latitude
                    );

                const lon =
                    parseFloat(
                        hazard.longitude
                    );

                if (
                    !Number.isNaN(lat)
                    &&
                    !Number.isNaN(lon)
                ) {

                    points.push(
                        [lat, lon]
                    );

                }

            }
        );

        if (points.length > 0) {

            map.fitBounds(
                points,
                {
                    padding: [30, 30]
                }
            );

        }

    }
}


/* ---------------------------------------------
   Load graph summary
--------------------------------------------- */

async function loadGraphSummary() {

    const response = await fetch(
        "/api/m1/graph/summary"
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load graph summary."
        );
    }

    const data = await response.json();

    document.getElementById(
        "nodeCount"
    ).textContent =
        data.nodes.toLocaleString();

    document.getElementById(
        "roadCount"
    ).textContent =
        data.physical_roads.toLocaleString();

    /*
     * Use API status counts directly.
     */

    const status =
        data.road_status || {};

    document.getElementById(
        "safeCount"
    ).textContent =
        (status.SAFE || 0)
        .toLocaleString();

    document.getElementById(
        "restrictedCount"
    ).textContent =
        (status.RESTRICTED || 0)
        .toLocaleString();

    document.getElementById(
        "blockedCount"
    ).textContent =
        (status.BLOCKED || 0)
        .toLocaleString();
}


/* ---------------------------------------------
   Load flood summary
--------------------------------------------- */

async function loadFloodSummary() {

    const response = await fetch(
        "/api/m1/flood/summary"
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load flood summary."
        );
    }

    const data = await response.json();

    const container =
        document.getElementById(
            "severityContainer"
        );

    container.innerHTML = "";

    const distribution =
        data.severity_distribution || {};

    Object.entries(
        distribution
    ).forEach(
        ([severity, count]) => {

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "severity-row";

            row.innerHTML =
                `
                <span>${severity}</span>
                <strong>
                    ${count.toLocaleString()}
                </strong>
                `;

            container.appendChild(
                row
            );

        }
    );

}


/* ---------------------------------------------
   Load complete dashboard
--------------------------------------------- */

async function loadDashboard() {

    const statusMessage =
        document.getElementById(
            "statusMessage"
        );

    statusMessage.textContent =
        "Loading...";

    statusMessage.style.color =
        "#f59e0b";

    try {

        await loadGraphSummary();

        await loadRoadStatus();

        await loadFloodHazards();

        await loadFloodSummary();

        statusMessage.textContent =
            "Live API data loaded";

        statusMessage.style.color =
            "#16a34a";

    }

    catch (error) {

        console.error(error);

        statusMessage.textContent =
            "Unable to load API data";

        statusMessage.style.color =
            "#dc2626";

    }

}


/* ---------------------------------------------
   Start application
--------------------------------------------- */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeMap();

        loadDashboard();

    }
);