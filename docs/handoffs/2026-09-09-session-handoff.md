# Session handoff — 2026-09-09

**Read this first. This is the brief.**

The archive is `~/.claude/plans/read-docs-handoffs-2026-09-08-session-h-purrfect-noodle.md`
— the approved plan with the full challenger review folded in. You do not need it
unless something here turns out to be wrong; it carries the reasoning, this
carries the decisions.

`docs/handoffs/2026-09-08-session-handoff.md` is **superseded** and banner-closed.
Its still-live sections are the pivot, grilling round 1, the star catalogue and
the skills research results.

Astronomy education game for Bulgarian children (~11–12). Browser, Phaser 3 +
TypeScript, a little Three.js, Python build-time only. Branch `development`.

---

## Already settled — DO NOT re-run, DO NOT re-ask

Each cost real time and produced a recorded answer. Re-doing any of them proves
nothing new.

- **Grilling rounds 1–4 are complete.** The Earth design is settled; the decision
  list below is the output. Round 1's own settled items (finish Earth first,
  scaffolding removal as the difficulty axis, the mystery never blocks,
  connect-the-dots is the constellation puzzle) still stand.
- **The plan has been challenged.** Two `challenger` agents ran in parallel, both
  returned REVISE at high confidence, and **every finding was accepted and folded
  in**. Do not re-challenge this plan.
- **The Бонов folklore research is closed**, not blocked. Findings are in
  `docs/sources.md` and `.claude/agent-memory/astronomy-accuracy-checker/`.
- **The skills research is done** (2026-09-08). One adoptable tool, Playwright,
  already installed. Do not redo it.
- **The `pdf_data_extractor_v2` workflow survey is done.** Its headline: that repo
  has **no implementation subagents at all** — every agent is a read-only reviewer,
  and context is kept small by files on disk, not by delegation.

---

## The Earth design — settled

### Puzzle types: 7, not 5, not 13

`rotate-match`, `connect-the-dots`, `parallax-compare`, `zoom-split-star`,
`trajectory-match`, **`gravity-drop`**, **`telescope-focus`**.

The owner first chose 13 (one type per beat). Both challengers independently
called that scope creep and proposed the same collapse; the owner accepted. The
ten Earth beats all still ship — they are **level content, not types**:

| Beat               | Type               | Config carries                      |
| ------------------ | ------------------ | ----------------------------------- |
| shadow-sundial     | `rotate-match`     | sundial renderer, 3 rounds          |
| day-night-spin     | `rotate-match`     | Earth sphere, terminator target     |
| seasons-tilt       | `rotate-match`     | globe renderer, tilt axis           |
| moon-phase         | `rotate-match`     | Moon + **orbit angle**, never spin  |
| orbit-drag         | `trajectory-match` | closed path, solstice/equinox stops |
| Зорница            | `trajectory-match` | `dataRef` to Venus                  |
| Big Dipper         | `connect-the-dots` | IAU figure — **stub this slice**    |
| day-length-compare | `parallax-compare` | two daylight arcs                   |
| gravity-drop       | **new**            | per-body gravity, air flag          |
| telescope-focus    | **new**            | focus slider, reveal target         |

Four of the ten are one interaction — rotate a rendered object until it matches a
reference — so they are one engine and four renderers. Extra type names remain
available if a future level genuinely needs one; none is created speculatively.
**Review trigger: any type not reused on a second level by the Mars build gets
deleted, not maintained.**

### Astronomy corrections that must not regress

- **`gravity-drop` never models mass.** A rock and a ball land indistinguishably
  over a few metres; making the heavier win teaches "heavy falls faster", the
  Aristotelian misconception. The beat is two contrastive panels, `с въздух` /
  `без въздух`, qualitative not simulated, driven only by sourced surface gravity
  and a binary air flag. The vacuum panel is anchored to **Apollo 15, David Scott,
  2 August 1971**. The fact string is built around **въздухът**, never weight.
- **`moon-phase` never rotates the Moon.** It is tidally locked; phases are
  Sun–Moon–observer geometry. The child moves the Moon around the Earth. Config
  pins `orbitAngle`, not `rotation`. `docs/sources.md:59-66` already warned about
  this trap.
- **`seasons-tilt`'s comparison must contradict the distance misconception** and
  must not draw an exaggerated ellipse (`docs/sources.md:40-55`).

### Rule 8 — what was cut

- **The player's home town**: cut.
- **The player's birthday month** as a marker on the orbit path: cut. Birth date
  is the heaviest GDPR category for a child. **Solstices and equinoxes replace it**
  — real, dated, and astronomically better.
