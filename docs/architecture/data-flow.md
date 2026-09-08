# Data flow

Nothing computes astronomy at runtime. The chain is one-directional and every
arrow is a committed file.

```
JPL de440s ephemeris          NASA source imagery
   (downloaded once,             (assets/images/nasa/raw/,
    data/ephemeris/,              gitignored, large)
    gitignored)                          |
        |                                |
        v                                v
data/scripts/                    data/scripts/
  orbital-positions.py             process-textures.py
        |                                |
        v                                v
data/generated/*.json          assets/images/nasa/*.webp
  (committed)                      (committed, <=2048px)
        \                              /
         \                            /
          v                          v
        src/scenes/<level>/<level>-data.json
          references generated files via `dataRef`
                        |
                        v
                  Phaser scenes
             (+ Three.js, lazily, for
              single-object planet renders)
```

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
.venv/bin/python data/scripts/orbital-positions.py --days 365 --step 1
.venv/bin/python data/scripts/validate-levels.py
.venv/bin/python -m pytest
```
