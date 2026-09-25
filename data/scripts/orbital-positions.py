#!/usr/bin/env python3
# pyright: reportAttributeAccessIssue=false, reportGeneralTypeIssues=false
# pyright: reportArgumentType=false
#
# Skyfield ships no py.typed marker, so pyright infers its API from source and
# cannot follow the `reify` lazy-property descriptors that back .hours, .degrees
# and .au, nor the dynamic dispatch behind ICRF.observe(). Every error it
# reports in this file is that inference failing, not a defect. timescale.utc()
# genuinely accepts arrays -- that vectorised call is how all 365 samples are
# produced in one pass -- but the inferred signature says int. The values are
# range-checked for real in tests/test_orbital_positions.py against known
# orbital bounds. Scoped to this file so the rest of the project keeps both
# rules enabled.
"""Precompute planetary positions into static JSON for the game to read.

Build-time only. The game never runs this — it reads the JSON this writes.

Why precompute at all: the puzzles need real geometry (where Venus actually is
at twilight, where Mars actually is when it appears to run backwards), but the
answers are deterministic. Computing them once and committing the result keeps
the game a pile of static files with no Python process behind it.

Usage:
    venv/bin/python data/scripts/orbital-positions.py
    venv/bin/python data/scripts/orbital-positions.py --start 2026-01-01 --days 730
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from skyfield import almanac
from skyfield.api import load, load_file

REPO_ROOT = Path(__file__).resolve().parents[2]
EPHEMERIS_DIR = REPO_ROOT / "data" / "ephemeris"
OUTPUT_PATH = REPO_ROOT / "data" / "generated" / "orbital-positions.json"

# de440s covers 1849-2150 in ~32MB. de440 is ~114MB and buys us centuries this
# game will never show a child. Smaller kernel = faster first run on a laptop.
EPHEMERIS_NAME = "de440s.bsp"

# Bodies the game actually teaches. Kept to the solar system on purpose: the
# brief puts anything interstellar out of scope for v1.
BODIES: dict[str, str] = {
    "mercury": "mercury barycenter",
    "venus": "venus barycenter",
    "earth": "earth",
    "mars": "mars barycenter",
    "jupiter": "jupiter barycenter",
    "saturn": "saturn barycenter",
    "moon": "moon",
}

# The frame `helioLonDegrees` is expressed in. ecliptic_latlon() with no epoch=
# returns the ecliptic and mean equinox of J2000, NOT the ecliptic of date --
# a systematic -0.38 degrees in this window (measured: -0.3758 at the September
# 2026 equinox, where the ecliptic of date gives exactly 360). That is fine for
# drawing orbit
# paths, and wrong for deciding which day an equinox falls on. Declared in the
# payload so no consumer can silently assume otherwise; the season instants are
# emitted separately instead of being derived from these longitudes.
HELIO_LON_FRAME = "ecliptic-of-J2000"

# Season events in Skyfield's almanac order. Deliberately hemisphere-neutral
# names: "spring equinox" is autumn south of the equator, and this game will
# eventually have players there.
SEASON_EVENT_KEYS = (
    "march-equinox",
    "june-solstice",
    "september-equinox",
    "december-solstice",
)


def _load_ephemeris():
    """Load the DE kernel, downloading it once into data/ephemeris/."""
    EPHEMERIS_DIR.mkdir(parents=True, exist_ok=True)
    local = EPHEMERIS_DIR / EPHEMERIS_NAME
    if local.exists():
        return load_file(str(local))
    loader = load.__class__(str(EPHEMERIS_DIR))
    return loader(EPHEMERIS_NAME)


def compute_seasons(
    ephemeris, timescale, start: date, days: int
) -> list[dict[str, str]]:
    """The solstices and equinoxes inside the generated window, as instants.

    Emitted explicitly rather than left to be derived from `helioLonDegrees`,
    because that derivation has two silent traps and a level that falls into
    either still validates:

      1. Earth's heliocentric longitude is the SUN's geocentric longitude plus
         180 degrees. Earth at lambda = 0 is the SEPTEMBER equinox, not the
         March one. Reading "0 = spring" mislabels every season by six months.
      2. Those longitudes are ecliptic-of-J2000 (see HELIO_LON_FRAME), so a
         crossing lands about 0.4 day late -- enough, with daily sampling, to
         move the December solstice and the March equinox onto the wrong
         calendar day.

    A named event has neither problem: the level asks for "june-solstice" and
    gets the instant, with no geometry to get backwards.
    """
    # If Skyfield ever reorders its season indices, this mapping must not
    # silently relabel every event. Fail the build instead.
    expected = [
        name.lower().replace(" ", "-") for name in almanac.SEASON_EVENTS_NEUTRAL
    ]
    if expected != list(SEASON_EVENT_KEYS):
        raise SystemExit(
            f"Skyfield season order changed: {expected} != {list(SEASON_EVENT_KEYS)}"
        )

    end = start + timedelta(days=days)
    times, indices = almanac.find_discrete(
        timescale.utc(start.year, start.month, start.day),
        timescale.utc(end.year, end.month, end.day),
        almanac.seasons(ephemeris),
    )
    return [
        {"event": SEASON_EVENT_KEYS[int(index)], "utc": time.utc_iso()}
        for time, index in zip(times, indices)
    ]


def compute(
    start: date, days: int, step_days: int, ephemeris, timescale
) -> dict[str, object]:
    """Geocentric apparent positions, sampled every `step_days`.

    Returns RA/Dec (where a body appears on the sky) plus distance in AU. RA/Dec
    is what a sky-watching puzzle needs; the heliocentric ecliptic longitude is
    what an orbit-path puzzle needs, so both are emitted.
    """
    earth = ephemeris["earth"]
    sun = ephemeris["sun"]

    samples = [start + timedelta(days=offset) for offset in range(0, days, step_days)]
    times = timescale.utc(
        [d.year for d in samples],
        [d.month for d in samples],
        [d.day for d in samples],
    )

    out: dict[str, object] = {}
    for key, target in BODIES.items():
        body = ephemeris[target]

        helio_lat, helio_lon, helio_distance = (
            sun.at(times).observe(body).ecliptic_latlon()
        )

        entry: dict[str, object] = {
            "dates": [d.isoformat() for d in samples],
            # Heliocentric ecliptic longitude in degrees: where the body is in
            # its orbit. This is what the Mars retrograde walk-the-orbits puzzle
            # needs to draw both paths side by side.
            "helioLonDegrees": [round(v, 6) for v in helio_lon.degrees.tolist()],
            # Distance from the Sun. For Earth this is the number that
            # contradicts the distance-causes-seasons misconception: we are
            # NEAREST the Sun in early January, in the middle of northern winter.
            "helioDistanceAu": [round(v, 8) for v in helio_distance.au.tolist()],
        }

        # Geocentric apparent position — where the body appears in our sky.
        # Meaningless for Earth itself (the observer is the origin, so every
        # value would be exactly zero), so it is omitted rather than emitted as
        # a row of zeros that looks like data and is not.
        if key != "earth":
            ra, dec, distance = earth.at(times).observe(body).apparent().radec()
            # Right ascension in hours, declination in degrees.
            entry["raHours"] = [round(v, 6) for v in ra.hours.tolist()]
            entry["decDegrees"] = [round(v, 6) for v in dec.degrees.tolist()]
            entry["distanceAu"] = [round(v, 8) for v in distance.au.tolist()]

        out[key] = entry
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--start", default=date.today().isoformat(), help="ISO start date"
    )
    parser.add_argument("--days", type=int, default=365, help="span in days")
    parser.add_argument("--step", type=int, default=1, help="sample every N days")
    args = parser.parse_args()

    start = date.fromisoformat(args.start)
    ephemeris = _load_ephemeris()
    timescale = load.timescale()
    bodies = compute(start, args.days, args.step, ephemeris, timescale)
    seasons = compute_seasons(ephemeris, timescale, start, args.days)

    payload = {
        "_readme": (
            "Generated by data/scripts/orbital-positions.py. Do not edit by hand. "
            "Per body, sampled daily: heliocentric ecliptic longitude and distance "
            "from the Sun, plus geocentric apparent RA (hours), Dec (degrees) and "
            "distance (AU) for every body except Earth, where the observer is the "
            "origin and those would all be zero. Regenerate rather than patch. "
            "helioLonDegrees is expressed in the frame named by `frame` -- it is "
            "NOT the ecliptic of date. Do NOT derive seasons from it: Earth's "
            "heliocentric longitude is the Sun's geocentric longitude + 180 "
            "degrees, so Earth at 0 degrees is the SEPTEMBER equinox, 90 the "
            "December solstice, 180 the March equinox and 270 the June solstice. "
            "Read the `seasons` block instead, which names each event and gives "
            "its UTC instant."
        ),
        "source": f"JPL {EPHEMERIS_NAME} via Skyfield",
        "generated": date.today().isoformat(),
        "start": start.isoformat(),
        "days": args.days,
        "stepDays": args.step,
        "frame": HELIO_LON_FRAME,
        "seasons": seasons,
        "bodies": bodies,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