- **Geolocation API stays permanently barred.**
- **The continent picker is deferred to the expansion.** v1 fixes Bulgaria's
  latitude, which is also the cleanest rule-8 position available. Challenger A
  showed the picker was astronomically indefensible anyway: Africa, Asia and the
  Americas each span **both hemispheres**, so one representative latitude per
  continent inverts the seasons and reverses shadow direction for half those
  children. When it returns it should be **latitude bands, not continents**. Task
  #25's visibility table stays keyed on latitude, so nothing needs reworking.

### Rule 2 — the two number leaks that were closed

- Solstice and equinox markers render as **season art, never a date string**.
- The daylight bar is a **continuous unlabelled arc** — no ticks, no segments, no
  hour count. The prompt's "segmented clock face lit for daylight hours" was an
  hour count in disguise.

### Gating

Earth is guided with a **required/optional split**. The spine — sundial →
day-night → seasons-tilt → day-length — is mandatory; the other six award progress
but never block.

**The invariant does not relax: guided still means 1.0, _of required markers_.**
The threshold computes over `solved ∩ required`. Challenger A found the hole —
`solvedCount()` counts all solved markers and `meetsThreshold` is a bare
`solved / total`, so a required-only denominator would let a child unlock the
level by finishing four **optional** puzzles and never touching the spine.
`required` defaults to `true`; a level with zero required markers is rejected.

### Companion

Three tiers — arrival line naming the goal, nudge on stall, success line carrying
the fact. Earth fires all three; later levels drop the arrival line, then the
nudge, until only the fact remains. **The tier count is level data, not code** —
same seam as `unlockThreshold`, so difficulty is authored rather than branched.

### Data sourcing

- **Gravity constants**: hand-authored table cited to NASA planetary fact sheets,
  in **`data/`, not `data/generated/`** — that directory's contract is
  machine-produced and reproducible, and `dataRef` resolves under it only.
- **Day length**: a cited published table (NOAA/USNO) for Bulgaria's latitude,
  same pattern, in `data/`. No new generator — the round-1 pivot bars more
  pipeline.
- **Four beats have no fact string and no sources entry at all** — `orbit-drag`,
  `gravity-drop`, `telescope-focus`, `day-length-compare`. Four new
  `docs/sources.md` entries must reach **VERIFIED before** any string is written.
- **All astronomical reference imagery is real photography** through
  `process-textures.py` with a sources entry. Non-astronomical props may be
  generated but must be **textless**. Generated astronomical art is a fabricated
  visual claim under rule 1.

### Folklore is demoted

Owner, 2026-09-09: the goal is **getting Bulgarian children interested in
astronomy and physics**. Folklore is the on-ramp, not the subject, and must not
drive design. This sharpens ADR 0005 rather than contradicting it.

Nothing built changes. The Зорница/Вечерница `trajectory-match` beat stays — it is
the case ADR 0005 exists for, where the folk belief in two sister stars creates
the misconception the orbit resolves, in one act. `connect-the-dots` uses the IAU
figures in `data/generated/constellation-lines.json` and never needed the folk
mapping. **Task #21 is off the critical path and no new folklore work opens.**

### Post-v1 intent

English and a worldwide education game, **after** v1. Bulgarian-only is a scope
decision, not permanent architecture — `content.ts` + `content/bg/` is already the
i18n seam. **The folklore beats do not translate**: a worldwide version needs each
culture's own sky stories, so specific puzzles get rewritten, not translated.
Record as an amendment to `docs/adr/0003-bulgarian-only-for-v1.md`, which already
carries the "reskinnable later" framing — not as a new ADR.

---

## Latent bugs found by reading, now scheduled

1. **`earth-data.json` `dataRef` has never resolved.** It says
   `orbital-positions.json#/venus`; the file nests bodies under `bodies`. The
   validator checks only the filename, so it passes silently. Fix:
   `#/bodies/venus`.
2. **The schema promises per-type `config` validation that does not exist.**
   `targets` and `tolerance` are unconstrained free-form.
3. **`reward.unlocks: ["earth-gate-telescope"]` points at nothing** and nothing
   checks it.
4. **`saveProgress` has no call site anywhere.** Progress is never written.
5. **`book-zoom-transition.ts` has no call site either.**
6. **No vitest config and zero `*.test.ts`**, though `package.json:19` declares
   `vitest run`. Rule 5 cannot be honoured on TypeScript until this exists.
7. **`planet-render.ts` cannot do what three beats need.** Handle exposes only
   `dispose`; auto-spins unconditionally; light pinned at `(5,2,3)`; ambient
   hardcoded at `0.35`, which visibly lights a moon's night side.
8. **`assets/images/nasa/` is empty** — there is no Earth texture to render.

---

## Build order

