# Docs

| Where           | What                                                                                                                                                                             |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adr/`          | Architecture decisions, numbered and dated. One decision per file. Records the constraint that forced the choice, so a future reader does not relitigate it without the context. |
| `architecture/` | How the pieces fit: the data flow from Python to the browser, the level lifecycle.                                                                                               |
| `design/`       | Game design notes — puzzle types, level progression, the story spine.                                                                                                            |
| `handoffs/`     | Session handoffs, one file per session, named `YYYY-MM-DD-session-handoff.md`. The newest is what a fresh session reads first: state, settled decisions that must not be re-asked, and what is left over. |
| `sources.md`    | **Every astronomy and folklore claim the game makes, with its source.** The `astronomy-report` skill checks content against this file.                                           |

## The rule that matters most here

`sources.md` is not optional documentation. This is an education game for
children: a claim that ships without a source is a claim nobody has checked, and
wrong astronomy taught to an 11-year-old is the most severe defect this project
can produce. Add the claim and its source _before_ the content that uses it.
