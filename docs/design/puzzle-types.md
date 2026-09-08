# Puzzle types

Five reusable types, each built once and reskinned per planet. A sixth type is a
one-off that needs its own maintenance forever — `schemas/level-data.schema.json`
enforces the list, and adding to it is a deliberate decision, not a drive-by.

| Type               | Teaches                                                   | First used                                                 |
| ------------------ | --------------------------------------------------------- | ---------------------------------------------------------- |
| `rotate-match`     | Moon phases, axial tilt — rotate a model to match a photo | Earth (sundial), Moon (phases)                             |
| `connect-the-dots` | Constellations, plus a fact about the brightest stars     | Earth (twilight)                                           |
| `parallax-compare` | Distance estimation from two viewpoints                   | Moon                                                       |
| `zoom-split-star`  | One dot resolves into several stars as you zoom           | See the DISPUTED entry in [`../sources.md`](../sources.md) |
| `trajectory-match` | Orbital transfer, simplified                              | Saturn (ring threading)                                    |

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
