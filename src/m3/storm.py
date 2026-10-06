class SevereStorm:
    """
    Severe Storm Engine for Member 3.

    Calculates storm severity and its effects on
    evacuation conditions.
    """

    def __init__(
        self,
        wind_speed,
        rainfall,
        visibility,
        affected_radius,
        severity,
    ):
        self.wind_speed = float(wind_speed)
        self.rainfall = float(rainfall)
        self.visibility = float(visibility)
        self.affected_radius = float(affected_radius)
        self.severity = self._normalize_severity(severity)

    def _normalize_severity(self, severity):
        """Normalize severity to LOW, MODERATE, HIGH, or EXTREME."""

        severity = str(severity).upper()

        valid_levels = {
            "LOW",
            "MODERATE",
            "HIGH",
            "EXTREME",
        }

        if severity not in valid_levels:
            raise ValueError(
                "Severity must be LOW, MODERATE, HIGH, or EXTREME"
            )

        return severity

    def get_speed_reduction(self):
        """
        Calculate percentage reduction in travel speed.
        """

        reduction = 0.0

        # Wind effect
        if self.wind_speed >= 100:
            reduction += 0.30
        elif self.wind_speed >= 70:
            reduction += 0.20
        elif self.wind_speed >= 40:
            reduction += 0.10

        # Rainfall effect
        if self.rainfall >= 100:
            reduction += 0.25
        elif self.rainfall >= 50:
            reduction += 0.15
        elif self.rainfall >= 20:
            reduction += 0.05

        # Visibility effect
        if self.visibility < 1:
            reduction += 0.20
        elif self.visibility < 3:
            reduction += 0.10
        elif self.visibility < 5:
            reduction += 0.05

        # Severity effect
        severity_penalty = {
            "LOW": 0.00,
            "MODERATE": 0.05,
            "HIGH": 0.10,
            "EXTREME": 0.20,
        }

        reduction += severity_penalty[self.severity]

        # Maximum 90% reduction
        return min(reduction, 0.90)

    def get_speed_factor(self):
        """
        Return remaining travel-speed factor.

        Example:
            30% reduction -> factor = 0.70
        """

        return 1.0 - self.get_speed_reduction()

    def get_travel_delay(self, base_travel_time):
        """
        Calculate storm-adjusted travel time.

        base_travel_time is assumed to be in minutes.
        """

        if base_travel_time < 0:
            raise ValueError(
                "base_travel_time cannot be negative"
            )

        speed_factor = self.get_speed_factor()

        if speed_factor <= 0:
            return float("inf")

        return base_travel_time / speed_factor

    def get_hazard_risk(self):
        """
        Calculate a hazard-risk score from 0 to 100.
        """

        risk = 0.0

        # Wind contribution
        risk += min(self.wind_speed / 150.0, 1.0) * 30

        # Rainfall contribution
        risk += min(self.rainfall / 150.0, 1.0) * 25

        # Visibility contribution
        visibility_risk = max(
            0.0,
            min((10.0 - self.visibility) / 10.0, 1.0)
        )

        risk += visibility_risk * 20

        # Radius contribution
        risk += min(
            self.affected_radius / 20.0,
            1.0
        ) * 10

        # Severity contribution
        severity_score = {
            "LOW": 5,
            "MODERATE": 10,
            "HIGH": 15,
            "EXTREME": 20,
        }

        risk += severity_score[self.severity]

        return min(round(risk, 2), 100.0)

    def get_road_restriction(self):
        """
        Determine road restriction caused by the storm.

        Returns:
            OPEN
            RESTRICTED
            BLOCKED
        """

        risk = self.get_hazard_risk()

        if self.severity == "EXTREME" or risk >= 80:
            return "BLOCKED"

        if self.severity == "HIGH" or risk >= 55:
            return "RESTRICTED"

        return "OPEN"

    def requires_rerouting(self):
        """
        Determine whether evacuation routes should be recalculated.
        """

        restriction = self.get_road_restriction()

        return restriction in {
            "RESTRICTED",
            "BLOCKED",
        }

    def get_effects(self, base_travel_time=30):
        """
        Return all storm effects in one dictionary.
        """

        speed_reduction = self.get_speed_reduction()
        speed_factor = self.get_speed_factor()
        travel_delay = self.get_travel_delay(
            base_travel_time
        )
        hazard_risk = self.get_hazard_risk()
        road_restriction = self.get_road_restriction()

        return {
            "speed_reduction_percentage": round(
                speed_reduction * 100,
                2,
            ),
            "speed_factor": round(
                speed_factor,
                4,
            ),
            "travel_delay_minutes": round(
                travel_delay,
                2,
            ),
            "hazard_risk": hazard_risk,
            "road_restriction": road_restriction,
            "requires_rerouting": self.requires_rerouting(),
            "affected_radius": self.affected_radius,
            "severity": self.severity,
        }

    def to_dict(self):
        """Return the storm configuration and effects."""

        return {
            "wind_speed": self.wind_speed,
            "rainfall": self.rainfall,
            "visibility": self.visibility,
            "affected_radius": self.affected_radius,
            "severity": self.severity,
            "effects": self.get_effects(),
        }