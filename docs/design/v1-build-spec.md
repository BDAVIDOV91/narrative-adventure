# The v1 build spec — in what order v1 is built

This is the ordered build spec that the [v1-build map](../wayfinder/v1-build/MAP.md) found its way to. It assembles
tickets 001–008 of that map (`T001`…`T008` = `docs/wayfinder/v1-build/tickets/NNN-*.md`) into one phase list. **What**
v1 contains is [`v1-spec.md`](v1-spec.md); this file says **in what order** it is built and what each phase must pass.
Where tickets conflict, the later one wins, and this file applies that already. A ticket holds the reasoning. This file
holds the answer. If they ever disagree, the ticket is the authority and this file has a bug.

**How to use it.** Start at E0. One phase per plan-mode session, plus two `challenger`s on the plan (CLAUDE.md "Review
gates"). Phases are strictly serial: a phase enters only on the exit before it (T003 d3). A phase plan that still
overruns one session splits further in its own plan; the Moon's eclipse beat is cut first (v1-spec §2). Bugs found on
the way follow rule 5, never a ticket. Do not re-derive anything here in a build session.

**Names.** Phases keep the names the tickets gave them. The offload phase is always written **M2 offload**, never bare
"M2", which is also a Moon marker. "M1" is this machine, the rule-9 target; "the M2" is the remote machine.

## 1. The phase list

| #   | Phase            | Milestone (merge to `main`)                  | Beyond the standard exit (§2)                                                 |
| --- | ---------------- | -------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | E0 Prune         | —                                            | router widened; `validate-levels.py` + pytest after the prune                 |
| 2   | M2 offload       | —                                            | preflight READY; vitest on the M2 by hostname; pin + guard tests              |
| 3   | E1 Overlay       | —                                            | ticket-004 gaps on both machines; the suite lands                             |
| 4   | E2 Renderer      | —                                            | `perf-report` + owner headed play on M1; lazy chunk under preview             |
| 5   | E3 rotate-match  | —                                            | `perf-report` + owner headed play on M1                                       |
| 6   | E4 parallax+dots | **1** — Earth is completable                 | `perf-report` (`stars.json`)                                                  |
| 7   | E5 trajectory    | —                                            | `perf-report` (`orbital-positions.json`)                                      |
| 8   | E6 telescope     | —                                            | `perf-report` + owner headed play on M1; no-stubs test                        |
| 9   | E7 Earth wrap    | **2** — Earth is playable                    | companion assertions; placeholder test                                        |
| 10  | Shell            | —                                            | re-runs E7's "Earth playable"                                                 |
| 11  | Grid + ribbon    | —                                            | 360×640 no-scroll + text-floor test; the storybook font                       |
| 12  | Moon A           | —                                            | `perf-report` + owner headed play on M1                                       |
| 13  | Moon B           | **3** — the Moon is playable (+ shell, grid) | imagery-entry test                                                            |
| 14  | Mars A           | —                                            | —                                                                             |
| 15  | Mars B           | **4** — Mars is playable                     | —                                                                             |
| 16  | Jupiter A        | —                                            | —                                                                             |
| 17  | Jupiter B1       | —                                            | `perf-report` + owner headed play on M1                                       |
| 18  | Jupiter B2       | **5** — Jupiter is playable                  | —                                                                             |
| 19  | Saturn A         | —                                            | `perf-report` + owner headed play on M1                                       |
| 20  | Saturn B         | **6** — Saturn is playable                   | —                                                                             |
| 21  | Back cover       | **7** — v1 reaches the finish bar            | back-cover assertions; finish-bar checklist; sources sweep; release re-checks |

## 2. The phase procedure (every phase)

**Entry.**

- The previous phase's exit passed. After a milestone, its `qa-report` passed and the milestone PR is open (§3).
- The plan records its **start SHA** (`git rev-parse HEAD`) at entry (T006 d1).
- The plan hands the owner the photo checklist for the **next** phase that needs photos: image, source URL,
  licence/credit line, drop path `assets/images/nasa/raw/` (T005 d5). Only a phase's exit waits on its files.

**Standard exit.** Every phase, E0 included (T001 d7, T006):

1. `npm run validate`, `npm test`, `venv/bin/python -m pytest` and `validate-levels.py` green.
2. A reduced path for every animation the phase adds; what "reduced" means is stated in the plan and approved by the
   owner (T001 d6).
3. **The router over the phase diff**: `PRECOMMIT_STAGED="$(git diff --name-only <start>..HEAD)"` fed through the
   pre-commit router with a `git commit` stdin. Deletions count. Every report it routes is clean (T006 d1).
4. **Claude's dev walk**: the Playwright MCP against `npm run dev` on M1, after `free -h` (T006 d7). It is functional
   only; it satisfies rule 5's "played via `npm run dev`".
5. **From E1, the suite** on the M2 against `npm run build` + `vite preview`, one worker, headless shell. The exit
   records the bundle chunk sizes from the suite's build (T006 d5, d8). If the M2 is down, a plain `claude` session runs
   the suite on M1 behind the MemAvailable guard, `workers: 1`, headless shell, dev server stopped, and the exit report
   says so. Work never waits for the M2 (T006 d6) — for suite runs at exits only. The M2 offload exit and E1 entry need the M2
   online; they have no fallback. Baselines belong to whichever machine runs the suite.
6. Every pytest guard landed so far runs: the placeholder test from E7, the imagery-entry test from Moon B (T006 d10).
7. **README** is updated if the phase added or changed a command or setup step (T007 d6).
8. The phase's own gates from §1 and its block in §4.

**Perf rule** (T006 d8). `perf-report` is an exit gate wherever a new renderer, a runtime texture or a
`data/generated/` file first enters the bundle, whatever the paths. Where §1 says "owner headed play on M1", the owner
plays `npm run dev` headed on M1 after `free -h`. A better GPU hides what this gate exists to catch, so it is never the
M2.

## 3. Milestones (T007)

A milestone is a phase exit that merges `development` into `main`. On top of §2:

1. README.md is updated **before** `qa-report` runs.
2. `qa-report` runs with the owner's play-through. The play may run on the M2 when the owner is home, but the frame-rate
   item is always played on M1, after `free -h` (T007 d7).
3. From merge 2, `qa-report` prints the `placeholder: true` list (T005 d8).
4. **A failed `qa-report` blocks the next phase's entry.** Fixes land RED/GREEN on `development`, and `qa-report`
   re-runs. A README-affecting fix re-checks README first.
5. **Stuck finding:** still failing after the third fix → the owner via `AskUserQuestion`
   (`.claude/rules/development-practices.md`). Only the owner may waive it; the waiver is written into the phase exit
   report and the PR body.
6. **Merge window:** after a pass, no commit lands on `development` until the owner has pushed it and opened the PR. The
   PR head is the approved SHA. The merge itself may come later.
7. **The PR:** `development` → `main`, "Create a merge commit", never squash or rebase. Conventional title, e.g.
   `chore(release): Earth is completable (E4)`. No git tags; the merge subject is the marker. After each merge `main` is
   one merge commit ahead of `development`, which is expected.
8. The owner opens and merges every PR and does every push (rule 7).

| Merge | Phase exit | PR title (example)                          | Extra                                                                                         |
| ----- | ---------- | ------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1     | E4         | `chore(release): Earth is completable (E4)` | no placeholder print yet; the font check (E4 block); (M2 catch-up gate dissolved, T006 am. 2) |
| 2     | E7         | `chore(release): Earth is playable (E7)`    | placeholder print from here on                                                                |
| 3     | Moon B     | `chore(release): the Moon is playable`      | also carries the shell and grid + ribbon                                                      |
| 4     | Mars B     | `chore(release): Mars is playable`          | —                                                                                             |
| 5     | Jupiter B2 | `chore(release): Jupiter is playable`       | —                                                                                             |
| 6     | Saturn B   | `chore(release): Saturn is playable`        | —                                                                                             |
| 7     | Back cover | `chore(release): v1 reaches the finish bar` | finish-bar checklist, sources sweep, release re-checks                                        |

## 4. The phases

**Exit words** (T001 d7, T003 d4):

- **Completable** — the level's threshold met in a real play-through, and the next page unlocks through E4's
  level-complete hook.
- **Playable** — every beat solved in play; nudges, hint steps and `remembers` cards shown; album elements lit; the
  memory glows once; the completion line, where the level has one; progress survives a reload; reduced motion honoured.
  For Earth also: no `ui.puzzle.coming-soon` left, and the `remembers` swap is proven by the fixture-pair test, not in
  play, since Earth has no real pair (T002 d9).

### E0 Prune

- **Scope:** the full v1-spec §6 prune list: both deleted types' enum entries and schema branches, seven → five in the
  enum description; delete `src/puzzles/zoom-split-star/`, `earth-gravity-drop` and its label; delete
  `fact.gravity-drop`, `.apollo`, `.bodies`, `fact.mizar-alcor.1-4`; fix `tests/test_validate_levels.py` and the
  `game-state.test.ts` fixture; the star-catalogue rationale (the file does not grow); `sources.md` RETIRED rows and
  re-keys; "seven" → "five" across CLAUDE.md, README, `docs/design/*`, `challenger.md` and the checker memory; correct
  `puzzle-types.md`'s Moon `gravity-drop`. 10 → 9 markers (T001).
- `surface-gravity.json` is re-documented, not trimmed: its `_readme` says it backs Jupiter's completion line and the
  Moon's hammer-and-feather line; test :91's name and docstring re-scoped; all four rows, `dropComparison` and every
  guard stay (T005 d2).
- The router gains `^data/reference/` → `astronomy-report`, with a RED/GREEN case in
  `.claude/hooks/test-precommit-checks-reminder.sh`, before any reference-row edit (T006 d2).
- The checker's memory gains T005's settled-sources and folk-figures lines (T008).
- **Exit:** standard; `validate-levels.py` and pytest after the prune. The router run over this diff counts deletions.

### M2 offload

- **Depends on:** E0. **Blocks E1 entry** (T006 d3).
- **Owner hands at entry:** Tailscale and the ssh alias, Mutagen, the M2 bootstrap (sudo on the M2).
- **Scope:** port `pdf_data_extractor_v2/ops/remote-shell/` as a deny-list wrapper: every Bash command runs on the M2
  except the pins.
  - Pins, each with a RED case in `test-pin-list.sh`: `git`; `free` and `/proc/meminfo`; `npm run dev`; the hook tests;
    the wayfinder viewer. Drop pdfx's `playwright` pin and flip its test case.
  - `test-pin-list.sh` joins husky's `^ops/` branch.
  - Strip: yarn, `nc-*`, the Supabase and `.env` checks, the gcloud, prisma and knavision pins.
  - Add: `uv venv`, `playwright install --only-shell`, de440s on the M2 (one-time download at setup).
  - The **MemAvailable guard** is new code with a sibling `test-*.sh`; it guards every heavy or 3D run on M1.
  - A CLAUDE.md section records the routing and why it fits the `Bash(ssh:*)` deny rule. Never a direct `ssh`.
  - Husky still runs vitest and pytest on M1 at commit, because `git` is pinned.
- **Exit:** `preflight.sh` READY, and a vitest run proven on the M2 by the wrapper's hostname check. README updated.
- **Amended 2026-10-01 (T006 amendment):** with the M2 offline, the phase builds its M1 side and exits
  M1-complete. The two M2 items move to the **M2 catch-up** gate before merge 1, and E1 enters without the M2.
- **Amended 2026-10-07 (T006 Amendment 2):** the M2 is online. The phase exits on the original items above; the
  catch-up gate is dissolved. Amendment 1's rules return only if the M2 goes offline again.

### E1 Overlay

- **Entry:** close ticket 004's gaps: peak RSS measured on **both** machines, the MCP browser-cache overlap, Playwright
  telemetry (T006 d4). Amended 2026-10-01: the M2 half is measured at the M2 catch-up gate, and the suite runs on M1 behind
  the guard until then. Amended 2026-10-07 (T006 Amendment 2): the M2 is online, so both halves are measured at E1
  entry as originally specified. E1 entry also sets the mem-guard floor from the measured **M1** peak RSS (owner,
  2026-10-01).
- **Scope:** 09-09 task #3: the puzzle overlay, the companion box (`content/bg/companion.json` plus its `content.ts`
  import), the progress write, the book-zoom call site; one shared reduced-motion helper; reduced paths for the zoom and
  the overlay. Closes latent bugs 4 and 5 (T001).
