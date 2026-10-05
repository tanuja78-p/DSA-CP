from .shelter import Shelter
from .hash_map import ShelterHashMap
from .bst import ShelterBST
from .priority_queue import ShelterPriorityQueue


class ShelterManager:
    """
    Member 3 - Shelter Management System.

    Responsibilities:
        - Store shelters using custom HashMap
        - Organize shelters using BST
        - Rank shelters using Priority Queue
        - Track shelter occupancy
        - Assign primary and backup shelters
        - Integrate with M2 safe-route distances
    """

    def __init__(self, shelters=None):
        self.shelters = ShelterHashMap()
        self.bst = ShelterBST()

        if shelters:
            for shelter in shelters:
                self.add_shelter(shelter)

    # =========================================================
    # SHELTER STORAGE
    # =========================================================

    def add_shelter(self, shelter):
        """
        Add a shelter to the HashMap and BST.
        """

        if not isinstance(shelter, Shelter):
            raise TypeError("Expected Shelter object")

        self.shelters.put(
            shelter.shelter_id,
            shelter
        )

        self.bst.insert(shelter)
        
    def add_shelters(self, shelters):
        """
        Add multiple shelters at once.
        Kept for compatibility with the Member 3 test suite.
        """

        for shelter in shelters:
            self.add_shelter(shelter)
    def get_shelter(self, shelter_id):
        """
        Return shelter using its ID.
        """

        return self.shelters.get(shelter_id)

    def remove_shelter(self, shelter_id):
        """
        Remove a shelter from the HashMap.

        BST is rebuilt afterwards so that stale entries
        are not left behind.
        """

        shelter = self.shelters.get(shelter_id)

        if shelter is None:
            return False

        self.shelters.remove(shelter_id)
        self.rebuild_bst()

        return True

    def get_all_shelters(self):
        """
        Return all shelters.
        """

        return self.shelters.values()

    def get_shelter_count(self):
        """
        Return total number of shelters.
        """

        return len(self.shelters)

    # =========================================================
    # BST
    # =========================================================

    def rebuild_bst(self):
        """
        Rebuild BST from current shelter data.

        This is useful after occupancy changes because
        available capacity changes.
        """

        self.bst.clear()

        for shelter in self.shelters.values():
            self.bst.insert(shelter)

    def get_capacity_order(self):
        """
        Return shelters ordered by available capacity.

        Highest available capacity comes first.
        """

        self.rebuild_bst()

        return self.bst.reverse_inorder()

    # =========================================================
    # OCCUPANCY
    # =========================================================

    def get_shelter_load(self, shelter_id):
        """
        Return occupancy information for a shelter.
        """

        shelter = self.get_shelter(shelter_id)

        if shelter is None:
            return None

        return {
            "shelter_id": shelter.shelter_id,
            "name": shelter.name,
            "capacity": shelter.capacity,
            "occupied": shelter.occupied,
            "available": shelter.available_capacity,
            "occupancy_percentage": shelter.occupancy_percentage,
            "status": shelter.status,
            "accessible": shelter.accessible
        }

    def admit_people(self, shelter_id, people):
        """
        Admit people into a shelter.
        """

        shelter = self.get_shelter(shelter_id)

        if shelter is None:
            return False

        shelter.add_occupants(people)

        self.rebuild_bst()

        return True

    def release_people(self, shelter_id, people):
        """
        Release people from a shelter.
        """

        shelter = self.get_shelter(shelter_id)

        if shelter is None:
            return False

        shelter.remove_occupants(people)

        self.rebuild_bst()

        return True

    def update_shelter_status(
        self,
        shelter_id,
        status
    ):
        """
        Update shelter status.
        """

        shelter = self.get_shelter(shelter_id)

        if shelter is None:
            return False

        shelter.status = status.upper()

        self.rebuild_bst()

        return True

    # =========================================================
    # SUITABILITY
    # =========================================================

    def _status_score(self, shelter):
        """
        Convert shelter safety status into a score.

        Lower score = better shelter.
        """

        status = str(
            shelter.status
        ).upper()

        if status in {
            "SAFE",
            "OPEN",
            "AVAILABLE"
        }:
            return 0.0

        if status in {
            "RESTRICTED",
            "LIMITED"
        }:
            return 0.5

        return 1.0

    def _accessibility_score(self, shelter):
        """
        Accessible shelters receive a better score.
        """

        return 0.0 if shelter.accessible else 1.0

    def suitability_score(
        self,
        shelter,
        distance
    ):
        """
        Calculate shelter suitability.

        Factors:
            - distance
            - available capacity
            - shelter status
            - accessibility

        Lower score = better shelter.
        """

        if shelter.capacity > 0:
            capacity_ratio = (
                shelter.available_capacity
                / shelter.capacity
            )
        else:
            capacity_ratio = 0.0

        distance_score = float(distance) / 10000.0

        status_score = self._status_score(
            shelter
        )

        accessibility_score = (
            self._accessibility_score(
                shelter
            )
        )

        score = (
            distance_score
            + (1.0 - capacity_ratio)
            + status_score
            + accessibility_score
        )

        return score

    # =========================================================
    # SHELTER ASSIGNMENT
    # =========================================================

    def assign_shelter(
        self,
        distances,
        people=1
    ):
        """
        Assign the best primary and backup shelters.

        Parameters:
            distances:
                Dictionary:
                    {
                        shelter_id: distance_in_metres
                    }

            people:
                Number of evacuees.

        Returns:
            Dictionary containing:
                primary
                backup
                ranked
                occupancy
        """

        if people <= 0:
            raise ValueError(
                "people must be greater than zero"
            )

        queue = ShelterPriorityQueue()

        ranked = []

        for shelter_id, distance in distances.items():

            shelter = self.get_shelter(
                str(shelter_id)
            )

            if shelter is None:
                continue

            if not shelter.is_available():
                continue

            if shelter.available_capacity < people:
                continue

            if distance is None:
                continue

            score = self.suitability_score(
                shelter,
                distance
            )

            details = {
                "distance": float(distance),
                "available_capacity":
                    shelter.available_capacity,
                "score": score
            }

            queue.push(
                score,
                shelter,
                details
            )

        while not queue.is_empty():

            item = queue.pop()

            ranked.append({
                "shelter_id":
                    item.shelter.shelter_id,

                "name":
                    item.shelter.name,

                "distance":
                    item.details["distance"],

                "available_capacity":
                    item.details[
                        "available_capacity"
                    ],

                "score":
                    item.details["score"]
            })

        primary = None
        backup = None

        if len(ranked) >= 1:
            primary = ranked[0]

        if len(ranked) >= 2:
            backup = ranked[1]

        return {
            "success": primary is not None,
            "primary": primary,
            "backup": backup,
            "ranked": ranked,
            "occupancy": {
                "people": people
            }
        }

    # =========================================================
    # DISTANCE SORTING
    # =========================================================

    def sorted_shelters_by_distance(
        self,
        distances
    ):
        """
        Return shelters sorted by distance.
        """

        records = []

        for shelter_id, distance in distances.items():

            shelter = self.get_shelter(
                str(shelter_id)
            )

            if shelter is None:
                continue

            records.append(
                (
                    float(distance),
                    shelter
                )
            )

        records.sort(
            key=lambda item: item[0]
        )

        return records

    # =========================================================
    # M2 INTEGRATION
    # =========================================================

    def assign_shelter_from_m2(
        self,
        source,
        shelter_nodes,
        people=1,
        m2_base_url="http://127.0.0.1:8000"
    ):
        """
        Complete M2 -> M3 integration.

        M2 calculates safe-route distances.

        M3 receives those distances and then:
            1. checks shelter capacity
            2. evaluates shelter suitability
            3. uses Priority Queue
            4. selects primary shelter
            5. selects backup shelter
        """

        from .m2_client import M2Client

        client = M2Client(
            m2_base_url
        )

        distances = (
            client.get_distances_to_shelters(
                source,
                shelter_nodes
            )
        )

        if not distances:
            return {
                "success": False,
                "reason":
                    "No reachable shelter found by M2",
                "primary": None,
                "backup": None,
                "ranked": [],
                "distances": {},
                "source": source
            }

        result = self.assign_shelter(
            distances,
            people
        )

        result["distances"] = distances
        result["source"] = source

        return result

    # =========================================================
    # M2 DISTANCE HELPER
    # =========================================================

    def get_distances_from_m2(
        self,
        source,
        shelter_nodes,
        m2_base_url="http://127.0.0.1:8000"
    ):
        """
        Ask M2 for distances to all supplied shelters.

        Returns:

            {
                shelter_id: distance
            }
        """

        from .m2_client import M2Client

        client = M2Client(
            m2_base_url
        )

        return client.get_distances_to_shelters(
            source,
            shelter_nodes
        )

    # =========================================================
    # COMPLETE ASSIGNMENT WORKFLOW
    # =========================================================

    def assign_and_admit_from_m2(
        self,
        source,
        shelter_nodes,
        people=1,
        m2_base_url="http://127.0.0.1:8000"
    ):
        """
        Complete evacuation workflow.

        1. M2 calculates safe distances.
        2. M3 selects primary shelter.
        3. M3 selects backup shelter.
        4. People are admitted to the primary shelter.
        """

        result = self.assign_shelter_from_m2(
            source=source,
            shelter_nodes=shelter_nodes,
            people=people,
            m2_base_url=m2_base_url
        )

        if not result.get("success"):
            return result

        primary = result.get("primary")

        if primary is None:
            return result

        primary_id = primary["shelter_id"]

        admitted = self.admit_people(
            primary_id,
            people
        )

        result["admitted"] = admitted

        if admitted:
            result["final_load"] = (
                self.get_shelter_load(
                    primary_id
                )
            )

        return result