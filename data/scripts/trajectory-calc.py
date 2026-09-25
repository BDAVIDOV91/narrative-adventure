#!/usr/bin/env python3
"""Precompute simplified transfer-window data for the Saturn ring-threading and
Mars trajectory puzzles.

Build-time only. Not implemented yet — the signature and output contract are
settled so the level data can already reference the file it will produce.

Output contract (data/generated/mars-trajectory.json):
    {
      "_readme": "...",
      "windows": [
        {"departure": "2026-11-02", "arrivalDays": 259, "relativeCost": 0.71},
        ...
      ]
    }

`relativeCost` is deliberately unitless and normalised to 0..1. The brief's
hide-the-math rule means the player never sees a delta-v figure — they see one
path costing visibly less than another.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "data" / "generated" / "mars-trajectory.json"


def main() -> int:
    raise NotImplementedError(
        "trajectory-calc is not built yet. It runs after the Mars level design "
        "settles which quantities the puzzle actually needs."
    )


if __name__ == "__main__":
    raise SystemExit(main())
