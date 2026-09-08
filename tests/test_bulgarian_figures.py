"""Guards on the Bulgarian folk figure resolver.

Unlike the international constellations, Ралица and Колата are authored by hand
from the ethnographic literature. That makes them the one place in the star
pipeline where a human types something, so the checks here are about what a
human gets wrong: a designation that does not exist, a figure whose folklore
claim is not sourced yet, a part labelled but never drawn.

The resolver refuses rather than degrades. A Bulgarian constellation drawn with
a limb missing would go unnoticed by everyone except the audience.
"""

from __future__ import annotations

import json

import pytest

from conftest import load_script


@pytest.fixture(scope="module")
def script():
    return load_script("bulgarian-figures")


@pytest.fixture(scope="module")
def designations(script) -> dict[str, int]:
    return script.load_designations()


@pytest.fixture(scope="module")
def star_hips(script) -> set[int]:
    return script.load_star_hips()


CONTENT_KEYS = {"figure.test.name", "figure.test.part"}


def make_figure(**overrides) -> dict:
    """A minimal valid figure: the Big Dipper bowl, which is not in doubt."""
    figure = {
        "id": "test",
        "constellation": "UMa",
        "nameKey": "figure.test.name",
        "status": "VERIFIED",
        "source": "test fixture",
        "parts": [
            {
                "id": "bowl",
                "nameKey": "figure.test.part",
                "stars": ["Alp UMa", "Bet UMa"],
            }
        ],
        "lines": [["Alp UMa", "Bet UMa"]],
    }
    figure.update(overrides)
    return figure


def test_bayer_designations_resolve_to_the_right_stars(designations):
    """Spot-check against the catalogue: these are the stars Колата is made of."""
    assert designations["Alp UMa"] == 54061  # Dubhe
    assert designations["Bet UMa"] == 53910  # Merak
    assert designations["Eps UMa"] == 62956  # Alioth
    assert designations["Zet UMa"] == 65378  # Mizar
    assert designations["Eta UMa"] == 67301  # Alkaid


def test_a_bayer_letter_alone_is_not_a_key(designations):
    """There is an alpha in every constellation. Ambiguity must not silently pick one."""
    assert "Alp" not in designations
    assert "Eps" not in designations


def test_the_constellation_disambiguates_the_same_letter(designations):
    """Epsilon UMa and epsilon Ori are different stars and must stay so."""
    assert designations["Eps UMa"] != designations["Eps Ori"]
    assert designations["Eps Ori"] == 26311  # Alnilam


def test_multiple_components_resolve_to_the_brightest(designations, script):
    """theta-1 Ori is the Trapezium: three catalogue rows, one naked-eye point.

    A figure line needs one endpoint, and the child sees one dot, so the
    brightest component is the honest choice. Pinned because the alternative —
    an arbitrary row — would move the line without any error.
    """
    assert designations["The-1 Ori"] == 26220
    assert script.resolve_star("Chi-1 Ori", designations) == 27913


def test_brightest_component_wins_even_when_it_has_the_higher_hip(script, tmp_path):
    """The pick must be by magnitude, not by catalogue number.

    Today exactly one designation in the catalogue has two rows (The-1 Ori), and
    there the lower HIP happens to also be the brighter star — so a resolver
    that sorted by HIP would look correct and be wrong. This feeds it the case
    real data does not currently contain.
    """
    names = tmp_path / "star-names.json"
    stars = tmp_path / "stars.json"
    names.write_text(
        json.dumps(
            {
                "names": [
                    {"hip": 100, "bayer": "Alp", "con": "Tst"},
                    {"hip": 200, "bayer": "Alp", "con": "Tst"},
                ]
            }
        ),
        encoding="utf-8",
    )
    stars.write_text(
        json.dumps({"stars": [[100, 1.0, 1.0, 5.9], [200, 1.0, 1.0, 2.1]]}),
        encoding="utf-8",
    )
    resolved = script.load_designations(names, stars)
    assert (
        resolved["Alp Tst"] == 200
    ), "picked the dimmer star because its HIP was lower"


def test_unknown_designation_stops_the_build(script, designations):
    with pytest.raises(script.FigureError, match="does not resolve"):
        script.resolve_star("Alp Xyz", designations)


def test_unsourced_figure_is_refused(script, designations, star_hips):
    """Rule 1: a claim marked NEEDS SOURCE must not ship, and a drawn figure ships."""
    for status in ("NEEDS SOURCE", "DISPUTED", "PLAUSIBLE", "NOT ATTESTED"):
        with pytest.raises(script.FigureError, match="not VERIFIED"):
            script.resolve_figure(
                make_figure(status=status), designations, star_hips, CONTENT_KEYS
            )


def test_unknown_status_is_refused(script, designations, star_hips):
    with pytest.raises(script.FigureError, match="not one of"):
        script.resolve_figure(
            make_figure(status="probably fine"), designations, star_hips, CONTENT_KEYS
        )


def test_missing_source_is_refused(script, designations, star_hips):
    with pytest.raises(script.FigureError, match="no source"):
        script.resolve_figure(
            make_figure(source="  "), designations, star_hips, CONTENT_KEYS
        )


def test_undefined_content_key_is_refused(script, designations, star_hips):
    """Rule 3: player-facing strings live in content/bg/, never in a data file."""
    with pytest.raises(script.FigureError, match="not defined in content"):
        script.resolve_figure(
            make_figure(nameKey="figure.missing.name"),
            designations,
            star_hips,
            CONTENT_KEYS,
        )


def test_a_named_but_undrawn_star_is_refused(script, designations, star_hips):
    """A label pointing at nothing is worse than no label."""
    figure = make_figure(
        parts=[
            {
                "id": "bowl",
                "nameKey": "figure.test.part",
                "stars": ["Alp UMa", "Bet UMa", "Gam UMa"],
            }
        ],
        lines=[["Alp UMa", "Bet UMa"]],
    )
    with pytest.raises(script.FigureError, match="never drawn"):
        script.resolve_figure(figure, designations, star_hips, CONTENT_KEYS)


def test_a_one_star_line_is_refused(script, designations, star_hips):
    with pytest.raises(script.FigureError, match="at least two stars"):
        script.resolve_figure(
            make_figure(lines=[["Alp UMa"]]), designations, star_hips, CONTENT_KEYS
        )


def test_a_valid_figure_resolves_to_hip_numbers(script, designations, star_hips):
    resolved = script.resolve_figure(
        make_figure(), designations, star_hips, CONTENT_KEYS
    )
    assert resolved["lines"] == [[54061, 53910]]
    assert resolved["parts"][0]["stars"] == [54061, 53910]
    assert "status" not in resolved, "status is a build-time gate, not shipped data"


def test_every_designation_maps_into_the_shipped_catalogue(designations, star_hips):
    """The resolver may only name stars the game actually has positions for."""
    unknown = sorted(hip for hip in designations.values() if hip not in star_hips)
    assert (
        not unknown
    ), f"designations resolve to stars absent from stars.json: {unknown}"