- **The suite lands:** a pinned `@playwright/test` (ADR 0004, reason inline), three tests: zero-network (any request
  outside the preview origin fails), reload persistence, a preview smoke (any failed request or 4xx inside the origin
  fails). `security-audit`, `privacy-guard` and `perf-report` fire through the router on `package.json`.
- `qa-report` SKILL.md gains vitest, the suite and the M2 routing (T006 d11).
- **Exit:** standard, the suite's first run included. README updated.

### E2 Renderer

- **Entry:** the owner's checklist for the NASA Earth texture (stays at entry, T005 d5).
- **Scope:** 09-09 #4, the `planet-render` widening and the disposal proof; #5, the Earth texture through
  `process-textures.py`. Defines the `sources.md` **imagery-entry format**: one stable id per committed file (T005 d7).
  Closes latent bugs 7 and 8. `planet-render` is not widened again after this (T002 d4).
- **Exit:** standard; `perf-report` + owner headed play on M1; the lazy Three.js chunk and the WebP URL proven under
  preview.

### E3 rotate-match

- **Scope:** the engine plus the sundial, day-night, seasons-tilt and moon-phase renderers, each played before the next;
  #8, the pedagogy pass over the 12 pre-existing fact strings. The renderer leaves room for J7's second body (T002).
- **Exit:** standard; "3 required beats playable" (a phase label, not a merge); `perf-report` + owner headed play on M1.

