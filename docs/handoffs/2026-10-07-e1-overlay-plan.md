# E1 Overlay — plan

**Start SHA `1eaa6c5`** (branch `development`, clean). Spec: `docs/design/v1-build-spec.md` §4 E1 (:152-166), §2.
Preflight at entry: `STATE=READY`, exit 0, 17 ok. This session is a plain `claude` on M1 (`TechnoJihad`).

## Context

E1 has two halves.

**Entry:**

- Close ticket 004's gaps (`docs/wayfinder/v1-build/tickets/004-playwright-qa.md:41-42`; T006 d4, Amendment 2):
  - peak RSS on both machines;
  - the MCP browser-cache overlap;
  - Playwright telemetry.
- Re-tune the provisional mem-guard floor (1536 MB, `ops/mem-guard/mem-guard.sh:29`) from the **M1** peak.

**Scope:**

- The 09-09 task #3:
  - the puzzle overlay;
  - the companion box (`companion.json` plus its `content.ts` import);
  - the progress write;
  - the book-zoom call site.
- One reduced-motion helper.
- Close latent bugs 4 and 5:
  - **Bug 4:** `saveProgress` (`src/shared/game-state.ts:67`) has no call site.
  - **Bug 5:** `zoomIntoPage`/`zoomOutToBook` (`src/shared/book-zoom-transition.ts`) have no call site.
- Land the Playwright suite: zero-network, reload persistence, preview smoke.
  - The favicon 404 is the smoke test's first RED: there is no `<link rel=icon>` and no `public/`.

## Owner decisions this session (settled, do not re-ask)

1. **Reduced zoom:** instant cut, with no pan or zoom and the scene switching at once.
2. **Reduced overlay:** the dim and the panel appear and disappear in one frame.
3. **Companion tier count:** a required top-level `companionTiers` field (2 or 3) in the level JSON and the schema. This is the same seam as `unlockThreshold`. Earth = 3.
4. **Floor formula:** floor = the M1 peak MemAvailable drop during the suite run + 512 MB, rounded up to 128 MB.
5. **Proving the progress write:**
   - A pure `recordSolve()` module, tested RED/GREEN.
   - The e2e reload test seeds `localStorage` through `page.evaluate`, then reloads.
   - E3 extends the test to a played solve.
   - No cheat or dev-only solve UI ships.
6. **`@playwright/test` pinned at `1.63.0`** (`/decide`):
   - 1.63.0 and the MCP's bundled `1.63.0-alpha-2026-08-31` both pin chromium-headless-shell revision **1243** (153.0.8010.12), per unpkg `browsers.json`.
   - `playwright`, `playwright-core` and `@playwright/test` 1.63.0 have no install scripts.
