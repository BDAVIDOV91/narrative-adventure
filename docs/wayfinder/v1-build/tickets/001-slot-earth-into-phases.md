---
id: "001"
title: Slot the ticket-005 prune and Earth's build into phases
type: grilling
status: open
assignee: ""
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
