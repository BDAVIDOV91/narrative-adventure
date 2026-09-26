---
id: "002"
title: Shared seams and their order
type: grilling
status: open
assignee: ""
blocked_by: ["001"]
---

## Question

In what order are the shared seams built, and what does each one depend on? This ticket decides order and dependencies
only. Ticket 003 assigns the seams to level phases. Ticket 001's placement of Earth tasks #3 and #4 is inherited.
Only their widening past Earth's needs is open here, such as drag and a movable light for the Moon terminator.

The seams (v1-spec §3, §5 and §6):

- the puzzle overlay, companion box and progress write; the level-complete hook and completion-line display (the Moon,
  Jupiter and Saturn completion lines);
- a data-driven level-scene shell for Moon, Mars, Jupiter and Saturn. Only `earth-scene.ts` exists, and three storybook
  pages are `sceneKey: null`;
- the storybook grid (to 360px, text floor, `resize`), the bookmark ribbon and the back cover;
- hints: the pointing nudge, the hint step and its per-type enum, and `remembers` cards (one id);
- the page album: per-marker page elements lit from `solved[]`, and the album card on tap;
- the companion bundle (`content/bg/companion.json` plus its `content.ts` import), the intro and the five memory
  elements;
- schema and validator work as one seam: renderer enum values, the `orbitAngle`/`spin` pins, the per-round eclipse flag,
  the hint-step enum, `remembers`, and `unlocks` reachability tests;
- `dataRef` to `data/reference/`: extend the seam, or add a sibling loader (the build plan's call);
- the `planet-render` widening past Earth;
- new renderers and variants:
  - the Moon views;
  - `ring-view`;
  - the J7 spin;
  - three-rung `telescope-focus`;
  - multi-body `trajectory-match` (J2, S4);
  - two-panel `connect-the-dots` (S2);
- reduced motion across levels. The handoff (`:368`) says what "reduced" means per animation is a design call for the
  owner. It covers the book zoom, the ring-view, the time scrubs and the memory glow.
