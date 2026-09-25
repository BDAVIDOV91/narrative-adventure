# Issue tracker for wayfinder: local Markdown

Adapted from upstream `skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md` (MIT), "Wayfinding
operations". The layout is NOT upstream's `.scratch/` layout. It is the one the read-only wayfinder viewer parses
(`ops/wayfinder-viewer/`), so a file that breaks a rule below is silently misread, not rejected.

## Layout

```
docs/wayfinder/<slug>/
  MAP.md                  the map
  tickets/NNN-slug.md     one file per ticket
  research/NNN-slug.md    findings backing a research ticket (optional)
```

- `<slug>` matches `^[A-Za-z0-9][A-Za-z0-9._-]*$`. A directory is a map only if it sits directly under
  `docs/wayfinder/` and holds a `MAP.md`.
- Any other top-level `.md` in the map directory is shown as an extra document. Put nothing else there.
- Maps are committed. No data about any child, no personal data, credentials or secret values, anywhere.

## MAP.md

```markdown
# <Map title>

<!-- wayfinder:map -->

## Destination
## Notes
## Decisions so far
## Not yet specified
## Out of scope
```

- The title is the first `# ` heading. Keep the marker line; the viewer does not read it, people do.
- The five `## ` names are exact, including case. A renamed section is lost.
- **Decisions so far:** one bullet per closed ticket, `- [<ticket title>](tickets/NNN-slug.md) — <one-line gist>`.
- **Not yet specified (fog):** one top-level bullet per patch. The patch title is the leading bold run, or the text
  before ` — `. Nested bullets and continuation lines belong to the patch above them. Prose placed before the first
  bullet counts as one live patch, so write none.
- **Graduating a patch:** do not delete it. Strike the title, and the strike must START the bullet:
  `- ~~**Title**~~ — graduated to ticket 007`. `- **~~Title~~**` is NOT read as cleared and the map looks stalled.

## Tickets

```markdown
---
id: "007"
title: Which level comes after the Moon
type: grilling
status: open
assignee: ""
blocked_by: ["001", "004"]
---

## Question

<the decision or investigation this ticket resolves>
```

- `id`: a quoted string, zero-padded to three digits, equal to the file name's `NNN`. Numbered from `"001"`.
- `type`: exactly one of `research`, `prototype`, `grilling`, `task`. Nothing else, no quotes, no punctuation. The
  viewer puts this value into the page unescaped.
- `status`: `open` or `closed`. Only the literal `closed` closes a ticket; every other value reads as open.
- `blocked_by`: a list of quoted ids, `[]` when empty. Each id must match an existing ticket's `id` exactly. An
  unknown or unpadded id (`"7"`, `7`) keeps the ticket blocked forever, and nothing warns you.
- `title`: unquoted; apostrophes are fine.

## Wayfinding operations

- **Create the map:** write `MAP.md` as above.
- **Create tickets:** first write every file with `blocked_by: []`, then wire `blocked_by` in a second pass, once the
  ids exist.
- **Frontier:** tickets that are `open`, have an empty `assignee`, and whose every `blocked_by` id is `closed`. The
  lowest id wins.
- **Claim:** set `assignee: owner` (or the name of the person driving the map) and save, before any other work.
- **Resolve:** append the answer under a `## Resolution` heading, set `status: closed`, then append the context pointer
  to the map's **Decisions so far**.
- **Rule out of scope:** set `status: closed`, add `## Resolution` saying why, and add one bullet to the map's
  **Out of scope**. Do not add it to **Decisions so far**.
- **Research findings:** `research/NNN-slug.md`, same `NNN` as its ticket, with this frontmatter:

  ```yaml
  ---
  ticket: "007"
  title: Which moons count as major for v1
  status: done
  ---
  ```

  The ticket's `## Resolution` links to it.

## Check after every write

Do not trust the viewer's UI to show a broken ticket. Check the files, or the JSON when the viewer is running
(`npm run wayfinder`):

```bash
# every blocked_by id must be some ticket's id
grep -h '^id:\|^blocked_by:' docs/wayfinder/<slug>/tickets/*.md
# every tickets[].blockedBy id must equal some tickets[].id
curl -s http://127.0.0.1:<port>/api/map/<slug>
```

In that JSON each ticket carries a derived `state`: `closed`, `claimed`, `frontier` or `blocked`. A ticket that stays
`blocked` while all its real blockers are closed has a bad id in `blocked_by`.
