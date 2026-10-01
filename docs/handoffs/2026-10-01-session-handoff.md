# Session handoff — 2026-10-01

## Where things stand

**E0 Prune is done.** It is the first phase of [`v1-build-spec.md`](../design/v1-build-spec.md) §4. Start SHA
`69bf816`. The phase landed as seven commits on `development`, none pushed:

| Commit    | What                                                                                  |
| --------- | ------------------------------------------------------------------------------------- |
| `203bc75` | router routes `^data/reference/` → `astronomy-report` (RED/GREEN hook case, T006 d2)  |
| `34f7dd7` | schema drops `zoom-split-star` and `gravity-drop`; Earth ships 9 markers              |
| `851f2c0` | content drops `puzzle.earth.gravity-drop.label`, `fact.gravity-drop*`, `mizar-alcor`  |
| `e67a6b7` | `surface-gravity.json` re-documented, not trimmed (v1-build T005 d2)                  |
| `2ca88dc` | star-catalogue rationale: the Mizar check guards the Big Dipper; file stays 500 lines |
| `d0d64b2` | `sources.md`: Mizar/Alcor RETIRED; gravity claims re-keyed to the Moon/Jupiter lines  |
| `df88e9e` | five types across CLAUDE.md, README, design docs, `challenger.md`, checker memory     |

The plan was challenged twice. Both challengers returned revise, and the fixes were folded in.

## Exit report (§2)

1. `npm run validate`, `npm test` (21), pytest (88) and `validate-levels.py` are green.
2. Reduced path: none. E0 adds no animation; the owner approved this on 2026-10-01.
3. Router over `69bf816..HEAD`, deletions included: `astronomy-report`, `pedagogy-report` and `privacy-guard`, all
   clean.
   - `astronomy-report` found one LOW/PLAUSIBLE wording note. "The Big Dipper that `earth-big-dipper` draws" describes
     the beat's design, but the marker has no config yet. Nothing player-facing is affected.
4. Dev walk (Playwright MCP, `npm run dev`, M1, after `free -h`): the book opened; tapping the Earth card opened
   EarthScene, which shows **9 markers**; the old `earth-gravity-drop` spot is empty. The book→Earth zoom is not wired
   yet (E1).
5. The suite starts at E1, and no pytest guards have landed yet (E7, Moon B).
6. README: no command changed. `README.md:70` now says five types.
7. Photo checklist: none from E0. E2's stays at E2 entry (v1-build T005 d5).

## The exact next step

**M2 offload.** It was planned and challenged on 2026-10-01, then **paused by the owner before any code was written**.
The owner resumes it once they confirm the M2 is online.

- Start SHA: `c0db095`. No implementation commit exists yet.
- The plan and both challenger reports (A and B, both revise) are in
  [`2026-10-01-m2-offload-plan.md`](2026-10-01-m2-offload-plan.md). The plan was written for the M1 side. Its
  "Challenger Findings" section lists 18 accepted fixes not yet folded in, and one open owner question (Q4, compound
  pinned commands).
- **If the M2 is online at resume**, the amendment's deferral may no longer be needed. The phase can exit on the
  original items, `preflight.sh` READY and the hostname-proven vitest run, instead of M1-complete. Ask the owner which
  exit applies; do not assume.

## Pending owner question

- **Q4. Compound or over-matched pinned commands.** For example, `git add -A && npm test` would run vitest on M1. The
  recommendation is to auto-guard heavy pinned commands through mem-guard. The other options are refusing them, or
  accepting the pdfx behaviour. The detail is in the plan file.

## Settled — do not re-ask

- **The M2 is offline; ticket 006 decision 3 is amended** (owner, 2026-10-01; see the amendment at the end of ticket
  006). M2 offload builds its M1 side and exits M1-complete. E1 and later phases enter without the M2; the suite runs
  on M1 behind the MemAvailable guard. The deferred M2 items (preflight READY, the hostname-proven vitest run, M2 peak
  RSS, one M2 suite run) form an **M2 catch-up gate before merge 1** (E4). If the M2 is still offline at E4's exit,
  the owner decides whether to waive it or wait.
- Everything in the 2026-09-27 handoff's settled list still holds.
- **M2 offload design** (owner, 2026-10-01):
  - The mem-guard floor is a provisional 1536 MB MemAvailable, overridable with `MEM_GUARD_MIN_MB`, and re-tuned at E1
    entry from the measured peak RSS.
  - The wrapper's default mode is `remote` and fails closed. An unknown mode refuses. `local` and `probe` run only when
    exported explicitly.
  - The wrapper auto-guards the pinned `npm run dev`.
- E0's reduced path: none (owner, 2026-10-01).
- **The favicon 404 is fixed in E1, as the preview smoke test's first RED** (owner, 2026-10-01). `/favicon.ico` has
  404'd since the scaffold: `index.html` has no icon link and there is no `public/`. E1's smoke test fails on any 4xx
  inside the origin, so it goes RED on this request. A self-hosted or inline `data:` icon turns it GREEN.
- The new Moon completion-line key is created in **Moon A** (spec :248-249), not E0. `sources.md` says "key assigned in
  Moon A" and invents no key name.
- `surface-gravity.json` keeps all four rows. Mars and Earth wait for Jupiter B2's plan.

## Owner items

- Push `development` (E0's commits, the handoff and the T006 amendment, on top of `69bf816`).
- Before merge 1 (E4), at the M2 catch-up gate: the M2 online, with Tailscale, the ssh alias, Mutagen and the bootstrap.
- Before merge 1 (E4): GitHub merge-commit default message "Pull request title".

## Left over

- Latent bugs 4, 5 (E1), 7, 8 (E2) and 10 (E5) are still open, as scheduled.
- Playwright MCP note for future walks: synthetic `PointerEvent`s through `browser_evaluate` do not reach Phaser's
  input. `page.mouse.click(x, y)` through `browser_run_code_unsafe` does. At 1700×1300 the whole 1600×1200 Earth map is
  on screen. The Earth card is at (626, 650).
