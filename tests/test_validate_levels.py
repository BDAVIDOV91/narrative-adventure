"""Regression tests for the level validator.

Every test here exists because the corresponding mistake is easy to make by
hand and invisible until a child opens the level. Per the PER FIX rule, each
one must fail RED against a validator that lacks the check.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType

import pytest
from jsonschema import Draft202012Validator


@pytest.fixture()
def validator(repo_root: Path) -> Draft202012Validator:
    schema = json.loads(
        (repo_root / "schemas" / "level-data.schema.json").read_text("utf-8")
    )
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@pytest.fixture()
def content_keys(validate_levels: ModuleType) -> set[str]:
    return validate_levels.load_content_keys()


@pytest.fixture()
def good_level(repo_root: Path) -> dict:
    return json.loads(
        (repo_root / "src/scenes/earth/earth-data.json").read_text("utf-8")
    )


def write(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "level-data.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def test_the_real_earth_level_passes(
    validate_levels, validator, content_keys, repo_root
):
    """The level that ships must validate. If this fails, the game is broken."""
    path = repo_root / "src/scenes/earth/earth-data.json"
    assert validate_levels.check_level(path, validator, content_keys) == []


def test_unknown_puzzle_type_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """The five reusable types are the whole vocabulary. A sixth is a one-off
    that would need its own maintenance forever, so it must not slip in."""
    good_level["markers"][0]["puzzle"] = "invent-a-new-minigame"
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("is not one of" in p for p in problems)


def test_marker_outside_the_map_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """An off-map marker is unreachable: the player walks the level, finds
    nothing, and can never hit the unlock threshold."""
    good_level["markers"][1]["position"] = {"x": 99_999, "y": -5}
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("outside the" in p for p in problems)


def test_spawn_outside_the_map_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    good_level["map"]["spawn"] = {"x": -1, "y": 40_000}
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("spawn" in p for p in problems)


def test_duplicate_marker_ids_are_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Progress is stored per marker id. Duplicates would let one puzzle mark
    another as solved."""
    good_level["markers"][1]["id"] = good_level["markers"][0]["id"]
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("duplicate marker id" in p for p in problems)


def test_missing_content_key_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """A key with no Bulgarian string behind it renders the raw key on screen."""
    good_level["markers"][2]["reward"]["fact"] = "fact.does-not-exist"
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("not in content/bg/" in p for p in problems)


def test_missing_data_ref_file_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """dataRef is the seam between the Python output and the game. Pointing it
    at a file no generator has written yet is a silent empty puzzle."""
    good_level["markers"][2]["dataRef"] = "never-generated.json#/venus"
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("dataRef points at missing" in p for p in problems)


def test_guided_level_must_unlock_at_full_completion(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """The brief: guided levels are linear tutorials (1.0), open levels use the
    forgiving 70% gate. Mixing them up silently changes the pacing."""
    good_level["mode"] = "guided"
    good_level["unlockThreshold"] = 0.7
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("expects unlockThreshold" in p for p in problems)


def test_cyrillic_literal_in_place_of_a_content_key_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Bulgarian text belongs in content/bg/, never in level data. The schema's
    ASCII contentKey pattern is what stops it."""
    good_level["markers"][0]["label"] = "Слънчевият часовник"
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert problems, "a Cyrillic literal must not validate as a content key"
