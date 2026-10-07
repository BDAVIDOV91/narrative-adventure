---
id: "004"
title: Playwright QA on this machine
type: research
status: closed
assignee: owner
blocked_by: []
---

## Question

The finish bar wants "a Playwright QA pass has run". Playwright exists here only as the MCP server
(`.mcp.json:9-12`, `@playwright/mcp@0.0.80`). What can run on this machine (~1.9 GB free RAM, integrated AMD APU), and
how?

- Headless Chromium's RAM use for a canvas/WebGL page, and the settings that keep it inside the budget.
- `@playwright/test` as a pinned devDependency against the MCP server. Can it reuse the browser the MCP server already
  cached?
- The browser download footprint, against ADR 0004's exact pin with the reason inline, and `security-audit` on the
  `package.json` change.
- Rule 8: dev-only, telemetry, and whether a spec can assert that the game makes zero network requests.
- Canvas-game testing: screenshots versus test hooks, reduced-motion emulation, and a 360px portrait viewport.

Output `research/004-playwright-qa.md`. Candidates only. Nothing is installed.

## Resolution

Researched on 2026-09-26 with the user-scope `research` skill, using built-in WebSearch.
Findings: [research/004-playwright-qa.md](../research/004-playwright-qa.md). These are candidates, not decisions; ticket
006 weighs them.

- **The regression artifact is a pinned `@playwright/test` suite.** The MCP server stays for exploratory walks and
  `qa-report`.
- **It fits the RAM only at one worker with the headless shell** (`--only-shell`, about 150–200 MB on disk). Reported
  RAM per Chromium instance ranges from about 400 MB to 1.5 GB. Run `free -h` before each run.
- **Pin exactly (ADR 0004), and check memory on any bump.** Playwright 1.57 moved to Chrome for Testing, and one issue
  reports very high memory after it.
- **Rule 8 becomes a test:** fail on any request outside the preview origin. For reduced motion, use
  `page.emulateMedia` (the config option has an open bug). Use a 360×640 project for the grid fit. Prefer test hooks
  over pixel baselines.
- **Gaps:** peak RSS measured on this machine; which Playwright version `@playwright/mcp@0.0.80` bundles, and whether
  the two share a browser cache; Playwright telemetry. Check these before adding the dependency.

## Gaps closed (E1 entry, 2026-10-07)

- **Telemetry:** none in `@playwright/test`, `playwright` or `playwright-core` 1.63.0, checked on `npm pack` tarballs
  before install. They have no install scripts. The only network they use is the browser download at
  `playwright install` time, from `cdn.playwright.dev` and `playwright.download.prss.microsoft.com`.
- **Browser cache vs the MCP:** `@playwright/mcp@0.0.80` bundles `playwright-core@1.63.0-alpha-2026-08-31`. That build
  and the pinned 1.63.0 both use `chromium-headless-shell` revision 1243. On M1 the MCP drives system Chrome, so today
  the two share no binary and no profile. If the MCP pin moves, the two headless-shell builds coexist on disk. Bump
  them together (ADR 0004).
- **Peak RSS** for `npm run test:e2e`, which is build plus `vite preview` plus the headless shell, one worker,
  zero-network spec, dev server stopped. Three runs each. Drop is MemAvailable sampled every 0.2 s (before minus
  minimum). Tree RSS is the summed VmRSS of the process tree, which overcounts shared pages.

  | Machine          | MemAvailable before | Peak drop | Tree RSS peak |
  | ---------------- | ------------------- | --------- | ------------- |
  | M1 (TechnoJihad) | 2.5-2.8 GB          | 828 MB    | 1283 MB       |
  | M2 (Bobby)       | 9.3-10.2 GB         | 1253 MB   | 1289 MB       |

- **Mem-guard floor:** the formula (M1 peak drop + 512, rounded up to 128) gives 1408 MB. The owner kept **1536 MB**
  (2026-10-07), which is max(formula, provisional), until E2's 3D renderer is measured.

