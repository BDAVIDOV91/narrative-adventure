---
id: "011"
title: Saturn level design: beats, types and the required/optional split
type: grilling
status: open
assignee: ""
blocked_by: ["010"]
---

## Question

Design Saturn's level the way tickets 004 and 006 designed Mars and Jupiter. That covers the beats, their types, which
are required, the spine, and the companion tier count.

Constraints, not to be re-asked:

- Everything in [What Saturn can teach, deep](010-what-saturn-can-teach.md), including its fail condition: if 010 found
  fewer than three honest required beats, close this ticket out of scope instead.
- The five kept types only. Once Saturn's types are known, append a Saturn reverse-dependency line to ADR 0006
  "When to revisit" (like Jupiter's).
- Hints and nudges follow ticket 008 and ADR 0007. Every adopted claim is VERIFIED by `astronomy-accuracy-checker`
  before this ticket closes.
- Saturn is the last world page. The back cover follows it and unlocks when Saturn is completed (ticket 009).
