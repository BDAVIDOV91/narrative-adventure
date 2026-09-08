---
name: security-audit
description: Use when reviewing the project's actual attack surface, or when adding anything that changes it (a server, a network call, file handling, user-supplied content, hosting). Scoped honestly to a static offline game rather than mirroring a SaaS checklist.
---

# Security Audit

## What does not apply, and why

Being explicit about this up front, so the report is not compliance theatre. This game is
static files served to a browser: no backend, no accounts, no sessions, no database, no
uploads, no PII, no payments, no multi-tenancy. See
`docs/adr/0001-python-is-build-time-only.md`.

So these standard sections have **no surface here** and should be marked N/A rather than
answered with invented content:

- Authentication and session management
- Authorization, roles, tenant isolation
- SQL/NoSQL injection, ORM query scoping
- Server-side input validation, file upload handling
- Secrets in a running service, audit logging of requests

If a report fills these in anyway, it is fabricating. Say N/A and move on.

## What actually applies

### 1. Supply chain — the main real risk
223 npm packages and a handful of Python ones, all executing at build time on the
developer's machine.

```bash
npm audit --omit=dev
npm audit
venv/bin/python -m pip list --format=columns
```

Check that pins are exact (`.npmrc` sets `save-exact=true`) and that a new dependency is
one a human chose, not one that arrived transitively with install scripts.

### 2. Untrusted input — what little there is
The only input the game parses that a user can control is **its own `localStorage`**, which
a curious child or anyone with devtools can edit.

- `src/shared/game-state.ts` must never `JSON.parse` into use without validation.
- Worst realistic case is a player editing their own progress, which is harmless in a
  single-player offline game. Do not overstate it.
- It must not **crash**: malformed stored JSON has to degrade to a fresh save, not a white
  screen. That is a robustness bug with a security flavour, and it is the real finding
  class here.

### 3. Content injection
- Any place game text reaches the DOM as HTML rather than as Phaser text.
- `innerHTML` anywhere in `src/`.
- Generated data interpolated into markup.

### 4. Secrets hygiene
- `.env` gitignored, `.env.example` committed with placeholders only.
- **No credential behind a `VITE_` prefix** — Vite embeds those in the client bundle, where
  anyone can read them.
- No key, token or password committed anywhere in the tree.

```bash
git log --all -p | grep -niE "api[_-]?key|secret|password|token" | head -20
grep -rnE "VITE_[A-Z_]*(KEY|SECRET|TOKEN|PASSWORD)" . --include="*.ts" --include="*.env*"
```

### 5. If hosting is ever added
Currently out of scope and should be marked so. When it changes: CSP headers,
Subresource Integrity on anything external, HTTPS. Revisit this section then, not before.

## Privacy

Data collection and outbound traffic are covered by the `privacy-guard` skill, which is the
more important of the two for this project. Run that as well; do not duplicate it here.

## Output

```markdown
### APPLICABLE FINDINGS
- <finding> — LOW/MEDIUM/HIGH/CRITICAL — file:line — fix

### SUPPLY CHAIN
- <real npm audit / pip output>

### NOT APPLICABLE
- <the sections above, marked N/A with the one-line reason>

### WHAT WAS CHECKED
<commands actually run>
```

## Rules

- No finding without `file:line` and a real command behind it.
- Do not inflate severity to make the report look substantial. In a static offline
  single-player game most classic findings genuinely do not apply, and saying so accurately
  is more useful than manufacturing concern.
