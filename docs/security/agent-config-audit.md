# Agent-config audit

The project's other security gates — `privacy-guard`, `security-audit`, `qa-report` —
audit the **shipped game**, which is static, offline, and makes zero network requests
by rule 8. Nothing audited the **development harness**: the hooks, settings, MCP
servers and agent definitions that run on the owner's machine with the owner's
permissions. That is where the live risk actually sits. A poisoned hook or an
auto-approved MCP server compromises the machine, not the game.

This file records what was audited, what was fixed, and — importantly — which
findings were examined and **deliberately not acted on**, so a future session does
not re-triage them from scratch.

## Tool

[AgentShield](https://github.com/affaan-m/agentshield) (`ecc-agentshield`, MIT),
invoked on demand:

```bash
npx -y ecc-agentshield scan --path .
```

**Not installed.** No plugin, no marketplace entry, nothing in `package.json`. It is
a development-time tool run against configuration, never part of the game build.
`--fix` is not used: `.claude/hooks/block-dangerous-git.sh` is load-bearing, and an
auto-fix that silently weakened it would be worse than any finding it resolves.

Do not run `--opus` on a repository holding real credentials without reviewing the
plain scan first — `--opus` sends findings to three model agents, while the plain
scan is local pattern matching. This repository holds no secrets, so the question
does not arise here.

Scan reports go to the session scratchpad. They are never committed.

## When to re-run

Only when the agent-config surface itself changes:

- `.claude/hooks/`
- `.claude/settings.json`, `.claude/settings.local.json`
- `.mcp.json`, or any new MCP server
- `.claude/agents/`, `.claude/skills/`
- `CLAUDE.md`

Not on the game-code pre-commit path — that is already covered by the existing
skill routing.

## 2026-09-09 — baseline

Grade **B (85/100)** before, **B (89/100)** after; 13 findings down to 12, criticals
1 to 0, and the MCP category from 81/100 to 100/100. Three findings were real.
Secrets scored 100/100 both times, correctly: this repository contains none.

### Fixed

| Finding                                       | Where                         | Why it mattered                                                                                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enableAllProjectMcpServers: true` (CRITICAL) | `.claude/settings.local.json` | Auto-approved **any** MCP server declared in `.mcp.json`, with no human review step. A branch or a clone could introduce a server that executes on session start. The explicit `enabledMcpjsonServers` list below it was made redundant by the blanket flag. Now `false`; the two named servers still load.                                                                      |
| `"deny": []` (HIGH)                           | `.claude/settings.local.json` | Empty, so the allow list was the only control — and it permits `Bash(npx:*)`, which executes arbitrary remote packages. Now populated, including `Bash(git push:*)`, which encodes rule 7 as configuration rather than relying on the hook alone.                                                                                                                                |
| `npx -y ...@latest` in both servers           | `.mcp.json`                   | Not an AgentShield finding — found while verifying its MCP report. Both servers resolved an unreviewed upstream version on every start. Chained with the critical above, that was the real compromise path. Pinned to `@upstash/context7-mcp@4.0.6` and `@playwright/mcp@0.0.80`, matching the exact-pin discipline in `docs/adr/0004-dependency-pins-and-their-constraints.md`. |

Guarded by `.claude/hooks/test-settings-hardening.sh`, which asserts all of the
above and fails RED on the pre-fix configuration.

### Which file the hardening lives in

`.claude/settings.local.json` is gitignored (`.gitignore:54`), so anything fixed
only there protects one machine and a fresh clone re-inherits the auto-approve.
The security properties therefore live in the **tracked** `.claude/settings.json`:

| Setting                             | File                            | Why                                                                                   |
| ----------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------- |
| `enableAllProjectMcpServers: false` | `settings.json` (tracked)       | a project security property; must survive a clone and be visible in review            |
| `permissions.deny`                  | `settings.json` (tracked)       | denials are project policy, not machine preference; `Bash(git push:*)` encodes rule 7 |
| `permissions.allow`                 | `settings.local.json` (ignored) | references machine paths such as `venv/bin/*`                                         |
| `enabledMcpjsonServers`             | `settings.local.json` (ignored) | which servers this machine opts into                                                  |

`settings.local.json` takes precedence at runtime, so it can silently undo the
tracked hardening. The guard test asserts it does not re-enable
`enableAllProjectMcpServers`, and treats its absence as a pass.

### File permissions

`CLAUDE.md` is injected into every prompt as system instructions, and the hooks in
`.claude/hooks/` execute on every Bash tool call. Group-writable versions of either
are an injection surface for any other account in the owner's group.

AgentShield flagged `CLAUDE.md` at `0o664`. It did **not** flag the hooks, which
were `0o775` — group-writable _executables_ that run automatically. That is the
strictly worse exposure of the two, and it was found by checking the surrounding
files rather than by the scanner.

Applied:

```bash
chmod 600 CLAUDE.md .mcp.json .claude/settings.json .claude/settings.local.json
chmod 700 .claude/hooks/*.sh .husky/pre-commit .husky/pre-push .husky/test-pre-commit-scope.sh
```

**Git does not carry this.** It records only the executable bit, so a fresh clone
materialises every one of these files at the umask default — `0o664` and `0o775`
on Ubuntu — and the hardening is silently gone. Rerun the two commands above after
a clone.

`.husky/_/` is generated by husky and regenerated on `npm install`, so it is left
alone deliberately; hardening it would not survive an install.

For this reason `test-settings-hardening.sh` reports permissions as an **advisory
note, not an assertion**. Making it fail would turn the suite red on every clone
for a property git cannot express. The note names the drifted files; the exit code
stays 0.

### Examined and deliberately not acted on

Re-triaging these wastes a future session's time. Each was checked against the
actual file.

| Finding                                                                              | Verdict                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Hook disables logging: `>/dev/null 2>&1`" — `test-block-dangerous-git.sh:18` (HIGH) | **False positive.** That line is the `run()` helper inside the _test harness_, suppressing hook output so `echo $?` yields a clean exit code to assert against. The tool does not distinguish `test-*.sh` from a live hook.                                                                                                                  |
| "No permissions block configured" — `.claude/settings.json` (MEDIUM, baseline)       | **False positive.** AgentShield scans each settings file in isolation and does not merge them. Resolved incidentally by moving `permissions` into the tracked file.                                                                                                                                                                          |
| "No deny list configured" — `.claude/settings.local.json` (HIGH, persists)           | **False positive, and it fires _because_ the fix is correct.** The deny list is in the tracked `settings.json` where it belongs; the scanner reads `settings.local.json` alone, sees an allow list with no deny, and reports the gap. Satisfying it would mean duplicating denials into a gitignored file. Expect this on every future scan. |
| "No PreToolUse security hooks configured" — `.claude/settings.local.json` (MEDIUM)   | **False positive**, same isolation limitation. Three PreToolUse hooks are configured in `settings.json`.                                                                                                                                                                                                                                     |
| "Missing deny rule: writing to device files (`> /dev/`)" (MEDIUM)                    | **Rejected on purpose.** The pattern is a substring match that would collide with the legitimate `>/dev/null` used throughout the test harnesses. Adding it would break the suite to satisfy a scanner.                                                                                                                                      |
| "Agent definition effective size is 6700 characters" — `challenger.md` (MEDIUM)      | **Noise.** Size heuristic. The file was read end to end; the tail is the verdict-format section and the astronomy/scope review criteria. No injected instructions.                                                                                                                                                                           |
| "`CLAUDE.md` is group-writable (0o664)" (MEDIUM)                                     | **Fixed** (initially accepted, then reversed on the owner's call). See "File permissions" below.                                                                                                                                                                                                                                             |
| "Agent has no model specified" ×5 (LOW)                                              | **Not a security finding.** It is a cost hint suggesting `haiku`. These agents do real reasoning work; `astronomy-accuracy-checker` on `haiku` would be a downgrade, and rule 1 makes that the most expensive kind of regression this project can ship.                                                                                      |
| "No Stop hooks for session-end verification" (LOW)                                   | **Not a defect.** Session-end checks are covered by the pre-commit routing.                                                                                                                                                                                                                                                                  |

### On `curl`

An early draft of the deny list blocked `Bash(curl:*)`. It was removed before being
applied: `docs/sources.md:306-319` documents fetching the HYG catalogue, the
Stellarium sky culture and the WDS orbit file with `curl`. Denying it would have
broken the documented data-acquisition path to satisfy a generic rule. Rule 8
governs the shipped game's runtime, not build-time source fetching.

### Verdict on the tool

Adopted, on-demand only. 3 of 13 findings were real, including one genuine critical
that no existing gate covered. The false-positive rate is high and concentrated in
one limitation — it does not merge `settings.json` with `settings.local.json` — so
the triage cost is predictable and this table absorbs most of it.
