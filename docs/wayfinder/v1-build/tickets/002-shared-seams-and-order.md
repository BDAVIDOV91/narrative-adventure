---
id: "002"
title: Shared seams and their order
type: grilling
status: closed
assignee: owner
blocked_by: ["001"]
---

## Question

In what order are the shared seams built, and what does each one depend on? This ticket decides order and dependencies
only. Ticket 003 assigns the seams to level phases. Ticket 001's placement of Earth tasks #3 and #4 is inherited.
Only their widening past Earth's needs is open here, such as drag and a movable light for the Moon terminator.
Ticket 001 also places the first build of the hint step, the page album and the companion intro and memory elements in
Earth's wrap phase E7, and the shared reduced-motion helper in E1. The same rule applies to them.

The seams (v1-spec §3, §5 and §6):

- the puzzle overlay, companion box and progress write; the level-complete hook and completion-line display (the Moon,
  Jupiter and Saturn completion lines);
- a data-driven level-scene shell for Moon, Mars, Jupiter and Saturn. Only `earth-scene.ts` exists, and three storybook
  pages are `sceneKey: null`;
- the storybook grid (to 360px, text floor, `resize`), the bookmark ribbon and the back cover;
- hints: the pointing nudge, the hint step and its per-type enum, and `remembers` cards (one id);
- the page album: per-marker page elements lit from `solved[]`, and the album card on tap;
- the companion bundle (`content/bg/companion.json` plus its `content.ts` import), the intro and the five memory
  elements;
- schema and validator work as one seam: renderer enum values, the `orbitAngle`/`spin` pins, the per-round eclipse flag,
  the hint-step enum, `remembers`, and `unlocks` reachability tests;
