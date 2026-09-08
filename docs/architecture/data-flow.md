# Data flow

Nothing computes astronomy at runtime. The chain is one-directional and every
arrow is a committed file.

```
JPL de440s ephemeris     HYG v4.4 + Stellarium      NASA source imagery
   (downloaded once,        modern_iau figures         (assets/images/nasa/raw/,
    data/ephemeris/,        (data/raw/, gitignored)     gitignored, large)
    gitignored)                     |                          |
        |                           |                          |
        v                           v                          v
data/scripts/               data/scripts/              data/scripts/
  orbital-positions.py        star-catalogue.py          process-textures.py
        |                           |                          |
        |                           |  <-- verified against    |
        |                           |      Hipparcos-2         |
        |                           |      (build fails on     |
        |                           |       any disagreement)  |
        v                           v                          v
data/generated/             data/generated/            assets/images/nasa/*.webp
  orbital-positions.json      stars.json                 (committed, <=2048px)
  (committed)                 constellation-lines.json
                              star-names.json
                              (committed, CC BY-SA 4.0)
        \__________________________ | _________________________/
                                    v
                    src/scenes/<level>/<level>-data.json
                      references generated files via `dataRef`
                                    |
                                    v
                              Phaser scenes
                         (+ Three.js, lazily, for
                          single-object planet renders)
```

The star branch carries an extra arrow the other two do not: a build-time check
against a source that did not produce the data. A catalogue can be internally
consistent and wrong — the rejected IAU NEC file placed Mizar 3.2 degrees off
while passing every bounds check — so `star-catalogue.py` re-checks every
emitted position against Hipparcos-2 and refuses to write on a disagreement over
30 arcseconds. See `docs/sources.md`.

## Why the generated files are committed

They are the game's input. A clean checkout must run without Python installed.
Regenerating is for when the underlying data or the sampling changes — not a
build step someone has to remember.

## The `dataRef` seam

A level marker points into generated data with a JSON pointer:

```json
"dataRef": "orbital-positions.json#/venus"
```

`data/scripts/validate-levels.py` checks the file exists. A `dataRef` to a file
no generator has written yet is a silently empty puzzle, so it fails at commit.

## What the generated ephemeris contains

Per body, sampled daily:

| Field             | Meaning                         | Used by                                                             |
| ----------------- | ------------------------------- | ------------------------------------------------------------------- |
| `raHours`         | Right ascension, hours          | Sky-position puzzles — where a body _appears_                       |
| `decDegrees`      | Declination, degrees            | Same                                                                |
| `distanceAu`      | Geocentric distance, AU         | Parallax and scale puzzles                                          |
| `helioLonDegrees` | Heliocentric ecliptic longitude | Orbit-path puzzles — Mars retrograde walks both orbits side by side |

RA is in **hours**, not degrees. `tests/test_orbital_positions.py` asserts this:
emitting degrees would span 0..360, load fine, and point every sky puzzle at the
wrong patch of sky.

## Regenerating

```bash
venv/bin/python data/scripts/orbital-positions.py --days 365 --step 1
venv/bin/python data/scripts/validate-levels.py
venv/bin/python -m pytest
```
