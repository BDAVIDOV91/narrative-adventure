#!/usr/bin/env python3
"""Precompute the scale comparisons the Jupiter level teaches.

Build-time only. Not implemented yet — the signature and output contract are
settled so the level data can already reference the file it will produce.

Output contract (data/generated/earth-mars-distances.json and friends):
    {
      "_readme": "...",
      "bodies": {
        "jupiter": {"radiusKm": 69911, "earthRadii": 10.97},
        ...
      }
    }

Radii are real. How they are *shown* is the puzzle's business — the brief's
hide-the-math rule means the player compares sizes visually rather than reading
a number, so this file feeds a drawing, not a label.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "data" / "generated" / "earth-mars-distances.json"


def main() -> int:
    raise NotImplementedError(
        "distance-scale is not built yet. It runs after the Jupiter level design "
        "settles which comparisons the puzzle actually shows."
    )


if __name__ == "__main__":
    raise SystemExit(main())
