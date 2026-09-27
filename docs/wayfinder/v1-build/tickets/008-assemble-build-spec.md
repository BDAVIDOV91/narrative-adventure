---
id: "008"
title: Assemble the ordered v1 build spec
type: grilling
status: open
assignee: ""
blocked_by: ["005", "007"]
---

## Question

Assemble the phases from tickets 001–007 into the ordered v1 build spec. The map's Destination names what it contains:
each phase with its dependencies, entry and exit criteria, and gates.

- Where it lives and its format (for example beside `docs/design/v1-spec.md`).
- Check it against road-to-v1's finish bar line by line. Each line names the phase that meets it, and no line is left
  unscheduled.
- Check that every item in v1-spec §6 lands in a phase.
- Fold in ticket 003's amendments to earlier tickets: the Moon blurb rewrite in E4 (ticket 001), the per-round eclipse
  flag in Moon A with M3 (ticket 002 decision 2), and the `ui.book.locked` deletion in grid + ribbon.
- Fold in ticket 005's amendments (its Resolution, "Handed on"): `surface-gravity.json` re-documented in E0; the
  ring-angle row and code-drawn Saturn in E6; Sun and Moon radii in Moon B; the imagery-entry format in E2; the degrade
  recipe and imagery test in Moon B; photo checklists one phase early; public-domain-only images before Saturn B.
- Fold in ticket 006's amendments (its Resolution, "Handed on"):
  - the M2 offload phase between E0 and E1 (amends ticket 001), with its pin list, strip/add list, MemAvailable guard,
    owner checklist and CLAUDE.md section;
  - the router's `data/reference/` widening in E0;
  - a start SHA in every phase plan;
  - the E1 suite, and the ticket-004 gap checks on both machines;
  - the perf rule and its applied list, including which of E5 and Mars A first reads `orbital-positions.json`;
  - the finish-bar assertions by phase, and the `qa-report` SKILL.md updates by phase.
- Fold in ticket 007's amendments (its Resolution, "Handed on"):
  - the seven milestones (E4, E7, Moon B, Mars B, Jupiter B2, Saturn B, back cover) as exit criteria, with their README,
    `qa-report` and owner-play gates;
  - the README rule per phase, including M2 offload and E1;
  - the merge window, the failed-report block and the stuck-finding waiver, in the phase-exit procedure;
  - the `qa-report` SKILL.md additions (README check and frame rate on M1 at E4, release re-checks at the back cover);
  - the one-time GitHub merge-message setting, as an owner checklist item before merge 1.
