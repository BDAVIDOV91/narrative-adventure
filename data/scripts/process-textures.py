#!/usr/bin/env python3
"""Downscale NASA source textures and emit WebP the game can actually load.

Build-time only. Reads from assets/images/nasa/raw/ (gitignored — the sources
are large) and writes committed WebP into assets/images/nasa/.

Why this matters more than it looks: the dev machine is an integrated AMD APU
with ~2GB of free RAM. NASA publishes planet maps at 8k and beyond. Handing an
8k texture to a sphere that occupies a few hundred pixels on screen costs the
whole download, the whole decode and the whole VRAM footprint for no visible
gain. Capping at 2048 is invisible to the player and is the single biggest
load-time lever in the project.

Usage:
    venv/bin/python data/scripts/process-textures.py
    venv/bin/python data/scripts/process-textures.py --max-size 1024 --quality 80
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "assets" / "images" / "nasa" / "raw"
OUTPUT_DIR = REPO_ROOT / "assets" / "images" / "nasa"

SOURCE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}

# 2048 is the practical ceiling for a sphere this game ever draws close-up.
DEFAULT_MAX_SIZE = 2048
DEFAULT_QUALITY = 82


def process(source: Path, max_size: int, quality: int) -> tuple[Path, str]:
    """Convert one source image. Returns (output path, a human-readable summary)."""
    with Image.open(source) as image:
        original = f"{image.width}x{image.height}"
        image = image.convert("RGB")

        if max(image.size) > max_size:
            # Keep the aspect ratio: planet maps are equirectangular (2:1) and
            # squashing them would visibly distort the surface features.
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        destination = OUTPUT_DIR / f"{source.stem}.webp"
        image.save(destination, "WEBP", quality=quality, method=6)
        summary = f"{original} -> {image.width}x{image.height}"

    source_kb = source.stat().st_size / 1024
    out_kb = destination.stat().st_size / 1024
    return destination, f"{summary}  {source_kb:.0f}KB -> {out_kb:.0f}KB"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-size", type=int, default=DEFAULT_MAX_SIZE)
    parser.add_argument("--quality", type=int, default=DEFAULT_QUALITY)
    args = parser.parse_args()

    if not SOURCE_DIR.exists():
        print(
            f"no source directory at {SOURCE_DIR.relative_to(REPO_ROOT)} — nothing to do"
        )
        print("drop raw NASA textures there; they stay local and are never committed")
        return 0

    sources = sorted(
        p for p in SOURCE_DIR.iterdir() if p.suffix.lower() in SOURCE_SUFFIXES
    )
    if not sources:
        print(
            f"no source images in {SOURCE_DIR.relative_to(REPO_ROOT)} — nothing to do"
        )
        return 0

    for source in sources:
        destination, summary = process(source, args.max_size, args.quality)
        print(f"{source.name}: {summary} -> {destination.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
