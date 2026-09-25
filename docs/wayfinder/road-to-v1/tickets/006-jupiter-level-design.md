---
id: "006"
title: Jupiter level design: beats, types and the required/optional split
type: grilling
status: open
assignee: ""
blocked_by: ["005", "007"]
---

## Question

What does the Jupiter level teach, and through which types? Jupiter is roster page 4 and open at 0.7 (ticket 001).
Decide:

- the beats;
- the type for each;
- the required/optional split;
- the companion tier count.

Candidates come from research 007, plus the Jupiter rows of research 002. Keeping a type alive is not a design goal.

Fixed:

- **Only types that survive ticket 005.**
  - Jupiter comes after the ADR 0006 anchor, so its use cannot revive a deleted type.
  - `zoom-split-star` is gone.
- **The moons.** The Galilean moons are "up to four" points in one undated, schematic arrangement.
  - Nightly positions would need a new pipeline, which is barred.
  - Binoculars, never the naked eye (NOT ATTESTED in `docs/sources.md`).
  - Never call the moons stars.
- **Hide the math.** Ganymede against Mercury, and Jupiter against Sirius, are visual comparisons only. No radius,
  magnitude or period on screen.
- **Physical constants.** Radii and the Galilean periods (#20, NEEDS SOURCE) are cited `data/reference/` rows.
- **Content.** Every string is a `content/bg/` key.
  - `fact.telescope-jupiter` (VERIFIED, `docs/sources.md:235`) is not yet wired to any beat, so it is free to adopt.
  - Earth's telescope beat rewards Saturn.
- **No folklore beats.**
- **The data window** is 365 days, which shows only about 30° of Jupiter's orbit.

If research 007 finds too few honest beats for a required spine, raise it with the owner through `AskUserQuestion`.
This does not reopen ticket 001; it reports what the designed level can carry.

Close only when every claim the design adopts is VERIFIED in `docs/sources.md`.

Settled by ticket 004: Mars reuses `telescope-focus`, `trajectory-match` and `parallax-compare`, so all three types
Jupiter's spine needs (research 007) have a second level. Jupiter's viability condition is met, pending 005.

Settled by ticket 005:

- **Five types survive**: `rotate-match`, `connect-the-dots`, `parallax-compare`, `trajectory-match`,
  `telescope-focus`. `gravity-drop` and `zoom-split-star` are deleted, so the "`gravity-drop` never models mass" wall
  is retired.
- **Candidate fact: `fact.gravity-drop.bodies`** (Moon slow, Mars faster, Jupiter much stronger pull), backed by
  `data/reference/surface-gravity.json`. It is not adoptable verbatim, since two thirds of it is about the Moon and
  Mars. A Jupiter use may say only "pull", never falls or lands (no true surface; `docs/sources.md:1286`). The value is
  the 1-bar row. A rewrite is a new string and needs its own wording check. If this ticket declines it, the claim is
  marked RETIRED and the build deletes the reference file and its test.
