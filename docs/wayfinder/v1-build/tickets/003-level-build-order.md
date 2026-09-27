---
id: "003"
title: Level build order after Earth
type: grilling
status: closed
assignee: owner
blocked_by: ["002"]
---

## Question

After Earth, in what order are Moon, Mars, Jupiter and Saturn built, and which phase owns each seam from ticket 002?

- Follow the roster (Moon → Mars → Jupiter → Saturn), or go by seam risk? For example, Saturn's `ring-view` and
  reference geometry could come early.
- Each level's entry criterion: which seams must already exist.
- Ticket 002 fixes the frame: the shell, then grid + ribbon come before any level, and the back cover comes after Saturn.
  The `reference/` `dataRef` lands in E4. Assign the per-level riders from 002's Resolution to their first-needing
  phase:
  - the completion-line display;
  - the variant renderers and their pins;
  - the eclipse flag and safety key;
  - image credits;
  - each level's reference rows.
- Any seam that lands in a level phase and makes it too big for one session splits here.

## Resolution

Grilled with the owner on 2026-09-27 in two rounds, then challenged by two `challenger`s (both revise). One round-1
answer (every A phase exits "completable") rested on a false premise and was re-asked: the open levels' A phases hold
only two required beats. Three challenger findings went to the owner. Every answer took the recommended option.

Facts checked first:

- `data/generated/orbital-positions.json` starts 2026-09-08 and runs 365 daily samples. Mars, Jupiter, Saturn and the
  Moon carry `raHours`, `decDegrees` and `distanceAu`. R1a (Nov 2026 – May 2027), J4 (Feb – Apr 2027), S2 and M5 need no
  new generator run.
- `src/scenes/moon/` and `src/scenes/mars/` hold only `.gitkeep`. The storybook has three pages; Moon and Mars have
  `sceneKey: null` (`src/scenes/storybook-scene.ts:30-41`).
