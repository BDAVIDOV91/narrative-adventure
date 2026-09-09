# Session handoff — 2026-09-08

Astronomy education game for Bulgarian children (~11–12). Browser, Phaser 3 +
TypeScript, a little Three.js, Python build-time only. Repo:
`/home/technojihad/narrative-adventure`, branch `development`.

**Resume point: grilling round 2. The design is half-settled and the answers so
far are recorded below — do not re-ask them.**

## State

**Nothing unpushed.** The owner has pushed; `origin/development` is at
`c09a930`, level with local. Claude never pushes; the owner does. Enforced by
`.claude/hooks/block-dangerous-git.sh`. The five commits below are now on the
remote and are listed only so a fresh session knows what landed.

```
c09a930 feat(data): stars come from a catalogue that checks itself against a second source
61884a4 docs: folklore earns its place only when it carries the astronomy
4f40aa9 feat(types): pyright makes Python hold the same bar as TypeScript
1c80faf fix(ephemeris): Earth carries its distance to the Sun, not a row of zeros
91f1b15 chore(toolchain): venv/ replaces .venv/, and the pre-commit hook stops lying
```

The Bulgarian figure resolver (`data/scripts/bulgarian-figures.py` and
`tests/test_bulgarian_figures.py`) survived a machine freeze uncommitted and is
now committed — task #22 is closed.

49 tests pass. `npm run validate`, pyright 0 errors, black, flake8, level
validation and both hook suites all clean as of the freeze.

## The pivot that matters

The owner called it out directly: `src/` is **469 lines** and all five puzzle
directories are empty `.gitkeep` files, while the data pipeline is ~1,000 lines
with 49 tests. **Infrastructure is ahead of design and must stop until the
concept is settled.** Do not build more pipeline.

## Grilling round 1 — SETTLED, do not re-ask

1. **Finish Earth completely first** — not a puzzle-type slice, not a greybox of
   all five. The brief's test is "genuinely finished, not infinite scope creep",
   and a complete Earth is the only artifact that proves we can finish anything.
2. **Difficulty axes**: scaffolding removal (the companion says less each level),
   element count (`config.targets` already exists), and distractors/ambiguity
   where the wrong answers are the real misconceptions. **Tolerance tightening
   was explicitly rejected** — it makes the child's hand the obstacle rather than
   their understanding.
3. **The dimming-star mystery is flavour only and never blocks.** The 0.7 open
   gate exists so a child who skips a puzzle keeps playing; a mystery gate would
   undo that.
4. **`connect-the-dots` is the constellation puzzle** — the owner's own framing:
   join stars into a real constellation, attach interesting facts about it,
   scale from simpler to harder by star count, and **make it dynamic by season
   and by the child's location**. This replaced the assumption that it was the
   Зорница puzzle.

## Round 2 frontier — ask these next

