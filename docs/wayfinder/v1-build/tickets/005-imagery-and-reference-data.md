---
id: "005"
title: Where imagery and reference-data work sits
type: grilling
status: open
assignee: ""
blocked_by: ["003"]
---

## Question

Where do the asset and data rows handed over by road-to-v1's struck "Imagery and data per level" patch
(`road-to-v1/MAP.md:106-137`, v1-spec §6) sit among the phases?

- **Imagery:**
  - the NASA textures (Earth first);
  - per-marker page art;
  - the M9, R3, PIA19400, J1, J7, Ganymede, Mercury and J4 frames;
  - PIA06230 and PIA20016;
  - Earth's telescope-Saturn art;
  - the back-cover vignettes and ribbon;
  - the five Сияна vignettes.
- **Reference data:**
  - the radius rows;
  - the Galilean periods and orbit radii;
  - the rotation rows;
  - the ring radii;
  - `saturn-ring-geometry.json` and its render test;
  - the `surface-gravity.json` trim or re-document.
- **Sources:** each image's `docs/sources.md` imagery entry.

Decide:

- whether each item rides in its level's phase, or batches into asset phases;
- which items need the owner's hands (downloads, licensing, hand-drawing), as checklists;
- where placeholder art is allowed, and the phase by which it is replaced. Placeholder art is allowed at the finish bar;
  AI-generated astronomy never is.
