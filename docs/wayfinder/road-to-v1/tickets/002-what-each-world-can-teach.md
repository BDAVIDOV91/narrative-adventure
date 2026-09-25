---
id: "002"
title: What each candidate world can teach through the seven types
type: research
status: closed
assignee: claude
blocked_by: []
---

## Question

For each candidate world, what can an 11–12 year old *notice* through the seven existing types? A beat is a candidate
only if it contradicts a real misconception or reveals something surprising, and hides the math (rule 2).

Two tiers, so this fits one session:

- **Deep: Moon and Mars.** List every candidate beat, with:
  - its type;
  - the misconception it contradicts;
  - a source;
  - the data it needs, and whether that data exists in `data/generated/` or `data/`.

  For the Moon, name what it teaches beyond Earth's existing `moon-phase` beat.
- **Breadth: the Sun, Mercury, Venus, Jupiter, Saturn, Uranus, Neptune and the major moons.** At most two candidate
  beats per world with a source URL, or "no honest beat".

Also answer: does `zoom-split-star` have any honest solar-system use (for example, Galilean moons resolving beside
Jupiter in a small telescope)? Its only sourced target today is Mizar/Alcor, which is stellar and therefore outside
rule 6.

Output: `research/002-what-each-world-can-teach.md`, a candidate list only. Nothing in it is a design fact until a
design ticket adopts it and `astronomy-accuracy-checker` verifies it.

## Resolution

Findings: [research/002-what-each-world-can-teach.md](../research/002-what-each-world-can-teach.md). It is a candidate
list, not design facts; no claim in it is adopted by closing this ticket.

- **Moon (deep):** nine candidate beats. M1–M4 all ride the existing `rotate-match` `orbitAngle` drive and go past
  Earth's `moon-phase`. They teach that the Moon turns, that it has no dark side, that the shadow is not the phase,
  and earthshine. M8 (`gravity-drop`) only repeats Earth.
- **Mars (deep):** retrograde (R1, `trajectory-match`) runs on committed data. There are also size (R2) and telescope
  (R3) beats. R7 (`gravity-drop`) hits an air-flag trap: Mars's thin real air fits neither panel.
- **Breadth:**
  - Neptune has no honest beat, and Io, Europa, Callisto, Triton and Enceladus get fact strings only.
  - Uranus's sideways tilt is a strong `seasons-tilt` reskin.
  - Jupiter is the only honest home for `zoom-split-star`.
- **Registered:** ten myths as NOT ATTESTED, plus Phobos's "only such moon" and Venus's "day longer than year" as
  DISPUTED, in `docs/sources.md` under "Claims ruled out during v1 roster research".
- **Checked:** Earth's `fact.seasons.distance` wording is specific to Earth, so Mars's eccentric seasons would extend
  the lesson, not contradict it.
- **Forks routed:**
  - Phobos as a major moon: ticket 001.
  - Repeat-only reuse: ticket 005.
  - `zoom-split-star` depends on Jupiter: tickets 001 and 005.
