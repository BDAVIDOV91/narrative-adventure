## Development practices

Adopted from the mentor's `development-practices.md` on 2026-09-24, keeping only what CLAUDE.md, the skills and the
tooling did not already enforce. Aimed at the failure the owner named: re-fixing something fixed weeks ago.

### Before re-fixing anything

- **Check recent changes first.** `git log -p -- <file>` and the latest `docs/handoffs/` latent-bugs list. If the same
  area was fixed before, find that fix and its regression test before writing a new one. A regression test that exists
  and still passes means the new bug is a different bug. Say so.
- **3+ failed fixes on one bug = an architectural problem.** Stop fixing. Question the pattern, and raise it with the
  owner through `AskUserQuestion` (CLAUDE.md rule 4). Two failed fixes is already a red flag.
- No fix without the root cause: reproduce it, trace the data flow, and form one falsifiable hypothesis. Change one
  variable at a time.

### Before changing a function

- **Find every caller** (Grep, or LSP find-references) before changing a signature, a JSON shape or a content key, and
  update all of them in the same change. Content keys resolve through `src/shared/content.ts`. Level data resolves
  through `dataRef`.

### File size

- **New files stay at or under 300 lines, and 500 is the hard limit**: stop and split. Test files are exempt.
  `data/scripts/star-catalogue.py` (500 lines, written before this rule) is grandfathered. Do not grow it.
