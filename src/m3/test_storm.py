from src.m3.storm import SevereStorm


def test_storm_engine():

    print("=" * 60)
    print("SEVERE STORM ENGINE TEST")
    print("=" * 60)

    storm = SevereStorm(
        wind_speed=100,
        rainfall=100,
        visibility=2,
        affected_radius=15,
        severity="HIGH",
    )

    # Test speed reduction
    speed_reduction = storm.get_speed_reduction()

    assert speed_reduction > 0
    assert speed_reduction <= 0.90

    print("PASS: Speed reduction")

    # Test speed factor
    speed_factor = storm.get_speed_factor()

    assert 0 < speed_factor <= 1

    print("PASS: Speed factor")

    # Test travel delay
    base_time = 30

    delay = storm.get_travel_delay(base_time)

    assert delay > base_time

    print("PASS: Travel delay")

    # Test hazard risk
    risk = storm.get_hazard_risk()

    assert 0 <= risk <= 100

    print("PASS: Hazard risk")

    # Test road restriction
    restriction = storm.get_road_restriction()

    assert restriction in {
        "OPEN",
        "RESTRICTED",
        "BLOCKED",
    }

    print("PASS: Road restriction")

    # Test rerouting decision
    rerouting = storm.requires_rerouting()

    assert isinstance(rerouting, bool)

    print("PASS: Rerouting decision")

    # Test combined effects
    effects = storm.get_effects(
        base_travel_time=30
    )

    assert "speed_reduction_percentage" in effects
    assert "speed_factor" in effects
    assert "travel_delay_minutes" in effects
    assert "hazard_risk" in effects
    assert "road_restriction" in effects
    assert "requires_rerouting" in effects

    print("PASS: Combined storm effects")

    # Test dictionary output
    data = storm.to_dict()

    assert data["wind_speed"] == 100
    assert data["rainfall"] == 100
    assert data["visibility"] == 2
    assert data["affected_radius"] == 15
    assert data["severity"] == "HIGH"

    print("PASS: Storm data export")

    print("=" * 60)
    print("ALL SEVERE STORM TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_storm_engine()