### E4 parallax + dots — milestone 1

- **Scope:** `earth-day-length` (`parallax-compare`), `earth-big-dipper` (`connect-the-dots`), #25 (constellation
  visibility by latitude). Seams (T002):
  - `dataRef` gains the `reference/…` root prefix; `earth-day-length` gains its `dataRef`; the validator change, the
    first runtime resolver and a RED/GREEN test ship together (d3);
  - the level-complete hook: sets `completed` at threshold, unlocks the next page (d7);
  - the `unlocks` reachability pin, trivial on Earth's chain (d2);
  - the variant config shapes for E4–E6's engines: arrays plus `minItems: 1`, per-element fields only for Earth's use,
    no code or tests for length > 1 (d5).
- The Moon blurb rewritten and claim-checked (T003 d6): the lit part changes, the face stays.
- `qa-report` SKILL.md gains a README check and "frame rate on M1" (T007 d6–7).
- **Owner hands before merge 1:** GitHub Settings → General → Pull Requests → merge-commit default message "Pull request
  title" (T007 d5).
- **Exit:** standard; "Earth completable" (the Moon page unlocks); `perf-report` (`stars.json`); milestone 1 (§3).

### E5 trajectory-match

- **Scope:** `earth-orbit-year` and `earth-twilight-zornitsa`; #7, the `dataRef` to `seasons`. Reuses E4's resolver.
  The plan states `earth-twilight-zornitsa`'s body count (T002). The config is a `bodies` array from day one, within
  T002 d5's limits. If the body count is above 1, multi-body `trajectory-match` lands here and Mars A reuses it (T003).
  Closes latent bug 10.
