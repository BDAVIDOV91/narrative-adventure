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
