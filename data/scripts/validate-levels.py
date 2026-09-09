#!/usr/bin/env python3
"""Validate every level's *-data.json against schemas/level-data.schema.json.

Build-time only. Runs from the pre-commit hook so a bad puzzle type or an
off-map marker fails at commit time rather than as a silently broken level in
a child's browser.

Beyond the schema, this checks things JSON Schema cannot express:
  - marker positions actually fall inside the level's own map bounds
  - marker ids are unique within a level
  - every content key referenced exists in content/bg/
  - every dataRef resolves — both the file under data/generated/ and the JSON
    pointer fragment inside it
  - every reward.unlocks target names something real
  - at least one marker is required, so the unlock threshold has a denominator

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


def known_level_ids() -> set[str]:
    """Level ids that actually have data committed under src/scenes/."""
    return {p.parent.name for p in REPO_ROOT.glob("src/scenes/*/*-data.json")}


def required_marker_ids(data: dict) -> list[str]:
    """Markers that count toward the unlock threshold.

    `required` defaults to true: an author who says nothing gets the safe
    reading, not a level that unlocks itself.
    """
    return [m["id"] for m in data["markers"] if m.get("required", True)]


def meets_threshold(data: dict, solved_ids: set[str]) -> bool:
    """Is this level unlocked, given the set of solved marker ids?

    The threshold is a fraction of the REQUIRED markers, and the numerator is
    `solved` intersected with `required`. Counting every solved marker against a
    required-only denominator would let a child unlock a guided level by
    finishing optional puzzles and never touching the causal spine.

    This is the canonical definition; the runtime must match it.
    """
    required = set(required_marker_ids(data))
    if not required:
        return False
    return len(required & set(solved_ids)) / len(required) >= data["unlockThreshold"]


MISSING = object()


def resolve_pointer(document: object, pointer: str) -> object:
    """Resolve an RFC 6901 JSON pointer, or return MISSING if it leads nowhere.

    A sentinel rather than None, because a pointer may legitimately resolve to
    a JSON null and that is not the same as an unresolvable pointer.
    """
    if pointer in ("", "/"):
        return document
    current = document
    for raw_token in pointer.lstrip("/").split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                return MISSING
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit() or int(token) >= len(current):
                return MISSING
            current = current[int(token)]
        else:
            return MISSING
    return current


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

    marker_ids = {marker["id"] for marker in data["markers"]}
    level_ids = known_level_ids()

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

        for target in marker.get("reward", {}).get("unlocks", []):
            if target == marker_id:
                problems.append(f"{path}: marker '{marker_id}' unlocks itself")
            elif target not in marker_ids and target not in level_ids:
                problems.append(
                    f"{path}: marker '{marker_id}' reward.unlocks '{target}' names "
                    "neither a marker in this level nor a level with data under "
                    "src/scenes/"
                )

        data_ref = marker.get("dataRef")
        if data_ref:
            filename, _, pointer = data_ref.partition("#")
            generated = GENERATED_DIR / filename
            if not generated.exists():
                problems.append(
                    f"{path}: marker '{marker_id}' dataRef points at missing "
                    f"data/generated/{filename} — run the generator script first"
                )
            else:
                try:
                    document = json.loads(generated.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    problems.append(
                        f"{path}: data/generated/{filename} is not valid JSON — {exc}"
                    )
                else:
                    if resolve_pointer(document, pointer) is MISSING:
                        problems.append(
                            f"{path}: marker '{marker_id}' dataRef '{data_ref}' "
                            f"does not resolve — nothing at '{pointer}' inside "
                            f"data/generated/{filename}"
                        )

    if data["displayName"] not in content_keys:
        problems.append(
            f"{path}: displayName '{data['displayName']}' not in content/bg/"
        )

    # The threshold is a fraction of the REQUIRED markers. With none required the
    # denominator vanishes and a guided level would unlock at zero puzzles solved.
    if not required_marker_ids(data):
        problems.append(
            f"{path}: no required markers — every marker is optional, so the "
            "unlock threshold has nothing to measure and the level unlocks at zero"
        )

    # The brief's forgiving gate: open levels unlock at 70%, guided ones at 100%.
    # Unchanged by the required/optional split — guided still means 1.0, of the
    # required markers.
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
