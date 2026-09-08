"""Guards on the generated star catalogue.

The failure mode these exist for is a catalogue that is internally consistent
and wrong. The IAU/WGSN "Naked Eye Catalog" is the worked example: it is
IAU-published, cut at exactly the right magnitude, carries the official proper
names — and gives Mizar a right ascension 3.2 degrees off. Data like that loads,
validates against the schema, passes every bounds check, and silently places the
zoom-split-star puzzle's subject three degrees from its companion.

So the tests here are not bounds checks. They assert *relationships between
specific stars* that a corrupt position breaks, because that is the only kind of
assertion the NEC file would have failed.

Most read data/generated/, which is committed, so they run on a clean checkout
without Python having been run. The few that need data/raw/ are marked
`integration`.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from conftest import load_script

REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED = REPO_ROOT / "data" / "generated"

# Stars this game teaches by name, so a position error in any of them is a
# content defect rather than a rounding artefact.
MIZAR = 65378
ALCOR = 65477
ALNILAM = 26311  # epsilon Ori, the middle belt star
ALNITAK = 26727  # zeta Ori
MINTAKA = 25930  # delta Ori
XI_UMA = 55203  # the HIP number Hipparcos does not actually contain


@pytest.fixture(scope="module")
def catalogue() -> dict:
    return json.loads((GENERATED / "stars.json").read_text("utf-8"))


@pytest.fixture(scope="module")
def by_hip(catalogue: dict) -> dict[int, list[float]]:
    return {row[0]: row for row in catalogue["stars"]}


@pytest.fixture(scope="module")
def figures() -> dict:
    return json.loads((GENERATED / "constellation-lines.json").read_text("utf-8"))


@pytest.fixture(scope="module")
def script():
    return load_script("star-catalogue")


def separation_arcsec(a: list[float], b: list[float]) -> float:
    """Great-circle separation between two catalogue rows, in arcseconds."""
    ra1, dec1 = math.radians(a[1] * 15.0), math.radians(a[2])
    ra2, dec2 = math.radians(b[1] * 15.0), math.radians(b[2])
    cosine = math.sin(dec1) * math.sin(dec2) + math.cos(dec1) * math.cos(
        dec2
    ) * math.cos(ra1 - ra2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine)))) * 3600.0


def test_mizar_and_alcor_are_708_arcsec_apart(by_hip):
    """THE regression test for the corrupt-catalogue class.

    708.4" = 11.8', recomputed independently from Hipparcos-2 and matching the
    figure committed in docs/sources.md. On IAU NEC data Mizar's RA is 3.2 deg
    wrong, which puts this at roughly 11,500" — so this assertion fails RED on
    the catalogue we rejected and passes GREEN on the one we shipped.

    It is also the pair the whole zoom-split-star puzzle rests on: if these two
    are not this far apart, the puzzle teaches nothing true.
    """
    assert MIZAR in by_hip, "Mizar is missing — the zoom-split-star target"
    assert ALCOR in by_hip, "Alcor is missing — the zoom-split-star target"
    assert separation_arcsec(by_hip[MIZAR], by_hip[ALCOR]) == pytest.approx(
        708.4, abs=5.0
    )


def test_alnilam_is_the_brightest_belt_star(by_hip):
    """docs/sources.md resolves the brief's inverted claim; this pins it.

    The brief said the brightest belt star is the multiple one. It is the
    reverse: Alnilam is both brightest and the only single star of the three.
    A magnitude mix-up would silently restore the brief's wrong version.
    """
    magnitudes = {hip: by_hip[hip][3] for hip in (ALNILAM, ALNITAK, MINTAKA)}
    assert min(magnitudes, key=lambda hip: magnitudes[hip]) == ALNILAM
    assert magnitudes[ALNILAM] < magnitudes[ALNITAK] < magnitudes[MINTAKA]


def test_belt_stars_lie_almost_on_a_line(by_hip):
    """The Belt is recognisable because it is straight; a bad position bends it.

    Each outer star sits within a degree of the same declination band and the
    middle star falls between them in right ascension. A single corrupt entry
    breaks one of those without touching any magnitude.
    """
    mintaka, alnilam, alnitak = by_hip[MINTAKA], by_hip[ALNILAM], by_hip[ALNITAK]
    assert mintaka[1] < alnilam[1] < alnitak[1], "belt stars out of order in RA"
    assert max(abs(mintaka[2]), abs(alnilam[2]), abs(alnitak[2])) < 3.0
    assert separation_arcsec(mintaka, alnitak) == pytest.approx(9900, rel=0.1)


def test_every_figure_star_is_in_the_catalogue(by_hip, figures):
    """The union invariant. Without it, lowering the magnitude cut breaks figures.

    A figure star filtered out for being too faint does not raise anything — the
    line just stops being drawable, and the constellation renders incomplete.
    """
    missing = sorted(
        {
            hip
            for constellation in figures["constellations"]
            for polyline in constellation["lines"]
            for hip in polyline
            if hip not in by_hip
        }
    )
    assert not missing, f"figure stars absent from stars.json: {missing}"


def test_xi_ursae_majoris_survived_the_hip_gap(by_hip):
    """HIP 55203 is referenced by the figures and is not in Hipparcos.

    HYG carries the star (xi UMa) from Gliese with an empty hip field, so a
    HIP-only join drops it and Ursa Major loses a line segment with no error.
    The HR/HD fallback is what keeps it, and this pins that the fallback works.
    """
    assert XI_UMA in by_hip
    assert by_hip[XI_UMA][3] < 6.5, "resolved to the wrong star — xi UMa is naked-eye"


def test_no_gaia_source_ids_reached_the_output(figures):
    """Stellarium's `modern` skyculture mixes 19-digit Gaia ids into HIP arrays.

    We take `modern_iau`, which is clean, but nothing stops a future switch. A
    Gaia id fails to join silently and drops a line segment.
    """
    oversized = sorted(
        {
            hip
            for constellation in figures["constellations"]
            for polyline in constellation["lines"]
            for hip in polyline
            if hip > 999_999
        }
    )
    assert not oversized, f"Gaia DR3 source_ids in figure data: {oversized}"


def test_all_88_constellations_are_present(figures):
    assert len(figures["constellations"]) == 88
    assert len({c["id"] for c in figures["constellations"]}) == 88


def test_magnitudes_and_coordinates_are_in_range(catalogue):
    """A unit slip (radians for degrees, degrees for hours) lands outside these."""
    for hip, ra_hours, dec_degrees, magnitude in catalogue["stars"]:
        assert 0.0 <= ra_hours < 24.0, f"HIP {hip} RA {ra_hours} is not in hours"
        assert -90.0 <= dec_degrees <= 90.0, f"HIP {hip} Dec {dec_degrees} out of range"
        assert -2.0 <= magnitude <= 12.0, f"HIP {hip} magnitude {magnitude} implausible"
    assert catalogue["magLimit"] == 5.5


def test_catalogue_carries_its_licence_and_attribution(catalogue, figures):
    """HYG is CC BY-SA 4.0 and share-alike is viral over this derived file.

    Shipping it without the notice is a licence breach, and the notice living in
    the generated file is what keeps it true after a regeneration.
    """
    for payload in (catalogue, figures):
        assert payload["license"] == "CC BY-SA 4.0"
        assert "HYG Database v4.4" in payload["attribution"]
        assert "Stellarium" in payload["attribution"]


def test_stars_json_stays_inside_the_payload_budget():
    """Hardware budget: 4 cores, ~1.9 GB free RAM. The sky is not the whole game."""
    size_kb = (GENERATED / "stars.json").stat().st_size / 1024
    assert size_kb < 200, f"stars.json is {size_kb:.0f} KB — re-check the magnitude cut"


def test_high_proper_motion_allowlist_is_not_a_dumping_ground(script):
    """The oracle check can be defeated by adding stars to the allowlist.

    Pinning the exact set means a real position error cannot be waved through by
    appending a HIP number: this test fails and forces the change to be argued.
    """
    assert script.HIGH_PROPER_MOTION_HIP == frozenset({57939, 104214, 104217, 19849})
    assert script.POSITION_TOLERANCE_ARCSEC == 30.0


def test_gaia_source_id_in_figures_raises(script):
    """The guard fires on contaminated input rather than dropping the segment."""
    contaminated = [{"id": "UMa", "lines": [[65378, 543989120214297472]]}]
    with pytest.raises(script.GeneratorError, match="Gaia"):
        script.figure_hips(contaminated)


def test_angular_separation_is_a_great_circle_not_an_ra_difference(script):
    """Near the pole, RA differences are not angles. Mizar sits at Dec +55."""
    at_pole = script.angular_separation_arcsec(0.0, 89.9, 180.0, 89.9)
    assert at_pole == pytest.approx(720.0, abs=1.0), "flat RA maths near the pole"
    assert script.angular_separation_arcsec(10.0, 0.0, 10.0, 0.0) == pytest.approx(0.0)


@pytest.mark.integration
def test_generated_positions_agree_with_hipparcos(script, catalogue):
    """Re-run the build-time oracle check against a source HYG did not produce.

    Marked integration: it needs data/raw/hyg/hip2_bright.tsv, which is
    gitignored. This is the check that would have caught the NEC corruption.
    """
    if not script.ORACLE_PATH.exists():
        pytest.skip("Hipparcos-2 oracle not downloaded")
    oracle = script.read_oracle()
    failures = list(script.verify(catalogue["stars"], oracle))
    assert not failures, f"positions disagree with Hipparcos-2: {failures[:5]}"
