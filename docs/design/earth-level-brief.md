# Earth level — design brief

The owner's ten-puzzle Earth design, rewritten 2026-09-09 against grilling rounds
2–4 and a two-challenger review. The original draft asked for eight new puzzle
types, the player's home town and birthday, and a gravity demo that would have
taught a falsehood; all four are resolved below.

**Status: approved, build in progress.** Decisions here are settled — see
`docs/handoffs/2026-09-09-session-handoff.md`. Do not reopen them without an
`AskUserQuestion`.

## What Earth is for

Earth is the player's **first** experience and the only **guided** level. It
teaches core astronomy and physics using things a Bulgarian 11-year-old already
half-intuits from daily life, before the game sends them to the Moon and outward.

The interaction model is fixed: walk to a glowing marker in the top-down world →
a focused overlay opens → solve it → it closes and returns to the walking view,
with a **visible world reaction** confirming success. Keep the total short and
snappy. Err toward _short and complete_ over _long and thorough_ — the brief's
governing test is "genuinely finished, not an infinite scope-creep exercise".

## The ten beats

Ten beats, **seven puzzle types**. Four of the beats are the same interaction —
rotate a rendered object until it matches a reference within tolerance — so they
are one engine with four renderers, not four engines. A beat is level content; a
type is code that must be maintained forever.

The walking route runs the causal chain in order: **rotation → tilt → day length**.

| #   | Beat               | Type               | Teaches                                                      |
| --- | ------------------ | ------------------ | ------------------------------------------------------------ |
| 1   | Shadow sundial     | `rotate-match`     | Earth's rotation changes the sun's angle through the day     |
| 2   | Day/night spinner  | `rotate-match`     | the day/night cycle comes from rotation                      |
| 3   | Seasons tilt       | `rotate-match`     | **axial tilt** causes seasons — not distance                 |
| 4   | One-year orbit     | `trajectory-match` | a year is one orbit                                          |
| 5   | Moon phase preview | `rotate-match`     | the lit fraction changes; full depth comes on the Moon level |
| 6   | Зорница            | `trajectory-match` | one object, two appearances                                  |
| 7   | Big Dipper         | `connect-the-dots` | constellation recognition                                    |
| 8   | Gravity drop       | `gravity-drop`     | **air** is what separates the feather from the rock          |
| 9   | Telescope focus    | `telescope-focus`  | how focus works; previews later planets                      |
| 10  | Day length         | `parallax-compare` | day length varies with season, tied back to tilt             |

**Required spine:** 1 → 2 → 3 → 10. The other six award progress but never block.
Guided still means a 1.0 threshold — **of required markers only**.

## The four corrections to the original draft

### 1. Eight new types became two

The draft named `shadow-sundial`, `day-night-spin`, `seasons-tilt`, `orbit-drag`,
`moon-phase-preview`, `find-zornitsa`, `gravity-drop`, `telescope-focus` and
`day-length-compare` as types. `CLAUDE.md`: _a sixth type is a one-off that needs
its own maintenance forever._ Only **`gravity-drop`** and **`telescope-focus`**
are genuinely new interactions. The rest are configs.

`find-zornitsa` in particular is **not** a type. The draft made it a pan-the-sky
"tap the brightest dot" puzzle, which teaches recognition, not why Venus appears
twice. As `trajectory-match` over the committed
`orbital-positions.json#/bodies/venus`, the child drags Venus along its real path
and watches the **same object** arrive at morning and at evening — so the folk
belief in two sister stars and its astronomical resolution become one act, which
is what ADR 0005 requires. The morning/evening sign flips fall on **2026-10-25**
and **2027-08-12**, both inside the committed window. Near conjunction Venus is
invisible; the puzzle must not imply continuous visibility across the flip.

### 2. No home town, no birthday

The draft asked the player to place their **home town** on the globe (beat 2) and
put their **birthday month** on the orbit path (beat 4). Rule 8 is zero collection
about a child, and birth date is the heaviest GDPR category there is. Both are
cut.

**Solstices and equinoxes replace the birthday** — real, dated, derivable, and
astronomically better than a personal anniversary. They render as **season art,
never a date string**: a displayed date is a number with units, and rule 2 bars it.