- **Exit:** standard; `perf-report`, as the first runtime reader of `orbital-positions.json`
  (`src/scenes/earth/earth-data.json:97,130`; T008). If the plan finds the engines do not read the `dataRef` at
  runtime, the gate moves to Mars A in that plan.

### E6 telescope-focus

- **Scope:** `earth-telescope-focus`; remove `ui.puzzle.coming-soon`. Telescope-Saturn is **drawn in code** (T005 d9):
  a 2D ball and ring ellipse, south face; its angle is a `data/reference/` row (the cited window,
  `docs/sources.md:1725`, and the angle drawn) with a pytest that it is negative and inside the window; the plan states
  the orientation convention and which ring arc crosses the globe, checked against a cited reference image; rendered to
  a runtime texture, so the engine takes a texture key per rung. The config is a `rungs` array from day one, within
  T002 d5's limits.
- The **no-stubs test** starts: no coming-soon marker (T006 d10).
- **Exit:** standard; `perf-report` + owner headed play on M1 (the Saturn texture).

### E7 Earth wrap — milestone 2

- **Scope:** the hint-step and album seams, built once; Earth's hint step and page element per marker; the
  `fact.day-night` repeat resolved; the Earth memory; the storybook intro; the Earth side of the J1 card (T001). Seams
  (T002): the hint-step enum and `remembers` pins (d2); the `remembers` card swap, tested with a fixture pair (d9); the
  pointing nudge (d10). The `solvedCount` doc comment reworded (v1-spec §3, T008).
