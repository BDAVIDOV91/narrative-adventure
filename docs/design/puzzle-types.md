# Puzzle types

Seven reusable types, each built once and reskinned per planet. An eighth type is
a one-off that needs its own maintenance forever — `schemas/level-data.schema.json`
enforces the list, and adding to it is a deliberate decision, not a drive-by.

| Type               | Teaches                                                  | First used                                         |
| ------------------ | -------------------------------------------------------- | -------------------------------------------------- |
| `rotate-match`     | Rotate a model until it matches a reference              | Earth (sundial, day/night, tilt, moon phase)       |
| `connect-the-dots` | Constellations, plus a fact about the brightest stars    | Earth (Big Dipper)                                 |
| `parallax-compare` | Compare two visuals and judge the difference             | Earth (day length), Moon (distance)                |
| `zoom-split-star`  | One dot resolves into several stars as you zoom          | Mizar/Alcor — see [`../sources.md`](../sources.md) |
| `trajectory-match` | Follow a real orbital path                               | Earth (one-year orbit, Зорница)                    |
| `gravity-drop`     | Air, not weight, is what separates a feather from a rock | Earth (with air), Moon (Apollo 15, without)        |
| `telescope-focus`  | How focus works; previews planets not yet visited        | Earth                                              |

### Why seven and not five

The count went 5 → 13 → 7. The Earth brief proposed one type per beat, which two
independent plan reviews called scope creep: four of the ten Earth beats are
**the same interaction** — rotate a rendered object until it matches a reference
within tolerance — so they are one engine and four renderers.

**A beat is level content. A type is code maintained forever.** Only
`gravity-drop` and `telescope-focus` were genuinely new interactions.

**Review trigger:** any type not reused on a second level by the Mars build gets
**deleted, not maintained.**

### Config is validated per type

`schemas/level-data.schema.json` carries an `if`/`then` branch per type
constraining that type's `config`. `rotate-match` requires
`{targets, tolerance}` with `additionalProperties: false`. **A type whose engine
does not exist yet must carry no config at all** — that is deliberate, so nobody
pins a guess about a shape only building can reveal. Whoever builds an engine
replaces the placeholder with a real schema.

## The rule every puzzle obeys

**Hide the math.** No equations. No typed numbers. No visible units. Sliders,
drag-and-drop, rotating models and visual comparison only. A child should feel
like they noticed something, not like they did homework.

This is checked by the `pedagogy-report` skill before a commit that touches
`src/puzzles/`.

## Interaction model

Player walks to a glowing marker → a focused mini-game opens → they solve it →
it closes → the world reacts (a path lights, a door opens).

## Unlock gate

A level unlocks the next at `unlockThreshold` in its level data: `1.0` for the
two guided levels (Earth, Moon), `0.7` for open-exploration levels. Kept as data
so both kinds run one code path, and deliberately forgiving — a child who solves
most of a level moves on.

**The threshold is computed over `solved ∩ required`, not over every marker.**
Each marker carries a `required` boolean defaulting to `true`; optional markers
award progress but never gate. So guided still means 1.0 — **of the required
markers** — and a level with zero required markers is rejected, since it would
unlock at nothing.

`data/scripts/validate-levels.py::meets_threshold` is the canonical definition.
**`src/shared/game-state.ts` must match it.** It does not yet: `solvedCount`
counts every solved marker and `meetsThreshold` takes a bare total, so a child
could unlock a guided level by finishing only optional puzzles. Porting the
intersection into the runtime is outstanding phase-2 work.