- **Where the "dynamic sky" comes from.** Recommendation: precompute per
  constellation which months it is well-placed after dark from ~42–44° N into a
  small committed table (task #25), so the runtime reads the device month and
  picks from the table. No runtime trig, no amendment to ADR 0001, and derivable
  entirely from the already-committed `data/generated/stars.json`.
- **Location, and it is a rule collision.** Season is free (device clock, no
  network, nothing collected). Location **cannot** use the geolocation API —
  rule 8 is zero collection about a child, and under GDPR children's location is
  the heaviest category. Legal options: a fixed Bulgarian latitude, or a city
  picker kept in `localStorage`. This is the owner's call.
- **The companion's voice budget** — unblocked by round 1's answer, since
  scaffolding removal is the difficulty axis, which makes the companion _be_ the
  scaffolding.
- **Where the Зорница/Вечерница beat now lives**, since connect-the-dots is
  taken. `orbital-positions.json#/venus` is already committed and holds the real
  motion; `trajectory-match` is the natural home.

## Restart this

The `astronomy-accuracy-checker` researching **Бонов's Ралица/Колата star
mapping** died in the freeze. It matters more now than when it was launched,
because the constellation puzzle is exactly where Ралица and Колата appear.
It was asked for: the citation (author, title, edition, page — likely Ангел
Бонов, _Митове и легенди за съзвездията_, but verify); whether χ really belongs
to the рало given χ¹/χ² sit ~2h of RA from the Belt past Betelgeuse; whether θ/χ
resolve to specific components; the narrow-vs-wide variant tension (Бонов's own
mapping includes Сириус and Процион, which is the _wide_ variant, while the game
tells the narrow one); any competing Вакарелски/Ковачев mapping; and whether
"вълк" for η UMa is really attested.

## Task list

| #   | Status          |                                                                       |
| --- | --------------- | --------------------------------------------------------------------- |
| 20  | pending         | Galilean moon periods from JPL — the last NEEDS SOURCE, non-blocking  |
| 21  | in progress     | Ралица/Колата figures — blocked on the Бонов citation                 |
| 22  | DONE            | Commit the figure resolver                                            |
| 23  | **in progress** | Settle the scenario + puzzle-scaling design (grilling)                |
| 24  | blocked by 23   | Build Earth end to end and playable                                   |
| 25  | pending         | Precompute constellation visibility by month                          |
| 26  | DONE            | Research game-building skills + the owner's shortlist (results below) |
| 27  | blocked by 24   | Playwright browser QA for the Earth level                             |

## Earth as currently drafted

`src/scenes/earth/earth-data.json` has three markers: sundial (`rotate-match`,
4 targets, tolerance 12), tilting globe (`rotate-match`, 2 targets, tolerance 8),
and twilight Зорница (`connect-the-dots`, `dataRef` to venus). Round 1 changed
what connect-the-dots is for, so **the third marker needs rework**. The scene
stub loads markers and a marker click currently just `console.warn`s which puzzle
it would open.

## Commands

```bash
npm run dev            # http://localhost:5173
npm run validate       # tsc + eslint + prettier
venv/bin/python -m pytest
venv/bin/python data/scripts/star-catalogue.py         # stars, figures, names
venv/bin/python data/scripts/orbital-positions.py      # ephemeris
venv/bin/python data/scripts/validate-levels.py
sh .husky/test-pre-commit-scope.sh
sh .claude/hooks/test-block-dangerous-git.sh
```

Python env is `venv/` (not `.venv/`), seeded with pip, driven by `uv`.

## Standing rules that bite (full set in CLAUDE.md)

1. **Scientific accuracy is severity-critical.** NEEDS SOURCE or DISPUTED must
   not ship. Numbers come from `data/generated/` or a cited source, never memory.
   Folklore earns its place only when learning it and learning the astronomy are
   the same act (ADR 0005).
2. **Hide the math.** No equations, numbers, units or formulas reach the player.
3. **Bulgarian only, nothing hardcoded.** Strings resolve through
   `src/shared/content.ts` to `content/bg/*.json`. Keys ASCII, values Cyrillic.
4. **Interview mode, not prose.** Every question or flag goes through
   `AskUserQuestion` the moment it is found. `grilling` for multi-branch designs.
5. **PER FIX RED/GREEN.** No fix ships without a regression test that failed on
   the old code.
6. Solar system only for v1.
7. **Never push.** Commit, then say it is ready.
8. **Zero network requests, collects nothing about a child.**
9. Hardware: 4 cores, ~1.9 GB free, integrated AMD APU.

## Star catalogue — done, do not redo

Resolved the blocking NEEDS SOURCE. **HYG v4.4** (CC BY-SA 4.0, Codeberg — the
GitHub repo is archived with NOASSERTION) filtered to 2,851 stars at mag ≤ 5.5,
plus Stellarium `modern_iau`'s 88 figures as HIP polylines, plus 2,106
designations. Downloads and commands are in `docs/sources.md`; `data/raw/` is
gitignored.

**The IAU/WGSN Naked Eye Catalog was rejected as corrupt** — 15 stars with wrong
RA, including **Mizar off by 3.2°**, the zoom-split-star target. It passes every
bounds check. The generator therefore verifies every position against
Hipparcos-2 at build time and fails over 30″, excluding four known
high-proper-motion stars. Two guards: Stellarium's `modern` mixes Gaia DR3
source_ids into HIP arrays, and HIP 55203 (ξ UMa, inside the Ursa Major figure)
does not exist in Hipparcos and needs the HR/HD fallback.

Corrected against Hipparcos I/239: Alioth/Dubhe **1.76/1.81** (margin 0.05, not
0.02), Alcor **3.99**, Mizar A/B **14.40″**, Rigel/Alnitak/Mintaka
**0.18/1.74/2.25**. Mizar–Alcor recomputed independently: **708.6″ = 11.81′**.
Pleiades naked-eye count reproduced from catalogue data: **6 at V ≤ 5.0, 7 with
Pleione at 5.05** — Квачката's folk number is the naked-eye limit.

## Earlier research — do not redo

**Orion's Belt**: the brief is exactly inverted. Alnilam is brightest AND the
only single star; Mintaka is faintest with five components. Oplištilová et al.,
A&A 704, A204 (2025).

**Mizar/Alcor is the zoom-split-star target**, not a belt star — Ursa Major is
circumpolar from Bulgaria, Orion is winter-only.

**Albireo is DISPUTED — do not use.** **Alioth is brightest in UMa but must not
become a player task** — the margin is invisible.

**Both folklore claims in the brief were wrong.** "кум" is the godfather, not
the groom. Кумова слама was cut. **NOT ATTESTED, never re-propose**: "Косери"
for Orion, "Стожер" for the Pole Star.

**Confirmed folklore**: Квачката (Pleiades), Лъжи керван (Sirius), Ралица
(Orion) and Колата (Ursa Major), the last two citable to Вакарелски 1977 p. 413
for the _names_ — the star-by-star mapping is what is still unsourced.

## Known wart

`4f40aa9` (pyright) also contains the `sources.md` and `facts.json` rewrites;
its message covers only type-checking. Documented in the following commit rather
than rewriting history. Not worth fixing.

## Skills research — THE BRIEF (done 2026-09-08; results at the end of this file)

Owner asked for **one fast research pass** on whether these are worth adopting
for this project, and explicitly said to let it sit until the usage reset:

- **Taste** (skill)
- **Impeccable**
- **Playwright CLI** — already installed; question is whether we actually use it
  (browser-driven QA of the Phaser scenes, screenshot regressions)
- **Awesome Design**
- **img2threejs**

Judge each against the constraints that actually bind here, not on general
merit: rule 8 (zero network requests, nothing collected), rule 3 (Bulgarian
only, no baked-in text — img2threejs output must be textless), the hardware
budget (single-object Three.js, 2048px WebP cap), and ADR 0001 (build-time only,
nothing in the runtime path). A dev-time-only tool is much easier to justify
than anything that ships.

**Done — findings are in the `## Skills research — RESULTS` section below.**

### The widened half of the brief: what else exists for building a browser game

The five above are the owner's shortlist, not the scope. The same research pass
should go looking for **skills, plugins and agents we do not yet know about**
that cover the parts of this game we have barely started — `src/` is 469 lines
and all five puzzle directories are empty. Search the skill marketplaces and
plugin registries, not just what is already installed.

Cover the whole span, and report what exists per band:

- **Mechanics and logic** — Phaser 3 scene/state patterns, input handling
  (drag, rotate, snap-to-target), tween and timeline work, save/progress state.
  Our five puzzle types are all direct-manipulation, so anything that helps
  build drag-rotate-connect interactions counts.
- **UI/UX** — layout and flow for a child-facing touch UI, the storybook
  level-select, hit-target sizing for 11-year-olds, feedback and reward loops,
  accessibility. Must survive Bulgarian text running long (containers wrap and
  grow, never fixed-width).
- **Visuals** — 2D art generation and asset pipelines, sprite/atlas packing,
  texture compression, palette and style consistency across levels, and the
  narrow Three.js slice we allow.
- **QA** — scene-level browser testing and screenshot regressions, which is
  where the already-installed Playwright CLI may earn its place.

For each candidate: what it does, which band it covers, whether it is
build/dev-time or ships, and the same four constraints (rule 8, rule 3, hardware
budget, ADR 0001). **Rank by what unblocks the Earth level**, since that is the
next build and the thing that proves we can finish anything — a tool that only
pays off at level six is not interesting yet.

Expect most to be rejected. The useful output is a short list worth trying plus
an explicit note of what was looked at and dismissed, so it is not re-proposed.

---

## Trigger message for a fresh session

Paste this as the first message of the new session:

> Read `docs/handoffs/2026-09-08-session-handoff.md` — it is the full handoff for
> narrative-adventure. Do not re-ask anything marked SETTLED, do not build more
> data pipeline, and do not redo the skills research (it is done; results and
> verdicts are at the end of the file). Start with grilling round 2.

## What is left over

Two things, in the order they should happen. The skills research that used to
sit here is **done** — task #26, results at the end of this file. Its only
outcome for the queue is task #27 (Playwright QA), which is blocked by #24 and
therefore not yet actionable.

**1. Restart the Бонов research agent.** It died in a machine freeze with no
completion record. Brief is in the "Restart this" section above. It matters more
now than when it was launched, because round 1 made connect-the-dots the
constellation puzzle, which is exactly where Ралица and Колата appear. Launch it
first so it researches while the grilling runs.

**2. Grilling round 2** (task #23, the actual resume point). The frontier is in
the "Round 2 frontier" section: where the dynamic sky comes from, the
location/rule-8 collision, the companion's voice budget, and where the
Зорница/Вечерница beat now lives. The location question is a genuine rule
collision and is **the owner's call, not Claude's** — geolocation is barred by
rule 8, so the legal options are a fixed Bulgarian latitude or a `localStorage`
city picker.

Task #21 — authoring the actual Ралица/Колата figures — stays blocked until the
Бонов citation comes back. The resolver that will consume them is committed and
green; what is missing is the sourced star-by-star mapping, not the code.

Not on the critical path: task #20 (Galilean moon periods, the last NEEDS SOURCE,
non-blocking) and task #25 (visibility table, which only becomes real once round
2 settles how the dynamic sky works).