- Page art and the Сияна vignette map to images through data with `placeholder: true`; the **placeholder test** lands:
  nothing under `assets/images/nasa/` is a placeholder, every flagged entry is on `qa-report`'s printed list, no
  flagged entry has an imagery entry (T005 d4, d8).
- **Companion assertions** (T006 d10): an unlit memory element is invisible; the intro shows only while no level is
  solved. Story lines go under "Story lines" in `docs/sources.md`.
- `qa-report` SKILL.md gains the placeholder print (T006 d11).
- **Exit:** standard; "Earth playable"; milestone 2.

### Shell

- **Scope:** the data-driven level-scene shell extracted from `earth-scene.ts`; Earth moves onto it in the same change
  (T002 d1).
- **Exit:** standard, re-running E7's "Earth playable".

### Grid + ribbon

- **Scope:** the storybook grid (columns from width and height, header included; to 360px portrait; text floor; drops a
  blurb that cannot fit; re-layout on `resize`); the bookmark ribbon (its art here, T005 d3); all six tiles, Jupiter
  and Saturn closed with their name keys, plus a plain, dim, closed back-cover tile; closed pages show the name only,
  so `ui.book.locked` is deleted (T002 d6, T003).
- **The storybook font** (T008): one self-hosted font in `assets/fonts/` whose default glyphs (not `locl`) are Bulgarian
  forms, verified per rule 3 and licence-checked. RED/GREEN test: `FONT_STACK` in `src/shared/fonts.ts` leads with the
  self-hosted family, and its woff2 exists under `assets/fonts/`. `privacy-guard` and `perf-report` run through the
  router. E0–E7 ship on the system stack until then; nothing reaches a child before v1.
- The **360×640 no-scroll and text-floor test** lands and re-runs at every exit after (T006 d9).
- **Exit:** standard; Earth's album, memory and intro re-played and tested to survive a `resize`.

### Moon A

- **Scope:** the Moon scene, data and real `sceneKey`; the Moon-view renderer(s) and the `orbitAngle` pin; the spine
  M1 → M3 → M2; the per-round eclipse flag and its test, with M3; the completion-line display and the Moon's line; the
  Mars blurb (T003). The suite's smoke opens the Moon scene (T006 d5). `remembers` pairs beyond J1 and S4 are chosen in
  each level's A plan and reviewed by `puzzle-pedagogy-reviewer`.
- **Owner hands:** this plan hands over Moon B's M9 photo checklist.
- **Exit:** standard; "Moon completable" (the Mars page unlocks); `perf-report` + owner headed play on M1.

### Moon B — milestone 3

- **Scope:** M5, M9; the Moon's nudges, hint steps, album ideas and memory; the eclipse beat **last**, with its view and
  safety key (T003). Reference rows: Sun radius and Moon radius, discs sized from radius over the ephemeris
  `distanceAu` (T005 d1). M5 draws its discs from data; a face texture only if M5's plan asks, then a real photo. M9
  frames. Page art and vignette may be placeholders.
- `process-textures.py` gains the **degrade mode**: a committed per-image recipe; a raw file with a recipe row is
  processed only by it. If M9 needs no degrade, the mode moves to Mars B (T005 d7).
- The **imagery-entry test** lands: every committed WebP under `assets/images/` has an imagery entry (T006 d10).
- **Exit:** standard; "Moon playable"; milestone 3, which also carries the shell and grid + ribbon.

### Mars A

- **Scope:** the Mars scene, data and real `sceneKey`; R1a `connect-the-dots` on committed Mars RA/Dec against
  `stars.json`; R1b sight-line `trajectory-match`, the first multi-body case (unless E5 already built it); the first non-trivial `unlocks`
  reachability test and data statement (T003). Smoke opens Mars.
- **Owner hands:** this plan hands over Mars B's R3 and PIA19400 checklist.
- **Exit:** standard; R1a and R1b played. No ephemeris perf gate (E5 took it).

### Mars B — milestone 4

