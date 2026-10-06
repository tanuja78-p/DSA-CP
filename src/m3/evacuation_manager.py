from src.m3.evacuation_queue import EvacuationQueue
from src.m3.population_distribution import PopulationDistributor
from src.m3.sorting_utils import SortingUtils


class EvacuationManager:
    """
    Coordinates the M3 evacuation flow.

    Responsibilities:
    - Manage evacuation groups
    - Process evacuation queue
    - Track group movement
    - Distribute population across routes
    - Rank routes using cost, traffic and congestion
    - Apply storm effects
    - Reassess evacuation routes after storms
    - Track evacuation progress
    """

    def __init__(self):
        self.queue = EvacuationQueue()
        self.population_distributor = PopulationDistributor()
        self.groups = {}

        # Track route assignments.
        self.route_assignments = {}

    # ========================================================
    # GROUP MANAGEMENT
    # ========================================================

    def add_group(self, group):
        """
        Add an evacuation group to the manager
        and place it into the waiting queue.
        """

        if group.group_id in self.groups:
            raise ValueError(
                f"Group {group.group_id} already exists"
            )

        self.groups[group.group_id] = group
        self.queue.enqueue(group)

    def get_group(self, group_id):
        """Return an evacuation group by ID."""

        return self.groups.get(group_id)

    def get_all_groups(self):
        """Return all evacuation groups."""

        return list(self.groups.values())

    def get_waiting_groups(self):
        """Return groups currently waiting in the queue."""

        return self.queue.get_all()

    # ========================================================
    # EVACUATION MOVEMENT
    # ========================================================

    def process_next_group(self):
        """
        Move the next waiting group onto its evacuation route.

        The queue changes the group status to ON_ROUTE.
        """

        group = self.queue.dequeue()

        if group is None:
            return None

        return group

    def assign_route_to_group(
        self,
        group_id,
        route
    ):
        """
        Assign a route to an evacuation group.

        route can be:
            - a route ID string
            - a list of graph nodes
            - a route dictionary
        """

        group = self.get_group(group_id)

        if group is None:
            raise ValueError(
                f"Group {group_id} not found"
            )

        group.route = route
        self.route_assignments[group_id] = route

        return group

    def get_group_route(self, group_id):
        """Return the route assigned to a group."""

        group = self.get_group(group_id)

        if group is None:
            return None

        return group.route

    def mark_group_arrived(self, group_id):
        """
        Mark a group as having reached its destination.
        """

        group = self.get_group(group_id)

        if group is None:
            raise ValueError(
                f"Group {group_id} not found"
            )

        self.queue.mark_arrived(group)

        return group

    # ========================================================
    # ROUTE RANKING
    # ========================================================

    def calculate_route_score(self, route):
        """
        Calculate an evacuation route score.

        Lower score = better route.

        Supported route fields:

            route_id
            capacity
            cost
            congestion
            traffic_flow
            feasible

        Optional fields default to safe values.

        The score combines:
            base route cost
            congestion penalty
            traffic-flow penalty
        """

        cost = float(
            route.get("cost", 0.0)
        )

        congestion = float(
            route.get("congestion", 0.0)
        )

        traffic_flow = float(
            route.get("traffic_flow", 0.0)
        )

        if cost < 0:
            raise ValueError(
                f"Cost for route {route.get('route_id')} "
                "cannot be negative"
            )

        if congestion < 0:
            raise ValueError(
                f"Congestion for route {route.get('route_id')} "
                "cannot be negative"
            )

        if traffic_flow < 0:
            raise ValueError(
                f"Traffic flow for route {route.get('route_id')} "
                "cannot be negative"
            )

        # Keep congestion within 0.0 - 1.0.
        congestion = min(
            congestion,
            1.0
        )

        # Congestion penalty.
        congestion_penalty = (
            congestion * 10.0
        )

        # Traffic-flow penalty.
        traffic_penalty = (
            traffic_flow * 0.01
        )

        return (
            cost
            + congestion_penalty
            + traffic_penalty
        )

    def rank_routes(self, routes):
        """
        Rank feasible evacuation routes.

        Routes are ranked using the custom Merge Sort.

        Lower route score = better route.

        Infeasible routes are removed before ranking.
        """

        feasible_routes = []

        for route in routes:

            feasible = route.get(
                "feasible",
                True
            )

            if not feasible:
                continue

            capacity = route.get(
                "capacity",
                0
            )

            if capacity < 0:
                raise ValueError(
                    f"Capacity for route {route.get('route_id')} "
                    "cannot be negative"
                )

            route_copy = dict(route)

            route_copy["score"] = (
                self.calculate_route_score(
                    route
                )
            )

            feasible_routes.append(
                route_copy
            )

        return SortingUtils.merge_sort(
            feasible_routes,
            key=lambda route: route["score"]
        )

    # ========================================================
    # POPULATION DISTRIBUTION
    # ========================================================

    def distribute_population(
        self,
        total_people,
        routes
    ):
        """
        Rank feasible routes and distribute
        population according to route capacity.
        """

        ranked_routes = self.rank_routes(
            routes
        )

        return self.population_distributor.distribute(
            total_people,
            ranked_routes
        )

    def assign_population_to_routes(
        self,
        total_people,
        routes
    ):
        """
        Distribute population across ranked routes.

        Returned allocations contain:
            route_id
            capacity
            assigned
            remaining_capacity
        """

        return self.distribute_population(
            total_people,
            routes
        )

    # ========================================================
    # STORM-DRIVEN ROUTE REASSESSMENT
    # ========================================================

    def apply_storm_to_routes(
        self,
        routes,
        storm
    ):
        """
        Apply storm conditions to evacuation routes.

        Each route can specify:

            storm_affected=True
                Route is directly affected by the storm.

            storm_affected=False
                Route remains available as an alternative.

        Storm-affected routes receive:
            - increased travel cost
            - increased congestion
            - possible blocking

        Unaffected routes retain their original conditions.
        """

        if storm is None:
            return [
                dict(route)
                for route in routes
            ]

        effects = storm.get_effects()

        hazard_risk = effects[
            "hazard_risk"
        ]

        road_restriction = effects[
            "road_restriction"
        ]

        speed_factor = effects[
            "speed_factor"
        ]

        if speed_factor <= 0:
            speed_factor = 0.01

        storm_routes = []

        for route in routes:

            updated_route = dict(route)

            base_cost = float(
                updated_route.get(
                    "cost",
                    0.0
                )
            )

            base_congestion = float(
                updated_route.get(
                    "congestion",
                    0.0
                )
            )

            storm_affected = updated_route.get(
                "storm_affected",
                False
            )

            # ------------------------------------------------
            # STORM-AFFECTED ROUTE
            # ------------------------------------------------

            if storm_affected:

                # Reduced speed increases travel cost.
                updated_route["cost"] = (
                    base_cost / speed_factor
                )

                # Storm hazard increases congestion.
                storm_congestion = (
                    hazard_risk / 100.0
                )

                updated_route["congestion"] = min(
                    1.0,
                    base_congestion
                    + storm_congestion
                )

                # A blocked storm condition makes
                # the affected route unusable.
                if road_restriction == "BLOCKED":

                    updated_route["feasible"] = False

                else:

                    updated_route["feasible"] = (
                        updated_route.get(
                            "feasible",
                            True
                        )
                    )

                updated_route[
                    "storm_restriction"
                ] = road_restriction

                updated_route[
                    "storm_hazard_risk"
                ] = hazard_risk

            # ------------------------------------------------
            # UNAFFECTED ROUTE
            # ------------------------------------------------

            else:

                # Keep original route conditions.
                updated_route["cost"] = (
                    base_cost
                )

                updated_route["congestion"] = (
                    base_congestion
                )

                updated_route["feasible"] = (
                    updated_route.get(
                        "feasible",
                        True
                    )
                )

                updated_route[
                    "storm_restriction"
                ] = "OPEN"

                updated_route[
                    "storm_hazard_risk"
                ] = 0.0

            updated_route[
                "storm_affected"
            ] = storm_affected

            storm_routes.append(
                updated_route
            )

        return storm_routes

    def reroute_evacuation(
        self,
        routes,
        storm=None
    ):
        """
        Reassess evacuation routes after a storm update.

        Storm conditions are applied first.
        Routes are then ranked again.

        Returns:
            Ranked routes after storm reassessment.
        """

        updated_routes = (
            self.apply_storm_to_routes(
                routes,
                storm
            )
        )

        return self.rank_routes(
            updated_routes
        )

    # ========================================================
    # STORM
    # ========================================================

    def simulate_storm_impact(
        self,
        storm,
        base_travel_time=30
    ):
        """
        Calculate the effect of a storm on evacuation.
        """

        return storm.get_effects(
            base_travel_time=base_travel_time
        )

    # ========================================================
    # COMPLETE EVACUATION SIMULATION
    # ========================================================

    def simulate_evacuation(
        self,
        total_people,
        routes,
        storm=None,
        base_travel_time=30
    ):
        """
        Run a complete evacuation simulation.

        If a storm is active:

            1. Apply storm effects to affected routes.
            2. Update route cost and congestion.
            3. Remove blocked routes.
            4. Re-rank remaining routes.
            5. Distribute evacuees according to
               updated route capacity.

        Returns:
            Dictionary containing:
            - total population
            - route allocations
            - storm effects
            - rerouting status
            - unassigned population
            - full distribution status
        """

        routes_after_storm = routes

        storm_effects = None

        # Apply storm conditions before allocation.
        if storm is not None:

            storm_effects = (
                self.simulate_storm_impact(
                    storm,
                    base_travel_time
                )
            )

            routes_after_storm = (
                self.apply_storm_to_routes(
                    routes,
                    storm
                )
            )

        # Rank and allocate using the updated routes.
        allocations = (
            self.distribute_population(
                total_people,
                routes_after_storm
            )
        )

        unassigned = (
            self.population_distributor
            .get_unassigned_people(
                total_people,
                allocations
            )
        )

        rerouting_required = False

        if storm is not None:
            rerouting_required = (
                storm.requires_rerouting()
            )

        return {
            "total_people": total_people,
            "route_allocations": allocations,
            "unassigned_people": unassigned,
            "fully_distributed": (
                unassigned == 0
            ),
            "storm_effects": storm_effects,
            "rerouting_required": (
                rerouting_required
            ),
        }

    # ========================================================
    # PROGRESS TRACKING
    # ========================================================

    def get_status(self):
        """
        Return the current evacuation system status.
        """

        waiting = 0
        on_route = 0
        arrived = 0

        people_waiting = 0
        people_on_route = 0
        people_arrived = 0

        for group in self.groups.values():

            if group.status == "WAITING":

                waiting += 1
                people_waiting += (
                    group.people_count
                )

            elif group.status == "ON_ROUTE":

                on_route += 1
                people_on_route += (
                    group.people_count
                )

            elif group.status == "ARRIVED":

                arrived += 1
                people_arrived += (
                    group.people_count
                )

        total_people = (
            people_waiting
            + people_on_route
            + people_arrived
        )

        return {
            "total_groups": len(
                self.groups
            ),

            "waiting": waiting,
            "on_route": on_route,
            "arrived": arrived,

            "queue_size": self.queue.size(),

            "total_people": total_people,
            "people_waiting": people_waiting,
            "people_on_route": people_on_route,
            "people_arrived": people_arrived,
        }