---

## Skills research — RESULTS (2026-09-08)

Star counts below come from the GitHub API, not from the aggregator sites. The
aggregators disagree wildly with each other and with reality (one lists
img2threejs at 85.3k, another at 4.2k; the real figure is 15.5k) — **do not cite
skillsllm.com, claudeskills.info, mcpmarket.com or similar as evidence.**

### The finding that governs all the others

Every popular design skill — Impeccable, Taste, the designer-skills collection —
audits and rewrites **DOM and CSS**. This game's player-facing UI is a **Phaser
canvas**. There is no DOM to audit: text is a `Phaser.GameObjects.Text` draw
call, layout is x/y coordinates, and "spacing" is not a stylesheet property.
Their tooling has nothing to grip. The _vocabulary_ (type scale, spacing rhythm,
motion easing) transfers to a human reading it; the commands do not run.

So the design gap here does not get closed by installing something. It gets
closed by us deciding what the storybook looks like.

### Verdicts

| Candidate                                 | Stars | Licence    | Verdict                           |
| ----------------------------------------- | ----- | ---------- | --------------------------------- |
| **Playwright** (installed)                | —     | MIT        | **Adopt** — the only clear win    |
| **Impeccable** (`pbakaus/impeccable`)     | 66.5k | Apache-2.0 | Read, do not install              |
| **Taste** (`Leonxlnx/taste-skill`)        | 85.4k | MIT        | Reject                            |
| **img2threejs**                           | 15.6k | Apache-2.0 | Reject for v1                     |
| **game-creator** (`PlayableIntelligence`) | 328   | **none**   | Do not install; mine for patterns |
| **designer-skills** (`Owl-Listener`)      | 2.6k  | MIT        | Unassessed, low priority          |

