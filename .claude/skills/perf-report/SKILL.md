---
name: perf-report
description: Use before any commit that touches assets/ or Three.js code, to audit texture dimensions and format, Three.js object counts, bundle chunk sizes and runtime cost against the integrated-APU hardware budget.
---

# Performance Budget Report

The target is the developer's real laptop, and a fair proxy for the school and home
machines these children use: 4 cores, ~1.9 GB free RAM, AMD Radeon R5/R6/R7 integrated
APU. A change that is smooth on a development desktop and unplayable there has failed.

**Measure, do not estimate.** Every number in this report comes from a command you ran.

## Step 1 — Ground in the diff

```bash
git diff --cached --stat
git diff --cached -- assets/ src/shared/planet-render.ts
find assets/images -type f -exec ls -la {} +
npm run build
```

For texture dimensions:

```bash
.venv/bin/python -c "
from PIL import Image; import pathlib
for p in sorted(pathlib.Path('assets/images').rglob('*.webp')):
    im = Image.open(p); print(f'{p}: {im.width}x{im.height} {p.stat().st_size//1024}KB')
"
```

## Step 2 — Walk the checklist

### Textures — the biggest lever
Every committed texture is WebP from `data/scripts/process-textures.py`, no dimension above
2048px, raw sources left in the gitignored `assets/images/nasa/raw/`, equirectangular maps
keeping their 2:1 aspect. NASA publishes at 8k+; an 8k map on a sphere drawn a few hundred
pixels wide costs the whole download, decode and VRAM for no visible gain.

### Three.js — single objects only
Still behind the dynamic import in `src/shared/planet-render.ts`. One mesh, not a scene
graph — a planet, not a system. `setPixelRatio` capped. Sane sphere segment counts.
Geometry, material, texture and renderer all disposed on close: a leaked WebGL context on a
machine with 1.9 GB free is a crash, not a slowdown.

### Bundle
Report real chunk sizes from `npm run build`. Phaser at ~1.2 MB raw / ~320 KB gzipped is
expected. **Three.js should be absent entirely** until a 3D moment is opened — a `three`
chunk appearing in a normal build means the lazy boundary is broken. Any new dependency:
does it earn its size?

### Runtime
Work in `update()` that belongs in `create()`. Objects allocated per frame. Tweens and
timers not cleaned up on scene shutdown.

Spawn the `perf-budget-checker` agent for a full audit.

## Step 3 — Output

Tables with real numbers: TEXTURES (file, dimensions, format, size, verdict), BUNDLE
(chunk, raw, gzipped, change), plus THREE.JS and RUNTIME findings with `file:line`, then an
explicit WHAT WAS MEASURED list naming the commands run.

## Rules

- A 40 KB increase is not a finding. Distinguish a real regression from a theoretical one.
- "No issues" only after measuring — say what was measured.
