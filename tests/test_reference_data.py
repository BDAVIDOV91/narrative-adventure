"""Guards on the hand-authored reference tables in data/reference/.

These are NOT generator output -- data/generated/ is reserved for that
(docs/architecture/data-flow.md). They are values transcribed from cited
sources, which is exactly the failure mode rule 1 exists for: a typo here
loads, validates and teaches a child something false.

Two of these tests exist because docs/sources.md records a specific trap:

  - Saturn's two fact-sheet columns straddle Earth in OPPOSITE directions
    (11.19 m/s2 is 1.14x Earth, 8.96 m/s2 is 0.92x Earth), so "a stone falls
    slower on Saturn" is an artefact of picking a column. Saturn must not
    reach the drop comparison at all.
  - Mercury (3.70) and Mars (3.73) are the same number at summary precision,
    so a "which pulls harder" pair built from them asks a child to see a
    difference that is not there.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

REFERENCE = Path(__file__).resolve().parents[1] / "data" / "reference"
GENERATED = Path(__file__).resolve().parents[1] / "data" / "generated"

GRAVITY_PATH = REFERENCE / "surface-gravity.json"
DAY_LENGTH_PATH = REFERENCE / "day-length-sofia.json"


def _load(path: Path) -> dict:
    assert path.exists(), f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def gravity() -> dict:
    return _load(GRAVITY_PATH)


@pytest.fixture(scope="module")
def day_length() -> dict:
    return _load(DAY_LENGTH_PATH)


def _gravity_rows(gravity: dict) -> list[dict]:
    return list(gravity["dropComparison"]) + list(gravity["excluded"])


def _by_body(rows: list[dict]) -> dict[str, dict]:
    return {row["body"]: row for row in rows}


# --- surface gravity -------------------------------------------------------


def test_every_gravity_row_cites_a_source_and_a_retrieval_date(gravity):
    """An uncited number is a number nobody checked.

    The live NSSDCA fact-sheet URLs 302-redirect to a landing page, so the
    citation must be the dated Wayback snapshot, not the dead address.
    """
    for row in _gravity_rows(gravity):
        body = row.get("body", "(unnamed)")
        assert row.get("sourceUrl"), f"{body} carries no sourceUrl"
        assert "web.archive.org" in row["sourceUrl"], (
            f"{body} cites {row['sourceUrl']} -- the live nssdc.gsfc.nasa.gov "
            "fact-sheet URLs are dead and must not be cited"
        )
        assert row.get("accessed"), f"{body} carries no accessed date"
        date.fromisoformat(row["accessed"])


def test_every_gravity_row_declares_metres_per_second_squared(gravity):
    """A unit slip here makes the Moon drop look like the Jupiter drop."""
    for row in _gravity_rows(gravity):
        assert (
            row.get("unit") == "m/s2"
        ), f"{row.get('body')} unit is {row.get('unit')!r}, expected 'm/s2'"


def test_every_gravity_row_names_the_fact_sheet_column_it_came_from(gravity):
    """Which column matters: it is the whole reason Saturn is excluded."""
    for row in _gravity_rows(gravity):
        assert row.get("factSheetLabel"), f"{row.get('body')} names no fact-sheet row"


def test_the_drop_comparison_runs_moon_mars_earth_jupiter(gravity):
    """The visible ordering the beat teaches: floating, then quicker, then hard.

    Asserted on the values, not on the array order, so a reordered file that
    still claims Moon-to-Jupiter cannot pass by accident.
    """
    rows = _by_body(list(gravity["dropComparison"]))
    for body in ("moon", "mars", "earth", "jupiter"):
        assert body in rows, f"{body} missing from the drop comparison"
    ordered = ["moon", "mars", "earth", "jupiter"]
    values = [rows[body]["value"] for body in ordered]
    assert values == sorted(values), (
        f"surface gravity does not increase Moon < Mars < Earth < Jupiter: "
        f"{dict(zip(ordered, values))}"
    )
    assert [row["body"] for row in gravity["dropComparison"]] == ordered


def test_saturn_is_absent_from_the_drop_comparison(gravity):
    """docs/sources.md: NOT ATTESTED for this beat, and it has no surface.

    11.19 m/s2 is 1.14x Earth and 8.96 m/s2 is 0.92x Earth -- the two published
    columns disagree about whether a stone falls faster or slower than at home.
    """
    bodies = [row["body"] for row in gravity["dropComparison"]]
    assert "saturn" not in bodies, (
        "Saturn is in the drop comparison; its fact-sheet columns straddle "
        "Earth in opposite directions, so no honest drop can be shown"
    )
    excluded = _by_body(list(gravity["excluded"]))
    assert "saturn" in excluded, "Saturn must stay recorded as deliberately excluded"
    assert excluded["saturn"].get("reason"), "Saturn's exclusion carries no reason"


def test_mercury_and_mars_cannot_form_a_which_pulls_harder_pair(gravity):
    """3.70 vs 3.73 is invisible -- the Alioth/Dubhe trap in another costume."""
    bodies = [row["body"] for row in gravity["dropComparison"]]
    assert not (
        "mercury" in bodies and "mars" in bodies
    ), "Mercury and Mars are both 3.7 at summary precision and must not be paired"


def test_jupiter_outweighs_earth_under_both_published_columns(gravity):
    """The test Saturn fails and Jupiter passes, made explicit.

    Jupiter is stronger than Earth whether you read the mean 1-bar figure or
    the equatorial one, so the beat's claim survives the column choice.
    """
    rows = _by_body(list(gravity["dropComparison"]))
    earth = rows["earth"]["value"]
    jupiter = rows["jupiter"]
    assert jupiter["value"] > earth
    assert "equatorialValue" in jupiter, "Jupiter must record its second column too"
    assert jupiter["equatorialValue"] > earth, (
        "Jupiter's equatorial figure does not exceed Earth's -- the claim would "
        "then depend on a column choice, exactly as Saturn's does"
    )


# --- day length ------------------------------------------------------------

SEASON_EVENTS = (
    "september-equinox",
    "december-solstice",
    "march-equinox",
    "june-solstice",
)


def test_day_length_covers_all_four_season_events(day_length):
    events = [row["event"] for row in day_length["days"]]
    assert set(events) == set(SEASON_EVENTS), f"day length covers {events}"


def test_every_day_length_row_cites_a_source_and_a_retrieval_date(day_length):
    assert day_length.get("sourceUrl"), "no USNO source recorded"
    assert day_length.get("accessed"), "no retrieval date recorded"
    date.fromisoformat(day_length["accessed"])
    for row in day_length["days"]:
        date.fromisoformat(row["date"])


def test_the_equinox_day_is_longer_than_twelve_hours(day_length):
    """Refraction and the Sun's own disc, not a rounding artefact.

    Equal day and night is the intuitive picture and it is wrong by about
    seven minutes. A future edit that "tidies" this to exactly 12 h would make
    the beat's arcs a lie, so the strict inequality is pinned.
    """
    rows = {row["event"]: row for row in day_length["days"]}
    for event in ("march-equinox", "september-equinox"):
        minutes = rows[event]["durationMinutes"]
        assert minutes > 720, (
            f"{event} day length is {minutes} minutes -- the equinox day is "
            "longer than 12 hours, never exactly half"
        )
        assert minutes < 735, f"{event} day length {minutes} is implausibly long"


def test_each_duration_matches_its_own_sunrise_and_sunset(day_length):
    """Catches a transcription slip in any one of the three fields."""
    for row in day_length["days"]:
        rise_h, rise_m = (int(part) for part in row["sunrise"].split(":"))
        set_h, set_m = (int(part) for part in row["sunset"].split(":"))
        span = (set_h * 60 + set_m) - (rise_h * 60 + rise_m)
        assert span == row["durationMinutes"], (
            f"{row['event']}: {row['sunrise']}-{row['sunset']} is {span} minutes, "
            f"but durationMinutes says {row['durationMinutes']}"
        )


def test_the_longest_day_is_about_seventeen_tenths_of_the_shortest(day_length):
    """The contrast the beat is built on: summer is about 1.7x winter."""
    rows = {row["event"]: row for row in day_length["days"]}
    ratio = rows["june-solstice"]["durationMinutes"] / (
        rows["december-solstice"]["durationMinutes"]
    )
    assert 1.65 <= ratio <= 1.75, f"summer/winter day-length ratio is {ratio:.3f}"


def test_the_shortest_day_is_the_december_solstice(day_length):
    """The tilt story fails outright if the extremes land on the wrong dates."""
    rows = day_length["days"]
    shortest = min(rows, key=lambda row: row["durationMinutes"])
    longest = max(rows, key=lambda row: row["durationMinutes"])
    assert shortest["event"] == "december-solstice"
    assert longest["event"] == "june-solstice"


@pytest.mark.integration
def test_day_length_dates_agree_with_the_generated_ephemeris(day_length):
    """The two halves of this beat must name the same four days.

    The day-length table is transcribed from USNO; the season instants are
    computed from de440s. If they ever disagree, the level would draw a
    solstice arc on a day that is not the solstice.
    """
    path = GENERATED / "orbital-positions.json"
    if not path.exists():
        pytest.skip("orbital-positions.json not generated yet")
    seasons = json.loads(path.read_text(encoding="utf-8"))["seasons"]
    computed = {entry["event"]: entry["utc"][:10] for entry in seasons}
    for row in day_length["days"]:
        assert row["date"] == computed[row["event"]], (
            f"{row['event']}: USNO table says {row['date']}, the ephemeris says "
            f"{computed[row['event']]}"
        )
