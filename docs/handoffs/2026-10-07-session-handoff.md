# Session handoff — 2026-10-07 (E1 Overlay)

## Where things stand

**E1 Overlay is done** (`v1-build-spec.md` §4). Start SHA `1eaa6c5`, end `HEAD` (12 commits, below). The plan of
record, with both challenger rounds and the rulings made during the build, is
[`2026-10-07-e1-overlay-plan.md`](2026-10-07-e1-overlay-plan.md). The earlier part of today, the M2 offload exit, is in
this file's git history (`1eaa6c5`).

| Commit    | What                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------ |
| `a10fc90` | the plan, both challengers folded; pre-install telemetry and cache checks                              |
| `0224e6e` | `@playwright/test` 1.63.0 + `playwright.config.ts` + zero-network (RED with a planted fetch, on Bobby) |
| `680ddfb` | E1 entry: ticket 004's gaps closed, RSS on both machines, the floor stays 1536                         |
| `275cace` | the preview smoke; the inline `data:` favicon (DOM-assertion RED, see below)                           |
| `4507d74` | `reduced-motion.ts`, the zoom's instant path, zoom-out recentres                                       |
| `f412af9` | **bug 5**: the book zooms into a page and back out (call-site tripwire RED/GREEN)                      |
| `a3f1f1e` | `companionTiers` in the schema and Earth; `companion.json` + its `content.ts` import; `isContentKey`   |
| `61dbcaa` | the arrival lines after `puzzle-pedagogy-reviewer`                                                     |
| `2a2aced` | **bug 4**: `progress-write.ts`, the shared overlay, the companion box, reload-persistence e2e          |
| `329f66c` | `qa-report` SKILL.md (T006 d11), README, CLAUDE.md                                                     |
| `73fc85b` | the overlay releases its resize listener on a mid-fade shutdown (perf-report finding)                  |
| (docs)    | this handoff; the `sources.md` note on arrival lines                                                   |

## Exit report (§2 + the E1 block)

1. **M1, through mem-guard:**
   - `npm run validate` rc 0;
   - vitest 50/50 after the last fix (48/48 at the M1 gate run);
   - pytest 92/92;
   - `validate-levels.py` OK.
2. **Reduced paths**, approved by the owner on 2026-10-07:
   - the zoom is an instant cut both ways;
   - the overlay appears and goes in one frame;
   - the companion box has no animation.
   - Covered by vitest (zoom), the smoke under `reducedMotion: 'reduce'`, and the dev walk.
3. **Router over `1eaa6c5..HEAD`** (42 files) routed five reports, all clean:
   - **privacy-guard:** CLEAN.
   - **security-audit:** CLEAN. `npm audit` shows the same 5 pre-existing high advisories, owner-deferred, none new.
   - **perf-report:** no regression. It found one latent leak, fixed in `73fc85b`.
   - **astronomy-report:** clean, with LOW notes. The table note is fixed; the MEDIUM item is under "Next" below.
   - **pedagogy-report:** the reviewer's fixes landed in `61dbcaa`. `src/puzzles/` is untouched.
4. **Dev walk:** Playwright MCP, system Chrome, `npm run dev` on M1 behind the guard after `free -h`.
   - The book → the zoom (caught mid-tween) → Earth.
   - A marker tapped 18 px off-centre (the 44 px target) → the overlay with the sundial arrival line.
   - Taps under the dim and the arrow keys were ignored. Close → the player walks.
   - Back → the book at zoom 1, centred.
   - Again under emulated reduced motion: instant everywhere, and the telescope marker shows no companion box.
   - Console: **no favicon 404**, no errors; only WebGL ReadPixels notes from the screenshots.
   - One limit: the 500 ms zoom-out cannot be caught mid-tween on M1, because screenshots take about 713 ms. Unit
     tests pin its calls, and the owner's E2 headed play will see it.
