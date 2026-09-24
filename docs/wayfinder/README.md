# Wayfinder maps

Decision maps for efforts too big for one session. The owner starts one with `/wayfinder`; see
`.claude/skills/wayfinder/SKILL.md`. The file format is in `.claude/skills/wayfinder/TRACKER.md`, and it is strict,
because the SessionStart hook and the read-only viewer (`ops/wayfinder-viewer/`) parse these files. This directory is
in `.prettierignore` for the same reason.

- **Copy-paste triggers for the owner: [QUICKSTART.md](QUICKSTART.md).**
- One directory per map: `<slug>/MAP.md`, `<slug>/tickets/`, `<slug>/research/`.
- A map holds decisions, not a build. When the way is clear, the build goes through plan mode and two challengers.
- A bug found on the way follows CLAUDE.md rule 5 (RED/GREEN) and goes on the current handoff's latent-bugs list, not
  into a ticket.
- **No data about any child, no personal data, no credentials** in any file here. Cite code as `file:line`, and cite
  astronomy through `docs/sources.md`.

Adopted 2026-09-24 from the owner's `pdf_data_extractor_v2`, where the mentor's wayfinder method was piloted and
widened. First map: `road-to-v1`.

This README sits directly under `docs/wayfinder/`, not inside a map directory, so the viewer ignores it.

## Mentor tooling: considered and not adopted (2026-09-24)

Recorded so none of these is re-proposed. The source is the mentor's bundle at `~/Desktop/hope_for_win/`. The rule is
"adopt only what is new". The items that were adopted are listed in `.claude/rules/`, CLAUDE.md rule 5, the Wayfinder
section of CLAUDE.md, and `eslint.config.mjs`.

| Item | Why not |
|---|---|
| `rethink` skill | Two `challenger`s, `astronomy-consultant` and `grilling` cover it. Six parallel web agents do not fit a 1.9 GB RAM budget. KNA rejected it too. Revisit only if a decision stalls twice. |
| `history` skill | It needs a session-logging hook and `~/.claude/history/`, and neither exists. claude-mem's `mem-search` already answers "did we fix this before?". |
| `domain-modeling` + `CONTEXT.md` glossary | A second ADR writer next to `grill-with-adr`. The vocabulary is already pinned by the schema enum and the `content/bg/` keys. |
| `testing.md` | Covered by CLAUDE.md rule 5 and the pre-commit gates. Its 80 % coverage floor and pytest markers are not adopted. |
| `verification.md` "Fix ALL errors — no asking" | Conflicts with CLAUDE.md rule 4: anything needing the owner is asked through an interview. Its useful line ("tests passing ≠ program working") is in rule 5. |
| `development-practices.md` "Always stash before a branch switch" | Stash is banned: `block-dangerous-git.sh` and the settings deny list. |
| `development-practices.md` "Self-correct without asking" | Conflicts with rule 4 for anything beyond a typo. |
| `task-and-workflow.md` "No built-in plan mode" | This repo's review gate is the plan-mode checkpoint with two challengers. Only its sizing table was kept (CLAUDE.md Wayfinder section). |
| `task-and-workflow.md` vexor / Pilot memory / `/p` | These tools are not installed here. |
| `standards-typescript.md` prose | Already enforced by tooling: strict tsconfig, `no-explicit-any`, `import-x/order`, `unicorn/filename-case`, `prefer-node-protocol`. The one residue (explicit return types) is an ESLint rule. "Log and re-throw" conflicts with `no-console`. |
| `standards-frontend.md` components / CSS methodology / fonts | Phaser draws on a canvas. Font choice is governed by CLAUDE.md rule 3 (Cyrillic coverage). |
| `standards-backend`, `-python`, `-golang`; `tm*` / `task-manager`; `qa-test`; `claude-global-review`; `dependency-review`; `commit-agent`; infra, vault and pilot rules | Tied to the mentor's employer (Asana, staging, VPN, the `~/.claude` feature registry), or to a backend this game does not have. `qa-report` and `security-audit` are this repo's counterparts. `commit-agent` runs with `bypassPermissions`. |
| `ops/remote-shell` (KNA's M1→M2 offload) | Machine-specific. Wayfinder only writes Markdown. |
