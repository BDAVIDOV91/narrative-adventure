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
    """The seven reusable types are the whole vocabulary. An eighth is a one-off
    that would need its own maintenance forever, so it must not slip in."""
    good_level["markers"][0]["puzzle"] = "invent-a-new-minigame"
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("is not one of" in p for p in problems)


def test_the_two_new_puzzle_types_are_accepted(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """gravity-drop and telescope-focus joined the enum by deliberate decision.
    Neither has an engine yet, so neither carries config."""
    good_level["markers"][0] = {
        "id": "earth-gravity-drop",
        "position": {"x": 400, "y": 400},
        "puzzle": "gravity-drop",
        "label": "puzzle.earth.sundial.label",
    }
    good_level["markers"][1] = {
        "id": "earth-telescope-focus",
        "position": {"x": 500, "y": 400},
        "puzzle": "telescope-focus",
        "label": "puzzle.earth.seasons.label",
    }
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert problems == []


def test_rotate_match_without_a_config_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """rotate-match has an engine, and the engine cannot run without knowing how
    many rounds to play and how close counts as matched."""
    del good_level["markers"][0]["config"]
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("'config' is a required property" in p for p in problems)


def test_rotate_match_rejects_a_zero_target_count(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Zero rounds is a puzzle that is solved before the child touches it."""
    good_level["markers"][0]["config"]["targets"] = 0
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("markers/0/config/targets" in p for p in problems)


def test_rotate_match_rejects_a_zero_tolerance(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """A tolerance of zero demands a pixel-exact drag — the opposite of the
    brief's forgiving gate, and unreachable for an 11-year-old."""
    good_level["markers"][0]["config"]["tolerance"] = 0
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("markers/0/config/tolerance" in p for p in problems)


def test_rotate_match_rejects_an_unknown_config_key(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """A typo'd or invented key is silently ignored at runtime, so the puzzle
    plays with defaults nobody authored."""
    good_level["markers"][0]["config"]["tollerance"] = 12
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("markers/0/config" in p for p in problems)


def test_a_type_with_no_engine_must_not_carry_config(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Six of the seven types have no engine yet, so no config shape is known.
    Pinning a guess would be worse than requiring emptiness: an authored config
    that no engine reads looks like a working setting and is not one."""
    good_level["markers"][2]["config"] = {"targets": 3, "tolerance": 5}
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("markers/2/config" in p for p in problems)


def test_a_level_with_no_required_markers_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """The threshold is a fraction of the REQUIRED markers. With none required
    the denominator vanishes and a guided level would unlock at zero puzzles."""
    for marker in good_level["markers"]:
        marker["required"] = False
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("no required markers" in p for p in problems)


def test_optional_markers_alone_never_meet_a_guided_threshold(
    validate_levels, good_level
):
    """The arithmetic hole: if solved counts every marker while the denominator
    counts only the required ones, a child unlocks a guided level by doing the
    optional puzzles and never touching the causal spine. The threshold is
    computed over `solved` intersected with `required`."""
    good_level["markers"][0]["required"] = True
    good_level["markers"][1]["required"] = False
    good_level["markers"][2]["required"] = False

    optional_only = {"earth-seasons-globe", "earth-twilight-zornitsa"}
    assert validate_levels.meets_threshold(good_level, optional_only) is False
    assert validate_levels.meets_threshold(good_level, {"earth-sundial"}) is True


def test_markers_are_required_by_default(validate_levels, good_level):
    """Omitting the flag must mean required — an author who says nothing gets
    the safe reading, not a level that unlocks itself."""
    for marker in good_level["markers"]:
        marker.pop("required", None)
    assert validate_levels.required_marker_ids(good_level) == [
        "earth-sundial",
        "earth-seasons-globe",
        "earth-twilight-zornitsa",
    ]


def test_unresolvable_data_ref_pointer_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Checking only the filename hides a broken pointer: the file exists, the
    fragment resolves to nothing, and the puzzle opens empty."""
    good_level["markers"][2]["dataRef"] = "orbital-positions.json#/venus"
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("does not resolve" in p for p in problems)


def test_dangling_reward_unlock_is_rejected(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """An unlock naming nothing is a world reaction that never fires — the
    child solves the puzzle and the promised door stays shut."""
    good_level["markers"][0]["reward"] = {"unlocks": ["earth-gate-telescope"]}
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("unlocks" in p and "earth-gate-telescope" in p for p in problems)


def test_reward_unlock_may_name_another_marker_or_a_level(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Two kinds of thing exist and can be unlocked: a marker in this level, and
    a level that has data committed. 'earth' is the only level with data so far,
    so it stands in for the level-id branch here."""
    good_level["markers"][0]["reward"] = {
        "unlocks": ["earth-twilight-zornitsa", "earth"]
    }
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert problems == []


def test_a_marker_may_not_unlock_itself(
    validate_levels, validator, content_keys, good_level, tmp_path
):
    """Self-unlocking is always an authoring slip, never a design."""
    good_level["markers"][0]["reward"] = {"unlocks": ["earth-sundial"]}
    problems = validate_levels.check_level(
        write(tmp_path, good_level), validator, content_keys
    )
    assert any("unlocks itself" in p for p in problems)


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


def test_pyright_suppressions_stay_scoped_and_explained(repo_root):
    """Type-check suppressions must not quietly spread.

    orbital-positions.py disables three pyright rules because Skyfield ships no
    py.typed marker and pyright cannot follow its `reify` descriptors or its
    vectorised timescale.utc(). That is legitimate, but a file-level suppression
    is exactly the kind of thing that gets copied into the next file and then
    hides a real defect. This pins it to the one file that has earned it.
    """
    scripts = sorted((repo_root / "data" / "scripts").glob("*.py"))
    suppressed = [p.name for p in scripts if "# pyright:" in p.read_text("utf-8")]
    assert suppressed == ["orbital-positions.py"], (
        "only orbital-positions.py may suppress pyright rules; "
        f"found suppressions in {suppressed}"
    )

    text = (repo_root / "data" / "scripts" / "orbital-positions.py").read_text("utf-8")
    assert (
        "py.typed" in text
    ), "the suppression must explain WHY, naming the untyped library"


def test_no_python_script_silences_a_whole_rule_set(repo_root):
    """A blanket `# type: ignore` on a module hides everything after it."""
    for path in sorted((repo_root / "data" / "scripts").glob("*.py")):
        first_lines = path.read_text("utf-8").splitlines()[:5]
        for line in first_lines:
            assert (
                line.strip() != "# type: ignore"
            ), f"{path.name} silences all type errors"
