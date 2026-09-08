# Sources

Every astronomy and folklore claim the game makes, with its source and its
verification status. The `astronomy-report` skill checks content against this
file before a commit that touches `content/` or `data/generated/`.

## Why this file is mandatory

This is an education game for children. A claim that ships without a source is a
claim nobody checked. Wrong astronomy taught to an 11-year-old is the most
severe defect this project can produce — it is this project's equivalent of a
security hole, and it gets the same treatment.

## What this game is about

**The astronomy and astrophysics are the point.** Bulgarian folklore is a bonus
layer that makes the sky feel like it belongs to the player — it is never the
lesson. A folk name earns its place only when learning the folklore and learning
the astronomy are the same act. See
`docs/adr/0005-folklore-beats-must-carry-astronomy.md`.

## Status vocabulary

| Status           | Meaning                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| **VERIFIED**     | Checked against a named authoritative source, cited below.                                      |
| **NEEDS SOURCE** | Believed true, no source recorded yet. Must not ship in player-facing content until it has one. |
| **DISPUTED**     | A specific problem has been identified. Must be resolved before it ships.                       |
| **NOT ATTESTED** | Investigated and found unsupported. Recorded so nobody re-adds it.                              |

---

## Solar system

### Day and night — Earth's rotation

- **Claim** (`fact.day-night`): Earth turns on its axis, so the Sun rises and sets.
- **Status**: VERIFIED — uncontroversial, standard reference astronomy.

### Seasons — axial tilt, not distance

- **Claim** (`fact.seasons`): Earth's axis is tilted; that causes seasons, _not_
  our distance from the Sun.
- **Status**: **VERIFIED, and now backed by our own generated data.**
- **Evidence in the repo**: `data/generated/orbital-positions.json`,
  `bodies.earth.helioDistanceAu`. Perihelion **2027-01-03 at 0.983 AU**,
  aphelion **2027-07-05 at 1.017 AU** — a **3.4%** variation whose near point
  falls in the middle of northern winter. Asserted by
  `tests/test_orbital_positions.py::test_perihelion_falls_in_northern_winter`.
- **Why it is called out explicitly**: "we are closer to the Sun in summer" is
  one of the most persistent misconceptions in science education. The level must
  actively contradict it, and it now has the real numbers to do so.
- **Design constraint**: do not draw Earth's orbit as a pronounced ellipse. At
  3.4% it is visually indistinguishable from a circle, and an exaggerated oval
  teaches the misconception the level exists to remove.

### Moon phases — illumination, not Earth's shadow

- **Claim** (`fact.moon-phases`): We see the part of the Moon the Sun lights.
- **Status**: VERIFIED.
- **Why it is called out**: children commonly believe phases are Earth's shadow
  on the Moon. That is a lunar eclipse, a different and much rarer event. The
  rotate-match puzzle must not accidentally reinforce the shadow model.
- **Related trap**: "the dark side of the Moon". The far side is not dark — it
  receives as much sunlight as the near side. Say **далечната страна**, never
  тъмната.

### Parallax

- **Claim** (`fact.parallax`): Viewing one object from two positions makes it
  appear to shift; astronomers use this to measure distance.
- **Status**: VERIFIED.

### Mars retrograde motion

- **Claim**: Mars sometimes appears to move backwards across the sky.
- **Status**: VERIFIED, and derivable from the repo's own data —
  `helioLonDegrees` for Earth and Mars drive the walk-the-orbits puzzle, so the
  apparent reversal comes out of real geometry rather than being asserted.

### Planetary positions — independently spot-checked

- **Status**: VERIFIED 2026-09-08 against In-The-Sky.org, not against the
  generator that produced them.
- Jupiter minimum distance **2027-02-11** vs opposition 2027-02-11 (exact);
  Mars **2027-02-20** vs opposition 2027-02-19; Saturn **2026-10-05** vs
  opposition 2026-10-04 — both within the 1-day sampling grid.
- Lunar perigee 2026-12-24 at 356,779 km and apogee 2027-01-07 at 406,564 km,
  both inside the true physical envelope.
