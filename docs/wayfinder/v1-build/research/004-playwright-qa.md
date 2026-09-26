---
ticket: "004"
title: Playwright QA on this machine
status: done
---

# Playwright QA on this machine: candidates

Everything here is a candidate for ticket 006 to weigh, not a decision. The sources are web search excerpts gathered on
2026-09-26 with the built-in WebSearch, because Perplexity was unavailable. Anything load-bearing gets re-read on its
page before a build plan relies on it.

## Answer first

- **A committed `@playwright/test` suite is the durable regression artifact. The MCP server is for exploration.** It is
  the tool an agent uses to walk the game and draft specs. Specs that are committed and run by `npx playwright test` are
  what can gate a merge. The MCP server already in `.mcp.json` stays useful for manual QA walks (`qa-report`).
- **It fits ~1.9 GB free with one worker and headless shell.** It does not fit with parallel workers.
  - One Chromium instance is reported at roughly 400 MB to 1.5 GB depending on the page.
  - Three workers on a 4 GB machine reached about 90% of memory.
  - The candidate settings: `workers: 1`, `--only-shell` install, and `free -h` before each run (the project rule for
    3D).
  - Treat the WebGL (Three.js) beats as the upper bound.
- **Pin the Playwright version exactly, and watch the Chromium build it pulls.**
  - From 1.57, Playwright launches Chrome for Testing instead of its own open-source Chromium.
  - One issue reports very high memory per instance after that change.
  - ADR 0004's rule (exact pin, with the reason inline) applies. Any bump is checked for memory before it lands.
- **Rule 8 holds.**
  - Playwright is a devDependency; nothing ships in the bundle.
  - The only network use is the one-time browser download from Playwright's CDN.
  - A spec can assert that the game makes zero network requests by failing on any request not served from the local
    preview origin.
  - No source found states whether Playwright has telemetry. This is a gap.

## Findings

### 1. RAM

- A single Chromium instance spikes to between 400 MB and 1.5 GB depending on page complexity and JS execution
  ([Medium, "8GB Was a Lie"](https://medium.com/@onurmaciit/8gb-was-a-lie-playwright-in-production-c2bdbe4429d6)).
- Three parallel workers on a 4 GB machine used up to 90% of memory ([microsoft/playwright#36686](https://github.com/microsoft/playwright/issues/36686)).
  Instances left open after tests exhaust memory on small machines ([#33086](https://github.com/microsoft/playwright/issues/33086)).
- Headless runs are leaner. Firefox is reported leaner than Chromium
  ([datawookie, browser footprint](https://datawookie.dev/blog/2025-06-06-playwright-browser-footprint/)).
- **Playwright 1.57 switched to Chrome for Testing.** An issue reports roughly 20 GB per instance and no way back to open-source
  Chromium ([#38489](https://github.com/microsoft/playwright/issues/38489)). Headless still uses the headless shell by
  default ([playwright.dev/docs/browsers](https://playwright.dev/docs/browsers)). Whether that report reproduces for
  headless shell is unverified, so it is a gap.
- **Candidate:** `workers: 1`, `fullyParallel: false`, headless shell only, and the dev server stopped while the suite runs
  against `vite preview`.

### 2. `@playwright/test` against `@playwright/mcp`

- MCP exposes a live browser as model-callable tools (`browser_navigate`, `browser_click`, `browser_snapshot` and so on),
  driven by accessibility snapshots.
- Playwright Test discovers and runs versioned spec files with fixtures, projects, retries and reporters. MCP can explore
  a flow and draft locators. The durable result is a reviewed spec run by `npx playwright test`
  ([testdino, CLI vs MCP](https://testdino.com/blog/playwright-cli-vs-mcp);
  [Medium, "Good for exploration, risky for regression"](https://medium.com/@rsb1201/playwright-mcp-good-for-exploration-risky-for-regression-b8b861dcc098)).
- **Candidate:** both. `@playwright/test` is pinned for the finish bar's "a Playwright QA pass has run". The MCP server
  serves `qa-report`'s manual walks. Each browser run happens on its own, never both at once.

### 3. Install footprint

- `npx playwright install --only-shell` skips the headed Chromium and fetches only `chromium-headless-shell`
  ([playwright.dev/docs/browsers](https://playwright.dev/docs/browsers)). That is reported at about 150–200 MB, against about
  400–600 MB for full Chromium ([QASkills, PLAYWRIGHT_BROWSERS_PATH](https://qaskills.sh/blog/playwright-browsers-path-environment-variable-reference)).
- Browsers live in `~/.cache/ms-playwright`, shared across projects and outside `node_modules`
  ([candidstartup](https://www.thecandidstartup.org/2024/12/16/bootstrapping-playwright.html)). Each Playwright version
  pins its own browser build.
- Downloads come from `playwright.azureedge.net` / `cdn.playwright.dev`. `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD` exists, but
  issues report it being ignored in some versions ([#24607](https://github.com/microsoft/playwright/issues/24607)).
- **Candidate:** the browser install is a documented one-off command the owner runs. `package.json` has no postinstall.

### 4. Network and privacy

- No source found describes Playwright telemetry. This is a gap: check the pinned version's docs or source before adding it,
  under `privacy-guard` and `security-audit`.
- **Candidate test:** register `page.on('request')` or `context.route('**/*')`, and fail on any URL outside the preview
  origin. This makes rule 8 a regression test rather than an audit.

### 5. Testing a canvas/WebGL game

- `expect(page).toHaveScreenshot()` compares against committed baselines
  ([visual comparisons](https://playwright.dev/docs/test-snapshots)). Font rendering differs by OS, so baselines are
  per-platform. On this project that means Linux on the owner's machine.
- Headless Chromium renders WebGL through SwiftShader, a software renderer
  ([createIT](https://www.createit.com/blog/headless-chrome-testing-webgl-using-playwright/);
  [Dave Snider](https://davesnider.com/gputests)). That is slower and more CPU-heavy, but it avoids the APU.
- Games are made testable by waiting on a readiness flag the game sets
  ([Barth Cave, web games E2E](https://barthpaleologue.github.io/Blog/posts/webgl-webgpu-playwright-setup/)).
- **Candidate:** a small test-only hook (a readiness flag, and a way to read progress from `localStorage`) instead of
  pixel baselines for the flows. Screenshots are kept only for the 360px grid fit and Cyrillic rendering.
- Reduced motion: set `reducedMotion: 'reduce'` in `use`, or `page.emulateMedia({ reducedMotion: 'reduce' })`
  ([TestOptions](https://playwright.dev/docs/api/class-testoptions)). One open issue says the config option can be
  silently ignored ([#42001](https://github.com/Microsoft/playwright/issues/42001)), so the per-page call is the safe form.
- Viewport: a 360×640 project covers the finish bar's "fits without scrolling down to 360px portrait"
  ([QASkills, mobile emulation](https://qaskills.sh/blog/playwright-mobile-emulation-guide)).

## Confidence and gaps

- **Medium confidence.** The findings are search excerpts, and the RAM numbers are anecdotal, not measured here.
- Not measured: the real peak RSS of this game under headless shell on this machine. The first build phase that adds
  Playwright measures it (`free -h` before and after) and records the result.
- Unknown: which Playwright version `@playwright/mcp@0.0.80` bundles, and whether it shares the browser cache with a
  pinned `@playwright/test`.
- Unknown: Playwright telemetry.
