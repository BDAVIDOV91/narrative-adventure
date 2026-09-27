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
