from math import floor
from typing import Dict, List, Optional, Tuple

from m1.graph import Graph, Node
from m1.hashmap import HashMap


class FloodHazard:
    """
    Represents one flood hazard observation.
    """

    def __init__(
        self,
        hazard_id: str,
        latitude: float,
        longitude: float,
        severity: str = "MODERATE",
        depth: Optional[float] = None,
        source: str = ""
    ):

        self.hazard_id = hazard_id
        self.latitude = latitude
        self.longitude = longitude
        self.severity = severity
        self.depth = depth
        self.source = source


class SpatialIndex:
    """
    Grid-based spatial index.

    Road nodes are grouped into geographic cells.

    HashMap is used to store:

        grid_cell -> road node IDs
    """

    def __init__(
        self,
        cell_size: float = 0.001
    ):

        self.cell_size = cell_size

        self.grid = HashMap(
            capacity=100003
        )

    def _cell_key(
        self,
        latitude: float,
        longitude: float
    ) -> Tuple[int, int]:

        row = floor(
            latitude / self.cell_size
        )

        column = floor(
            longitude / self.cell_size
        )

        return (
            row,
            column
        )

    def add_node(
        self,
        node: Node
    ):

        key = self._cell_key(
            node.latitude,
            node.longitude
        )

        existing = self.grid.get(
            key
        )

        if existing is None:

            existing = []

            self.grid.put(
                key,
                existing
            )

        existing.append(
            node.node_id
        )

    def get_nearby_nodes(
        self,
        latitude: float,
        longitude: float,
        radius_cells: int = 1
    ) -> List[str]:

        center_row, center_column = (
            self._cell_key(
                latitude,
                longitude
            )
        )

        result = []

        for row_offset in range(
            -radius_cells,
            radius_cells + 1
        ):

            for column_offset in range(
                -radius_cells,
                radius_cells + 1
            ):

                key = (
                    center_row + row_offset,
                    center_column + column_offset
                )

                nodes = self.grid.get(
                    key
                )

                if nodes:

                    result.extend(
                        nodes
                    )

        return result


def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
) -> float:

    latitude_difference = (
        latitude1 - latitude2
    )

    longitude_difference = (
        longitude1 - longitude2
    )

    return (
        latitude_difference
        * latitude_difference
        +
        longitude_difference
        * longitude_difference
    )


def find_nearest_node(
    graph: Graph,
    spatial_index: SpatialIndex,
    latitude: float,
    longitude: float
) -> Optional[str]:
    """
    Find the closest road node to a flood location.
    """

    candidates = spatial_index.get_nearby_nodes(
        latitude,
        longitude,
        radius_cells=1
    )

    if not candidates:

        candidates = spatial_index.get_nearby_nodes(
            latitude,
            longitude,
            radius_cells=3
        )

    if not candidates:

        return None

    nearest_node = None

    nearest_distance = float(
        "inf"
    )

    for node_id in candidates:

        node = graph.nodes.get(
            node_id
        )

        if node is None:
            continue

        distance = calculate_distance(
            latitude,
            longitude,
            node.latitude,
            node.longitude
        )

        if distance < nearest_distance:

            nearest_distance = distance

            nearest_node = node_id

    return nearest_node


def classify_flood_severity(
    depth: Optional[float] = None,
    category: str = ""
) -> str:
    """
    Convert flood information into a common
    hazard severity.

    Depth-based classification is preferred
    when depth information is available.
    """

    if depth is not None:

        if depth >= 5:

            return "CRITICAL"

        if depth >= 3:

            return "HIGH"

        if depth >= 1:

            return "MODERATE"

        return "LOW"

    category = category.strip().lower()

    if "very high" in category:

        return "CRITICAL"

    if "high" in category:

        return "HIGH"

    if "moderate" in category:

        return "MODERATE"

    if "low" in category:

        return "LOW"

    return "MODERATE"


def severity_to_status(
    severity: str
) -> str:
    """
    Convert flood severity into a road status.
    """

    severity = severity.upper()

    if severity == "CRITICAL":

        return "BLOCKED"

    if severity == "HIGH":

        return "BLOCKED"

    if severity == "MODERATE":

        return "RESTRICTED"

    return "RESTRICTED"


def build_spatial_index(
    graph: Graph
) -> SpatialIndex:
    """
    Build the spatial index for all road nodes.
    """

    spatial_index = SpatialIndex()

    for node in graph.get_all_nodes():

        spatial_index.add_node(
            node
        )

    return spatial_index


def apply_flood_hazards(
    graph: Graph,
    spatial_index: SpatialIndex,
    hazards: List[FloodHazard]
) -> Dict[str, List[str]]:
    """
    Map flood hazards onto the road graph.

    The nearest road node is found for each
    flood observation.

    Roads connected to affected nodes are
    updated according to flood severity.
    """

    affected_nodes = []

    affected_roads = {
        "RESTRICTED": [],
        "BLOCKED": []
    }

    for hazard in hazards:

        nearest_node = find_nearest_node(
            graph,
            spatial_index,
            hazard.latitude,
            hazard.longitude
        )

        if nearest_node is None:

            continue

        affected_nodes.append(
            nearest_node
        )

        status = severity_to_status(
            hazard.severity
        )

        for edge in graph.adjacency.get(
            nearest_node,
            []
        ):

            graph.update_road_status(
                edge.road_id,
                status
            )

            if edge.road_id not in (
                affected_roads[status]
            ):

                affected_roads[
                    status
                ].append(
                    edge.road_id
                )

    return {
        "affected_nodes": affected_nodes,
        "RESTRICTED": affected_roads[
            "RESTRICTED"
        ],
        "BLOCKED": affected_roads[
            "BLOCKED"
        ]
    }