Location: v1 fixes **Bulgaria's latitude**. A continent picker was designed and
then deferred, because Africa, Asia and the Americas each span both hemispheres —
one representative latitude per continent inverts the seasons and reverses shadow
direction for half those children, which would poison beat 1 directly. When the
worldwide version needs it, it returns as **latitude bands, not continents**.

### 3. Gravity drop is honest about air

The draft had a feather and a rock landing together on Earth, "no air resistance
in this stylized world". That is false on Earth's surface and this audience will
notice.

The first correction — model air resistance **and rock mass** — was itself wrong,
and both challengers caught it: over a few metres a rock and a ball land
indistinguishably, so making the heavier one win teaches _heavy falls faster_, the
Aristotelian misconception. There are also no sourced drag numbers; NASA fact
sheets carry surface gravity, not drag coefficients.

**The beat is two contrastive panels, qualitative not simulated**: `с въздух`
(feather flutters, rock drops) and `без въздух` (they land together). Only sourced
surface gravity and a **binary air flag** drive it. The vacuum panel is anchored to
**Apollo 15 — David Scott, 2 August 1971** — filmed, citable, and true. The fact
string is built around **въздухът**, never weight.

Because gravity is a per-body constant, this type is reused on every level: the
same drop on the Moon and on Mars is visibly slower, which is the payoff.

### 4. Moon phases are not the Moon rotating

The draft has the player _rotate_ a moon model until the lit portion matches. The
Moon is tidally locked; rotating it produces no phase change at all, and this is
the third live childhood misconception alongside the two `CLAUDE.md` names.
`docs/sources.md:59-66` already warns this beat must not reinforce the shadow
model.

The child **moves the Moon around the Earth** (or moves the Sun's direction) and
the lit fraction follows. The config pins `orbitAngle`, never `rotation`. The
renderer needs near-zero ambient light, or the night side stays visibly lit.

## Constraints every beat inherits

- **Hide the math.** No equations, typed numbers, displayed units or formulas. The
  day-length bars in beat 10 are **continuous unlabelled arcs** — no ticks, no
  segments, no hour count. The draft's "segmented clock face lit for daylight
  hours" was an hour count in disguise.
- **Bulgarian only, nothing hardcoded.** Every string resolves through
  `src/shared/content.ts` to `content/bg/*.json`. Keys ASCII, values Cyrillic,
  written to read naturally for an 11–12 year old rather than as translated
  English. Containers wrap and grow; Bulgarian runs longer.
- **Every claim is sourced before it is written.** Four beats — 4, 8, 9 and 10 —
  currently have **no** `docs/sources.md` entry and no fact string. Those entries
  must reach VERIFIED first.
- **All astronomical reference imagery is real photography** through
  `process-textures.py`, with a sources entry. Generated astronomical art is a
  fabricated visual claim. Non-astronomical props may be generated but must be
  **textless** — generators mangle Cyrillic.
- **Hardware.** Beats 2, 5 and 9 want 3D. One WebGL context at a time, rendered
  only while the overlay is open, disposed on every close with
  `forceContextLoss()`. Check free RAM before any 3D run.
- **A wrong attempt must teach something.** Distractors are the real
  misconceptions — seasons-by-distance, phases-by-Earth's-shadow,
  heavy-falls-faster. A puzzle that only fails is a lock, not a lesson.

## The companion

Beat 6 was the draft's proposed home for introducing the companion. It arrives
earlier, in phase 2, because every beat needs it.

Three tiers per puzzle: an **arrival** line naming the goal, a **nudge** if the
child stalls, a **success** line carrying the fact. Earth fires all three. Later
levels drop the arrival line, then the nudge, until only the fact remains — that
fade **is** the difficulty curve, since round 1 settled scaffolding removal as the
axis rather than tolerance tightening. The tier count is **level data, not code**.

## Deliberately not in Earth

Interstellar content (rule 6, solar system only for v1). The continent picker. The
constellation-visibility-by-month table — beat 7 ships as a **stub** whose config
is deliberately minimal until task #25 exists. Any sixth, eighth or ninth puzzle
type. Folklore beyond the Зорница beat: folklore is the on-ramp for this audience,
not the subject, and no new folklore work opens.
