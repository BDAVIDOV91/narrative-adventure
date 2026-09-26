# 0006 — Seven puzzle types, because a beat is not a type

- **Status**: accepted
- **Date**: 2026-09-09
- **Amended**: 2026-09-25 — see "the trigger applied" below

## Context

`CLAUDE.md` has always said the enum is closed and that **"a sixth type is a
one-off that needs its own maintenance forever — adding one is a deliberate
decision, never a drive-by."** This is that deliberate decision, recorded so a
future reader does not relitigate it or, worse, quietly repeat the mistake it
corrects.

The Earth level brief proposed **ten puzzles and named eight new type IDs**:
`shadow-sundial`, `day-night-spin`, `seasons-tilt`, `orbit-drag`,
`moon-phase-preview`, `find-zornitsa`, `gravity-drop`, `telescope-focus`,
`day-length-compare`. One type per beat.

The owner initially chose to adopt all of them, taking the enum from 5 to 13.
Two `challenger` agents then reviewed the build plan independently and **both
called it scope creep, arriving at the same collapse without seeing each other's
work**. The owner reversed the decision on that evidence.

## Decision

**Seven types**: `rotate-match`, `connect-the-dots`, `parallax-compare`,
`zoom-split-star`, `trajectory-match`, **`gravity-drop`**, **`telescope-focus`**.

All ten Earth beats still ship. They are **level content, not types**:

- `shadow-sundial`, `day-night-spin`, `seasons-tilt` and `moon-phase` are one
  interaction — rotate a rendered object until it matches a reference within
  tolerance. **One engine, four renderers.**
- `orbit-drag` is `trajectory-match` with a closed path.
- `find-zornitsa` is `trajectory-match` over real Venus ephemeris — and is better
  for it, since dragging Venus along its actual path shows the _same object_
  arriving at morning and at evening, which is the whole point of the folk beat.
- `day-length-compare` is `parallax-compare`'s shape: two visuals, judge the
  difference.

Only `gravity-drop` and `telescope-focus` are genuinely new interactions.

## Why

**A beat is content that ships once. A type is code that is maintained forever.**
Each type costs a config sub-schema, a validator branch, content keys, an engine,
a pedagogy review and a regression suite — costs meant to amortise across every
planet. Thirteen types to serve ten beats inverts that: reuse _inside_ the first
level would have been zero, and three of the thirteen would have been used by no
level that exists.

The governing test in the brief is that this game is **"meant to be genuinely
finished, not an infinite scope-creep exercise."** With `src/` at 531 lines and
no puzzle code at all, committing to thirteen engines was the shape of not
finishing.

## Consequences

- `schemas/level-data.schema.json` constrains `config` **per type**, in an
  `if`/`then` branch each. A type whose engine does not exist yet must carry no
  config at all — deliberately, so nobody pins a guess about a shape that only
  building can reveal. Whoever builds an engine replaces the placeholder.
- **Review trigger: any type not reused on a second level by the Mars build gets
  deleted, not maintained.** A dead type is worse than a missing one, because it
  looks like a decision.
- The renderer, not the type, carries what differs between the four
  `rotate-match` beats. If those renderers turn out to share nothing, that is
  evidence the collapse was wrong — revisit here rather than adding types
  silently.
- Extra type names remain available if a future level genuinely needs one. None
  is created speculatively.
- Supersedes the "five puzzle types" wording in `CLAUDE.md`,
  `docs/design/puzzle-types.md` and `README.md`, all updated.

## Amendment, 2026-09-25 — the trigger applied

The review trigger above fired when the Moon and Mars were designed (wayfinder map `road-to-v1`, tickets
[003](../wayfinder/road-to-v1/tickets/003-moon-level-design.md),
[004](../wayfinder/road-to-v1/tickets/004-mars-level-design.md) and
[005](../wayfinder/road-to-v1/tickets/005-adr-0006-verdict.md)). Mars is the anchor. Jupiter is roster page 4 and
comes after it, so Jupiter's uses do not count, and Jupiter cannot revive a deleted type.

| Type               | Earth | Moon                | Mars   | Verdict    |
| ------------------ | ----- | ------------------- | ------ | ---------- |
| `rotate-match`     | 4     | M1, M3, M2, eclipse | —      | keep       |
| `connect-the-dots` | 1     | —                   | R1a    | keep       |
| `parallax-compare` | 1     | M5                  | R2, R6 | keep       |
| `trajectory-match` | 2     | —                   | R1b    | keep       |
| `telescope-focus`  | 1     | M9                  | R3     | keep       |
| `zoom-split-star`  | 0     | —                   | —      | **delete** |
| `gravity-drop`     | 1     | —                   | —      | **delete** |

**Five types remain.** No exception was granted.

- `zoom-split-star` has no use on any designed level. Its only target, Mizar/Alcor, is stellar and outside CLAUDE.md
  rule 6.
- `gravity-drop` has no second level. Mars's drop beat was cut on its astronomy: it repeats Earth's Mars rung, and
  Mars's thin real air makes neither air flag honest.
- Earth therefore ships **nine** beats, not ten. The Decision section's "All ten Earth beats still ship" is superseded.
- Losing `gravity-drop` does not lose its lessons. The air-not-weight lesson and the Apollo 15 hammer-and-feather drop
  become the Moon level's completion line. The Moon/Mars/Jupiter pull comparison is offered to the Jupiter design as a
  fact only.

The title and the lines above still say "seven". They are the 2026-09-09 decision, left as written; the live count is
five.

### When to revisit

The verdict reopens if the build cuts a beat that is a type's only second-level use. Each type dies with its own set:

- `connect-the-dots`: Mars R1a;
- `trajectory-match`: Mars R1b;
- `telescope-focus`: both Moon M9 and Mars R3;
- `parallax-compare`: Moon M5 and Mars R2 and R6, all three.

A deleted type is not restored by a later level. A future level that genuinely needs one of these interactions makes
the case as a new deliberate decision, here.

Jupiter (ticket 006, page 4, after the anchor) uses `telescope-focus`, `trajectory-match`, `parallax-compare` and
`rotate-match`. Its uses change none of the sets above. The dependency runs the other way: if a set above is cut and
its type deleted, ticket 006 reopens for the Jupiter markers on that type (R1b → J2; M9 and R3 → J1; M5, R2 and R6 →
J3 and J4).

Saturn (ticket 011, page 5) uses `rotate-match`, `connect-the-dots`, `parallax-compare` and `trajectory-match`. Its
uses change none of the sets above. If a set is cut and its type deleted, ticket 011 reopens for the Saturn markers on
that type (R1a → S2; M5, R2 and R6 → S3; R1b → S4). S1 is on Earth's own `rotate-match` engine, which is in no set.