5. **The suite's first run was on the M2.** `bash-remote-shell.sh -c 'hostname; npm run test:e2e'` → **Bobby, 7/7**,
   re-run green after every later step.
   - **Chunk sizes** from the M2 build: `index.html` 1.04 kB (0.66 gzip), `index-*.js` 20.21 kB (7.55), `phaser-*.js`
     1,196.92 kB (318.73), no `three` chunk.
6. **Pytest guards:** none landed yet (E7, Moon B).
7. **README** updated (setup, checks, where the suite runs).
8. **E1 block:**
   - ticket 004's gaps recorded closed (ticket 004, "Gaps closed");
   - the floor decided;
   - `qa-report` updated;
   - the hook tests are green: 5 hook tests, pin-list 78, mem-guard 13, `test:ops` 10;
   - preflight READY, headless shell ok on the M2.

**Latent bugs:**

- **Bug 5: closed.** The call sites are wired and walked.
- **Bug 4: call site plus behavioural unit test landed.** `commitSolve` is tested against happy-dom `localStorage`, and
  `EarthScene`'s `onSolved` calls it. No engine reports a solve until E3, so the **first runtime solve is E3's**. E3
  extends `e2e/reload-persistence.spec.ts` to a played solve.

## The exact next step

**E2 Renderer** (`v1-build-spec.md` §4).

- Its entry hands the owner the **NASA Earth texture photo checklist**: image, source URL, licence/credit line, drop
  path `assets/images/nasa/raw/`. E1 deferred it here (CF A8).
- E2's exit includes `perf-report` and the owner's headed play on M1. That play is also where the zoom-out tween gets
  seen.

**E3 entry items carried from E1:**

- **The seasons beat (owner ruling):** `earth-data.json:67` still says `"drives": "tilt"`. Per `puzzle-types.md:43`,
  that means the child changes the tilt, which contradicts the owner's fixed-tilt ruling (astronomy-report MEDIUM).
  - E3 changes the seasons engine to drive orbit position or the Sun's direction, or redefines `tilt` in
    `puzzle-types.md`.
  - It pins the choice with a test, like `moon-phase` → `orbitAngle`.
  - It re-checks „Нагласи Земята" against what actually moves.
- **The first played solve** extends the reload test (above).

## Settled — do not re-ask

- Everything in the 2026-10-01 handoff's settled list, plus the M2 offload settlements (T006 Amendment 2, Q4, git
  commit guarded inside husky, the mutagen session, the npm audit deferral).
