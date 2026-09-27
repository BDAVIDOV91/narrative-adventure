---
id: "006"
title: Where the pedagogy, perf, privacy, astronomy and QA gates run
type: grilling
status: closed
assignee: owner
blocked_by: ["003", "004"]
---

## Question

Per phase, which gates are exit criteria, beyond what the pre-commit router already fires (CLAUDE.md "Review gates")?

The gates:

- `pedagogy-report`;
- `perf-report`;
- `privacy-guard`;
- `astronomy-report`;
- `security-audit`;
- Playwright;
- `qa-report`.

Name where each finish-bar check first runs, and where it re-runs:

- `npm run build` + `vite preview` (the lazy Three.js chunk and WebP URLs break only there);
- the 360px portrait no-scroll and text-floor check;
- progress persisting across a reload;
- a zero-network assertion, which makes rule 8 a regression test;
- `free -h` before any 3D run, Playwright included (rule 9).

Uses ticket 004's findings for what Playwright can run.

The phase list runs E0–E7, the shell, grid + ribbon, Moon A/B, Mars A/B, Jupiter A/B1/B2, Saturn A/B and the back
cover (ticket 003).

Ticket 005 adds: `qa-report` prints the `placeholder: true` list at every milestone, and the placeholder test (and the
imagery-entry test from Moon B) runs with the suite.

## Resolution

Grilled with the owner on 2026-09-27 in two rounds, then challenged by two `challenger`s (both revise). Eight challenger
findings and one owner note went back to the owner. Every answer took the recommended option, except item 6 of round 2:
the owner proposed moving heavy tests to the remote M2, as `pdf_data_extractor_v2` does.

Facts checked first:

- The router fires per commit from staged paths only (`.claude/hooks/precommit-checks-reminder.sh:14-30`). Its
  astronomy regex misses `data/reference/` (:18). Its perf regex covers only `assets/`, `planet-render.ts` and
  `package.json` (:22).
- `qa-report` has no vitest, no Playwright suite, no preview, no placeholder print and no finish-bar checklist
  (`.claude/skills/qa-report/SKILL.md:15-23`).
- The MCP browser is headless (`.mcp.json:12`), so its WebGL is software (SwiftShader, `research/004-playwright-qa.md`),
  not the APU.
- pdfx's wrapper sends every Bash command that is not pinned to M2 (`pdf_data_extractor_v2/ops/remote-shell/remote-shell.sh:138-149`).
  It pins `git` and `playwright` to M1. Mutagen ignores `dist/` (`.claude/remote-shell/mutagen.yml:49` there). M2 is
  Ubuntu WSL.
- The repo has no git tags and no phase markers. `.claude/settings.json:60` denies `Bash(ssh:*)`.
- The M2 was offline on 2026-09-27.

### Decisions

1. **Phase-exit rule.** Every phase exit re-runs the router table over the phase's cumulative diff, and each report
   it routes is an exit criterion. No new gate definitions.
   - Each phase plan records its start SHA at entry.
   - The router runs as `PRECOMMIT_STAGED="$(git diff --name-only <start>..HEAD)"`, with a `git commit` stdin.
   - Deletions count, which matters for E0's prune.
2. **The router gains `^data/reference/` → `astronomy-report`, in E0**, with a RED/GREEN case in
   `.claude/hooks/test-precommit-checks-reminder.sh`. It lands before the first reference-row edit.