- **Not checked**: per-sample RA/Dec against an almanac, and whether the
  committed file still matches what the script produces today.

### Jupiter's Galilean moons

- **Claim**: Io, Europa, Ganymede and Callisto shift position night to night;
  their orbital periods can be deduced from watching them.
- **Status**: **NEEDS SOURCE** for the specific periods. The four names and
  Galileo's discovery are uncontroversial; the numbers the puzzle depends on
  must come from a cited source (JPL) and be generated into
  `data/generated/`, never typed from memory.

---

## Stars and constellations

### Orion's Belt — the brief's claim is FALSE, and the truth is better

- **Claim in the brief**: the belt's _brightest-looking_ point resolves into
  multiple stars as you zoom in.
- **Status**: **RESOLVED — the claim is false and was never shipped.** Verified
  2026-09-08.
- **What is actually true — the claim is exactly inverted.** The brightest belt
  star is **Alnilam (ε Ori, V = 1.69)** and it is the **only single star of the
  three**. Alnitak (ζ Ori) is second at V = 1.77 combined and has **four**
  components; Mintaka (δ Ori) is faintest at V = 2.23 and has **five**, in the
  hierarchy [(Aa1 + Aa2) + Ab] + (Ca + Cb). There is no reading of "brightest"
  — combined or primary-alone — under which the brief's version survives.
- **Source**: Oplištilová, Brož, Hummel et al., _"VLTI observations of the Orion
  Belt stars: I. ε Orionis"_, **A&A 704, A204 (2025)**,
  doi:10.1051/0004-6361/202556154 — ε Ori "represents the only massive single
  star in Orion's Belt". Magnitudes cross-checked in SIMBAD (Ducati 2002).
  https://arxiv.org/abs/2507.02276
- **The teaching point this unlocks**: the brightest-looking dot is the lonely
  one, and the faintest is a family of five. Brightness tells you nothing about
  how many stars are there. That is a better lesson than the brief's version.
- **Separations, if an Orion split is ever built** (from SIMBAD ICRS J2000,
  cross-checked against WDS/ORB6): δ Ori A–C **52.3″** (binoculars); δ Ori Aa–Ab
  **0.26″**; δ Ori Aa1–Aa2 spectroscopic + eclipsing, P = 5.7324 d. ζ Ori A–B
  **2.42″**; ζ Ori Aa–Ab **0.036″** (Hummel et al. 2013, A&A 554, A52),
  interferometry only. Use **Mintaka**, not Alnitak — ζ Ori's only
  amateur-reachable split is 2.42″ at a 1.7-mag contrast, which cannot be made
  honest at storybook zoom.

### Mizar and Alcor — the primary `zoom-split-star` target

- **Claim** (`fact.mizar-alcor.*`): what looks like one star in the handle of
  Колата separates into more stars at each level of magnification, and there are
  six in total.
- **Status**: **VERIFIED** 2026-09-08.
- **The zoom ladder, each rung sourced**:
  1. Naked eye — one point. Mizar, combined V = 2.04.
  2. Sharp eye or binoculars — Alcor appears at **708.6″ (11.8′)**, V = 4.01.
     The classic eyesight test, confirmed experimentally: Bohigian, _"An Ancient
     Eye Test — Using the Stars"_, Surv. Ophthalmol. **53** (2008) 536.
  3. Small telescope — Mizar splits into A (V 2.22) and B (V 3.88) at **14.44″**.
  4. Instruments only — Mizar A is a spectroscopic binary (P = 20.54 d, the
     **first ever discovered**), Mizar B likewise (P = 175.06 d), and Alcor has
     a red-dwarf companion at ~1″ (Zimmerman et al. 2010, ApJ 709, 733; Mamajek
     et al. 2010, AJ 139, 919).
  - **Six stars, all gravitationally bound** — 100% probability, Shaya & Olling
    2011, ApJS 192, 2. Distance ~83 ly.
    https://en.wikipedia.org/wiki/Mizar_and_Alcor
- **Why this and not a belt star**: Ursa Major is circumpolar from Bulgaria
  (42–44° N) — visible every clear night, all year. Orion is winter-only. A
  child can perform rung 2 the evening they play the level.
