# Звездната книга

A story-driven astronomy education game for Bulgarian children (~11-12), played
in the browser. The game is framed as a magical storybook: the book is the
level-select screen, and tapping a page zooms into that world, played from a
top-down view.

The player is a Bulgarian kid who finds an old telescope with a tiny AI
companion inside. Something is dimming a star, and the mystery unravels by
learning real astronomy at each location — with Bulgarian folklore woven through
as flavour: Зорница and Вечерница turning out to be one planet, Кумова слама
running across the sky.

> **Status**: early. The storybook shell runs, the Earth level has its data and
> markers, and the precompute pipeline produces real ephemeris data. The puzzle
> mini-games themselves are not built yet.

## Requirements

|        |                                |
| ------ | ------------------------------ |
| Node   | ≥ 22.12 (developed on 22.17.0) |
| Python | 3.12                           |
| uv     | for the Python environment     |

## Setup

```bash
npm install

uv venv venv
uv pip install -r requirements.txt

# Generate the astronomy data the game reads (downloads a ~32MB JPL kernel once)
venv/bin/python data/scripts/orbital-positions.py
```

## Running

```bash
npm run dev     # http://localhost:5173
```

There is nothing else to start. The game is static files — no server, no
database, no accounts. See `docs/adr/0001-python-is-build-time-only.md`.

## Checks

```bash
npm run validate                                  # type-check + lint + format
npm test                                          # vitest — the TypeScript suite
npm run build                                     # production build
venv/bin/python -m pytest                        # regression suite
venv/bin/python data/scripts/validate-levels.py  # every level against the schema
```

## Structure

```
src/
  scenes/          storybook + one folder per level (<level>-scene.ts + <level>-data.json)
  puzzles/         the seven reusable puzzle types
  shared/          content (i18n), game-state, fonts, player, zoom transition,
                   planet-render (the only Three.js)
  **/*.test.ts     vitest, co-located with what it tests
content/bg/        every player-facing string — Bulgarian, keyed
data/
  scripts/         Python, build-time only
  generated/       JSON the game reads (committed)
schemas/           level-data.schema.json
assets/            images (NASA + generated), audio, fonts
prompts/           the exact prompts used for generated art
docs/              ADRs, architecture, sources.md, dated session handoffs, security audits
tests/             pytest regression suite (Python only — TypeScript tests live in src/)
```

## Tech

**Phaser 3.90** for 2D gameplay and the storybook transitions — chosen over the
newer Phaser 4 for its example library and its Canvas renderer fallback, which
matters on Linux with integrated graphics. **Three.js** for a handful of
single-object planet renders, behind a dynamic import so it costs nothing until
opened. **Python + Skyfield** for real orbital math, run at build time and
committed as static JSON.

## Language

Bulgarian is the only locale. No player-facing string lives in a `.ts` file —
everything resolves through `src/shared/content.ts` to `content/bg/*.json`, so a
future reskin for another culture means swapping content and art rather than
editing scenes.

## Data credits

The game's astronomy is generated from real catalogues at build time, never
typed into a scene. Sources, licences and the download commands are in
`docs/sources.md`.

- **Planetary positions** — JPL DE440s via Skyfield.
- **Star positions and magnitudes** — [HYG Database v4.4](https://codeberg.org/astronexus/hyg),
  D. Nash / astronexus, **CC BY-SA 4.0**.
- **Constellation figures** — Stellarium `modern_iau` skyculture, **CC BY-SA 4.0**.
  These are the shapes people usually draw. The IAU standardised constellation
  _boundaries_ and has never defined stick figures.
- **Double-star separations** — Washington Double Star Catalog and ORB6, USNO,
  public domain.
- **Position verification** — Hipparcos-2 (van Leeuwen 2007, VizieR I/311), ESA.
- **Imagery** — NASA, public domain.

HYG and the Stellarium figures are share-alike, so the files derived from them —
`data/generated/stars.json`, `constellation-lines.json` and `star-names.json` —
are themselves offered under **CC BY-SA 4.0**, and each carries its licence and
attribution inline. This does not affect the licence of the game's code.

## Contributing

`main` is merge-only; work happens on `development`. See `CLAUDE.md` for the
rules that govern changes — in particular that no astronomy claim ships without a
source in `docs/sources.md`, and that no bug fix ships without a regression test.
