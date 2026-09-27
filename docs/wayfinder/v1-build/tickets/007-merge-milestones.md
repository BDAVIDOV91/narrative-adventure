---
id: "007"
title: Milestones for merging development into main
type: grilling
status: closed
assignee: owner
blocked_by: ["006"]
---

## Question

Which phase exits are milestones where `development` merges into `main`, each after a `qa-report` pass? `main` is
merge-only, and `development` is 55 commits ahead at charting. The owner performs every push and merge (CLAUDE.md
rule 7).

- Is there a first merge soon, of the road-to-v1 docs plus the prune, or only once Earth is playable?
- One merge per completed level, or fewer?
- The final merge at the finish bar.

Ticket 006 adds: every milestone picked here carries a `qa-report` run and the owner's play-through (the M2 is allowed
for play); the back cover is always one.

## Resolution

Grilled with the owner on 2026-09-27 in two rounds, then challenged by two `challenger`s (both revise). Six challenger
findings went back to the owner, and the rest were fact fixes. Every answer took the recommended option.

Facts checked first:

- `main` holds only the scaffold (`c0f9080`). `development` was 62 commits ahead and 0 behind at resolution. The repo
  has no tags.
- `.husky/pre-push:5-8` blocks a push while on `main`. `.claude/hooks/block-dangerous-git.sh` blocks Claude's
  `gh pr create`, so the owner opens and merges every PR (rule 7).
- `qa-report` checks "A level completes" (`.claude/skills/qa-report/SKILL.md:50`). E4 is the first exit that can pass
  that check (ticket 001). `data/ephemeris/de440s.bsp` is present on M1, so `qa-report` step 2 runs at E4 without the
  M2.
- `qa-report` has no README check. Its frame-rate item means "on this APU" (`SKILL.md:54`).
- A GitHub "Create a merge commit" writes the subject `Merge pull request #N …` by default, with the PR title in the
  body.

### Decisions

1. **The first merge is at E4's exit**, "Earth completable". It is the first state that can pass `qa-report` in full.
   Nothing merges before it: the planning docs and the prune wait.
2. **Milestones are E4, every level exit whose criteria include "playable", and the back cover.** That makes seven
   merges (table below). Ticket 001's "Milestone exit" labels, E3 included, name phase exits, not merge points.
3. **A failed milestone `qa-report` blocks the next phase's entry.**
   - Fixes land RED/GREEN on `development`, and `qa-report` re-runs.
   - **Merge window:** after a pass, no commit lands on `development` until the owner has pushed it and opened the
     milestone PR. The PR head is the approved SHA. The merge itself may come later.
   - **Stuck finding:** a finding still failing after the third fix goes to the owner through `AskUserQuestion`
     (`.claude/rules/development-practices.md`). Only the owner may waive it, and the waiver is written into the phase
     exit report and the PR body.
4. **Every PR is `development` → `main` with "Create a merge commit"**, never squash or rebase.
   - `development` stays an ancestor of `main`, so each PR's merge base is the previous milestone and it merges
     cleanly.
   - After each merge, `main` is one merge commit ahead of `development`. That is expected, not a defect to fix.
5. **Merge subject.** No git tags; the merge commit subject is the milestone marker.
   - **One-time owner step:** in GitHub Settings → General → Pull Requests, set the merge-commit default message to
     "Pull request title".
   - Milestone PR titles are Conventional, e.g. `chore(release): Earth is completable (E4)`.
6. **README cadence** (clears the map's fog patch):
   - README.md is updated at every milestone exit, before `qa-report` runs.
   - It is also updated at any phase exit that adds or changes a command or a setup step: the M2 offload phase, E1, and
     any phase whose plan flags one.
   - `qa-report`'s SKILL.md gains a manual check at E4: "README reflects this milestone's commands, setup and changes".
     It is re-checked after any fix that changes a command, before `qa-report` re-runs.
7. **Frame rate on M1.** A milestone play may run on the M2 (ticket 006 decision 7), but `qa-report`'s frame-rate item
   is always played on M1, after `free -h`. M1 is the rule-9 target.
8. **Release-time re-checks gate the back-cover merge** (clears the map's fog patch), inside its `qa-report`:
   - re-run the monthly Saturn ring-opening table behind `docs/sources.md` "Through a small telescope" (road-to-v1 010,
     011);
   - re-read every VERIFIED claim whose source page may have moved.

### The milestones

| Merge | Phase exit | PR title (example)                                   | Gates beyond the phase's own exit                                                   |
| ----- | ---------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 1     | E4         | `chore(release): Earth is completable (E4)`          | README; `qa-report` (no placeholder print yet) + owner play; frame rate on M1         |
| 2     | E7         | `chore(release): Earth is playable (E7)`             | README; `qa-report` with the placeholder print + owner play; frame rate on M1         |
| 3     | Moon B     | `chore(release): the Moon is playable`               | as merge 2; the merge also carries the shell and grid + ribbon                        |
| 4     | Mars B     | `chore(release): Mars is playable`                   | as merge 2                                                                            |
| 5     | Jupiter B2 | `chore(release): Jupiter is playable`                | as merge 2                                                                            |
| 6     | Saturn B   | `chore(release): Saturn is playable`                 | as merge 2                                                                            |
| 7     | Back cover | `chore(release): v1 reaches the finish bar`          | as merge 2; the finish-bar checklist and sources sweep (ticket 006); release re-checks |

Every milestone also runs ticket 006's exit gates for its phase (the router, the M1 dev walk and the suite).

Handed on:

- **Ticket 008** folds in:
  - the seven milestones as exit criteria on their phases, with the README, `qa-report` and owner-play gates;
  - the README rule per phase, including M2 offload and E1;
  - the merge window, the failed-report block and the stuck-finding waiver, in the spec's phase-exit procedure;
  - the `qa-report` SKILL.md additions: the README check at E4, frame rate on M1 at E4, and the release re-checks at
    the back cover (alongside ticket 006's E1, E7 and back-cover updates);
  - the one-time GitHub merge-message setting, as an owner checklist item before merge 1.