- **Wording constraint**: 11.8′ is about two-fifths of the Moon's diameter.
  Content must say Mizar and Alcor **look like** one star, never that they _are_
  one star, and rung 2 is "another appears beside it", not "it splits".

### The Pleiades — one smudge, a thousand stars

- **Claim** (`fact.kvachka`): the naked eye sees a handful, binoculars show
  dozens, and the cluster really contains far more.
- **Status**: VERIFIED. NASA, Messier 45: "contains over a thousand stars",
  ~445 ly, apparent magnitude 1.6, best observed in December.
  https://science.nasa.gov/mission/hubble/science/explore-the-night-sky/hubble-messier-catalog/messier-45/
  Naked-eye count 6–7 (Ангел Бонов). Galileo's _Sidereus Nuncius_ (1610) plate
  showed **36 stars beyond the six known**.
- **Culminates at 71.5°** from Bulgaria, best in the game's winter play season.

### Brightest stars, for the connect-the-dots level

- **Orion**: **Rigel (β Ori, V = 0.13)** is the brightest. Betelgeuse (α Ori) is
  the Bayer α but is usually _second_, V ≈ 0.50 mean, varying **0.0–1.6** — the
  widest range of any first-magnitude star (AAVSO VSX; en.wikipedia Betelgeuse).
  Status VERIFIED. **A string saying Betelgeuse is Orion's brightest star is
  false and must not ship.**
- **Ursa Major**: Alioth (ε UMa, V = 1.77) is brightest, Dubhe (α UMa) 1.79.
  Status VERIFIED **but must not become a player task** — a 0.02-mag margin is
  invisible to the eye and to the screen, and asking a child to spot it teaches
  that magnitude differences are visible when they are not. Teach the shape.
- **Albireo (β Cyg)**: **DISPUTED — do not use.** Whether A and B form a
  physical binary or are an optical double is unresolved (Bastian & Anton 2018,
  A&A 620, L2; Gaia DR2 astrometric noise). Do not teach an unsettled binary as
  a binary.
- **Trapezium (θ¹ Ori)**: VERIFIED as a genuine multi-star split (A–B 8.85″,
  A–C 12.86″, C–D 13.41″). Good as a _second_ panel, not the primary — the
  nebulosity competes with the "one dot becomes several" reading, and six stars
  need ~5″ aperture.

---

## Bulgarian folklore — the bonus layer

Folklore claims are factual claims, and this audience will notice errors. None
of these is the lesson; each is attached to a lesson.

### Зорница and Вечерница — one planet, two names

- **Claim** (`fact.zornitsa`): Зорница (morning) and Вечерница (evening) are
  traditionally treated as two different stars, but are the same object — the
  planet Venus.
- **Status**: **VERIFIED.** Дарина Младенова, _Звездното небе над нас_, БАН 2006,
  с. 52–53 (via Бајић 2020, Proc. XII Serbian-Bulgarian Astronomical Conference,
  p. 158). Other attested Bulgarian names: Деница, Зора, Овчарската звезда,
  Вечерната звезда, Големата звезда.
- **Why it works**: the folklore creates the misconception and the astronomy
  resolves it. This is the model every other folklore beat is measured against.
- **The kinship detail from the brief — DISPUTED, and deliberately not told.**
  The brief has "Зорница = sister of the sun, Вечерница = sister of the moon".
  Two sources conflict:
  - **ИЕФЕМ–БАН** (Валентина Шарланова, "Космогония", citing Маринов, _Народна
    вяра и религиозни народни обичаи_, СбНУ т. 28, 1914): **all stars are the
    Sun's sisters**, and the Moon is herself the Sun's sister — so "sister of the
    Moon" has no slot. A folk song has the hero take from the Sun "his dear
    sister… вечерница и зорница".
  - **Иваничка Георгиева**, _Българска народна митология_, с. 29: "според някои
    вярвания те са две сестри: зорницата е спътница на брат си слънцето, а
    вечерницата — на месеца" — note her own hedge.
  - Јанковић (1951) has Даница as the Sun's sister and the Moon's **cousin**.
  - **Decision**: the game states only that folk tradition calls them sisters,
    and makes no claim about whose. Both sources agree on that much. Revisit only
    with Маринов in hand.

