# 0006 — Seven puzzle types, because a beat is not a type

- **Status**: accepted
- **Date**: 2026-09-09

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
