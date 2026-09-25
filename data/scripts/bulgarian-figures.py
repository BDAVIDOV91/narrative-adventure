#!/usr/bin/env python3
"""Resolve hand-authored Bulgarian star figures into HIP numbers.

Build-time only. The game never runs this — it reads the JSON this writes.

Why this script exists at all. The international constellation figures come from
Stellarium and are already keyed by HIP number. The Bulgarian ones — Ралица and
Колата, the folk names this game actually teaches — exist in no downloadable
set. They are described in the ethnographic literature in the only terms that
literature uses: Greek-letter designations. "колела = α,β,γ,δ" is what the
source says.

So the authored file says exactly that, and this script does the join. The
author writes what the cited source wrote; the HIP numbers and positions come
from data/generated/, which came from a catalogue. Neither half is typed from
memory, which is the whole of rule 1.

A figure whose designation fails to resolve stops the build. The alternative —
skipping it — draws a Bulgarian constellation with a limb missing, in the one
place in the game where a Bulgarian child is most likely to notice.

Input:
    data/figures-bg.json          authored, committed, cites its source
Reads:
    data/generated/star-names.json
    data/generated/stars.json
Writes:
    data/generated/figures-bg.json

Usage:
    venv/bin/python data/scripts/bulgarian-figures.py
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = REPO_ROOT / "data" / "generated"

SOURCE_PATH = REPO_ROOT / "data" / "figures-bg.json"
NAMES_PATH = GENERATED_DIR / "star-names.json"
STARS_PATH = GENERATED_DIR / "stars.json"
OUTPUT_PATH = GENERATED_DIR / "figures-bg.json"
CONTENT_DIR = REPO_ROOT / "content" / "bg"

# Statuses docs/sources.md uses. A figure may only be generated once its claim
# is VERIFIED there: rule 1 says a claim marked NEEDS SOURCE or DISPUTED must
# not ship, and a drawn constellation is a shipped claim.
SHIPPABLE_STATUS = "VERIFIED"
KNOWN_STATUSES = {"VERIFIED", "NEEDS SOURCE", "DISPUTED", "NOT ATTESTED", "PLAUSIBLE"}


class FigureError(RuntimeError):
    """A build-stopping problem with an authored figure."""


def load_designations(
    names_path: Path = NAMES_PATH,
    stars_path: Path = STARS_PATH,
) -> dict[str, int]:
    """Map "Alp UMa" -> HIP, from the generated designation table.

    Bayer letters are not unique on their own — there is an alpha in every
    constellation — so the constellation abbreviation is part of the key.

    A designation can still cover more than one catalogue row: theta-1 Orionis
    is the Trapezium, four stars a child sees as a single point of light. The
    brightest component wins, because a figure line needs one endpoint and the
    brightest is the one the eye is actually following.

    That tie-break reads magnitudes rather than taking the first row. Today
    exactly one designation in the catalogue has two rows and its lower HIP
    happens to also be the brighter star, so sorting by catalogue number would
    look correct and be wrong the moment that stops holding.
    """
    if not names_path.exists():
        raise FigureError(
            f"{names_path.relative_to(REPO_ROOT)} is missing. Run "
            "data/scripts/star-catalogue.py first."
        )
    magnitudes = load_magnitudes(stars_path)
    payload = json.loads(names_path.read_text(encoding="utf-8"))
    designations: dict[str, int] = {}
    for entry in payload["names"]:
        bayer = entry.get("bayer", "").strip()
        constellation = entry.get("con", "").strip()
        if not bayer or not constellation:
            continue
        key = f"{bayer} {constellation}"
        hip = int(entry["hip"])
        incumbent = designations.get(key)
        if incumbent is None or magnitudes.get(hip, 99.0) < magnitudes.get(
            incumbent, 99.0
        ):
            designations[key] = hip
    return designations


def load_magnitudes(stars_path: Path = STARS_PATH) -> dict[int, float]:
    if not stars_path.exists():
        raise FigureError(
            f"{stars_path.relative_to(REPO_ROOT)} is missing. Run "
            "data/scripts/star-catalogue.py first."
        )
    payload = json.loads(stars_path.read_text(encoding="utf-8"))
    return {int(row[0]): float(row[3]) for row in payload["stars"]}


def load_star_hips(stars_path: Path = STARS_PATH) -> set[int]:
    if not stars_path.exists():
        raise FigureError(
            f"{stars_path.relative_to(REPO_ROOT)} is missing. Run "
            "data/scripts/star-catalogue.py first."
        )
    payload = json.loads(stars_path.read_text(encoding="utf-8"))
    return {int(row[0]) for row in payload["stars"]}


def load_content_keys(content_dir: Path = CONTENT_DIR) -> set[str]:
    """Every key content/bg/ defines, so a figure cannot name a missing string."""
    keys: set[str] = set()
    for path in sorted(content_dir.glob("*.json")):
        keys.update(json.loads(path.read_text(encoding="utf-8")))
    return keys


def resolve_star(designation: str, designations: dict[str, int]) -> int:
    hip = designations.get(designation)
    if hip is None:
        raise FigureError(
            f"designation {designation!r} does not resolve to a star. Check the "
            "spelling against data/generated/star-names.json — Bayer letters are "
            "abbreviated three letters plus the constellation, e.g. 'Alp UMa', "
            "and multiples carry their number, e.g. 'Chi-1 Ori'."
        )
    return hip


def resolve_figure(
    figure: dict[str, object],
    designations: dict[str, int],
    star_hips: set[int],
    content_keys: set[str],
) -> dict[str, object]:
    """Turn one authored figure into HIP numbers, or refuse to."""
    figure_id = str(figure["id"])
    status = str(figure.get("status", ""))
    if status not in KNOWN_STATUSES:
        raise FigureError(
            f"{figure_id}: status {status!r} is not one of {sorted(KNOWN_STATUSES)}. "
            "Every figure is a folklore claim and carries a status from "
            "docs/sources.md."
        )
    if status != SHIPPABLE_STATUS:
        raise FigureError(
            f"{figure_id}: status is {status}, not {SHIPPABLE_STATUS}. A drawn "
            "constellation is a shipped claim, and rule 1 forbids shipping one "
            "that is not sourced. Resolve it in docs/sources.md first."
        )
    if not str(figure.get("source", "")).strip():
        raise FigureError(f"{figure_id}: no source recorded.")

    name_key = str(figure["nameKey"])
    if name_key not in content_keys:
        raise FigureError(
            f"{figure_id}: nameKey {name_key!r} is not defined in content/bg/. "
            "Player-facing strings live there, never in a data file (rule 3)."
        )

    parts: list[dict[str, object]] = []
    for part in figure["parts"]:  # type: ignore[index]
        part_key = str(part["nameKey"])
        if part_key not in content_keys:
            raise FigureError(
                f"{figure_id}: part nameKey {part_key!r} is not defined in "
                "content/bg/."
            )
        hips = [resolve_star(str(d), designations) for d in part["stars"]]
        missing = sorted(set(hips) - star_hips)
        if missing:
            raise FigureError(
                f"{figure_id}/{part['id']}: HIP {missing} resolved but is absent "
                "from stars.json. Add it to the figure union in "
                "data/scripts/star-catalogue.py rather than dropping the part."
            )
        parts.append({"id": part["id"], "nameKey": part_key, "stars": hips})

    lines: list[list[int]] = []
    for polyline in figure["lines"]:  # type: ignore[index]
        resolved = [resolve_star(str(d), designations) for d in polyline]
        if len(resolved) < 2:
            raise FigureError(
                f"{figure_id}: a line needs at least two stars, got {polyline}."
            )
        lines.append(resolved)

    drawn = {hip for polyline in lines for hip in polyline}
    named = {hip for part in parts for hip in part["stars"]}  # type: ignore[union-attr]
    if named - drawn:
        raise FigureError(
            f"{figure_id}: stars {sorted(named - drawn)} are named in a part but "
            "never drawn by a line. A child would read the label and see nothing."
        )

    return {
        "id": figure_id,
        "constellation": figure["constellation"],
        "nameKey": name_key,
        "source": figure["source"],
        "parts": parts,
        "lines": lines,
    }


def main() -> None:
    if not SOURCE_PATH.exists():
        raise FigureError(f"{SOURCE_PATH.relative_to(REPO_ROOT)} does not exist.")

    authored = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    designations = load_designations()
    star_hips = load_star_hips()
    content_keys = load_content_keys()

    figures = [
        resolve_figure(figure, designations, star_hips, content_keys)
        for figure in authored["figures"]
    ]

    payload = {
        "_readme": (
            "Generated by data/scripts/bulgarian-figures.py from "
            "data/figures-bg.json. Do not edit by hand. Bulgarian folk star "
            "figures resolved to HIP numbers, joining to stars.json. Authored "
            "from the ethnographic literature -- unlike the international "
            "figures, these exist in no downloadable set. Each figure carries "
            "its source; every one is VERIFIED in docs/sources.md or the build "
            "refuses to write it."
        ),
        "generated": date.today().isoformat(),
        "figures": figures,
    }

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    stars = sum(
        len(polyline)
        for figure in figures
        for polyline in figure["lines"]  # type: ignore[union-attr]
    )
    print(
        f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} "
        f"({len(figures)} figures, {stars} line endpoints)"
    )


if __name__ == "__main__":
    main()
