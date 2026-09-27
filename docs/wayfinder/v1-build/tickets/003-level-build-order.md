---
id: "003"
title: Level build order after Earth
type: grilling
status: open
assignee: ""
blocked_by: ["002"]
---

## Question

After Earth, in what order are Moon, Mars, Jupiter and Saturn built, and which phase owns each seam from ticket 002?

- Follow the roster (Moon → Mars → Jupiter → Saturn), or go by seam risk? For example, Saturn's `ring-view` and
  reference geometry could come early.
- Each level's entry criterion: which seams must already exist.
- Ticket 002 fixes the frame: the shell, then grid + ribbon come before any level, and the back cover comes after Saturn.
  The `reference/` `dataRef` lands in E4. Assign the per-level riders from 002's Resolution to their first-needing
  phase:
  - the completion-line display;
  - the variant renderers and their pins;
  - the eclipse flag and safety key;
  - image credits;
  - each level's reference rows.
- Any seam that lands in a level phase and makes it too big for one session splits here.
