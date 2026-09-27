---
id: "008"
title: Assemble the ordered v1 build spec
type: grilling
status: closed
assignee: owner
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

## Resolution

Grilled with the owner on 2026-09-27 in two rounds, then challenged by two `challenger`s (coverage: approve;
feasibility: revise). One round-1 answer (the font) rested on a false premise and was re-asked. Every answer took the
recommended option.

The spec: [`docs/design/v1-build-spec.md`](../../../design/v1-build-spec.md). Twenty-one phases, the phase procedure
once, seven milestones, and a finish-bar and a v1-spec §6 table with no line unscheduled.

Facts checked first:

- `earth-orbit-year` and `earth-twilight-zornitsa`, both E5 beats, carry `dataRef`s into `orbital-positions.json`
  (`src/scenes/earth/earth-data.json:97,130`). No `src/` code reads a `dataRef` yet.
- `qa-report`'s Cyrillic check looks for blank boxes and fallback substitution only, not Bulgarian letter shapes
  (`.claude/skills/qa-report/SKILL.md:45-46`). On M1, `fc-match Georgia` gives Noto Serif, so M1 does not show what a
  child's machine renders from `src/shared/fonts.ts:10`.
- `drives` has no `rotation` already (`schemas/level-data.schema.json:71-73`).
- v1-spec §6's agent-memory lines (:350-352) and the `solvedCount` comment (:167) had no phase.

### Decisions

1. **Home and format:** one file, `docs/design/v1-build-spec.md`, beside `v1-spec.md`, with the same authority rule.
   The offload phase is always "M2 offload", never bare "M2", which is also a Moon marker.
2. **E5 is the first runtime reader of `orbital-positions.json`**, so `perf-report` gates E5 and Mars A carries no
   ephemeris perf gate. If E5's plan finds its engines do not read the `dataRef`, the gate moves to Mars A in that plan.
3. **The storybook font** (re-asked after the challenge): one self-hosted font whose default glyphs are Bulgarian forms,
   verified per rule 3, lands in grid + ribbon. RED/GREEN: `FONT_STACK` leads with it and its woff2 exists under
   `assets/fonts/`. Clears the map's fog patch.
4. **§6 orphans by first needer:** T005's agent-memory lines → E0; the `solvedCount` comment → E7; T006's Galilean,
   NSSDC, J2000 and JPL-column notes → Jupiter A; T011's PIA03156, ring-speed and Wayback notes → Saturn A.
5. **A handoff** in `docs/handoffs/2026-09-27-session-handoff.md`.
6. **Pointers** to the spec from CLAUDE.md's Wayfinder section, README and `v1-spec.md`.

Challenger fixes folded into the spec: Earth's `remembers` swap is proven by the fixture test, not in play (T002 d9);
E5 and E6 state their `bodies` and `rungs` arrays; multi-body `trajectory-match` lands in E5 if its body count is above
1 (T003); "work never waits for the M2" covers exit suite runs only, so M2 offload's exit and E1's entry need the M2
online; the missing finish-bar and §6 rows.

The map is finished: no ticket remains, and both fog patches are struck.
