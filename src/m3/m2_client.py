import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


class M2Client:
    """
    Client used by Member 3 to communicate with Member 2.

    M2 provides safe-route distances through:

        GET /api/m2/distance-to-shelter
    """

    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def get_distance_to_shelter(self, source, shelter_node):
        """
        Get safe-route distance from an evacuee node
        to one shelter graph node.
        """

        params = urlencode({
            "source": source,
            "shelter": shelter_node,
        })

        url = (
            f"{self.base_url}"
            f"/api/m2/distance-to-shelter"
            f"?{params}"
        )

        try:
            with urlopen(url, timeout=30) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            if not data.get("reachable"):
                return None

            return data.get("distance_meters")

        except HTTPError as error:
            raise RuntimeError(
                f"M2 returned HTTP {error.code}"
            )

        except URLError as error:
            raise RuntimeError(
                f"Could not connect to M2: {error.reason}"
            )

    def get_distances_to_shelters(
        self,
        source,
        shelter_nodes
    ):
        """
        Get safe-route distances from one evacuee
        location to multiple shelters.

        Returns:

            {
                shelter_id: distance
            }

        shelter_nodes format:

            {
                "S1": "80.26185_13.09112",
                "S2": "80.26200_13.09200"
            }
        """

        distances = {}

        for shelter_id, shelter_node in shelter_nodes.items():

            distance = self.get_distance_to_shelter(
                source,
                shelter_node
            )

            if distance is not None:
                distances[str(shelter_id)] = distance

        return distances