---
id: "001"
title: Slot the ticket-005 prune and Earth's build into phases
type: grilling
status: closed
assignee: owner
blocked_by: []
---

## Question

Earth's content is fixed ([v1-spec](../../../design/v1-spec.md) §1, "Earth's build scope"). How does it group into build
phases, each one plan-mode session plus two challengers?

Earth's scope, listed not reopened:

- the ticket-005 prune (v1-spec §6);
- 09-09 phase-2 #3–#9 (`docs/handoffs/2026-09-09-session-handoff.md:354-367`), which ends at 3 beats playable (`:277`);
- engines and renderers for the six beats #6 does not build: `earth-day-length` (`parallax-compare`), `earth-orbit-year`
  and `earth-twilight-zornitsa` (`trajectory-match`), `earth-big-dipper` (`connect-the-dots`), `earth-telescope-focus`
  (`telescope-focus`), and the `moon-phase` renderer;
- #25, constellation visibility by latitude;
- Earth's share of road-to-v1 008 and 012: a hint step and page element per marker, album cards, the `fact.day-night`
  repeat, the `earth-telescope-focus` → J1 card, the Earth memory and the storybook intro. These are slotted here, not
  redesigned.

Decide:

- whether the prune runs before task #3 or beside it;
- how #3–#9 and the rest group into phases, and in what order;
- each Earth phase's exit criteria, including "Earth playable": 9 beats, progress written and reloaded, reduced motion;
- which latent bugs each phase closes (4, 5, 7, 8 and 10; handoff `:211`).

Where #3 (overlay, companion box, progress write) and #4 (the `planet-render` widening) land is decided here. Ticket 002
inherits that placement.

## Resolution

Grilled with the owner on 2026-09-26 in two rounds. All seven decisions took the recommended option.

Facts checked first:

- `src/puzzles/` holds `.gitkeep`-only directories. There is no `telescope-focus` directory.
- Latent bug 10 (task #7) is `earth-orbit-year` (`src/scenes/earth/earth-data.json:97`), a `trajectory-match` beat. It
  closes with trajectory-match, not with #6.
- The required markers (threshold 1.0) are the three `rotate-match` beats plus `earth-day-length` (`parallax-compare`).

### Earth's phases, in order

| #   | Phase            | Scope                                                                                                                                                                                                                                  | Closes | Milestone exit                   |
| --- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | -------------------------------- |
| E0  | Prune            | The T005 prune, the full v1-spec §6 list; 10 → 9 markers                                                                                                                                                                              | —      | —                                |
| E1  | Overlay          | #3: overlay, companion box (`companion.json` plus its `content.ts` import), progress write, book-zoom call site; one shared reduced-motion helper; reduced paths for the zoom and the overlay                                           | 4, 5   | —                                |
| E2  | Renderer         | #4: `planet-render` widening and the disposal proof; #5: the NASA Earth texture, an owner checklist at entry                                                                                                                           | 7, 8   | —                                |
| E3  | rotate-match     | The engine plus the sundial, day-night, seasons-tilt and moon-phase renderers, each played; #8, the pedagogy pass over the 12 pre-existing fact strings                                                                                | —      | 3 required beats playable        |
| E4  | parallax + dots  | `earth-day-length`, `earth-big-dipper`, #25                                                                                                                                                                                            | —      | Earth completable (Moon unlocks) |
| E5  | trajectory-match | `earth-orbit-year`, `earth-twilight-zornitsa`; #7, the `dataRef` to `seasons`                                                                                                                                                          | 10     | —                                |
| E6  | telescope-focus  | `earth-telescope-focus`; remove `ui.puzzle.coming-soon`                                                                                                                                                                                | —      | —                                |
| E7  | Earth wrap       | The hint-step and album seams, built once; Earth's hint step and page element per marker; the `fact.day-night` repeat; the Earth memory; the storybook intro; the Earth side of the J1 card (its wiring stays with Jupiter) | —      | Earth playable                   |

### Decisions

1. The prune is its own phase and runs first, so #3 builds on the final nine markers.
2. One puzzle type per phase. The two single-beat types, parallax-compare and connect-the-dots, share one.
3. Earth's share of T008 and T012 lands in one wrap phase, E7. Its seams are built once, against nine real beats.
4. The #5 texture sits in E2 as an owner checklist: which image, and where to drop it.
5. Required beats come first: parallax-compare before trajectory-match, so completion is proven at E4.
6. Reduced motion: E1 adds one shared helper. Each phase decides what "reduced" means for its own animations in its
   plan, and the owner approves it.
7. Exit criteria:
   - Every phase: `npm run validate`, `npm test`, pytest and `validate-levels.py` green; a `npm run dev` play-through
     (after `free -h` for 3D); the pre-commit routed reports clean; a reduced path for every animation it adds.
   - Milestones: E3 "3 required beats playable"; E4 "Earth completable"; E7 "Earth playable", meaning all 9 beats solved
     in a real play-through, progress written and surviving reload, reduced motion honoured, and no
     `ui.puzzle.coming-soon` left.
   - Where Playwright and `qa-report` sit is ticket 006's call.

Handed on: ticket 002 inherits #3 in E1, #4 in E2, the reduced-motion helper in E1, and the first build of the hint
step, album, intro and memory elements in E7. It decides only their widening past Earth.