**Playwright — adopt.** Already installed and currently unused. It is the answer
to "how do we know the Earth level still works", which is a real gap: there is no
browser-level test in this repo at all. Screenshot regression plus
`browser_evaluate` to drive the game. **Caveat:** a Phaser canvas is opaque to
accessibility snapshots — the scene must expose a small test handle on `window`
(dev builds only) or the tests can only diff pixels. Dev-time only, ships
nothing.

**Impeccable — read, do not install.** Its seven pillars are a decent checklist
and its anti-pattern list (glassmorphism, bento grids, "AI cream" palettes) is
worth knowing. But its commands audit CSS, and its UX-writing pillar is
English-centric — this game's copy is Bulgarian for 11-year-olds, where its rules
would actively mislead. Cost of reading the pillar list: ten minutes. Cost of
installing: a skill that fires on the wrong kind of file.

**Taste — reject.** Same canvas mismatch, and it is React/GSAP shaped. Its
image-generation skills call an external image API and want a key, which is a
poor fit for art in this project on two counts: generated art mangles Cyrillic
(rule 3 forbids baking text into art at all), and an invented planet or star
field is a **fabricated visual claim** under rule 1. Our planet art comes from
NASA imagery through `process-textures.py`.

**img2threejs — reject for v1, revisit if a non-astronomical 3D prop appears.**
The engineering is genuinely well matched on one axis: it emits a code-only
procedural `THREE.Group` factory, and our Three.js budget is _single objects_
(`src/shared/planet-render.ts`). But the only 3D object this game has is a
planet, and a planet must be real imagery, not a procedural guess. There is
nowhere for its output to live. Apache-2.0 and actively maintained, so it stays
worth remembering.

