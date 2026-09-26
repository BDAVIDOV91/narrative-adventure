# The v1 build plan

<!-- wayfinder:map -->

## Destination

An ordered v1 build spec: a sequence of build phases, each sized for one plan-mode session plus two challengers, each
with its dependencies, its entry and exit criteria, and the gates it must pass. Followed in order, the phases end at
road-to-v1's finish bar ([road-to-v1/MAP.md](../road-to-v1/MAP.md), "The finish bar").

This map decides; it does not build.

## Notes

- **Fixed inputs, not tickets.** Do not reopen these:
  - [`docs/design/v1-spec.md`](../../design/v1-spec.md), the first input: what road-to-v1 decided, with later tickets
    already winning;
  - every closed ticket in [road-to-v1](../road-to-v1/MAP.md), and its struck "Imagery and data per level" patch
    (`road-to-v1/MAP.md:106-137`), which lists the assets and reference-data rows to schedule;
  - ADRs 0001–0008;
  - the 09-09 handoff's phase-2 task list (`docs/handoffs/2026-09-09-session-handoff.md:354-367`);
  - CLAUDE.md rules 1–9 and the hardware budget.
- **Earth is inside the spec** (owner, 2026-09-26). Its content is fixed; the map only slots it into phases. The scope
  is:
  - the ticket-005 prune;
  - phase-2 #3–#9;
  - engines and renderers for the six beats #6 does not build;
  - #25;
  - Earth's share of the later tickets' work (road-to-v1 008 and 012).

  See `v1-spec.md` §1 "Earth".
- **State at charting (2026-09-26):**
  - no puzzle engine exists (`src/puzzles/*` holds only `.gitkeep`);
  - a marker click only warns (`src/scenes/earth/earth-scene.ts:40-43`);
  - `saveProgress` has no caller;
  - the prune has not run;
  - `dataRef` reaches only `data/generated/`;
  - `assets/images/*` is empty;
  - Playwright exists only as the MCP server (`.mcp.json:9-12`);
  - `development` is 55 commits ahead of `main`.
- **Bugs follow rule 5 (RED/GREEN), never tickets.** The map decides; plan mode plus two `challenger`s builds.
- **Skills per ticket:** `grilling`. Add `perf-budget-checker` for 3D, asset or bundle questions, and `privacy-guard`
  for any new devDependency.
- **Question format** (owner): every question goes through `AskUserQuestion`, one decision at a time. Options are
  ordered by confidence, and each description ends with "(CL: N%)", the percentages summing to 100. The top label ends
  exactly "(Recommended)" and states the reason and what would change the pick. The question text opens with
  "Item N of M — <ref>: <claim>", then three paragraphs labelled "What it is." (with file:line cites), "Why it
  matters." and "Proposed action."

## Decisions so far

- [Playwright QA on this machine](tickets/004-playwright-qa.md) — a pinned `@playwright/test` suite is the regression artifact, run with one worker on the headless shell and a zero-network assertion; the MCP server is for exploration; RSS on this machine, the MCP cache overlap and telemetry are still unmeasured.

## Not yet specified

- **Per-phase sizing and wording**: each phase's exact scope, entry criteria and exit criteria. Graduates once the Earth
  slotting, the seam order and the level order settle; ticket 008 may absorb it.
- **Release-time re-checks**: re-run the monthly Saturn ring-opening table behind `docs/sources.md` "Through a small
  telescope" (road-to-v1 010, 011), and re-read any VERIFIED claim whose source page may have moved.
- **README cadence**: CLAUDE.md rule 7 wants README updated after big changes. Decide which phase exits carry it.
- **Storybook display font**: `src/shared/fonts.ts:10` is a system stack, so Bulgarian glyph forms depend on the OS. Any
  adopted font is self-hosted (rule 8) and verified for Bulgarian forms (rule 3). The finish bar does not demand one.

## Out of scope

- **Worlds after Saturn, Pluto, and the companion finale**: post-v1, a fresh map (road-to-v1 Out of scope).
- **English and a worldwide version**: after v1 (ADR 0003 amendment).
- **Deploy / delivery to children, and sound**: each returns as its own effort when the owner says so.
- **New folklore work, the latitude picker, and interstellar content**: road-to-v1 Out of scope; rule 6.
- **Bugs as tickets**: bugs follow rule 5.
