# Provenance: Pocock skills

Vendored from https://github.com/mattpocock/skills ("Skills for Real Engineers", MIT license), pinned at commit
`3cca18b3`, by way of the owner's `pdf_data_extractor_v2` repo (KNA Vision), where it was piloted first.

| Local skill | Upstream path | Notes |
|---|---|---|
| `wayfinder` | `skills/engineering/wayfinder` | Added 2026-09-24 (owner decision, mentor suggestion). Upstream text is byte-identical; local rules sit between `NA:BEGIN`/`NA:END` markers plus one inline `NA:` comment. `agents/openai.yaml` not vendored. + `TRACKER.md`, adapted from upstream `setup-matt-pocock-skills/issue-tracker-local.md` to the layout the read-only viewer parses (`ops/wayfinder-viewer/`). |

Not a skill, but from the same collection: `.claude/hooks/block-dangerous-git.sh` came here from
`pdf_data_extractor_v2`, which adapted it from `skills/misc/git-guardrails-claude-code/`.

## Deliberately NOT vendored

- **`domain-modeling`** (with `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`): wayfinder calls it on every grilling ticket, but
  it would be a second ADR writer next to `grill-with-adr`, and its `CONTEXT.md` glossary is a business-domain tool —
  this game's vocabulary is already pinned by `schemas/level-data.schema.json` and the `content/bg/` keys. The NA block
  routes those calls to `grilling` + the `grill-with-adr` ADR format (owner decision 2026-09-24).
- **`prototype`**: no rough-artifact skill is vendored; the NA block says what to do instead.
