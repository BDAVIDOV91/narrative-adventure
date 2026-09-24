---
paths:
  - 'src/**/*.ts'
  - 'index.html'
  - '**/*.css'
---

## Frontend standards for an 11–12-year-old player

Adopted from the mentor's `standards-frontend.md` on 2026-09-24. Only the lines that matter for a child's Phaser game
are kept. The component, CSS-methodology and font-choice advice was dropped: Phaser draws the UI on a canvas, and the
font rule is CLAUDE.md rule 3 (Cyrillic coverage).

- **Touch targets at least 44×44 px**, measured at the game's rendered scale, not in source units. Children tap
  imprecisely, and the game must also work on a touchscreen.
- **Contrast at least 4.5:1** for normal text and 3:1 for large text. Never carry meaning by colour alone: a solved
  marker needs a shape or icon change as well as a colour change.
- **Respect `prefers-reduced-motion`.** The book-zoom transition and any spinning model must have a reduced or instant
  path. Nothing handles it yet: phase-2 task #9 in `docs/handoffs/2026-09-09-session-handoff.md`. Do not build it as a drive-by; raise it as its own
  task.
- **Bulgarian runs long** (rule 3): text containers wrap and grow, never fixed-width, and a label is checked at its
  longest real string.
- Every animation has a purpose. A child should be looking at the astronomy, not waiting for a transition.
