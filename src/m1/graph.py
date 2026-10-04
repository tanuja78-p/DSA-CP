from dataclasses import dataclass
from typing import Dict, List
import math


@dataclass
class Node:
    """
    Represents a geographic point in the Chennai road network.
    """

    node_id: str
    latitude: float
    longitude: float


@dataclass
class Edge:
    """
    Represents a road connection between two nodes.
    """

    source: str
    destination: str
    road_id: str
    distance: float
    status: str = "SAFE"


class Graph:
    """
    Dynamic weighted graph representing the Chennai road network.

    The graph uses an adjacency list.
    """

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adjacency: Dict[str, List[Edge]] = {}

    def add_node(
        self,
        node_id: str,
        latitude: float,
        longitude: float
    ):
        """
        Add a node if it does not already exist.
        """

        if node_id not in self.nodes:

            self.nodes[node_id] = Node(
                node_id=node_id,
                latitude=latitude,
                longitude=longitude
            )

            self.adjacency[node_id] = []

    def add_edge(
        self,
        source: str,
        destination: str,
        road_id: str,
        distance: float
    ):
        """
        Add a bidirectional road connection.
        """

        if source not in self.nodes:
            raise ValueError(
                f"Source node {source} does not exist."
            )

        if destination not in self.nodes:
            raise ValueError(
                f"Destination node {destination} does not exist."
            )

        forward_edge = Edge(
            source=source,
            destination=destination,
            road_id=road_id,
            distance=distance
        )

        backward_edge = Edge(
            source=destination,
            destination=source,
            road_id=road_id,
            distance=distance
        )

        self.adjacency[source].append(
            forward_edge
        )

        self.adjacency[destination].append(
            backward_edge
        )

    def update_road_status(
        self,
        road_id: str,
        status: str
    ):
        """
        Update the condition of a road.

        Valid states:
            SAFE
            RESTRICTED
            BLOCKED
        """

        valid_statuses = {
            "SAFE",
            "RESTRICTED",
            "BLOCKED"
        }

        status = status.upper()

        if status not in valid_statuses:
            raise ValueError(
                f"Invalid road status: {status}"
            )

        for node_id in self.adjacency:

            for edge in self.adjacency[node_id]:

                if edge.road_id == road_id:
                    edge.status = status

    def get_neighbors(
        self,
        node_id: str
    ) -> List[Edge]:
        """
        Return all neighboring road segments.
        """

        return self.adjacency.get(
            node_id,
            []
        )

    def get_active_neighbors(
        self,
        node_id: str
    ) -> List[Edge]:
        """
        Return roads that are not blocked.
        """

        return [
            edge
            for edge in self.adjacency.get(
                node_id,
                []
            )
            if edge.status != "BLOCKED"
        ]

    def get_node_count(self) -> int:
        """
        Return the number of graph nodes.
        """

        return len(self.nodes)

    def get_edge_count(self) -> int:
        """
        Return the number of physical road segments.

        Each bidirectional road is stored twice,
        so divide the adjacency count by 2.
        """

        total_edges = sum(
            len(edges)
            for edges in self.adjacency.values()
        )

        return total_edges // 2

    def get_road_status(
        self,
        road_id: str
    ) -> str:
        """
        Return the current road status.
        """

        for node_id in self.adjacency:

            for edge in self.adjacency[node_id]:

                if edge.road_id == road_id:
                    return edge.status

        return "UNKNOWN"

    def get_all_nodes(self) -> List[Node]:
        """
        Return all graph nodes.
        """

        return list(
            self.nodes.values()
        )

def get_all_edges(self) -> List[Edge]:
    """
    Return every physical road segment once.

    The graph stores each road segment twice:
        source -> destination
        destination -> source

    We remove only the reverse duplicate.

    road_id is included so that different road segments
    belonging to different roads are never merged.
    """

    edges = []
    seen = set()

    for node_id in self.adjacency:

        for edge in self.adjacency[node_id]:

            endpoint_pair = tuple(
                sorted(
                    [
                        edge.source,
                        edge.destination
                    ]
                )
            )

            key = (
                edge.road_id,
                endpoint_pair
            )

            if key not in seen:

                seen.add(key)
                edges.append(edge)

    return edges


def haversine_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
) -> float:
    """
    Calculate geographic distance between two coordinates.

    Returns distance in metres.
    """

    earth_radius = 6371000

    lat1 = math.radians(latitude1)
    lat2 = math.radians(latitude2)

    delta_lat = math.radians(
        latitude2 - latitude1
    )

    delta_lon = math.radians(
        longitude2 - longitude1
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def make_node_id(
    longitude: float,
    latitude: float
) -> str:
    """
    Create a stable geographic node ID.
    """

    longitude = round(
        longitude,
        5
    )

    latitude = round(
        latitude,
        5
    )

    return (
        f"{longitude:.5f}_"
        f"{latitude:.5f}"
    )