**game-creator — do not install; mine it for patterns.** Closest stack match
found: Phaser `^3.90` (our exact version), Three.js, Vite, Playwright QA. Two
blockers. First, **no licence at all** — vendoring its code is legally
unresolved. Second, it is built around `/viral-game`: deploy, promo video, and
**Play.fun monetization that injects a CDN script and syncs points to a
leaderboard**. That is a direct hit on rule 8 — zero network requests, nothing
collected — in a game for children. Its `phaser` and `game-qa` reference skills
are still worth reading for architecture ideas.

### What was looked at and dismissed, so it is not re-proposed

`senlindesign/taste-skill` (335 stars, no licence — a different project that
merely shares the name), `HermeticOrmus/claude-code-game-development` (62 stars,
thin), Unity and Unreal plugins from the official marketplace (wrong engine
entirely), `superdesign` and `playground` (DOM canvases and HTML explorers,
not game UI), Figma and Canva plugins (no design file exists to import).

### The uncomfortable conclusion

The research turned up **one** adoptable tool, and it was already installed. That
is consistent with the pivot recorded above: the bottleneck is not tooling, it is
that nobody has decided what the storybook looks like or how a puzzle escalates.
More plugins would be the same mistake in a new costume.

### Decisions taken on the research (owner, 2026-09-08)

**Adopt Playwright only, and read Impeccable's pillars without installing it.**
**Schedule the QA work after Earth is playable** — task #27, blocked by #24. A
test written before the scene exists would pin a guess.

One more reason not to install Impeccable, found while reading it: the skill
ships a **platform-specific binary** fetched into `~/.impeccable/bin/` on first
use. An opaque binary that phones out is a poor neighbour for a repo whose
defining rule is zero network and nothing collected — even at dev time it is
worth avoiding when the payoff is a checklist we can read for free.

#### Impeccable's pillars, translated to a Phaser canvas

The seven pillars are typography, colour, spatial design, responsiveness,
interactions, motion, and UX writing. Only the first six survive translation —
the UX-writing rules are English-shaped and this game's copy is Bulgarian for
11-year-olds, so `content/bg/*.json` stays governed by the pedagogy reviewer, not
by an English design skill.

Its anti-pattern list, restated for what we are actually building:

- **No default fonts.** Arial, Inter and system stacks read as unfinished. Ours
  is constrained harder anyway: any font must be verified for Bulgarian Cyrillic
  glyph forms and self-hosted in `assets/fonts/` (rules 3 and 8).
- **Never pure black or pure grey — always tint.** Free to apply; it is a
  `Phaser.Text` colour value like any other.
- **No grey text on coloured backgrounds.** Matters more here than in a normal
  UI: this is a night-sky game, so light-on-dark contrast is the default case
  and low-contrast text over a star field is the obvious failure.
- **Don't nest cards in cards.** The storybook framing pushes the same way — a
  page is a page, not a panel inside a panel.
- **No bounce or elastic easing.** Directly usable, since Phaser tweens name
  their easings exactly this way (`Bounce`, `Elastic`). Worth pinning as a
  convention before the first tween is written, because "playful = bouncy" is
  the reflex for a children's game and it dates the whole thing.

That is the whole transferable payload. It cost one read and no install.