**Phase 0** — schema and validator. _(Delegated to a worker agent this session;
check its state before redoing any of it.)_ Enum to 7, per-type config branches,
`required` flag, pointer resolution, `reward.unlocks` validation, RED test per
guard. `CLAUDE.md`'s "five puzzle types" section and `docs/design/puzzle-types.md`
both go stale and need updating.

**Phase 1** — all 10 markers in `earth-data.json`, content keys, the two data
tables and their sources entries. `src/shared/content.ts` **must** be edited when
`companion.json` is added — it hardcodes four bundle imports, so a fifth file is
visible to the Python validator but invisible to `t()`. `ui.puzzle.coming-soon`
is needed for the stub markers; a Cyrillic literal in a `.ts` file would violate
rule 3.

**Phase 2** — shared infrastructure, carried by engine 1. **Vitest first**, before
any other TypeScript, or the shared runtime ships untested. Decide jsdom vs
happy-dom, and accept the consequence: **solve and tolerance logic lives in pure
modules importable without a Phaser `Scene`**, or nothing is testable. Drop
`--passWithNoTests` from `.husky/pre-commit`. Then the puzzle overlay, companion
box, progress write, world reaction, and the widened `planet-render.ts`.

**Phase 3** — three engines, each finished end to end and **played** before the
next starts: sundial, day/night, seasons tilt. All three are `rotate-match` with
different renderers.

**This slice ends with Earth at 3 of 10 beats playable and 7 stub markers.** Said
out loud so the check-in is judged against the right expectation — round 1's
"finish Earth completely" is the destination, not this checkpoint.

### Disposal is engineered, not asserted

Reuse one module-level canvas and renderer across opens, add
`forceContextLoss()`, and prove it with a vitest test (`three` stubbed) asserting
open×N / close×N yields N disposals and ≤1 live renderer. On the error path —
`TextureLoader.loadAsync` rejects — the overlay closes cleanly, the marker stays
unsolved, and **no context is left open**. **Check free RAM before any 3D run**:
~1.9 GB on an integrated AMD APU, where a leaked context is a crash.

---

## Two ADRs owed

1. **The enum expansion** — `CLAUDE.md` says adding a type is "a deliberate
   decision, never a drive-by". Record the collapse reasoning and the Mars review
   trigger.
2. **Amend `0003-bulgarian-only-for-v1.md`** with the folklore-does-not-translate
   payload.

---

## Workflow changes adopted this session

From the `pdf_data_extractor_v2` survey:

- **This handoff format** — brief-vs-archive opening, and the stop-list above.
- **`session-recovery` skill** (`.claude/skills/session-recovery/`) — reconciles
  docs against git, the suites and the running game, and reports the
  disagreements. Its evidence table distinguishes **test-verified** from
  **played-verified**; never conflate them.
- **Agent research memory** at `.claude/agent-memory/<agent>/MEMORY.md`, a pointer
  index and never content. Wired into `astronomy-accuracy-checker`.
- **Archive discipline**, documented in `docs/README.md`.

**Delegation policy settled:** one writer at a time, never two on this working
tree. Self-contained file-scoped work (phase 0) is delegated with the plan as its
written brief; judgement work (the engines) stays in the main session. A
subagent's report is a **claim**, not a result — verify the parts you build on.
Every worker prompt must carry the never-stash rule, because sessions share one
tree.

---

## Task list

| #   | Status          |                                                                     |
| --- | --------------- | ------------------------------------------------------------------- |
| 20  | pending         | Galilean moon periods from JPL — last NEEDS SOURCE, non-blocking    |
| 21  | **parked**      | Ралица/Колата figures — off the critical path, folklore demoted     |
| 23  | **DONE**        | Scenario + puzzle-scaling design settled (grilling rounds 1–4)      |
| 24  | **in progress** | Build Earth — phase 0 delegated, phases 1–3 queued                  |
| 25  | pending         | Constellation visibility by month, keyed on **latitude**            |
| 26  | DONE            | Skills research                                                     |
| 27  | blocked by 24   | Playwright browser QA for the Earth level                           |
| 28  | **new**         | Two ADRs — enum expansion, and the 0003 amendment                   |
| 29  | **new**         | NASA Earth texture through `process-textures.py` — blocks day/night |

## Commands

```bash
npm run dev            # http://localhost:5173
npm run validate       # tsc + eslint + prettier
npm test               # vitest — does not exist yet, phase 2 creates it
venv/bin/python -m pytest
venv/bin/python data/scripts/validate-levels.py
sh .husky/test-pre-commit-scope.sh
sh .claude/hooks/test-block-dangerous-git.sh
free -h                # before any 3D run
```

Python env is `venv/` (not `.venv/`), driven by `uv`.
