---
name: grill-with-adr
description: A relentless interview that also writes the decisions down. Use when grilling a choice that future readers will otherwise relitigate — a stack change, a scope boundary, a puzzle mechanic the whole level hangs on.
disable-model-invocation: true
---

Run the `grilling` skill to work the design tree to an empty frontier.

Then capture what was settled, so the reasoning survives the conversation.

## Write the ADR

Create `docs/adr/NNNN-<kebab-slug>.md`, numbering from the highest existing file. Follow the
shape the existing ADRs use:

```markdown
# NNNN — <the decision, as a sentence>

- **Status**: accepted
- **Date**: YYYY-MM-DD

## Context
<the situation that forced a choice — what pulled in opposite directions>

## Decision
<what was decided, plainly>

## Why
<the reasoning from the interview, including the options rejected and what would
have made them win>

## Consequences
<what this now commits the project to, and what it makes harder>

## When to revisit
<the concrete signal that should reopen this>
```

The **Why** and **When to revisit** sections are the point. A decision recorded without its
reasoning gets reversed by the next reader who does not know what it cost.

## Also update, when the interview touched them

- `docs/sources.md` — any astronomy or folklore claim the design now depends on, with its
  status. A claim the design assumes but nobody has sourced is the most expensive kind of
  silent assumption in this project.
- `schemas/level-data.schema.json` — if a puzzle type or level field was added.
- `CLAUDE.md` — only if a standing rule changed. Rules are expensive; do not add one for a
  single decision an ADR already covers.

Record only what was actually settled. An open question written as a decision is worse than
no ADR, because it looks answered.
