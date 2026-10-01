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

**M2 offload** (§4), in plan mode with two `challenger`s. It blocks E1 entry. Its exit and E1's entry need the M2
online, and neither has a fallback.

## Settled — do not re-ask

- Everything in the 2026-09-27 handoff's settled list still holds.
- E0's reduced path: none (owner, 2026-10-01).
- **The favicon 404 is fixed in E1, as the preview smoke test's first RED** (owner, 2026-10-01). `/favicon.ico` has
  404'd since the scaffold: `index.html` has no icon link and there is no `public/`. E1's smoke test fails on any 4xx
  inside the origin, so it goes RED on this request. A self-hosted or inline `data:` icon turns it GREEN.
- The new Moon completion-line key is created in **Moon A** (spec :248-249), not E0. `sources.md` says "key assigned in
  Moon A" and invents no key name.
- `surface-gravity.json` keeps all four rows. Mars and Earth wait for Jupiter B2's plan.

## Owner items

- Push `development` (seven E0 commits on top of `69bf816`).
- Before the M2 offload exit: the M2 online, with Tailscale, the ssh alias, Mutagen and the bootstrap.
- Before merge 1 (E4): GitHub merge-commit default message "Pull request title".

## Left over

- Latent bugs 4, 5 (E1), 7, 8 (E2) and 10 (E5) are still open, as scheduled.
- Playwright MCP note for future walks: synthetic `PointerEvent`s through `browser_evaluate` do not reach Phaser's
  input. `page.mouse.click(x, y)` through `browser_run_code_unsafe` does. At 1700×1300 the whole 1600×1200 Earth map is
  on screen. The Earth card is at (626, 650).