3. **A new phase, M2 offload, runs between E0 and E1 and blocks E1 entry** (amends ticket 001's phase list). E0 stays
   the prune plus the `surface-gravity.json` re-doc.
   - **Model:** the pdfx wrapper, a deny-list. Every Bash command runs on M2 except a pin list.
   - **Pins, each with a RED case in `test-pin-list.sh`:** `git`; `free` and `/proc/meminfo`; `npm run dev`; hook
     tests; wayfinder-viewer. Drop pdfx's `playwright` pin and flip its test case, because the suite runs on M2.
   - **Wiring:** `test-pin-list.sh` joins husky's `^ops/` branch.
   - **Strip:** yarn, `nc-*`, the Supabase and `.env` checks, and the gcloud, prisma and knavision pins.
   - **Add:** `uv venv`, `playwright install --only-shell`, and de440s on M2 (a one-time download at setup).
   - **The MemAvailable guard is new code:** it gets a sibling `test-*.sh` and guards every heavy or 3D run on M1.
   - **Owner checklist at entry:** Tailscale and the ssh alias, Mutagen, and the M2 bootstrap (sudo on M2).
   - **Exit:** `preflight.sh` READY, and a vitest run proven on M2 by the wrapper's hostname check. Never a direct
     `ssh`; the deny rule stays.
   - Husky still runs vitest and pytest on M1 at commit, because `git` is pinned. M2 covers explicit runs and
     phase-exit runs.
   - A CLAUDE.md section records the routing and why it fits the ssh deny rule.
4. **Playwright lands in E1.**
   - E1 entry closes ticket 004's gaps: RSS measured on **both** machines, the MCP browser-cache overlap, and
     telemetry.
   - The pinned `@playwright/test` suite starts with three tests:
     - zero-network: rule 8 as a regression test, failing on any request outside the preview origin;
     - reload persistence;
     - a preview smoke that fails on any failed request or 4xx inside the preview origin.
   - `security-audit`, `privacy-guard` and `perf-report` fire through the router when `package.json` changes.
5. **Suite cadence.** From E1 on, the suite runs on M2 at every phase exit, against `npm run build` + `vite preview`,
   with one worker and the headless shell.
   - Build+preview, zero-network and persistence therefore re-run at every exit.
   - Each level phase extends the smoke to open its scene.
   - Baselines belong to whichever machine runs the suite. They are regenerated if the fallback moves it.
6. **M2 down at an exit:** a plain `claude` session runs the suite on M1. It runs behind the guard, with `workers: 1`,
   the headless shell only and the dev server stopped (`research/004-playwright-qa.md`). The exit report says it ran
   on M1. Work never waits for the M2.
7. **Play-through.** Claude walks every phase exit (E0 included) with the Playwright MCP against `npm run dev` on M1.
   That covers rule 5's dev play, and the finish bar's two modes are dev walked and preview in the suite.
   - The owner plays at each milestone, inside `qa-report`.
   - When the owner is home, those plays may run on the M2 and its better GPU.
8. **Perf.** `perf-report` is an exit gate wherever a new renderer, a runtime texture or a `data/generated/` file first
   enters the bundle, whatever the paths.
   - Applied, that is: E2, E3, E4 (`stars.json`), E6 (the code-drawn Saturn texture), the first reader of
     `orbital-positions.json` (E5 or Mars A, ticket 008 decides), Moon A, Jupiter B1 and Saturn A.
   - Every exit also records the bundle chunk sizes from the suite's build.
   - The MCP walk is functional only. The real-hardware judgment at each renderer or texture phase is a short headed
     `npm run dev` play by the owner on **M1** (the rule-9 target), after `free -h`. A better GPU hides what this gate
     exists to catch.
9. **360×640 no-scroll and text-floor test** lands in grid + ribbon and re-runs at every exit after.
10. **Finish-bar assertions land with the seam they test:**
    - E6: the no-stubs test starts with no coming-soon marker.
    - E7: an unlit memory element is invisible, the intro shows only while no level is solved, and the placeholder
      test lands.
    - Moon B: the imagery-entry test lands.
    - Back cover: no world page has `sceneKey: null`, no off-roster `level.<world>.*` key exists, the cover is not
      tappable, and it points at nothing unbuilt.
    - The placeholder and imagery tests are pytest and run at every exit.
11. **`qa-report`** runs at every milestone (ticket 007 picks them) and always at the back cover, which is the finish
    bar. It carries the owner play-through and prints the `placeholder: true` list. Its SKILL.md is updated:
    - E1: vitest, the suite and M2 routing;
    - E7: the placeholder print;
    - back cover: the finish-bar checklist (`road-to-v1/MAP.md:15-37`) and a whole-corpus `docs/sources.md` status
      sweep, because the router only sees diffs.

| Phase                                | Gates beyond the router over the phase diff, the M1 dev walk and (from E1) the suite                |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| E0                                   | router widened to `data/reference/`; `validate-levels.py` + pytest after the prune                   |
| M2 offload                           | preflight READY; vitest on M2 by hostname; pin-list + guard tests                                    |
| E1                                   | ticket-004 gaps on both machines; suite lands; `qa-report` gains the suite                           |
| E2, E3                               | `perf-report` + owner headed play on M1; E2 proves the lazy Three.js chunk and WebP under preview    |
| E4                                   | `perf-report` (`stars.json` enters the bundle)                                                        |
| E5 or Mars A                         | `perf-report` (first `orbital-positions.json` reader)                                                |
| E6                                   | `perf-report` + owner headed play (Saturn texture); no-stubs test starts                             |
| E7                                   | companion assertions; placeholder test; `qa-report` placeholder print                                |
| grid + ribbon                        | 360×640 no-scroll + text-floor test                                                                  |
| Moon A, Jupiter B1, Saturn A         | `perf-report` + owner headed play on M1                                                              |
| Moon B                               | imagery-entry test                                                                                   |
| every other phase                    | the router, the walk and the suite only                                                              |
| each milestone (ticket 007)          | `qa-report`, the owner's play (M2 allowed)                                                           |
| back cover                           | back-cover assertions; `qa-report` with the finish-bar checklist and the sources sweep               |

Handed on:

- **Ticket 007**: every milestone it picks carries a `qa-report` run and the owner's play-through. The back cover is
  always one.
- **Ticket 008** folds in:
  - the M2 offload phase between E0 and E1 (amends ticket 001), with its pin list, strip/add list, guard, owner
    checklist and CLAUDE.md section;
  - the router's `data/reference/` widening in E0;
  - the start SHA in every phase plan;
  - the E1 suite and the ticket-004 gap checks on both machines;
  - the perf rule and its applied list, including which of E5 and Mars A first reads `orbital-positions.json`;
  - the finish-bar assertions by phase, and the `qa-report` SKILL.md updates by phase.