- **Scope:** R3, R2, R6; the Mars nudges, hint steps, four album ideas and memory; the Jupiter blurb (T003). The Mars
  radius row, reusing the Moon radius (T005 d1). The R3 disc (a degrade recipe row) and PIA19400.
- **Owner hands:** this plan hands over Jupiter A's J1 rung-3 checklist.
- **Exit:** standard; "Mars completable and playable" (the Jupiter page unlocks); milestone 4.

### Jupiter A

- **Scope:** real `sceneKey`; J1 three-rung `telescope-focus` (the E6 array shape) and its `remembers` data; J2,
  extending the multi-body `trajectory-match` with four moons and the edge-on strip; the reachability statement (T003).
  Rows: Galilean periods and orbit radii (NSSDC), Jupiter radius (T005 d1). J1 rung-3 frames (recipe rows). The
  checker's memory gains T006's Galilean, NSSDC, J2000 and JPL-column notes (T008). Smoke opens Jupiter.
- **Owner hands:** this plan hands over Jupiter B1's J7 close-up checklist.
- **Exit:** standard; J1 and J2 played; the J1 `remembers` card shows.

### Jupiter B1

- **Scope:** J7: the spin renderer and the `spin` pin (T003 d7). Rows: Jupiter and Earth rotation periods. The J7
  close-up.
- **Owner hands:** this plan hands over Jupiter B2's Ganymede, Mercury and J4 checklist.
- **Exit:** standard; J7 played; `perf-report` + owner headed play on M1.

### Jupiter B2 — milestone 5

- **Scope:** J3, J4; the Ganymede and Mercury names; the J4 key trimmed from `fact.brightest-is-a-planet`; the
  completion line; nudges, hint steps, five album ideas, memory; the Saturn blurb (T003). Rows: Ganymede and Mercury
  radii. Ganymede and Mercury discs, the J4 frame. Any `surface-gravity.json` row deletion is decided here (T005 d2).
- **Exit:** standard; "Jupiter completable and playable" (the Saturn page unlocks); milestone 5.

### Saturn A

- **Scope:** real `sceneKey`; S1 `ring-view`, its `orbitAngle` pin and the schema's moon-phase description update; S4
  after S1, and its `remembers` data; the reachability statement (T003). Rows: C, B, A ring radii and
  `saturn-ring-geometry.json` with its narrow-south-face render test, plus a test that it agrees with E6's ring-angle
  row (T005 d9). The checker's memory gains T011's PIA03156, ring-speed and Wayback notes (T008). Smoke opens Saturn.
- **Owner hands:** this plan hands over Saturn B's PIA06230 and PIA20016 checklist.
- **Exit:** standard; S1 and S4 played; the S4 `remembers` card shows; `perf-report` + owner headed play on M1.

### Saturn B — milestone 6

