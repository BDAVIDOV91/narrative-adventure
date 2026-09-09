# Docs

| Where           | What                                                                                                                                                                                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adr/`          | Architecture decisions, numbered and dated. One decision per file. Records the constraint that forced the choice, so a future reader does not relitigate it without the context.                                                                                  |
| `architecture/` | How the pieces fit: the data flow from Python to the browser, the level lifecycle.                                                                                                                                                                                |
| `design/`       | Game design notes — puzzle types, level progression, the story spine.                                                                                                                                                                                             |
| `handoffs/`     | Session handoffs, one file per session, named `YYYY-MM-DD-session-handoff.md`. The newest is what a fresh session reads first: state, settled decisions that must not be re-asked, and what is left over.                                                         |
| `security/`     | Audits of the **development harness** — hooks, settings, MCP servers, agent definitions — as distinct from the shipped game, which `privacy-guard` and `security-audit` cover. Records which scanner findings were rejected, and why, so they are not re-triaged. |
| `sources.md`    | **Every astronomy and folklore claim the game makes, with its source.** The `astronomy-report` skill checks content against this file.                                                                                                                            |

## Keeping this directory readable

Adopted 2026-09-09, after surveying a sibling repo whose `docs/reviews/` reached
110 files and could no longer be understood by listing it. The fixes are cheap on
day one and expensive at file sixty, so they start now.

- **Every handoff opens by saying what it is and what it supersedes.** The first
  lines name the archive it replaces, with that file's path, so a fresh session
  can price the decision to open it: _"Read this first. This is the brief; that is
  the archive."_
- **A handoff also carries a stop-list** — a section naming what has already been
  verified and must **not** be re-run. That is the part that actually buys context
  back.
- **Superseded documents are banner-closed in place, never silently deleted.** A
  banner at the top saying it is closed, what replaced it, and that the body is
  kept as the record. The movement stays visible; the stale content stops being
  mistaken for current.
- **The newest file is not automatically the governing one.** Follow the
  supersedes chain a handoff names, not the modification date.
- **Finished work moves to `docs/archive/`** so the top level stays scannable.
  Create that directory lazily — when the first document actually needs to move.

Agent research memory lives outside this tree, at
`.claude/agent-memory/<agent>/MEMORY.md`. That file is an **index of pointers,
never content**: a returning agent loads two lines and pulls only the topic file
it needs. It exists so an expensive research pass is not paid for twice.

## The rule that matters most here

`sources.md` is not optional documentation. This is an education game for
children: a claim that ships without a source is a claim nobody has checked, and
wrong astronomy taught to an 11-year-old is the most severe defect this project
can produce. Add the claim and its source _before_ the content that uses it.
