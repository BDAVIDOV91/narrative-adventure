# 0002 — Phaser 3.90 over the newer Phaser 4.2

- **Status**: accepted
- **Date**: 2026-09-08

## Context

Phaser 4.2.1 is the current major release. Phaser 3.90 is the mature previous
line. The brief's framing is explicit: this project is "meant to be genuinely
finished, not an infinite scope-creep exercise."

## Decision

Phaser 3.90.0.

## Why

- **Example library.** Nearly every tutorial, forum answer and code sample
  targets v3. On a solo side project the binding constraint is not raw engine
  performance, it is how fast a problem gets unstuck at 11pm.
- **Canvas renderer fallback.** Phaser 4 is WebGL-only. Development happens on
  Linux with AMD integrated graphics, where Mesa WebGL can be unreliable.
  Phaser 3's `AUTO` mode degrades to Canvas instead of showing a blank screen.
- Phaser 4's rewritten renderer is genuinely faster, but this game draws a
  handful of sprites on a small map. It is not renderer-bound.

## Consequences

- v3 API idioms throughout. A future v4 migration is a real rewrite, not a bump.
- `src/main.ts` uses `type: AUTO` deliberately, for the fallback.

## When to revisit

If a level turns out to be renderer-bound on the target hardware — measured, not
assumed.
