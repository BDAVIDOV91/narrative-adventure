# 0001 — Python is a build-time toolchain, never a runtime backend

- **Status**: accepted
- **Date**: 2026-09-08

## Context

The game needs real astronomy: where Venus actually sits at twilight, how Mars
actually appears to reverse, how far apart things actually are. Python with
Skyfield is the right tool for that math. The obvious-looking design is a small
API the game calls.

## Decision

No backend. No Python process runs while the game is being played. Python
scripts write files into the repo; the browser reads those files.

**The boundary rule:** if the output can be computed once and committed, it is a
build step. If it would need to respond to a player action, redesign it into
precomputed data.

## Why

- Every astronomy quantity this game teaches is deterministic. There is nothing
  to compute live.
- The brief scopes the project as local-only with no hosting. A server is a
  deployment problem deferred, not avoided.
- The dev machine has ~1.9GB RAM free. A Python process alongside Vite, a
  browser and Three.js is waste.
- Nothing needs server authority: single-player, offline, no score to protect.

## Consequences

- Save data goes to `localStorage`. No account, no sync. See [0003](0003-bulgarian-only-for-v1.md)
  for the related scoping decisions.
- Adding a level means running a generator and committing its JSON.
- `data/generated/*.json` is committed even though it is generated — it is the
  game's input, and the game must work on a clean checkout without Python.
- Verified by killing every Python process and reloading the game.

## When to revisit

Cross-device progress sync, or classroom features where a teacher sees student
progress. Both are post-v1 and both are hosting concerns, not local-process ones.
