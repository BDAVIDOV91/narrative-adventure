#!/usr/bin/env python3
"""Validate every level's *-data.json against schemas/level-data.schema.json.

Build-time only. Runs from the pre-commit hook so a bad puzzle type or an
off-map marker fails at commit time rather than as a silently broken level in
a child's browser.

Beyond the schema, this checks things JSON Schema cannot express:
  - marker positions actually fall inside the level's own map bounds
  - marker ids are unique within a level
  - every content key referenced exists in content/bg/
  - every dataRef points at a file that exists under data/generated/

Usage:
    venv/bin/python data/scripts/validate-levels.py
    venv/bin/python data/scripts/validate-levels.py src/scenes/earth/earth-data.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "level-data.schema.json"
CONTENT_DIR = REPO_ROOT / "content" / "bg"
GENERATED_DIR = REPO_ROOT / "data" / "generated"


def load_content_keys() -> set[str]:
    keys: set[str] = set()
    for path in sorted(CONTENT_DIR.glob("*.json")):
        keys.update(json.loads(path.read_text(encoding="utf-8")).keys())
    return keys


def check_level(
    path: Path, validator: Draft202012Validator, content_keys: set[str]
) -> list[str]:
    """Return a list of human-readable problems. Empty means the level is good."""
    problems: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: not valid JSON — {exc}"]

    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in error.path) or "(root)"
        problems.append(f"{path}: {location}: {error.message}")

    # Schema passed? Then the structural checks are safe to run.
    if problems:
        return problems

    width = data["map"]["width"]
    height = data["map"]["height"]

    spawn = data["map"]["spawn"]
    if not (0 <= spawn["x"] <= width and 0 <= spawn["y"] <= height):
        problems.append(f"{path}: spawn {spawn} is outside the {width}x{height} map")

    seen: set[str] = set()
    for marker in data["markers"]:
        marker_id = marker["id"]
        if marker_id in seen:
            problems.append(f"{path}: duplicate marker id '{marker_id}'")
        seen.add(marker_id)

        pos = marker["position"]
        if not (0 <= pos["x"] <= width and 0 <= pos["y"] <= height):
            problems.append(
                f"{path}: marker '{marker_id}' at {pos} is outside the {width}x{height} map"
            )

        for key_field in ("label",):
            key = marker.get(key_field)
            if key and key not in content_keys:
                problems.append(
                    f"{path}: marker '{marker_id}' {key_field} '{key}' not in content/bg/"
                )

        fact = marker.get("reward", {}).get("fact")
        if fact and fact not in content_keys:
            problems.append(
                f"{path}: marker '{marker_id}' reward.fact '{fact}' not in content/bg/"
            )

        data_ref = marker.get("dataRef")
        if data_ref:
            filename = data_ref.split("#", 1)[0]
            if not (GENERATED_DIR / filename).exists():
                problems.append(
                    f"{path}: marker '{marker_id}' dataRef points at missing "
                    f"data/generated/{filename} — run the generator script first"
                )

    if data["displayName"] not in content_keys:
        problems.append(
            f"{path}: displayName '{data['displayName']}' not in content/bg/"
        )

    # The brief's forgiving gate: open levels unlock at 70%, guided ones at 100%.
    expected = 1.0 if data["mode"] == "guided" else 0.7
    if data["unlockThreshold"] != expected:
        problems.append(
            f"{path}: mode '{data['mode']}' expects unlockThreshold {expected}, "
            f"got {data['unlockThreshold']}"
        )

    return problems


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    content_keys = load_content_keys()

    if len(sys.argv) > 1:
        paths = [Path(a) for a in sys.argv[1:]]
    else:
        paths = sorted(REPO_ROOT.glob("src/scenes/*/*-data.json"))

    if not paths:
        print("no level data files found")
        return 0

    all_problems: list[str] = []
    for path in paths:
        problems = check_level(path, validator, content_keys)
        status = "OK" if not problems else f"{len(problems)} problem(s)"
        print(f"{path.relative_to(REPO_ROOT)}: {status}")
        all_problems.extend(problems)

    if all_problems:
        print()
        for problem in all_problems:
            print(f"  ERROR {problem}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
