---
name: privacy-guard
description: Use before any commit, and always when a dependency is added, to protect the property that this children's game collects nothing and contacts no one. Fails on new network calls, analytics, telemetry, third-party scripts, or any data collection, and audits the dependency tree.
---

# Privacy Guard

This game currently makes **zero network requests** and collects **nothing** about a child.
That is the correct posture for software aimed at children, and under GDPR children's data
carries the heaviest obligations. The safest position is the one the project already holds:
collect nothing.

That property does not erode in one big decision. It erodes when someone adds analytics
"just to see how far kids get", or loads a font from a CDN, or wires up a crash reporter.
This skill exists to catch that.

## Step 1 — Check for new outbound anything

```bash
git diff --cached -- src/ index.html

# Network calls in game code. planet-render.ts loading a LOCAL texture is fine;
# anything pointing at a remote host is not.
grep -rnE "fetch\(|XMLHttpRequest|WebSocket|navigator\.sendBeacon|EventSource" src/ index.html

# Remote origins anywhere in shipped code.
grep -rnE "https?://" src/ index.html | grep -vE "schemas/|\.local/|localhost"

# Third-party script or style tags.
grep -nE "<script[^>]+src=|<link[^>]+href=" index.html
```

Any hit is a finding until proven local.

## Step 2 — Check for collection

```bash
grep -rniE "analytics|telemetry|gtag|googletagmanager|mixpanel|segment|posthog|sentry|amplitude|hotjar|clarity" src/ index.html package.json
grep -rniE "\b(email|birthday|birthdate|fullname|geolocation)\b" src/ content/
grep -rn "localStorage\|sessionStorage\|indexedDB" src/
```

`localStorage` is expected and fine — progress stays on the child's own device and never
leaves it. Confirm nothing stores anything **identifying**: progress and puzzle completion
only, no name, no age, no device id, no timestamps that could act as one.

## Step 3 — Dependency audit

```bash
npm audit --omit=dev
npm ls --all --omit=dev 2>/dev/null | tail -40
.venv/bin/python -m pip list --format=columns
```

Report real advisories. For any newly added runtime dependency, ask what it does at
runtime and whether it phones home.

## Step 4 — Output

```markdown
### NETWORK
- <every outbound call found, or "none — verified by grep over src/ and index.html">

### COLLECTION
- <what is stored, where, and whether any of it identifies a child>

### THIRD-PARTY CODE
- <scripts, styles, fonts loaded from anywhere but this repo>

### DEPENDENCY ADVISORIES
- <real npm audit / pip output>

### VERDICT
- <CLEAN, or the specific thing that broke the collect-nothing property>

### WHAT WAS CHECKED
<the commands actually run>
```

## Rules

- Fonts must be **self-hosted** in `assets/fonts/`. A Google Fonts link sends every child's
  IP address to a third party on every load.
- A finding here is not theoretical. Name the file and the line.
- This reports; it does not block. But say plainly when the collect-nothing property has
  been broken, because getting it back after release is much harder than not losing it.
