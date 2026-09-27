# Session handoff — 2026-09-27

## Where things stand

Both wayfinder maps are **finished**:

- [road-to-v1](../wayfinder/road-to-v1/MAP.md) decided **what** v1 is: [`docs/design/v1-spec.md`](../design/v1-spec.md).
- [v1-build](../wayfinder/v1-build/MAP.md) decided **in what order** it is built:
  [`docs/design/v1-build-spec.md`](../design/v1-build-spec.md). Tickets 001–008 are closed, and no fog is left.

No game code changed today. `development` holds the v1-build tickets 002–008 as docs commits. `main` still holds only the
scaffold.

## The exact next step

Plan mode on **E0 Prune**, the first phase of `v1-build-spec.md` §4, then two `challenger`s. Record the start SHA at
entry. One phase per session, strictly serial.

## Settled — do not re-ask

- Every closed ticket in both maps, v1-spec.md, and v1-build-spec.md. If the build spec and a ticket disagree, the
  ticket wins and the spec has a bug.
- Ticket 008's own decisions: E5 is the first `orbital-positions.json` reader and takes that perf gate. A self-hosted
  font with Bulgarian glyph forms lands in grid + ribbon; this was re-asked after `qa-report` turned out to have no
  letter-shape check. The unplaced §6 items go to their first needer.
- The M2 offload phase sits between E0 and E1 and blocks E1 entry. Its exit and E1's entry need the M2 online.

## Owner items

- Push `development`. It is ahead with ticket 007's commit, `bfd2678`, and this session's ticket 008 commit.
- Before merge 1 (E4): GitHub Settings → General → Pull Requests → merge-commit default message "Pull request title".
- Before the M2 offload phase exits: the M2 online (it was offline on 2026-09-27), with Tailscale, the ssh alias,
  Mutagen and the bootstrap.

## Left over

- Latent bugs 4, 5, 7, 8 and 10 (09-09 handoff) are still open. They are scheduled in E1 (4, 5), E2 (7, 8) and
  E5 (10).
- `v1-build-spec.md` is about 430 lines. That is over `.claude/rules/development-practices.md`'s 300-line new-file
  rule, which reads as a source-code rule, and under its 500-line hard limit. `v1-spec.md` (352 lines) sets the
  precedent.
- README still says "the seven reusable puzzle types" (`README.md:69`). E0's prune fixes it.
