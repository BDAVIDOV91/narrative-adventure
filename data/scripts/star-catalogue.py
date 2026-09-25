#!/usr/bin/env python3
"""Turn the HYG catalogue and Stellarium's figures into static JSON for the game.

Build-time only. The game never runs this — it reads the JSON this writes.

Why a generator and not typed constants: a star position typed from memory into
a scene file is exactly the defect class CLAUDE.md rule 1 calls severity-
critical, and it is invisible once written. Every number here is traceable to a
catalogue row, and every run re-checks itself against an independent source.

The self-check is not decoration. The obvious candidate catalogue for this job —
the IAU/WGSN "Naked Eye Catalog" — carries a corrupt right ascension for Mizar,
off by 3.2 degrees, which is this game's primary zoom-split-star target. That
file loads, validates and passes bounds tests while placing Mizar three degrees
from Alcor instead of eleven arcminutes. It was caught only by checking against
a source that was not the file's own generator, so that check is built in here
and the build fails on it.

Inputs (all under data/raw/, gitignored — see the download commands in
docs/sources.md):
    data/raw/hyg/hyg_v44.csv.gz        positions, magnitudes, designations
    data/raw/skyculture/modern_iau.json constellation figures, keyed by HIP
    data/raw/hyg/hip2_bright.tsv       Hipparcos-2, the verification oracle

Usage:
    venv/bin/python data/scripts/star-catalogue.py
    venv/bin/python data/scripts/star-catalogue.py --mag 6.5
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
from datetime import date
from pathlib import Path
from typing import Iterator

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"
GENERATED_DIR = REPO_ROOT / "data" / "generated"

HYG_PATH = RAW_DIR / "hyg" / "hyg_v44.csv.gz"
SKYCULTURE_PATH = RAW_DIR / "skyculture" / "modern_iau.json"
ORACLE_PATH = RAW_DIR / "hyg" / "hip2_bright.tsv"

STARS_OUT = GENERATED_DIR / "stars.json"
LINES_OUT = GENERATED_DIR / "constellation-lines.json"
NAMES_OUT = GENERATED_DIR / "star-names.json"

# Naked-eye is mag 6.5 under a perfect dark sky. We cut at 5.5 on purpose: it
# draws a sky a child in a Bulgarian town recognises, instead of the
# undifferentiated wash of dots 8,921 stars produce, and it keeps the whole
# star payload under 100 KB on the hardware budget. Figure stars fainter than
# the cut are added back unconditionally (see collect_stars) so no constellation
# line can ever reference a star that was filtered out.
DEFAULT_MAG_LIMIT = 5.5

# Stellarium's `modern` skyculture mixes 19-digit Gaia DR3 source_ids into the
# same arrays as 5-digit HIP numbers. `modern_iau` is clean, but the guard stays:
# a Gaia id silently fails to join and drops a line segment, which draws a
# constellation wrong with no error anywhere. Fail loudly instead.
MAX_HIP = 999_999

# HIP 55203 is referenced by modern_iau but has an empty `hip` field in HYG:
# the row came from Gliese, not Hipparcos. The star is Xi Ursae Majoris (Alula
# Australis), present in HYG under its HR and HD numbers. Resolved by the
# fallback rather than dropped, because dropping it breaks the Ursa Major
# figure — the exact failure the guard above exists to prevent.
HIP_ALIASES: dict[int, dict[str, str]] = {
    55203: {"hr": "4375", "hd": "98231"},
}

# Column order of every row in stars.json. Declared in the emitted file too.
STAR_COLUMNS = ["hip", "raHours", "decDegrees", "mag"]
HIP, RA_HOURS, DEC_DEGREES, MAG = range(4)

# Offsets between HYG and Hipparcos-2 above this are treated as a build failure.
# The Mizar corruption that motivated this check was 11,545 arcseconds, so the
# threshold has three orders of magnitude of headroom and still catches it.
POSITION_TOLERANCE_ARCSEC = 30.0

# The only stars legitimately further apart than the tolerance: HYG and
# Hipparcos-2 quote different epochs, so the highest-proper-motion naked-eye
# systems drift past 30" between them. Every entry here was identified by
# running the check, not assumed — see tests/test_star_catalogue.py, which
# pins the list so a new offender cannot be waved through by adding to it.
HIGH_PROPER_MOTION_HIP: frozenset[int] = frozenset(
    {
        57939,  # Groombridge 1830
        104214,  # 61 Cygni A
        104217,  # 61 Cygni B
        19849,  # Keid (40 Eridani A)
    }
)


class GeneratorError(RuntimeError):
    """A build-stopping problem with the catalogue inputs."""


def _write_json(path: Path, header: dict[str, object], key: str, records: list) -> None:
    """Write metadata pretty-printed, then one compact record per line.

    json.dumps(indent=2) turns 2,851 stars into 306 KB — four times the payload
    for the same data, on a 1.9 GB hardware budget. Dumping it all on one line
    fixes the size and makes every regeneration a single unreadable diff line.
    One record per line gets both: small on disk, and a regeneration that
    changes four stars shows as four changed lines.
    """
    lines = [
        json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        for record in records
    ]
    body = ",\n    ".join(lines)
    head = json.dumps(header, indent=2, ensure_ascii=False)[:-2].rstrip()
    path.write_text(
        f"{head},\n  {json.dumps(key)}: [\n    {body}\n  ]\n}}\n", encoding="utf-8"
    )


def _float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def read_hyg(path: Path = HYG_PATH) -> list[dict[str, str]]:
    """Every HYG row, as-is. ra is in hours, dec in degrees, dist in parsecs."""
    if not path.exists():
        raise GeneratorError(
            f"{path.relative_to(REPO_ROOT)} is missing. It is gitignored on "
            "purpose; the download command is in docs/sources.md."
        )
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_indexes(
    rows: list[dict[str, str]],
) -> tuple[
    dict[int, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]
]:
    """Index HYG by HIP, and by HD and HR for the rows HIP cannot reach."""
    by_hip: dict[int, dict[str, str]] = {}
    by_hd: dict[str, dict[str, str]] = {}
    by_hr: dict[str, dict[str, str]] = {}
    for row in rows:
        hip = row.get("hip", "").strip()
        if hip:
            by_hip.setdefault(int(hip), row)
        hd = row.get("hd", "").strip()
        if hd:
            by_hd.setdefault(hd, row)
        hr = row.get("hr", "").strip()
        if hr:
            by_hr.setdefault(hr, row)
    return by_hip, by_hd, by_hr


def read_figures(path: Path = SKYCULTURE_PATH) -> list[dict[str, object]]:
    """The 88 IAU-region figures, as lists of HIP polylines.

    These are the shapes people usually draw, not an IAU standard: the IAU
    defined constellation *boundaries* and has never defined stick figures.
    Content must never call them official. Boundaries are deliberately not read
    from this file — they are 1930 rectilinear arcs in B1875, and they teach a
    child that a constellation is a box.
    """
    if not path.exists():
        raise GeneratorError(
            f"{path.relative_to(REPO_ROOT)} is missing. It is gitignored on "
            "purpose; the download command is in docs/sources.md."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    figures: list[dict[str, object]] = []
    for constellation in data["constellations"]:
        # "CON modern_iau UMa" -> "UMa", so the id joins to HYG's `con` column.
        abbreviation = str(constellation["id"]).rsplit(" ", 1)[-1]
        lines = [[int(hip) for hip in polyline] for polyline in constellation["lines"]]
        figures.append(
            {
                "id": abbreviation,
                "name": constellation["common_name"]["english"],
                "lines": lines,
            }
        )
    return figures


def figure_hips(figures: list[dict[str, object]]) -> set[int]:
    """Every star id the figures reference, guarded against Gaia contamination."""
    hips: set[int] = set()
    for figure in figures:
        for polyline in figure["lines"]:  # type: ignore[index]
            for hip in polyline:
                if hip > MAX_HIP:
                    raise GeneratorError(
                        f"{figure['id']} references star id {hip}, which is too "
                        "long to be a HIP number — this is a Gaia DR3 source_id. "
                        "Joining it would silently drop the line segment."
                    )
                hips.add(hip)
    return hips


def resolve(
    hip: int,
    by_hip: dict[int, dict[str, str]],
    by_hd: dict[str, dict[str, str]],
    by_hr: dict[str, dict[str, str]],
) -> dict[str, str] | None:
    """HYG row for a HIP number, falling back to HR/HD for the known gaps."""
    row = by_hip.get(hip)
    if row is not None:
        return row
    alias = HIP_ALIASES.get(hip)
    if alias is None:
        return None
    if "hr" in alias and alias["hr"] in by_hr:
        return by_hr[alias["hr"]]
    if "hd" in alias and alias["hd"] in by_hd:
        return by_hd[alias["hd"]]
    return None


def collect_stars(
    rows: list[dict[str, str]],
    required_hips: set[int],
    mag_limit: float,
    by_hip: dict[int, dict[str, str]],
    by_hd: dict[str, dict[str, str]],
    by_hr: dict[str, dict[str, str]],
) -> list[list[float]]:
    """Stars brighter than the cut, plus every star a figure line needs.

    The union is what makes the cut safe to change: lower it as far as you like
    and the constellations still draw, because their stars come back in
    regardless of magnitude.
    """
    unresolved = sorted(
        hip for hip in required_hips if resolve(hip, by_hip, by_hd, by_hr) is None
    )
    if unresolved:
        raise GeneratorError(
            f"{len(unresolved)} figure star id(s) do not resolve in HYG: "
            f"{unresolved}. Add an entry to HIP_ALIASES with the HR/HD number "
            "rather than dropping them — a dropped id draws the figure wrong."
        )

    required_rows = {
        id(row): (hip, row)
        for hip in required_hips
        if (row := resolve(hip, by_hip, by_hd, by_hr)) is not None
    }

    stars: dict[int, list[float]] = {}
    for hip, row in required_rows.values():
        stars[hip] = _star_entry(hip, row)

    for row in rows:
        magnitude = _float(row.get("mag", ""))
        if magnitude is None or magnitude > mag_limit:
            continue
        hip_text = row.get("hip", "").strip()
        if not hip_text:
            # No HIP number means nothing can reference it: figures join on HIP
            # and so will the Bulgarian figures. A star the game cannot name is
            # not worth the bytes.
            continue
        hip = int(hip_text)
        if hip not in stars:
            stars[hip] = _star_entry(hip, row)

    return [stars[hip] for hip in sorted(stars)]


def _star_entry(hip: int, row: dict[str, str]) -> list[float]:
    """[hip, raHours, decDegrees, mag] — see STAR_COLUMNS.

    A positional row rather than an object: repeating four key names 2,851
    times costs more than the data itself. The order is declared in the file's
    own `columns` field so a reader never has to guess it.
    """
    return [
        hip,
        round(float(row["ra"]), 6),
        round(float(row["dec"]), 6),
        round(float(row["mag"]), 2),
    ]


def read_oracle(path: Path = ORACLE_PATH) -> dict[int, tuple[float, float]]:
    """Hipparcos-2 (van Leeuwen 2007) positions in degrees, keyed by HIP.

    Deliberately a different source from HYG. Checking a catalogue against its
    own generator proves nothing; this is the check that catches a file whose
    numbers are internally consistent and wrong.
    """
    if not path.exists():
        raise GeneratorError(
            f"{path.relative_to(REPO_ROOT)} is missing. The build refuses to "
            "run unverified — the download command is in docs/sources.md."
        )
    oracle: dict[int, tuple[float, float]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        parts = [field.strip() for field in line.split("\t")]
        if len(parts) < 3:
            continue
        try:
            hip = int(parts[0])
            ra = float(parts[1])
            dec = float(parts[2])
        except ValueError:
            continue  # header rows
        oracle[hip] = (ra, dec)
    if not oracle:
        raise GeneratorError(f"{path.relative_to(REPO_ROOT)} parsed to zero rows.")
    return oracle


def angular_separation_arcsec(
    ra1_deg: float, dec1_deg: float, ra2_deg: float, dec2_deg: float
) -> float:
    """Great-circle separation. Not a flat RA difference — that breaks near the poles."""
    ra1, dec1, ra2, dec2 = map(math.radians, (ra1_deg, dec1_deg, ra2_deg, dec2_deg))
    cosine = math.sin(dec1) * math.sin(dec2) + math.cos(dec1) * math.cos(
        dec2
    ) * math.cos(ra1 - ra2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine)))) * 3600.0


def verify(
    stars: list[list[float]], oracle: dict[int, tuple[float, float]]
) -> Iterator[tuple[int, float]]:
    """Yield (hip, arcsec) for every star further from Hipparcos-2 than tolerated."""
    for star in stars:
        hip = int(star[HIP])
        if hip in HIGH_PROPER_MOTION_HIP:
            continue
        reference = oracle.get(hip)
        if reference is None:
            continue
        separation = angular_separation_arcsec(
            star[RA_HOURS] * 15.0,
            star[DEC_DEGREES],
            reference[0],
            reference[1],
        )
        if separation > POSITION_TOLERANCE_ARCSEC:
            yield hip, separation


def build_names(
    stars: list[list[float]],
    by_hip: dict[int, dict[str, str]],
    by_hd: dict[str, dict[str, str]],
    by_hr: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    """Catalogue designations for the emitted stars.

    Authoring metadata, not player content: rule 3 puts every player-facing
    string in content/bg/. This file is how a level author knows which HIP
    number is Ригел without typing a position from memory.
    """
    names: list[dict[str, object]] = []
    for star in stars:
        hip = int(star[HIP])
        row = resolve(hip, by_hip, by_hd, by_hr)
        if row is None:
            continue
        entry: dict[str, object] = {"hip": hip, "con": row.get("con", "").strip()}
        for source_key, out_key in (
            ("proper", "proper"),
            ("bayer", "bayer"),
            ("flam", "flamsteed"),
        ):
            value = row.get(source_key, "").strip()
            if value:
                entry[out_key] = value
        if len(entry) > 2:
            names.append(entry)
    return names


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mag",
        type=float,
        default=DEFAULT_MAG_LIMIT,
        help=f"magnitude cut (default {DEFAULT_MAG_LIMIT})",
    )
    args = parser.parse_args()

    rows = read_hyg()
    by_hip, by_hd, by_hr = build_indexes(rows)
    figures = read_figures()
    required = figure_hips(figures)
    stars = collect_stars(rows, required, args.mag, by_hip, by_hd, by_hr)

    oracle = read_oracle()
    failures = list(verify(stars, oracle))
    if failures:
        detail = ", ".join(f'HIP {hip} off by {sep:.1f}"' for hip, sep in failures[:10])
        raise GeneratorError(
            f"{len(failures)} star(s) disagree with Hipparcos-2 by more than "
            f'{POSITION_TOLERANCE_ARCSEC}": {detail}. The catalogue is wrong, or '
            "a new high-proper-motion star crossed the threshold. Do not widen "
            "the tolerance to make this pass."
        )
    checked = sum(1 for star in stars if int(star[HIP]) in oracle)

    generated = date.today().isoformat()
    attribution = (
        "HYG Database v4.4 (D. Nash / astronexus), CC BY-SA 4.0. "
        "Constellation figures: Stellarium modern_iau skyculture, CC BY-SA 4.0. "
        "Verified against Hipparcos-2 (van Leeuwen 2007, VizieR I/311)."
    )

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    _write_json(
        STARS_OUT,
        {
            "_readme": (
                "Generated by data/scripts/star-catalogue.py. Do not edit by "
                "hand. Stars brighter than magLimit, plus every star any "
                "constellation figure references regardless of magnitude, so no "
                "line can reference a star that was filtered out. Each row is "
                "positional -- see `columns`. raHours is right ascension in "
                "hours (0-24), decDegrees is declination in degrees. Regenerate "
                "rather than patch."
            ),
            "license": "CC BY-SA 4.0",
            "attribution": attribution,
            "generated": generated,
            "magLimit": args.mag,
            "verifiedAgainst": "Hipparcos-2 (VizieR I/311)",
            "verifiedCount": checked,
            "columns": STAR_COLUMNS,
        },
        "stars",
        stars,
    )

    _write_json(
        LINES_OUT,
        {
            "_readme": (
                "Generated by data/scripts/star-catalogue.py. Do not edit by "
                "hand. The 88 IAU-region figures as polylines of HIP numbers, "
                "joining to stars.json. These are the shapes people usually "
                "draw; the IAU standardised constellation boundaries and has "
                "never defined stick figures, so content must never call them "
                "official."
            ),
            "license": "CC BY-SA 4.0",
            "attribution": attribution,
            "generated": generated,
        },
        "constellations",
        figures,
    )

    names = build_names(stars, by_hip, by_hd, by_hr)
    _write_json(
        NAMES_OUT,
        {
            "_readme": (
                "Generated by data/scripts/star-catalogue.py. Do not edit by "
                "hand. Catalogue designations for the stars in stars.json. "
                "Authoring metadata, NOT player content -- every player-facing "
                "string lives in content/bg/ per CLAUDE.md rule 3."
            ),
            "license": "CC BY-SA 4.0",
            "attribution": attribution,
            "generated": generated,
        },
        "names",
        names,
    )

    for path in (STARS_OUT, LINES_OUT, NAMES_OUT):
        size_kb = path.stat().st_size / 1024
        print(f"wrote {path.relative_to(REPO_ROOT)} ({size_kb:.0f} KB)")
    print(
        f"{len(stars)} stars at mag <= {args.mag}, "
        f"{len(figures)} constellations, {len(names)} named; "
        f"{checked} positions verified against Hipparcos-2"
    )


if __name__ == "__main__":
    main()
