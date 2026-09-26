---
id: "006"
title: Where the pedagogy, perf, privacy, astronomy and QA gates run
type: grilling
status: open
assignee: ""
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