- **E1 rulings (owner, 2026-10-07):**
  - **Motion:**
    - reduced zoom is an instant cut, and the reduced overlay appears and goes in one frame;
    - non-reduced: zoom 700/500 ms, overlay fade 200 ms.
  - **Companion:**
    - `companionTiers` is a required schema field, 2 or 3, and Earth is 3;
    - arrival lines are **per marker**, `companion.<marker-id>.arrival`, shown when the overlay opens. E1 authors the 4
      required markers; the other 5 come with their engines.
  - **Progress:**
    - E1 proves the progress write by a pure module plus a seeded reload e2e. **No cheat or dev-only solve UI ships.**
    - The `completed` flip lives in `recordSolve` now (T002 d7's hook, early). E4 proves it in play.
  - **Playwright:**
    - `@playwright/test` is pinned at **1.63.0**, the same headless-shell revision (1243) as `@playwright/mcp@0.0.80`.
      Bump the two together (ADR 0004).
    - The favicon's regression test is a **DOM assertion**, because the headless shell never fetches favicons.
  - **The mem-guard floor stays 1536 MB.** The formula, M1 peak drop (828 MB) + 512, gives 1408. Re-check at E2's 3D.
  - **M2 runs from a plain session go through `bash-remote-shell.sh -c '<cmd>'`**, with `hostname` proof in the same
    command.
  - **The mutagen session was re-created** with the Playwright output dirs ignored.
  - **The seasons engine (E3):** a fixed tilt, and the child moves Earth along its orbit.

## Owner items

- Push `development` (`1eaa6c5..HEAD`).
- E2 entry: the NASA Earth texture (checklist at E2 entry).
- Before merge 1 (E4): the GitHub merge-commit default message "Pull request title".

## Left over

- **`npm audit`: 5 high advisories,** dev-only and deferred: braces → micromatch → lint-staged, and source-map-js.
- **The wrapper's reachability probe reads stdin.** This is inherited from pdfx; see the M2 offload handoff in git
  history. It does not affect sessions.
- **Pin side effects:** a command that merely names `free`, `/proc/meminfo`, `mem-guard` or `git` runs on M1. During
  E1 the RSS sampler lived in a synced repo path so it could run on the M2, and was then deleted.
- **context-mode is outdated** (v1.0.127, v1.0.169 available: `/ctx-upgrade`). Its hook blocks commands that contain
  `curl` or `fetch(` text; use the Edit tool for such code and `ctx_execute` for network checks.
- **Latent bugs:** 7 and 8 are scheduled for E2, and 10 for E5.

## E2 entry: the NASA Earth texture (pulled 2026-10-07, not yet processed)

The source file is already in the drop path. It is gitignored, so nothing has been committed or processed.

| Field      | Value                                                                                                                                  |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| File       | `assets/images/nasa/raw/earth-bmng-200407.jpg`, 5400×2700 (2:1 equirectangular), 1,617,810 bytes                                       |
| SHA-256    | `f55226d46d27e05511f2118dc6aa24f5dbf9b6b2cddc87cc6e0e7dd067c00b11`                                                                     |
| Image      | Blue Marble: Next Generation, **base map**, July 2004: a MODIS true-colour monthly composite, 500 m/px, no shaded relief or bathymetry |
| Source URL | https://assets.science.nasa.gov/content/dam/science/esd/eo/images/bmng/bmng-base/july/world.200407.3x5400x2700.jpg                     |
| Page       | https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-map/                                                 |
| Credit     | "Blue Marble: Next Generation was produced by Reto Stöckli, NASA Earth Observatory (NASA Goddard Space Flight Center)."                |
| Licence    | NASA imagery, public domain (T005 d6: the credit goes in `sources.md` only). The usage sentence was not fully confirmed this session.  |

Open for E2's plan: **which month.**

- July shows northern summer, with no Alpine snow.
- January is on the same URL pattern (`…/bmng-base/january/world.200401.3x5400x2700.jpg`).
- The old `eoimages.gsfc.nasa.gov` and `visibleearth.nasa.gov` links are dead. Everything moved to `science.nasa.gov`.

If the file must be re-fetched by hand:

1. Open the page above in a browser. No login is needed.
2. Pick the month, then the 5400×2700 JPEG.
3. Save it as `assets/images/nasa/raw/earth-bmng-2004MM.jpg`.

The other variants (base-topography, base-topography-bathymetry) add shaded relief. That is not plain photography, so avoid them.

## Trigger for the next session

```text
Start phase E2 Renderer (docs/design/v1-build-spec.md §4). Read
docs/handoffs/2026-10-07-session-handoff.md first; its "Settled" list is
not to be re-asked. Start SHA is <git rev-parse --short HEAD>.

Run ops/remote-shell/preflight.sh first; if it is not READY, ask me.
Create the native task list (TaskCreate) right after plan approval and
keep it updated.

E2 entry: the NASA Earth texture is already in assets/images/nasa/raw/
(earth-bmng-200407.jpg, details in the handoff). Confirm the month with
me, then run it through process-textures.py and define the sources.md
imagery-entry format (T005 d7). Latent bugs 7 and 8 close in this phase.
Carry the E3 entry items from the handoff, do not build them.

Plan mode first, with two challengers. Then implement in plan-approved
steps, RED/GREEN for each step, one commit per step, and do the full §2
exit, including perf-report and my headed play on M1 after free -h. The
suite runs on the M2 through bash-remote-shell.sh with hostname proof.
```
