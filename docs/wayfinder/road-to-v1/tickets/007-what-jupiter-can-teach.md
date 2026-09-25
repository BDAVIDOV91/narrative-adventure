---
id: "007"
title: What Jupiter can teach, deep
type: research
status: closed
assignee: claude
blocked_by: []
---

## Question

Research 002 gave Jupiter only two breadth rows, and one of them used `zoom-split-star`, which ticket 005 deletes.
Jupiter is roster page 4 (ticket 001). What can it honestly teach through the remaining types?

The research should follow 002's Moon and Mars format:

- what is actually happening;
- candidate beats, each with a type and a fallback type;
- misconception risks;
- a do-not-claim list.

It should also answer two questions:

- Can Jupiter carry a required spine at 0.7 on `rotate-match` alone, the one type certain to survive 005?
- Which beats depend on which types surviving?

Run by `astronomy-consultant`. The findings are candidates, not design facts.

## Resolution

Findings: [research/007-what-jupiter-can-teach.md](../research/007-what-jupiter-can-teach.md). It is a candidate list,
not design facts.

- **The candidates.** There are eleven. The recommended spine is J1 (the naked eye → binoculars → telescope ladder),
  J2 (the moons move; a circle seen edge-on is a line), J4 (brighter than Sirius) and J7 (the fast spin), with J3
  (Ganymede wider than Mercury) as an extra.
- **Jupiter cannot carry a 0.7 spine on `rotate-match` alone.** It needs `telescope-focus`, `trajectory-match` and
  `parallax-compare` to survive ticket 005. At minimum it needs `parallax-compare` plus a new `rotate-match` renderer.
- **If 005 keeps only `rotate-match`,** ticket 006 must raise Jupiter's viability with the owner.
- **The Galilean periods are sourced by excerpt** (NASA moon fact pages). That closes #20 for a schematic use once the
  checker fetches them.
- **`gravity-drop` has no honest Jupiter scene:** there is no surface.
- **Registered in `docs/sources.md`:** five Jupiter myths as NOT ATTESTED, and the Red Spot's "twice Earth" as
  DISPUTED.
