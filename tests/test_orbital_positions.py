"""Sanity checks on the generated ephemeris.

These guard against the failure mode that matters most in an education game:
data that is wrong but plausible-looking. A unit slip (radians for degrees, km
for AU) produces a file that loads fine and teaches a child something false.

Marked `integration` because they read data/generated/orbital-positions.json,
which exists only after the generator has run:
    venv/bin/python data/scripts/orbital-positions.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

GENERATED = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "generated"
    / "orbital-positions.json"
)

# Real geocentric distance ranges in AU. Sourced from the bodies' orbital
# geometry: min is opposition/perigee, max is conjunction/apogee.
DISTANCE_BOUNDS_AU = {
    "moon": (0.0022, 0.0028),
    "venus": (0.26, 1.75),
    "mars": (0.37, 2.70),
    "jupiter": (3.9, 6.7),
    "saturn": (8.0, 11.1),
}


@pytest.fixture(scope="module")
def data() -> dict:
    if not GENERATED.exists():
        pytest.skip(f"{GENERATED.name} not generated yet")
    return json.loads(GENERATED.read_text("utf-8"))


def test_every_taught_body_is_present(data):
    """The levels reference these by name; a missing one is an empty puzzle."""
    for body in ("mercury", "venus", "earth", "mars", "jupiter", "saturn", "moon"):
        assert body in data["bodies"], f"{body} missing from generated positions"


def test_distances_fall_inside_real_orbital_bounds(data):
    """Catches a unit slip: km instead of AU would be off by ~1e8."""
    for body, (low, high) in DISTANCE_BOUNDS_AU.items():
        values = data["bodies"][body]["distanceAu"]
        assert low <= min(
            values
        ), f"{body} minimum distance {min(values)} below {low} AU"
        assert (
            max(values) <= high
        ), f"{body} maximum distance {max(values)} above {high} AU"


def test_right_ascension_is_in_hours_not_degrees(data):
    """RA in hours spans 0..24. If someone emits degrees it spans 0..360, and
    every sky-position puzzle silently points at the wrong patch of sky."""
    for body, values in data["bodies"].items():
        if "raHours" not in values:
            continue
        assert 0 <= min(values["raHours"]), f"{body} has negative RA"
        assert max(values["raHours"]) < 24, f"{body} RA exceeds 24h — likely degrees"


def test_declination_is_a_real_sky_angle(data):
    for body, values in data["bodies"].items():
        if "decDegrees" not in values:
            continue
        assert -90 <= min(values["decDegrees"]), f"{body} declination below -90"
        assert max(values["decDegrees"]) <= 90, f"{body} declination above +90"


def test_earth_has_no_geocentric_position(data):
    """Earth is the observer, so its geocentric position is the origin.

    Emitting it as zeros looked like data and was not: a level whose dataRef
    resolved to `earth` would have pointed at RA 0h, Dec 0 without complaining.
    The fields are omitted instead.
    """
    earth = data["bodies"]["earth"]
    for field in ("raHours", "decDegrees", "distanceAu"):
        assert field not in earth, f"earth should not carry geocentric {field}"


def test_earth_completes_one_orbit_per_year(data):
    """Earth's heliocentric longitude must advance ~360 degrees over 365 days.
    A wrong reference frame shows up here immediately."""
    longitudes = data["bodies"]["earth"]["helioLonDegrees"]
    if len(longitudes) < 300:
        pytest.skip("generated span is shorter than a year")
    advance = (longitudes[-1] - longitudes[0]) % 360
    assert 355 <= advance <= 360, f"Earth advanced {advance:.2f} deg, expected ~359"


def test_every_body_has_one_value_per_sampled_date(data):
    """Ragged arrays would silently misalign a date with a position."""
    for body, values in data["bodies"].items():
        count = len(values["dates"])
        for field in (
            "raHours",
            "decDegrees",
            "distanceAu",
            "helioLonDegrees",
            "helioDistanceAu",
        ):
            if field not in values:
                continue
            assert len(values[field]) == count, f"{body}.{field} length mismatch"


def test_no_body_has_a_constant_zero_distance_series(data):
    """A body whose distance is zero at every sample carries no information.

    Earth-from-Earth is arithmetically zero in a geocentric frame, so this
    passed the bounds checks above while being useless: a level whose dataRef
    resolved to `earth` would have silently pointed at RA 0h, Dec 0.
    """
    for body, values in data["bodies"].items():
        distances = values.get("distanceAu")
        if distances is None:
            continue
        assert any(
            value != 0 for value in distances
        ), f"{body}.distanceAu is zero at every sample — it carries no information"


def test_earth_carries_its_distance_to_the_sun(data):
    """Earth's useful distance is heliocentric, and the seasons puzzle needs it.

    This is the number that contradicts the distance-causes-seasons
    misconception: Earth is NEAREST the Sun in early January, in the middle of
    northern winter. Range is roughly 0.983 AU at perihelion to 1.017 at
    aphelion.
    """
    earth = data["bodies"]["earth"]
    assert "helioDistanceAu" in earth, "earth must carry its distance to the Sun"
    values = earth["helioDistanceAu"]
    assert 0.98 <= min(values) <= 0.99, f"perihelion looks wrong: {min(values)}"
    assert 1.01 <= max(values) <= 1.02, f"aphelion looks wrong: {max(values)}"


def test_perihelion_falls_in_northern_winter(data):
    """The fact the seasons puzzle rests on, asserted as data.

    If this ever fails, either the ephemeris frame changed or the data is wrong
    -- and the Earth level would start teaching that we are closer to the Sun in
    summer, which is the exact misconception it exists to correct.
    """
    earth = data["bodies"]["earth"]
    if "helioDistanceAu" not in earth:
        pytest.skip("heliocentric distance not generated yet")
    pairs = list(zip(earth["dates"], earth["helioDistanceAu"]))
    nearest_date, _ = min(pairs, key=lambda pair: pair[1])
    month = int(nearest_date.split("-")[1])
    assert month in (12, 1), f"perihelion fell in month {month}, expected Dec or Jan"
