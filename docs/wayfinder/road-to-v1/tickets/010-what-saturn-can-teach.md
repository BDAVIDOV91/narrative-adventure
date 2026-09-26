---
id: "010"
title: What Saturn can teach, deep
type: research
status: closed
assignee: claude
blocked_by: []
---

## Question

Saturn joined v1 as page 5 (ticket 009 Q5, Q8). What honest beats can Saturn carry on the **five kept puzzle types**:
`rotate-match`, `connect-the-dots`, `parallax-compare`, `trajectory-match` and `telescope-focus`?

**Fail condition (owner, ticket 009 Q17):** if fewer than **three** honest _required_ beats survive, Saturn returns to
post-v1 and the ticket 001 amendment is reverted. Say so plainly in the findings; do not pad the list.

Constraints, not to be re-asked:

- **The five kept types only.** Reviving `zoom-split-star` or `gravity-drop` reopens ticket 005. That is argued in ADR
  0006, not here. Saturn's uses do not count toward the ADR 0006 trigger.
- **The Saturn drop/pull wall** holds: Saturn is absent from any drop or pull comparison (`docs/sources.md`, "Surface
  gravity per body").
- **Already shipped, so no repeat:** Earth's `fact.telescope-saturn`, the ring "ears" through a small telescope.
  - A rings beat must teach something new: for example the ring-tilt cycle (a `rotate-match` candidate in research
    002).
  - The ring-opening angle is not in `data/generated/`. Say which cited row or one-off computation would feed it
    (ticket 001's round-1 pivot bars new pipeline).
- **Naked eye:** Saturn is a point of light and always fainter than Sirius. Rings need a telescope.
- **Titan** is a major moon and a candidate. It gets no page of its own.
- Check `docs/sources.md` NOT ATTESTED (and RETIRED, once it exists) before proposing a claim. No folklore beats.

Method: the `astronomy-consultant` agent for physics, the `research` skill for other external facts. Findings go to
`research/010-what-saturn-can-teach.md`; they are candidates, not design facts (map Notes). Research 002's Saturn rows are
the starting point.

## Resolution

Findings: [research/010-what-saturn-can-teach.md](../research/010-what-saturn-can-teach.md). It is a candidate list,
not design facts.

- **Verdict: three honest required beats survive, so Saturn stays in v1.** The margin is thin.
  - **S1, the rings come and go (spine).** Drag Saturn round a circular orbit (`rotate-match`, `drives: orbitAngle`, a
    new renderer, axis arrow kept parallel): open from above, a thin line, open from below. The rings never move; the
    viewpoint does. It links to Saturn's seasons from its tilt. Never `drives: tilt`, which would teach that the rings
    tip. Fallback `trajectory-match`.
  - **S2, the slowest wanderer.** Saturn's short creep on the real star map beside Mars's trail (`connect-the-dots`,
    existing RA/Dec). The weakest of the three: a new lesson on a reused interaction.
  - **S3, the moon wrapped in fog.** Our Moon against Titan at true scale; the Moon shows craters, Titan only haze,
    then a labelled spacecraft infrared view (`parallax-compare`).
- **The fail line for ticket 011.** If 011 judges S2 a repeat of Mars, the count falls to two and Saturn returns to
  post-v1, unless S4 (the rings are a swarm; inner pieces overtake outer, `trajectory-match`) gets its NEEDS SOURCE
  closed by a NASA or primary page.
- **The gate.** Exactly three required markers at 0.7 means all three are needed. S4, once sourced, restores choice
  (3 of 4). Ticket 011 decides.
- **Out:** faintness vs Sirius (back cover only), density/"floats", the hexagon, a standalone seasons or fast-spin
  beat (repeats Earth and J7), Enceladus (not major under rule 6). S5, Saturn's own ladder (`telescope-focus`),
  overlaps Earth's beat and is optional only.
- **Ring-opening data.** Not in `data/generated/`. A hand-authored `data/reference/saturn-ring-geometry.json`
  (obliquity from NSSDC, IAU pole from Archinal et al. 2018, the 2025-03-23 crossing and 2025-05-06 equinox anchors)
  draws S1; the window inset needs the one-off computation behind `docs/sources.md` "Through a small telescope",
  re-run monthly and recorded there, which settles the post-opposition dip.
- **Cross-level:** Earth's `fact.telescope-saturn` art should show a narrowly open south face for 2026–27, not the
  poster view.
- **False claims recorded now** in `docs/sources.md` "Saturn myths — NOT ATTESTED" (floats; vanishes every 15 years;
  disappears completely; rings tip; open steadily; Titan largest / heavier than Mercury / only atmosphere; hexagon in
  a telescope) and "Saturn's ring thickness — DISPUTED".
- **Types Saturn would use** (for ADR 0006's reverse-dependency line, written by 011): `rotate-match`,
  `connect-the-dots`, `parallax-compare`, and `trajectory-match` if S4 is adopted.
- All external sources are search excerpts; `astronomy-accuracy-checker` must fetch each page when 011 adopts a claim.