- **Scope:** S2 two-panel `connect-the-dots` (R1a's data drawn faint); S3 with PIA06230 and PIA20016, their on-screen
  credit lines and the infrared label; the Titan name and radius row; the completion line; nudges, hint steps, four
  album ideas, memory (T003, T005). Images before this phase are public-domain NASA/JPL with the credit in `sources.md`
  only; a frame whose licence needs visible attribution pulls the credit display forward to its phase (T005 d6).
- **Exit:** standard; "Saturn completable and playable": `completed` survives a reload and the cover tile stays closed;
  milestone 6.

### Back cover — milestone 7

- **Scope:** the cover opens on Saturn's `completed`, with no new storage field; the ribbon moves to it; vignettes of
  completed worlds only (placeholders allowed, T005 d4); the Сияна line, then T009's lines (T003).
- **Back-cover assertions** (T006 d10): no world page has `sceneKey: null`; no off-roster `level.<world>.*` key; the
  cover is not tappable; it points at nothing unbuilt.
- `qa-report` SKILL.md gains the finish-bar checklist (`road-to-v1/MAP.md:15-37`), a whole-corpus `docs/sources.md`
  status sweep, and the release re-checks: re-run the monthly Saturn ring-opening table behind "Through a small
  telescope", and re-read every VERIFIED claim whose source page may have moved (T006 d11, T007 d8).
- **Exit:** standard; the cover opens after a real Saturn completion and survives reload; milestone 7.

## 5. The finish bar, line by line

Each line of road-to-v1's finish bar (`docs/wayfinder/road-to-v1/MAP.md:15-37`), with the phase that first meets it
and where it is re-checked.

| Finish-bar line                                               | First met                                      | Re-checked                                                            |
| ------------------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------- |
| Every roster level playable in `npm run dev`                  | E7, Moon B, Mars B, Jupiter B2, Saturn B       | every exit's dev walk; `qa-report` at each milestone                  |
| … and in `npm run build` + `vite preview`                     | E1 (suite), per level's smoke                  | every exit's suite; a full preview play in the back-cover `qa-report` |
| Progress persists across a reload                             | E1 (suite test)                                | every exit's suite; every "playable" exit                             |
| Every shipped claim is VERIFIED                               | each phase's `astronomy-report` via the router | back-cover whole-corpus sweep                                         |
| Pedagogy, perf and privacy gates pass                         | each phase's router run; §1 perf gates         | back-cover `qa-report`                                                |
| A Playwright QA pass has run                                  | E1                                             | every exit; back-cover `qa-report`                                    |
| Back cover unlocks when the last world is completed           | Back cover                                     | back-cover `qa-report`                                                |
| Back cover is not tappable; points at nothing unbuilt         | Back cover (assertions)                        | back-cover `qa-report`                                                |
| Fits without scrolling to 360px portrait; text floor          | Grid + ribbon (test)                           | every exit after                                                      |
| No world page with `sceneKey: null`                           | Saturn A (last real `sceneKey`)                | back-cover assertion                                                  |
| No coming-soon marker                                         | E6 (no-stubs test)                             | every exit after                                                      |
| No off-roster `level.<world>.*` key or page                   | Grid + ribbon (six tiles)                      | back-cover assertion                                                  |
| Each completed page shows its memory element, opens its card  | E7 (Earth), each level's B                     | each "playable" exit                                                  |
| An unlit memory element is invisible                          | E7 (assertion)                                 | every exit after                                                      |
| The intro shows only while no level has a solved marker       | E7 (assertion)                                 | every exit after                                                      |
| Memory astronomy VERIFIED; story lines listed in `sources.md` | E7, each level's B, back cover                 | back-cover sweep                                                      |
| A rewarded fact may mention any solar-system body             | no build work: it relaxes a rule               | `astronomy-report` on each content batch                              |
| Placeholder art is allowed                                    | E7 (placeholder test and print)                | every milestone's printed list                                        |

The parent lines ("The book ends on a back cover", "No stubs", "The companion's story") are met by their sub-lines above.

## 6. v1-spec §6, item by item

| §6 group     | Item                                                                        | Phase                                                            |
| ------------ | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Prune        | every prune bullet                                                          | E0                                                               |
| Earth        | overlay, companion box, progress write; reduced motion; bugs 4, 5           | E1                                                               |
| Earth        | `planet-render` widening + disposal proof; Earth texture; bugs 7, 8         | E2                                                               |
| Earth        | three `rotate-match` renderers + `moon-phase`; pedagogy pass                | E3                                                               |
| Earth        | `parallax-compare`, `connect-the-dots`, #25                                 | E4                                                               |
| Earth        | two `trajectory-match` beats; beat 4's `dataRef` to `seasons`; bug 10       | E5                                                               |
| Earth        | `telescope-focus`; remove `ui.puzzle.coming-soon`                           | E6                                                               |
| Earth        | `fact.day-night` repeat                                                     | E7                                                               |
| Schema       | `drives` has no `rotation`                                                  | already pinned (`schemas/level-data.schema.json:71-73`)          |
| Schema       | hint-step enum; `remembers`                                                 | E7                                                               |
| Schema       | reachability                                                                | E4 (trivial), Mars A (first real)                                |
| Schema       | Moon renderers + `orbitAngle` pin; eclipse flag                             | Moon A                                                           |
| Schema       | multi-body `trajectory-match`                                               | Mars A (R1b), or E5 if its body count > 1; extended in Jupiter A |
| Schema       | three-rung `telescope-focus`                                                | Jupiter A (shape from E6)                                        |
| Schema       | J7 spin renderer + `spin` pin                                               | Jupiter B1                                                       |
| Schema       | `ring-view` + pin; moon-phase description update                            | Saturn A                                                         |
| Schema       | two-panel `connect-the-dots`                                                | Saturn B                                                         |
| Data         | `dataRef` to `data/reference/`                                              | E4                                                               |
| Data         | Sun and Moon radii                                                          | Moon B                                                           |
| Data         | Mars radius                                                                 | Mars B                                                           |
| Data         | Galilean periods and orbit radii; Jupiter radius                            | Jupiter A                                                        |
| Data         | Jupiter and Earth rotation periods                                          | Jupiter B1                                                       |
| Data         | Ganymede and Mercury radii                                                  | Jupiter B2                                                       |
| Data         | C, B, A ring radii; `saturn-ring-geometry.json` + render test               | Saturn A                                                         |
| Data         | Titan radius                                                                | Saturn B                                                         |
| Data         | `surface-gravity.json` re-document (row deletions: Jupiter B2's plan)       | E0                                                               |
| Data         | `test_reference_data.py` for each row                                       | with its row                                                     |
| Content      | facts, nudges, album keys, labels, completion lines per level               | each level's A and B                                             |
| Content      | eclipse safety key                                                          | Moon B                                                           |
| Content      | Ganymede, Mercury; Titan                                                    | Jupiter B2; Saturn B                                             |
| Content      | blurbs: Moon; Mars; Jupiter; Saturn                                         | E4; Moon A; Mars B; Jupiter B2                                   |
| Content      | intro and Earth memory; the other four memories; back-cover lines           | E7; each B; Back cover                                           |
| Content      | drop `ui.book.locked`                                                       | Grid + ribbon                                                    |
| Content      | `pedagogy-report` and `astronomy-report` on every batch                     | every exit (router)                                              |
| Storybook    | Jupiter's and Saturn's real `sceneKey`s                                     | Jupiter A; Saturn A                                              |
| Storybook    | grid; ribbon                                                                | Grid + ribbon                                                    |
| Storybook    | memory elements; intro                                                      | E7, each B                                                       |
| Storybook    | back cover                                                                  | Grid + ribbon (closed tile); Back cover                          |
| Imagery      | Earth texture                                                               | E2                                                               |
| Imagery      | Earth's telescope-Saturn art                                                | E6 (drawn in code)                                               |
| Imagery      | per-marker page art; Сияна vignettes                                        | E7, then each B                                                  |
| Imagery      | M9 frames                                                                   | Moon B                                                           |
| Imagery      | R3 disc; PIA19400                                                           | Mars B                                                           |
| Imagery      | J1 rung-3 frames; J7 close-up; Ganymede, Mercury, J4                        | Jupiter A; B1; B2                                                |
| Imagery      | PIA06230, PIA20016                                                          | Saturn B                                                         |
| Imagery      | back-cover vignettes                                                        | Back cover                                                       |
| Imagery      | all through `process-textures.py`, ≤2048px WebP, each with an imagery entry | E2 (format), Moon B (test), then every image phase               |
| Agent memory | T005 settled-sources and folk-figures lines                                 | E0                                                               |
| Agent memory | T006 Galilean, NSSDC, J2000, JPL-column notes                               | Jupiter A                                                        |
| Agent memory | T011 PIA03156, ring-speed, Wayback notes                                    | Saturn A                                                         |

## 7. The owner's hands, by phase

| When                                           | What                                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------ |
| Every phase                                    | push `development` when ready (Claude never pushes)                      |
| M2 offload entry                               | the M2 online; Tailscale + ssh alias, Mutagen, M2 bootstrap (sudo)       |
| E1 entry                                       | the M2 online (RSS measured on both machines)                            |
| Grid + ribbon                                  | approve the chosen font (Bulgarian forms, licence)                       |
| E2 entry                                       | the NASA Earth texture into `assets/images/nasa/raw/`                    |
| E2, E3, E6, Moon A, Jupiter B1, Saturn A exits | headed `npm run dev` play on M1 after `free -h`                          |
| Before merge 1                                 | GitHub merge-commit default message → "Pull request title"               |
| Each milestone                                 | play inside `qa-report` (frame rate on M1); push; open and merge the PR  |
| Moon A → Saturn A plans                        | drop the next phase's photos (the checklist arrives one phase early)     |
| Any time                                       | replace a `placeholder: true` picture by editing data (not a phase exit) |
| A stuck finding                                | decide whether to waive it                                               |