7. **M2 runs:** stay in this session and run each M2 command through `ops/remote-shell/bash-remote-shell.sh -c '<cmd>'`, with `hostname` echoed in the same command as proof. M1 heavy runs go through `ops/mem-guard/mem-guard.sh --` explicitly.
8. Non-reduced timings stay as now: zoom 700/500 ms. The overlay gets a 200 ms fade. (Implementer's default; the owner approves it at ExitPlanMode.)

## Steps (one commit each, RED/GREEN each)

### Step 0 — the plan goes into the repo (`docs`), plus the pre-install checks

- Copy this plan and its challenger findings to `docs/handoffs/2026-10-07-e1-overlay-plan.md`.
- **CF A7:** ticket 004 says "check before adding the dependency", so the telemetry and cache-overlap checks run here:
  - `npm pack @playwright/test@1.63.0 playwright@1.63.0 playwright-core@1.63.0` into a fresh scratchpad dir, unpacked;
  - grep the unpacked packages; nothing is installed;
  - record the result in the plan copy.
  - Step 2 keeps only the RSS measurement and the floor, because RSS needs the installed suite.
- **CF A8, photo checklist:** deferred to E2 entry (`v1-build-spec.md:170`, "stays at entry", T005 d5). The NASA Earth texture is E2's first need, and E1 needs no photos. Recorded here.

### Step 1 — the suite scaffolding and zero-network (`test(e2e)` + `chore(deps)`)

**Dependency:**

- `npm i -D -E @playwright/test@1.63.0`.
- Add an ADR 0004 row in the happy-dom style: the reason, "devDependency only; nothing reaches the bundle", and that it matches the MCP's headless-shell revision 1243.

**Config:**

- `playwright.config.ts`:
  - `webServer`: `npm run build && npx vite preview --strictPort --port 4173`, with `reuseExistingServer: false`.
  - `workers: 1`, `fullyParallel: false`.
  - One chromium project, headless. This uses the headless shell, so no `channel`.
  - `reporter: 'list'` (no HTML report).
  - `use.serviceWorkers: 'block'`.
- Add the script `"test:e2e": "playwright test"`.
- `tsconfig.json` `include` gains `e2e` and `playwright.config.ts`.
- `eslint.config.mjs` gains a node-globals block for `e2e/**`, and its ignores gain `playwright-report/` and `test-results/`.
- `.gitignore` and `.prettierignore` gain `playwright-report/`, `test-results/` and `blob-report/`.
- Keep the specs out of vitest's reach: they live in `e2e/*.spec.ts`, and vitest's include is `src/**/*.test.ts`.

**Wrapper:**

- `ops/remote-shell/remote-shell.sh` HEAVY regex (:103) gains `npm run test:e2e`, so a local or pinned run is guarded.
- RED case first in `test-pin-list.sh`: in local mode, `npm run test:e2e` → GUARD.

**Test:**

- `e2e/zero-network.spec.ts`: record every `request` and fail on any URL whose origin is not the preview origin (`data:` and `blob:` allowed). It loads the book and waits for the canvas.
- **RED proof:** a temporary, uncommitted `fetch('https://example.com')` in `main.ts` makes the test fail. Revert it, and the test passes. Both runs go in the commit body.

**Install:**

- On M1: `npx playwright install --only-shell chromium`, a one-time CDN download at setup, not in the game.
- On the M2: re-run `ops/remote-shell/setup-m2.sh` through the wrapper. Its `:75-83` branch now fires.
- Re-run `preflight.sh`. Its `[info]` for headless_shell should turn ok.

### Step 2 — E1 entry: ticket 004's gaps and the floor (`fix(ops)` + docs)

**Telemetry:**

- grep the installed `node_modules/playwright-core` and `@playwright/test` for `telemetry`, `analytics`, `DO_NOT_TRACK` and hardcoded `https://` endpoints outside browser download hosts.
- Record the result. If any endpoint exists, AskUserQuestion before going on.

**Cache overlap:**

- Record: the same revision (1243) as MCP 0.0.80. On M1 the MCP actually drives system Chrome (`channel: chrome`, `~/.cache/ms-playwright-mcp/` profile), so today no binary is shared and the profile dirs are disjoint.
- Record what changes if the MCP version moves.

**Peak RSS on both machines:**

- Sample MemAvailable every 0.2 s during one `npm run test:e2e`: drop = before − min. Also take peak RSS summed over the chromium + node process tree, from `/proc/*/status` VmRSS.
- **M2:** through the wrapper, with `hostname` proof.
- **M1:** dev server stopped, `free -h` first, through mem-guard.
- The sampler is an ad-hoc scratchpad script, not committed. Only the numbers go into docs.

**Floor:**

- new = ceil128(M1 drop + 512).
- RED: change `ops/mem-guard/test-mem-guard.sh` :29, :39 and :56 to the new value. It fails against the 1536 default.
- GREEN: change `mem-guard.sh:29` and `:8-9` (provisional → measured, with the date and the numbers) and the usage text `:18`.
- Also run `test-pin-list.sh`, whose under-floor fixtures must still hold.
- Update the 1536 mentions in CLAUDE.md.
- Record the results in ticket 004 (a "Gaps closed (E1 entry, 2026-10-07)" section) and in the E1 handoff.
- **Stop rule:** if the M1 drop + 512 exceeds what M1 typically has free (~2.8 GB available now), AskUserQuestion. The suite could not then run on M1 at all, and that changes T006 d6's fallback.

### Step 3 — the preview smoke and the favicon (`fix`)

- **Test:** `e2e/preview-smoke.spec.ts` fails on any `requestfailed`, on any response ≥400 inside the origin, and on any `pageerror`.
- **RED:** `/favicon.ico` 404.
- **Fix:** an inline `data:` SVG `<link rel="icon">` in `index.html`. It is textless and makes zero requests, so it needs no `public/` dir.
- **GREEN:** the test passes.
- `privacy-guard` routes here on `index.html` and will see a `data:` href only.

### Step 4 — the reduced-motion helper and the zoom paths (`feat`)

**Helper:**

- `src/shared/reduced-motion.ts`: `prefersReducedMotion(win = window): boolean` via `matchMedia('(prefers-reduced-motion: reduce)')`. It is false if `matchMedia` is missing or throws.
- vitest `src/shared/reduced-motion.test.ts`, with `matchMedia` stubbed to true, false, missing and throwing. RED first, because the module is absent.

**Zoom:**

- `book-zoom-transition.ts`: both functions take `reduced = prefersReducedMotion()`. When reduced, they call `onComplete` synchronously and touch no camera or timer.
- vitest `book-zoom-transition.test.ts`, with a stub scene of spies on `cameras.main.pan`/`zoomTo` and `time.delayedCall`:
  - reduced → `onComplete` called, no camera calls;
  - not reduced → the current calls are unchanged.

### Step 5 — bug 5: the book-zoom call sites (`fix`)

**Regression test:** `src/shared/call-sites.test.ts` reads the scene sources (`import.meta.glob(..., { query: '?raw' })`) and asserts:

- `storybook-scene.ts` calls `zoomIntoPage`, and a level scene's back path reaches `zoomOutToBook`.
- RED on the current code.

**Fix:**

- **Storybook card tap** → `zoomIntoPage(this, {x,y}, () => this.scene.start(sceneKey))`, with the input disabled during the zoom so there is no double start.
- **Earth's back button** → `this.scene.start(STORYBOOK_SCENE, { returnFrom: 'earth' })`.
- **Storybook `create(data)`:** when `returnFrom` names a page, it sets camera zoom 4 centred on that card, then `zoomOutToBook`. Reduced → instant.

**CF A1/B3, the zoom-out recentres:**

- `zoomOutToBook(scene, home, onComplete, d, reduced)` runs `pan(home.x, home.y, d)` alongside `zoomTo(1, d)`.
- Reduced → `setZoom(1)` + `centerOn(home)` synchronously, with no tween and no timer.
- In reduced mode, `create(data)` does not pre-zoom.
- Input is disabled until the zoom-out completes.
- Step 4's vitest asserts "reduced → zoom 1, centred, no tween/timer". That replaces "no camera calls".

**CF A2/B4, the tripwire:** assert that `storybook-scene.ts` calls `zoomIntoPage` **and** `zoomOutToBook`, and that `earth-scene.ts` passes `returnFrom`.

**Why a source test:** the behaviour lives in Phaser scenes, which vitest does not boot (`vitest.config.ts:16-20`). The tripwire stops the call site being deleted again. The dev walk verifies the behaviour in both motion modes, using MCP `emulate` for `prefers-reduced-motion`.

### Step 6 — the companion box (`feat`)

**Schema:**

- `schemas/level-data.schema.json` gains a required `companionTiers` (`enum: [2, 3]`), with a description citing v1-spec :27-29.
- `earth-data.json` gets `"companionTiers": 3`.
- pytest RED case in `tests/test_validate_levels.py`: missing or out-of-range → rejected. Then GREEN.

**Content (superseded by CF A5, owner 2026-10-07: per marker, seam only):**

- `companion.json` holds `companion.earth.<beat>.arrival` for the **4 required markers** (sundial, day-night-spin, seasons-globe, day-length).
- Each line names the goal and makes no sky claim.
- The line is shown when that marker's overlay opens, above the coming-soon body.
- The other five markers get theirs with their engines.
- `docs/sources.md` "Story lines" table (:864-872) gets one row per key: "none — pure story" (ADR 0008, CF A6).
- Wording rules :848-862 apply.
- Nothing is shown on level entry.

The original line, kept for the record:

- Create `content/bg/companion.json` with `companion.earth.arrival`, Earth's arrival line naming the goal.
  - Draft Bulgarian, gender-neutral first person (ADR 0008), never „спътник".
  - Reviewed by `pedagogy-report`. `astronomy-report` routes on `content/`.
- This makes `content.test.ts` go RED (its every-key-reachable tripwire). Then add the import at `content.ts:1-14` → GREEN.

**Pure tiers:**

- `src/shared/companion-tiers.ts`: `companionStages(tiers): readonly ('arrival'|'nudge'|'fact')[]` (3 → all, 2 → nudge and fact). vitest RED/GREEN.
- Nudge keys are not authored now: stall detection needs an engine (E3+). The fact tier reuses each marker's existing `reward.fact`.

**Phaser:**

- `src/shared/companion-box.ts`, ≤150 lines: a screen-fixed box with a wrapping Bulgarian text area, so it grows and is never fixed-width (rule 3), `show(key)` and `hide()`.
- EarthScene shows the arrival line on entry when `companionStages` includes `arrival`.

### Step 7 — bug 4: the overlay and the progress write (`fix` + `feat`)

**Pure module:**

- `src/shared/progress-write.ts`: `recordSolve(progress, levelId, markerId, markers, threshold): GameProgress`.
  - Adding a solve is idempotent.
  - It sets `completed` when `meetsThreshold` holds, and never un-completes.
  - The function is pure and returns new objects.
- vitest RED/GREEN, including idempotence, an optional marker never completing alone, and a completed flag that stays put.

**Regression test for bug 4:** extend `call-sites.test.ts` to assert `saveProgress` is called from a production module. RED → GREEN.

**Overlay:**

- `src/shared/puzzle-overlay.ts`, ≤200 lines, Phaser:
  - a camera-sized dim rectangle that swallows input, a panel and a title;
  - a close button `ui.puzzle.close`, ≥44×44 hit area;
  - a body slot, filled with `ui.puzzle.coming-soon` for every E1 marker, since there are no engines yet;
  - `onSolved(markerId)` → `recordSolve` + `saveProgress` + the companion shows `reward.fact` + `ui.puzzle.solved`.
  - The player is frozen while it is open. Fade 200 ms, or instant when reduced.
- EarthScene's marker tap opens the overlay and the `console.warn` is removed.
- Marker hit areas grow to ≥44 px (`standards-frontend.md:14`). The visible dot stays.

**E2E:** `e2e/reload-persistence.spec.ts`:

- seed `narrative-adventure:progress:v1` with Earth `completed: true` via `page.evaluate`;
- `page.reload()`;
- assert the key is byte-identical after the game booted, so boot does not clobber it, and that it parses to version 1.
- RED proof: temporarily make the boot call `saveProgress(empty)`. Revert it for GREEN.

### Step 8 — `qa-report` and the docs (`docs`)

- `.claude/skills/qa-report/SKILL.md` gains these (T006 d11):
  - `npm test` (vitest) through mem-guard;
  - the suite on the M2 through the wrapper with `hostname` proof;
  - the M1 fallback (mem-guard, `workers: 1`, dev server stopped, said in the report);
  - recording the chunk sizes from the suite's build.
- README: the `test:e2e` command, the one-time `playwright install --only-shell chromium`, the suite's checks.
- CLAUDE.md commands: `npm run test:e2e`.

## Exit (§2 standard + E1 block)

1. On M1 through mem-guard: `npm run validate`, `npm test`, `venv/bin/python -m pytest` and `validate-levels.py` are green.
2. Reduced paths: zoom = instant cut, overlay = instant. Both are verified in the dev walk with reduced motion emulated.
3. Router: `PRECOMMIT_STAGED="$(git diff --name-only 1eaa6c5..HEAD)"` piped with a `git commit` stdin. Run every routed report: expect `perf-report`, `privacy-guard`, `security-audit` (package.json), `pedagogy-report` and `astronomy-report` (content/bg). Each must be clean.
4. The dev walk: Playwright MCP against `npm run dev` on M1 after `free -h`:
   - the book → the zoom → Earth → the arrival line → tap a marker → the overlay with coming-soon → close → back → the zoom out;
   - repeat with `prefers-reduced-motion: reduce`;
   - console clean (no favicon 404).
5. **The suite's first run on the M2:** `bash-remote-shell.sh -c 'hostname; npm run test:e2e'` → `Bobby`, 3/3 green. Record the chunk sizes from that build.
6. Pytest guards: none are landed yet (E7 and Moon B add them).
7. README updated.
8. The E1 block:
   - ticket 004's gaps recorded closed;
   - the floor re-tuned;
   - `qa-report` updated;
   - also: all hook tests, `test-pin-list.sh` and `test-mem-guard.sh` green.

- Handoff `docs/handoffs/2026-10-07-session-handoff.md` (updated, or a new dated file if the date has changed). Latent bugs 4 and 5 are marked closed. Ask whether to commit; never push.

## Critical files

- **New:**
  - `playwright.config.ts`
  - `e2e/{zero-network,preview-smoke,reload-persistence}.spec.ts`
  - `src/shared/{reduced-motion,companion-tiers,companion-box,progress-write,puzzle-overlay}.ts` + tests
  - `src/shared/call-sites.test.ts`
  - `content/bg/companion.json`
  - `docs/handoffs/2026-10-07-e1-overlay-plan.md`
- **Changed:**
  - `package.json`/lock, `tsconfig.json`, `eslint.config.mjs`, `.gitignore`, `.prettierignore`, `index.html`
  - `src/shared/{book-zoom-transition,content}.ts`
  - `src/scenes/storybook-scene.ts`, `src/scenes/earth/{earth-scene.ts,earth-data.json}`
  - `schemas/level-data.schema.json`, `tests/test_validate_levels.py`
  - `ops/mem-guard/{mem-guard,test-mem-guard}.sh`, `ops/remote-shell/{remote-shell,test-pin-list}.sh`
  - `docs/adr/0004-*.md`, ticket 004, `.claude/skills/qa-report/SKILL.md`, README, CLAUDE.md
- **Reuse:**
  - `loadProgress`/`saveProgress`/`meetsThreshold`/`requiredMarkerIds` (`game-state.ts`)
  - `t()` (`content.ts`), `FONT_STACK` (`fonts.ts`)
  - the existing zoom functions
  - `setup-m2.sh:75-83` and the `preflight.sh:85-92` headless_shell check

## Risks

- **The Bulgarian arrival line:** content quality is gated by `pedagogy-report`. The owner reads it at the exit.
- **The source-text call-site test** is a tripwire, not a behaviour test. The dev walk carries the behaviour.
- **The headless-shell download** is network at setup time on both machines, not in the game. Rule 8 is unaffected.
- **Every new file stays ≤300 lines.**

## Challenger Findings

Two challengers ran in parallel: A on coverage, B on feasibility. **Both returned REVISE, at medium confidence.** The owner answered three of the forks on 2026-10-07. Every other fix below is accepted and folded. Where a fix and the step text above conflict, this section wins.

### Owner rulings on the forks

- **A5:** arrival lines are per marker, seam only, and E1 authors the 4 required markers (folded into Step 6).
- **A9:** keep the `completed` flip in E1's `recordSolve`. The handoff records that T002 d7's hook landed early in `progress-write.ts` and that E4 proves it in play.
- **A4/B1:** run the smoke on today's `index.html` before writing the fix.
  - If the headless shell shows no `/favicon.ico` 404, the RED becomes a DOM assertion: `link[rel~=icon]` with a `data:` href.
  - "No favicon 404" stays an exit check in the dev walk, on system Chrome.

### Folded fixes, by step

**Step 0**

- **A7:** the telemetry and cache-overlap checks run before install, against `npm pack` tarballs.
- **A8:** the photo checklist is deferred to E2 entry.

**Step 1**

- **B7:** `ops/remote-shell/mutagen.yml` ignore gains `test-results`, `playwright-report` and `blob-report`. Re-create the mutagen session using the command in `mutagen.yml`. Tell the owner first, because a sync-session change is operational.
- **B8:** `vite preview --host 127.0.0.1 --strictPort --port 4173`. Set `webServer.url` and `use.baseURL` to `http://127.0.0.1:4173`, and compare the origin against exactly that string. `webServer.timeout: 180_000`.
- **B (verified premise):** the HEAVY RED is an executed `run` case in local mode, in the style of `test-pin-list.sh:178`, not an explain `check`.

**Step 2**

- **B2, the M2 sampler:**
  - It lives in a synced, git-untracked repo path (`ops/scratch-rss-sampler.sh`) that mutagen does not ignore. Delete it after measuring.
  - Invoke it by a command line that names neither `/proc/meminfo`, `free` nor `mem-guard`. The file's contents are not pattern-matched.
  - `hostname` goes in the same command.
- **B5, the fixtures:** set LOW to `floor − 512` (or a fixed 256 MB) and HIGH to `floor + 1024`, in **both** `test-mem-guard.sh` (:25, :27) and `test-pin-list.sh` (:60-61). If the new floor is 1536, record "no change, no RED" instead of inventing one.
- **A11, the stop rule:** also AskUserQuestion if the new floor exceeds the M1 MemAvailable measured during a normal session with the dev server running. Husky's vitest and pytest share this floor.

**Step 3**

- **A3(b):** the smoke also runs one case under `page.emulateMedia({ reducedMotion: 'reduce' })`.
- **A13:** the smoke taps into Earth (the canvas coordinates of the Earth card) and asserts no errors. That covers the zoom path under preview. This lands once Step 5 exists; Step 5 extends the smoke.

**Step 4**

- **A1/B3:** reduced mode means zoom 1, centred, with no tween or timer (see Step 5).

**Step 5**

- **A1/B3:** the zoom-out recentres.
- **A2/B4:** the tripwire is fixed.
- **A3:** the MCP 0.0.80 has no `browser_emulate_media`. The dev walk uses `browser_run_code_unsafe` → `page.emulateMedia({ reducedMotion: 'reduce' })`. The MCP is not bumped.

**Step 6**

- **A6:** add the `sources.md` Story-lines rows.
- **A12:** the companion box is `setScrollFactor(0)`, re-lays out on `scale` `resize` (`Scale.RESIZE`), has ≥4.5:1 contrast and has no animation. It is shown and hidden only by the overlay open and close, so it needs no reduced path.

**Step 7**

- **B6:** add `isContentKey(k: string): k is ContentKey` to `content.ts`, backed by the bundle keys, with a vitest case. The marker `label` and `reward.fact` (JSON `string`) go through it. A miss logs and shows the key path, matching `t()`.
- **A10:** add `commitSolve(levelId, markerId, markers, threshold)` (load → `recordSolve` → `saveProgress`) in `progress-write.ts`. Vitest it against happy-dom `localStorage`. That is the behavioural RED/GREEN for bug 4, in place of only a source tripwire. The overlay calls it.
- **A12/B10:**
  - the overlay is screen-fixed and re-lays out on resize, with ≥4.5:1 contrast;
  - EarthScene skips `player.update()` and zeroes the body velocity while the overlay is open; `player-character.ts` gets `setEnabled(on)`;
  - marker hit area: `new Geom.Circle(12, 12, 22)` + `Geom.Circle.Contains`;
  - Earth's back button gets a ≥44×44 hit area.
- **B10:** the reload test polls the key for about 500 ms after the game is ready to show it stays byte-identical. "Ready" means the canvas plus one `requestAnimationFrame` tick after `scene` create.

**Handoff (A10/B9)**

- **Bug 4:** "call site + behavioural unit test landed; first runtime solve in E3". Not "closed".
- **Bug 5:** closed (call sites wired and walked).

### Rejected

- None. A13 (optional) is accepted as cheap coverage.

### Verdicts

- **Challenger A (coverage):** REVISE, medium. 13 findings, all folded.
- **Challenger B (feasibility):** REVISE, medium. 10 findings, all folded.

## Step 0 result: pre-install checks (ticket 004, "before adding the dependency")

Method: `npm pack @playwright/test@1.63.0 playwright@1.63.0 playwright-core@1.63.0` into a scratch dir, then unpack and grep. Nothing was installed.

- **Install scripts:** none in any of the three packages (`scripts: {}`).
- **Telemetry:** none found.
  - grep for `telemetry|analytics|DO_NOT_TRACK|sentry|segment.io|mixpanel|google-analytics`. The only real hits are protocol type docs and a Firefox pref that _disables_ Firefox telemetry (`datareporting.usage.uploadEnabled: false`, `telemetry.fog.test.localhost_port: -1`).
  - The other case-insensitive hits are `hasEntry`/`OPFSEntry`.
  - No `fetch`/`request` to a hardcoded https endpoint exists in `lib/`.
- **Network the packages can use:** only the browser download at `playwright install` time, from `cdn.playwright.dev` and `playwright.download.prss.microsoft.com`. That is setup on the developer machine, never the game (rule 8 unaffected). Every other `https://` string is a doc or comment link (playwright.dev, MDN, GitHub, …).
- **Cache overlap with the Playwright MCP:**
  - `@playwright/test@1.63.0` and `@playwright/mcp@0.0.80` (bundled `playwright-core@1.63.0-alpha-2026-08-31`) both pin `chromium-headless-shell` revision **1243** (153.0.8010.12), per each version's `browsers.json`.
  - On M1 the MCP actually drives **system Chrome** (`channel: chrome`, profile in `~/.cache/ms-playwright-mcp/`), so today the two share no binary and no profile directory. The suite's headless shell lands in `~/.cache/ms-playwright/chromium_headless_shell-1243`.
  - If the MCP pin moves to a version on another revision, two headless-shell builds coexist in the cache, which costs disk, not RAM. That is a reason to bump them together, per ADR 0004.

## Settled during the build (owner, 2026-10-07)

- **The mem-guard floor stays at 1536 MB:** the formula gives 1408 and the owner kept max(1408, 1536) until E2's 3D is
  measured.
- **The seasons-tilt engine (E3):** the tilt angle is **fixed**, and the child moves Earth along its orbit, or turns
  the Sun's direction, until a hemisphere leans toward or away from the Sun. A child-varied tilt angle would teach
  that the tilt changes through the year, which is false. This came from the pedagogy review of the arrival lines.
  It changes only the meaning of `drives`; no new type.
- **The arrival lines after `puzzle-pedagogy-reviewer`:**
  - sundial: „сянката падне", not „легне"; „точно" dropped (the engine has a tolerance);
  - seasons: „Нагласи", neutral about what moves;
  - day-length: asks which day has **light** for longer, because a whole day lasts the same in summer and winter.
- The keys are `companion.<marker-id>.arrival` (e.g. `companion.earth-sundial.arrival`). The plan's
  `companion.earth.<beat>.arrival` is superseded.