- `dataRef` to `data/reference/`: extend the seam, or add a sibling loader (the build plan's call);
- the `planet-render` widening past Earth;
- new renderers and variants:
  - the Moon views;
  - `ring-view`;
  - the J7 spin;
  - three-rung `telescope-focus`;
  - multi-body `trajectory-match` (J2, S4);
  - two-panel `connect-the-dots` (S2);
- reduced motion across levels. The handoff (`:368`) says what "reduced" means per animation is a design call for the
  owner. It covers the book zoom, the ring-view, the time scrubs and the memory glow.

## Resolution

Grilled with the owner on 2026-09-27 in two rounds, then challenged by two `challenger`s (both revise). One decision
(the `dataRef` phase) rested on a false fact and was re-asked, and three gaps were put to the owner. Every answer took
the recommended option.

Facts checked first:

- `src/scenes/earth/earth-scene.ts` (63 lines) is already data-driven from `earth-data.json` (:29-44). Two storybook
  pages, not three, have `sceneKey: null` (`src/scenes/storybook-scene.ts:34,40`).
- `dataRef` is resolved only by the validator, under `data/generated/` (`data/scripts/validate-levels.py:164-185`).
  Nothing in `src/` resolves one yet.
- `data/reference/day-length-sofia.json` feeds `earth-day-length` (its `_readme`, :8). That is a required E4 beat with no
  `dataRef` (`src/scenes/earth/earth-data.json:76-87`). So the first reader of reference data is Earth, not a later
  level.
- `completed` is in the progress shape (`src/shared/game-state.ts:12`) and `meetsThreshold` exists (:117), but nothing
  sets `completed`.
- No beat after Earth needs `planet-render`:
  - new renderers are 2D (v1-spec §5; road-to-v1 003:88);
  - J7 drives two bodies (road-to-v1 006:76);
  - M9, R3, J1 and S3 are image frames.

### Decisions

| #   | Seam                          | Decision                                                                                                                                                                                                                                                                                                                                                      |
| --- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Level-scene shell             | Extracted from `earth-scene.ts` as the first seam after E7. Earth moves onto it in the same change, which re-runs E7's "Earth playable" exit. Every later level depends on it.                                                                                                                                                                                |
| 2   | Schema and validator          | Not one seam. Each pin lands with its first user and its own RED/GREEN test: the hint-step enum and `remembers` in E7; each renderer's enum value and pin with that renderer; the eclipse flag with the eclipse beat; `unlocks` reachability in E4 (Earth's chain, trivial at 1.0), where Mars (0.7, R1a in every passing set) is the first non-trivial case. |
| 3   | `dataRef` → `data/reference/` | Extend `dataRef` with an explicit root prefix (`reference/…`). It lands in **E4**: `earth-day-length` gains the `dataRef`, and the validator change, the first runtime resolver and a RED/GREEN test ship with it. E5 reuses them. No sibling loader.                                                                                                         |
| 4   | `planet-render` past Earth    | The seam is deleted; `planet-render` stays as E2 leaves it. A beat that truly needs 3D reopens this in its own plan. The Moon terminator's "movable light" belongs to the 2D Moon-view renderer.                                                                                                                                                              |
| 5   | Engine variants               | The E4–E6 engines take the variant's config shape from day one: arrays of rungs, bodies and panels. Only Earth's case is rendered and played. Variant renderers land with their first level.                                                                                                                                                                  |
| 6   | Storybook                     | Grid and ribbon form one seam, right after the shell and before the Moon, with all six tiles: Jupiter and Saturn closed with their existing name keys, plus a plain, dim, closed back-cover tile. Its exit re-plays Earth's album, memory and intro, and tests that they survive a `resize`. The back cover's opening, art and lines come after Saturn.       |
| 7   | Level-complete hook           | Lands in E4 (it sets `completed` at threshold and unlocks the next page), proven by the "Earth completable" exit. The completion-line display is a data-driven optional field that lands with the Moon.                                                                                                                                                       |
| 8   | Hint, album, companion        | Past E7 these are data-only per level: content keys, page elements, one memory, `remembers` links. A level that needs a code change raises it in its plan as a defect against the seam. The back-cover Сияна line rides with the back cover.                                                                                                                  |
| 9   | `remembers` card swap         | Built in E7 and tested with a fixture pair; Earth has no real pair. Jupiter adds only the J1 data and plays it. Ticket 001's "wiring stays with Jupiter" means the data link.                                                                                                                                                                                 |
| 10  | Pointing nudge                | Built in E7 with the hint step. Data-only past Earth.                                                                                                                                                                                                                                                                                                         |

Also:

- **Reduced motion:** inherited from ticket 001, decision 6. There is no new seam.
- **`rotate-match` is exempt from decision 5.** Its later variants are renderers (the Moon views, `ring-view`, J7's
  spin). E3's plan leaves room for J7's second body in the renderer, not the engine config.
- **Decision 5 against ADR 0006 (:61-63),** which says "nobody pins a guess about a shape that only building can reveal".
  The arrays are not guesses: J1, J2, R1b, S2 and S4 are designed levels. Limits:
  - array shape plus `minItems: 1`, and nothing more;
  - per-element fields only for what Earth uses;
  - no code or tests for length > 1 until that level's plan;
  - E5's plan states `earth-twilight-zornitsa`'s body count.
- **Overlay riders past Earth:**
  - the eclipse safety key, shown whenever the beat opens, rides with the eclipse beat;
  - image credit lines and the infrared label ride with the first credited image (S3).

### Resulting order

E0–E7, with these additions:

- E4 gains the `reference/` `dataRef`, the resolver, the level-complete hook and the reachability pin;
- E4–E6 gain the variant config shapes;
- E7 gains the hint-step enum and `remembers` pins, the card swap and the nudge.

Then comes the shell (Earth migrated), then grid + ribbon + the closed cover tile, then the levels, then the back cover
after Saturn.

Handed on:

- **Ticket 003** orders the levels and assigns the per-level riders:
  - the completion-line display (Moon);
  - variant renderers and their pins;
  - the eclipse flag and safety key;
  - image credits;
  - each level's reference rows.
- **Ticket 008** folds decisions 1–3, 5–7, 9 and 10 into the phase list.
