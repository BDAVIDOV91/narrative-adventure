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
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

GENERATED = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "generated"
    / "orbital-positions.json"
)

# The four season instants inside the committed window, from docs/sources.md
# ("A year is one orbit — and the season markers on it"), computed from de440s
# in the ecliptic of date. These are the anchors the year-orbit beat renders as
# season art; if the generator drifts off them the beat labels the wrong art.
EXPECTED_SEASONS_UTC = {
    "september-equinox": datetime(2026, 9, 23, 0, 5, tzinfo=timezone.utc),
    "december-solstice": datetime(2026, 12, 21, 20, 50, tzinfo=timezone.utc),
    "march-equinox": datetime(2027, 3, 20, 20, 24, tzinfo=timezone.utc),
    "june-solstice": datetime(2027, 6, 21, 14, 11, tzinfo=timezone.utc),
}

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


def test_seasons_block_names_all_four_events(data):
    """The year-orbit beat reads a NAMED event, never a longitude crossing.

    Earth's heliocentric longitude is the Sun's geocentric longitude + 180, so
    lambda = 0 is the SEPTEMBER equinox. Anyone deriving seasons from
    helioLonDegrees mislabels every season by six months and still validates.
    An explicit block removes the choice.
    """
    assert "seasons" in data, "payload carries no seasons block"
    events = [entry["event"] for entry in data["seasons"]]
    assert set(events) == set(
        EXPECTED_SEASONS_UTC
    ), f"seasons block names {events}, expected the four solstices and equinoxes"
    assert len(events) == len(set(events)), f"duplicate season events: {events}"


def test_each_season_event_lands_on_its_known_instant(data):
    """Within a minute of the de440s instants recorded in docs/sources.md.

    A wrong reference frame (J2000 ecliptic instead of ecliptic of date) is a
    systematic -0.38 degrees, which lands the December solstice and the March
    equinox on the wrong calendar day. A one-minute tolerance catches that.
    """
    assert "seasons" in data, "payload carries no seasons block"
    found = {entry["event"]: entry["utc"] for entry in data["seasons"]}
    for event, expected in EXPECTED_SEASONS_UTC.items():
        assert event in found, f"{event} missing from the seasons block"
        actual = datetime.fromisoformat(found[event].replace("Z", "+00:00"))
        assert actual.tzinfo is not None, f"{event} instant carries no UTC marker"
        drift = abs(actual - expected)
        assert drift <= timedelta(minutes=1), (
            f"{event} at {actual.isoformat()} is {drift} from the sourced "
            f"{expected.isoformat()}"
        )


def test_season_events_are_in_chronological_order(data):
    """The beat walks the orbit; the markers must come off it in orbit order."""
    assert "seasons" in data, "payload carries no seasons block"
    instants = [
        datetime.fromisoformat(entry["utc"].replace("Z", "+00:00"))
        for entry in data["seasons"]
    ]
    assert instants == sorted(instants), "seasons block is not in time order"


def test_payload_declares_the_frame_of_its_ecliptic_longitudes(data):
    """A consumer must not be able to silently assume ecliptic of date.

    orbital-positions.py calls ecliptic_latlon() with no epoch, so
    helioLonDegrees is J2000 ecliptic. That is a defensible choice, but only if
    the file says so; undeclared it reads as ecliptic of date and is off by
    about -0.38 degrees.
    """
    assert "frame" in data, "payload does not declare the frame of helioLonDegrees"
    frame = data["frame"]
    assert isinstance(frame, str) and frame, "frame must be a non-empty string"
    assert "j2000" in frame.lower(), f"frame '{frame}' does not name an epoch"


def test_readme_states_the_earth_sun_longitude_offset(data):
    """The +180 trap is the one a future author will walk into unaided."""
    assert "180" in data["_readme"], (
        "_readme does not state that Earth's heliocentric longitude is the "
        "Sun's geocentric longitude + 180 degrees"
    )