### Кумова слама — removed from the game

- **Status**: the name is **VERIFIED** as a Bulgarian folk name for the Milky Way
  (ИЕФЕМ–БАН; Ангел Бонов), alongside **Попова слама, Сламата, Пато**.
- **The brief was wrong twice**: "кум" is not "groom" — it is the _godfather /
  wedding sponsor_ (groom is "младоженец"), so the name means "the **godfather's**
  straw", a possessive naming the **victim**. And "a groom visiting his best man"
  omits the theft, which is the whole tale: a кумец takes straw from his
  кръстник in a bottomless basket, trails it across the sky, and is cursed.
- **Why it is out**: it teaches a moral about stealing, not about the Milky Way.
  No Bulgarian variant encodes "many stars" — Попова слама, Пато and the
  milk-of-the-moon version all fail the same test. **The fix is not folklore, it
  is Galileo**: the eye says smear, the tube says stars.
- **Trap**: a popular Bulgarian children's book is titled _"Съзвездието Кумова
  слама"_. The Milky Way is a galaxy seen edge-on from inside — **never** write
  съзвездие for it.

### Лъжи керван — Sirius mistaken for the morning star

- **Claim** (`fact.lazhi-kervan`): caravan drivers woke, saw a bright star in the
  east, took it for Зорница and set off far too early.
- **Status**: **VERIFIED.** Иваничка Георгиева, _Българска народна митология_,
  с. 29: "Лъжи керван, мами керван е звезда, вероятно Сириус…". Ангел Бонов
  gives the same tale in fuller form.
- **Why it works**: this is the Зорница pattern _running backwards_. There the
  folklore splits one object into two; here it fuses two into one. The same
  physics resolves both — Venus is tied to the Sun and can never be high in the
  east at midnight; Sirius is a star and can.
- **Checked against our own ephemeris** (Sofia, 2026): Sirius at morning twilight
  +5.3° on 20 Aug, +14.6° on 1 Sep, +26.7° on 22 Sep; at local midnight below
  the horizon until roughly early November. Both sources' timings hold.

### Квачката — the Pleiades as a hen with chicks

- **Claim** (`fact.kvachka`): the folk name is a hen with her chicks.
- **Status**: **VERIFIED.** Георгиева, с. 28: "Квачката (кокошка, стожари,
  власи, власци, влашкови) са съзвездието Плеяди"; бел. 111: "**съзвездието
  квачката се смята за кокошка с 6—7 пиленца**". Бонов: the brightest is the
  hen, the six fainter ones the chicks.
- **Why it works**: the folk name _encodes the naked-eye count_. Nobody has to be
  told the number — the name is the number, and the telescope then breaks it.
- **The seasonal calendar is VERIFIED and astronomically real.** Georgieva frames
  the cluster's heliacal setting and rising as dividing the year. Computed from
  our own `de440s.bsp` for Sofia 2026: Гергьовден (6 May) altitude +6.2° at
  Sun = −8°, gone by 15 May; летен Тодоровден (8 June) +4.2° at morning
  twilight, not yet visible on 1 June. Accurate to within days.
- **DO NOT REPEAT** Georgieva's line that the Pleiades rise _with the Sun_ at
  Димитровден. Read literally that is **false** — they are near opposition then
  (elongation 152.4° on 26 Oct; true opposition 17 Nov). Say they rise as it gets
  dark and are up all night.
- **"Бабите" is NOT ATTESTED** in either primary source. The forms власи /
  власци / влашкови are attested but their etymology is contested — do not gloss
  them as "Wallachian stars".

### Bulgarian constellation names

- **Orion = Рало / Ралица**; **Ursa Major = Колата**.
- **Status**: **VERIFIED (secondary)** — Христо Вакарелски, _Етнография на
  България_, София 1977, стр. 413, as cited by bg.wikipedia for both. Promote to
  primary once p. 413 is read directly.
