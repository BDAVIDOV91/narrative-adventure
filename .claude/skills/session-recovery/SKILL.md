---
name: session-recovery
description: Use at the start of a session, after a compaction, or whenever you have lost the thread — reconstructs durable project state by reconciling the docs against live reality (git, the test suites, the running game) instead of trusting either alone.
---

# Session recovery

## The failure this exists to prevent

**A stale note is indistinguishable from a current one.** A handoff says a task is
blocked; the thing that blocked it was resolved two commits later and nobody went
back to edit the line. A fresh session reads the handoff, believes it, and either
re-does finished work or refuses to start unblocked work.

Docs record **intent at the time of writing**. Only git, the test suites and the
game actually running record **what is true now**. Recovery means reconciling the
two and reporting the **disagreements** — those are the whole point. A recovery
that just summarises the newest handoff has done nothing.

## Evidence table — what actually proves a claim

| Claim in a doc | What actually proves it |
| --- | --- |
| "fixed" | the commit exists in `git log`, **and its regression test exists in the suite** — rule 5 means a fix without a test is not a fix |
| "tests pass" | you ran them and can **quote the summary line** with counts. Never paraphrase |
| "verified" | say **which**: *test-verified* (suite green) or *played-verified* (a level actually completed in a browser). Never conflate them — for a children's game they are as different as staging and production |
| "the data says X" | a value read out of `data/generated/*.json` in this checkout, not remembered |
| "sourced" | the entry exists in `docs/sources.md` **and its status is VERIFIED** — NEEDS SOURCE and DISPUTED must not ship |
| "committed" | `git log` shows it. "Ready to commit" and "committed" are different states |
| "pushed" | irrelevant — **Claude never pushes.** If a doc says Claude pushed, the doc is wrong |
| "blocked by X" | check whether X is still true before repeating it |

## Constraints that survive every compaction

Restate these in every recovery summary, because a fresh context will not have
them and they are the rules most expensive to violate:

1. **Scientific accuracy is severity-critical.** Numbers come from
   `data/generated/` or a cited source, never from memory. A NEEDS SOURCE or
   DISPUTED claim must not ship.
2. **Hide the math.** No equations, numbers, units or formulas reach the player.
3. **Bulgarian only, nothing hardcoded.** Player-facing strings live in
   `content/bg/*.json`, reached through `src/shared/content.ts`. Keys ASCII,
   values Cyrillic.
4. **Interview mode.** Questions and flags go through `AskUserQuestion` the moment
   they are found, not banked for a summary.
5. **RED/GREEN per fix.** No fix ships without a test that failed on the old code.
6. **Never push.** Commit, then say it is ready.
7. **Zero network requests, nothing collected about a child.**
8. **Hardware:** 4 cores, ~1.9 GB free, integrated AMD APU. Check RAM before any
   3D or graphics-heavy run.

## Procedure

1. **Read the newest handoff in `docs/handoffs/` — but check the supersedes
   chain.** The newest file by date is not always the governing one; a handoff
   normally names which doc it supersedes and which are closed. Follow that chain
   rather than sorting by modification time.
2. **Reconcile against git.** `git log --oneline -15`, `git status`. Does the
   handoff's claimed state match the tree? Is anything uncommitted that the
   handoff thinks landed?
3. **Reconcile against the suites.** `venv/bin/python -m pytest` and `npm test`.
   Quote the counts. If a doc claims a test exists, grep for it.
4. **Reconcile against the data.** If a decision rests on a generated value, read
   it out of `data/generated/` rather than trusting the prose.
5. **Report the disagreements first**, then the state. A recovery whose output is
   "everything matches" is only credible if it says what was checked.

## What NOT to do

- Do **not** open a full test run "just to see where we are" before reading
  `git log` and the newest handoff. Run the suite when you have a reason.
- Do **not** re-derive a decision the handoff marks SETTLED. If you think a
  settled decision is wrong, raise it through `AskUserQuestion` — do not quietly
  re-open it.
- Do **not** re-run anything the handoff lists under a "do not re-run" stop-list
  without saying why the old evidence is no longer good.
- Do **not** trust a subagent's report as a result. It is a **claim**; verify the
  parts you are about to build on.
