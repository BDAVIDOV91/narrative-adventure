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
        assert 0 <= min(values["raHours"]), f"{body} has negative RA"
        assert max(values["raHours"]) < 24, f"{body} RA exceeds 24h — likely degrees"


def test_declination_is_a_real_sky_angle(data):
    for body, values in data["bodies"].items():
        assert -90 <= min(values["decDegrees"]), f"{body} declination below -90"
        assert max(values["decDegrees"]) <= 90, f"{body} declination above +90"


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
        for field in ("raHours", "decDegrees", "distanceAu", "helioLonDegrees"):
            assert len(values[field]) == count, f"{body}.{field} length mismatch"
