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
- Assign every seam from 002 to its first-needing phase. The `data/reference/` loader, for example, belongs to whichever
  of Moon (radius rows), Mars (R2) or Jupiter comes first.
- Any seam that lands in a level phase and makes it too big for one session splits here.