- Бонов's star-by-star mapping for Ралица: рало = the Belt + σ,θ,χ; орач =
  Сириус; остен = η,τ,β; кучето = Процион; воловете = Бетелгейзе, Белатрикс.
  For Колата: колела = α,β,γ,δ; волове = ε,ζ; вълк = η.
- **The variant the game does not tell**: some Bulgarian astronomy writing holds
  Ралицата to be a scene spanning several IAU constellations. Status PLAUSIBLE.
  **The game tells the narrow variant (Орион = Рало)** and says so here.
- **"Косери" is NOT ATTESTED for Orion.** Do not use it.
- **Mizar = "Мечката" / Alcor = "кучето"** — PLAUSIBLE only, blog-level sourcing.
  Do not put in game text until traced to Вакарелски or Ковачев.

### Стожер for the Pole Star — NOT ATTESTED

- Investigated because it is an appealing metaphor: a стожер is the pole at the
  centre of a threshing floor that everything turns around, which would be a
  beautiful and astronomically apt folk name for the celestial pole.
- **It is not one.** Речник на българския език (ИБЕ–БАН) records **no
  astronomical sense** for стожер. Worse for the hypothesis, **стожари** is
  attested as a name for the **Pleiades** (Георгиева, с. 28) — the opposite slot.
- **No Bulgarian folk name for Polaris was found** in Георгиева, Бонов, the ИБЕ
  dictionary, or Младенова's bibliography.
- Recorded here so it is not re-proposed. The image may be used as the game's own
  teaching metaphor ("небето се върти като харман около кол"), never as a folk
  name.

---

## Terminology

Standard Bulgarian, checked against bg.wikipedia's own astronomy articles.

| English                            | Bulgarian                          | Note                                                            |
| ---------------------------------- | ---------------------------------- | --------------------------------------------------------------- |
| Solar System                       | Слънчева система                   |                                                                 |
| Milky Way                          | Млечен път                         | Кумова слама is the _folk_ name, never a replacement            |
| Mercury / Venus / Earth / Mars     | Меркурий / Венера / Земя / Марс    |                                                                 |
| Jupiter / Saturn                   | Юпитер / Сатурн                    |                                                                 |
| Moon / Sun                         | Луна / Слънце                      | folk texts use Месечина; keep that inside quoted folklore only  |
| morning / evening star             | Зорница / Вечерница                |                                                                 |
| Orion's Belt                       | Поясът на Орион                    | not "Коланът"                                                   |
| asterism                           | астеризъм                          | the Belt is an asterism, not a constellation                    |
| open cluster                       | разсеян звезден куп                | not "отворен куп", never "клъстер"                              |
| double / multiple star             | двойна / кратна звезда             | use кратна for 3+, not "множествена"                            |
| magnitude                          | звездна величина                   | correct term, but **must never appear in player text** (rule 2) |
| supergiant                         | свръхгигант                        |                                                                 |
| Alnitak / Alnilam / Mintaka        | Алнитак / Алнилам / Минтака        |                                                                 |
| Rigel / Betelgeuse / Mizar / Alcor | Ригел / Бетелгейзе / Мицар / Алкор |                                                                 |
| far side of the Moon               | далечната страна                   | never "тъмната страна"                                          |

**"кум" ≠ groom.** кум = godfather / wedding sponsor; кумец = the man whose
wedding he sponsored; младоженец = groom. This error is in the brief.

---

## Data sources

| What                    | Source                  | Notes                                                                                                                                                                                               |
| ----------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Planetary positions     | JPL DE440s via Skyfield | `data/ephemeris/`, gitignored. Covers 1849–2150.                                                                                                                                                    |
| Planet and moon imagery | NASA                    | Public domain. Real Mars must look like real Mars — imagery is never AI-generated.                                                                                                                  |
| Star catalogue          | **NEEDS SOURCE**        | Blocking. Every new constellation claim above depends on real positions and magnitudes. HYG or Hipparcos, pulled by a generator script into `data/generated/` — never constants typed into a scene. |