- A page unlocks when the previous level is `completed`, and a bright tile shows its blurb
  (`src/scenes/storybook-scene.ts:78-79,95`). The Moon blurb („сменя лицето си всяка нощ", `content/bg/levels.json:6`)
  contradicts M1. The Mars blurb („тръгва назад", :9) is the "reverses" claim. Jupiter and Saturn have no blurb key.
- Gates (v1-spec :19-22): the Moon's is its three-beat spine; Mars and Jupiter need the head + 3 of 4; Saturn the head +
  2 of 3.
- M3's passive tilt inset is preset per round as "eclipse month" or "ordinary month" by the per-round flag
  (`road-to-v1/tickets/003-moon-level-design.md:60,76-79`). M3 is that flag's first user, not the eclipse beat.

### Decisions

1. **Roster order**: Moon → Mars → Jupiter → Saturn. No risk-first jump: `ring-view` is 2D, the ring geometry is data,
   and the ephemeris is committed.
2. **Phases per level.** A = the level's scene, its head beat and the beat that head unlocks, with the code they need.
   B = the remaining beats, including any remaining variant renderers, plus the level's content. Jupiter's B splits in
   two (below).
3. **Entry is strictly serial.** Moon A enters on the grid + ribbon exit (ticket 002 decision 6). Every later phase
   enters on the exit before it.
4. **Exits.** "Completable" = the threshold met in a real play-through, and the next page unlocks through E4's
   level-complete hook. For Saturn it means `completed` is set and survives a reload, and the cover tile stays closed
   until the back-cover phase. "Playable" = every beat solved in play; nudges, hint steps and `remembers` cards shown;
   album elements lit; the memory glows once; the completion line (where the level has one); progress survives a reload;
   reduced motion honoured. Every phase also carries ticket 001 decision 7's per-phase exit.
5. **The eclipse flag moves to Moon A, with M3** (owner, amending ticket 002 decision 2's wording under its own rule,
   "each pin lands with its first user"). Moon B keeps only the eclipse view and its safety key, so cutting the eclipse
   on overrun (v1-spec :141) never takes M3's flag.
6. **Blurb rule** (owner): a page's blurb, rewritten or new and claim-checked, lands no later than the phase whose exit
   unlocks that page. The Moon blurb rewrite is added to **E4** (an addition to ticket 001's E4). Mars → Moon A;
   Jupiter → Mars B; Saturn → Jupiter B2. No wrong claim and no raw key ever reaches a bright tile.
7. **Jupiter B splits** (owner): B1 is J7 alone; B2 is J3, J4 and the content. Jupiter A stays whole: J1's rungs are
   the array shape E6 already takes (ticket 002 decision 5), and J2 extends the multi-body `trajectory-match` that R1b
   builds first.
8. **Reference rows: first needer only.** Ticket 005 decides where each is built.

   | Row                                         | First needer        |
   | ------------------------------------------- | ------------------- |
   | Moon radius, Mars radius                    | Mars B (R2)         |
   | Galilean periods and orbit radii            | Jupiter A (J2)      |
   | Jupiter radius                              | Jupiter A (J2)      |
   | Jupiter and Earth rotation periods          | Jupiter B1 (J7)     |
   | Ganymede and Mercury radii                  | Jupiter B2 (J3)     |
   | `surface-gravity.json` trim or re-document  | Jupiter B2          |
   | C, B, A ring radii; `saturn-ring-geometry.json` | Saturn A (S1, S4) |
   | Titan radius                                | Saturn B (S3)       |

   M5 draws its discs from `bodies.moon.distanceAu` alone. If M5's plan draws an absolute size, the Moon radius moves to
   Moon B.
9. **Back cover**: one phase, after Saturn B.

### The level phases

| Phase      | Scope                                                                                                                                                                                                                                                                       | Exit                                                        |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Moon A     | Moon scene, data and real `sceneKey`; the Moon-view renderer(s) and the `orbitAngle` pin; the spine M1 → M3 → M2; the per-round eclipse flag and its test, with M3; the completion-line display and the Moon's line; the Mars blurb                                           | Moon completable; the Mars page unlocks                     |
| Moon B     | M5, M9; the Moon's nudges, hint steps, album ideas and memory; the eclipse beat **last**, with its view and safety key                                                                                                                                                      | Moon playable                                               |
| Mars A     | Mars scene, data and real `sceneKey`; R1a `connect-the-dots` on committed Mars RA/Dec against `stars.json`; R1b sight-line `trajectory-match`, the first multi-body case (unless E5 already needs it); the first non-trivial `unlocks` reachability test and data statement | R1a and R1b played                                          |
| Mars B     | R3, R2, R6; the Mars nudges, hint steps, four album ideas and memory; the Jupiter blurb                                                                                                                                                                                     | Mars completable and playable; the Jupiter page unlocks     |
| Jupiter A  | real `sceneKey`; J1 three-rung `telescope-focus` and its `remembers` data; J2, extending the multi-body `trajectory-match` with four moons and the edge-on strip; the reachability statement                                                                                | J1 and J2 played; the J1 `remembers` card shows             |
| Jupiter B1 | J7: the spin renderer and the `spin` pin                                                                                                                                                                                                                                    | J7 played                                                   |
| Jupiter B2 | J3, J4; the Ganymede and Mercury names; the J4 key trimmed from `fact.brightest-is-a-planet`; the completion line; nudges, hint steps, five album ideas, memory; the Saturn blurb                                                                                            | Jupiter completable and playable; the Saturn page unlocks   |
| Saturn A   | real `sceneKey`; S1 `ring-view`, its `orbitAngle` pin and the schema description update; S4 after S1, and its `remembers` data; the reachability statement                                                                                                                  | S1 and S4 played; the S4 `remembers` card shows             |
| Saturn B   | S2 two-panel `connect-the-dots` (it draws R1a's data faint); S3 with its credit lines and infrared label; the Titan name; the completion line; nudges, hint steps, four album ideas, memory                                                                                  | Saturn completable and playable                             |
| Back cover | opens on Saturn's `completed` with no new storage field; the ribbon moves to it; vignettes of completed worlds (placeholder policy: ticket 005); the Сияна line, then T009's lines                                                                                          | the cover opens after a real Saturn completion and survives reload |

Also:

- A phase plan that still overruns one session splits further in its own plan; the Moon's eclipse beat is cut first.
- Variant pins ride with their renderer's phase (ticket 002 decision 2). Credit lines first land in Saturn B.
- `remembers` pairs beyond J1 and S4 are chosen in each level's A plan and reviewed by `puzzle-pedagogy-reviewer`
  (v1-spec :160-161).
- `ui.book.locked` is deleted in grid + ribbon, whose "closed pages show the name only" removes its only caller
  (`src/scenes/storybook-scene.ts:95`).

Handed on:

- **Ticket 005** places the reference rows in decision 8 and all imagery, including placeholder policy.
- **Ticket 006** places the gates across the phase list: E0–E7, the shell, grid + ribbon, the nine level phases, the back
  cover.
- **Ticket 008** folds in the two amendments made here: the Moon blurb in E4 (ticket 001) and the eclipse flag in Moon A
  (ticket 002 decision 2), plus `ui.book.locked` in grid + ribbon.
