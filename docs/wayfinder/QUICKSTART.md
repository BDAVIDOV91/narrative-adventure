# Wayfinder quickstart: copy-paste triggers (owner)

Blocks marked **terminal** go into a shell. Blocks marked **Claude** go into a Claude Code session.
How the skill works: `.claude/skills/wayfinder/SKILL.md`. File format: `.claude/skills/wayfinder/TRACKER.md`.
Viewer details: `ops/wayfinder-viewer/README.md`.

## When to use it, and how Claude guides you

One question decides it: **are the open items decisions that depend on each other, and too many for one sitting?**

| Work | Wayfinder? | Why |
|---|---|---|
| The road from here to a finished v1 | yes (`road-to-v1`) | big, the level roster is open, and the decisions feed each other |
| A new level's design, once the roster is decided | maybe | yes if its beats and types are five or more linked open decisions |
| One puzzle engine from a settled design | no | plan mode plus two challengers covers it |
| A bug | no | test first, then fix (CLAUDE.md rule 5) |
| One doc, one script, one asset | no | just do it |

- **At session start**, while a map has open work, the hook `.claude/hooks/wayfinder-frontier.sh` prints what is
  takeable and the exact line to type. It also warns about a ticket blocked by an id that does not exist, which the
  viewer never shows. It is silent when there is no map or the map is finished.
- **In plan mode**, Claude asks whether the work should be a map when the plan cannot fit one session or carries five
  or more linked open decisions. It runs only if you say yes and type `/wayfinder`.
- **Unsure?** Paste this:

```
Should this be a wayfinder map, or plain plan mode? Give me the reason.
```

## 1. Start a fresh session (terminal)

```bash
cd ~/narrative-adventure && claude
```

## 2. Check the skill is there (Claude)

Type `/way` and confirm `/wayfinder` appears in the menu. It never appears in Claude's own skill list; that is by design
(`disable-model-invocation: true`).

## 3. Create the map (Claude, once)

```
/wayfinder Road to a finished v1 of Звездната книга. Destination: a shippable, genuinely finished v1 within CLAUDE.md rule 6 (Sun, planets, major moons). Fixed inputs, NOT tickets: Earth's ten beats and grilling rounds 1–4 (docs/handoffs/2026-09-09-session-handoff.md), the seven-type set with its ADR 0006 deletion trigger at the Mars build, and the rule 1/2/8 walls. Decide with me: the level roster after Earth (Moon is guided; a Mars scene exists), which existing types each later level reuses, and what remains fog. Out of scope: interstellar, the continent picker, English, new folklore (#21 parked). Phase-2 task #3 is build work, not a ticket. Slug: road-to-v1.
```

What follows:
- a grilling to name the destination;
- a breadth-first grilling for the open decisions;
- `MAP.md` and the first tickets are written.

Claude asks ONCE before it fires research sub-agents, then stops. Charting resolves nothing. Typing `/wayfinder`
approves the nested `grilling` calls for that session, and nothing else.

## 4. Open the viewer (second terminal)

```bash
cd ~/narrative-adventure && npm run wayfinder
```

```bash
xdg-open http://127.0.0.1:7777
```

- If the port was busy, use the URL the first command prints. Stop with Ctrl-C.
- The bright green border marks a ticket that is takeable now. The page re-reads the files every 4 seconds.
- "Open in Claude Code" and the other launch buttons answer "The wayfinder viewer is read-only". That is intended.

## 5. Every later session: resolve ONE ticket (Claude)

The next takeable ticket:

```
/wayfinder docs/wayfinder/road-to-v1/MAP.md
```

A specific ticket (replace the file name):

```
/wayfinder docs/wayfinder/road-to-v1/MAP.md tickets/003-REPLACE-ME.md
```

The frontier without the viewer:

```
Show me the frontier of docs/wayfinder/road-to-v1 as a table: id, title, type, blocked_by.
```

| Ticket type | Who works | Your part |
|---|---|---|
| `grilling` (the default) | you and Claude | answer the questions; Claude never answers for you |
| `research` | a sub-agent alone | approve the batch once, then read `research/NNN-slug.md`; astronomy claims land in `docs/sources.md` |
| `prototype` | you and Claude | react to a rough artifact; Claude asks before making one |
| `task` | Claude, or you with a checklist | anything needing your hands (a push, a play-through, a download) comes to you |

## 6. After 3–5 closed tickets (Claude)

```
Run the wayfinder pilot exit interview: keep, widen or drop. Show what the pilot produced first.
```

## 7. When the map is finished (Claude, plan mode)

A map is finished when every ticket is closed AND "Not yet specified" has no live patch. Closed tickets with fog left
means the map has stalled: the next session turns the fog into tickets or rules it out of scope.

```
The road-to-v1 map is clear. Start plan mode and hand off: ordered build slices per level, no decisions reopened.
```

The map decides; plan mode with two challengers builds.

## Rules

- One interactive session at a time (the RAM budget). Only research sub-agents run in parallel.
- No data about any child, no personal data, no credentials in a map, a ticket or a research file.
- A bug found on the way follows rule 5 and goes on the handoff's latent-bugs list, not into a ticket.
- Hand-editing a ticket: ids are quoted and three digits (`"007"`), and `blocked_by: ["001"]` must match a real ticket
  exactly. A wrong id keeps the ticket blocked forever, with no warning.

## If something looks wrong

| Symptom | Cause |
|---|---|
| The map is missing in the viewer | it needs `MAP.md` directly under `docs/wayfinder/<slug>/` |
| A ticket stays blocked though its blockers are closed | a bad id in `blocked_by` |
| `wayfinder-view` says the viewer is missing | reinstall: `ops/wayfinder-viewer/README.md` |
| A map looks stalled at 100 % | a graduated fog patch whose strike does not START the bullet: `- ~~**Title**~~ — …` |

Health checks (terminal):

```bash
cd ~/narrative-adventure && npm run test:ops
```

```bash
cd ~/narrative-adventure && bash .claude/hooks/test-wayfinder-frontier.sh | tail -1
```

Pass the test FILE: `node --test <directory>` runs zero tests.
