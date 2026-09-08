# Sources

Every astronomy and folklore claim the game makes, with its source and its
verification status. The `astronomy-report` skill checks content against this
file before a commit that touches `content/` or `data/generated/`.

## Why this file is mandatory

This is an education game for children. A claim that ships without a source is a
claim nobody checked. Wrong astronomy taught to an 11-year-old is the most
severe defect this project can produce — it is this project's equivalent of a
security hole, and it gets the same treatment.

## Status vocabulary

| Status           | Meaning                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| **VERIFIED**     | Checked against a named authoritative source, cited below.                                      |
| **NEEDS SOURCE** | Believed true, no source recorded yet. Must not ship in player-facing content until it has one. |
| **DISPUTED**     | A specific problem has been identified. Must be resolved before it ships.                       |

---

## Astronomy claims

### Day and night — Earth's rotation

- **Claim** (`fact.day-night`): Earth turns on its axis, so the Sun rises and sets.
- **Status**: VERIFIED — uncontroversial, standard reference astronomy.

### Seasons — axial tilt, not distance

- **Claim** (`fact.seasons`): Earth's axis is tilted; that causes seasons, _not_
  our distance from the Sun.
- **Status**: VERIFIED.
- **Why it is called out explicitly**: "we are closer to the Sun in summer" is
  one of the most persistent misconceptions in science education, and Earth is
  in fact nearest the Sun in early January. The level must actively contradict
  it rather than leave it unaddressed.

### Moon phases — illumination, not Earth's shadow

- **Claim** (`fact.moon-phases`): We see the part of the Moon the Sun lights.
- **Status**: VERIFIED.
- **Why it is called out**: children commonly believe phases are Earth's shadow
  on the Moon. That is a lunar eclipse, a different and much rarer event. The
  rotate-match puzzle must not accidentally reinforce the shadow model.

### Parallax

- **Claim** (`fact.parallax`): Viewing one object from two positions makes it
  appear to shift; astronomers use this to measure distance.
- **Status**: VERIFIED.

### Mars retrograde motion

- **Claim**: Mars sometimes appears to move backwards across the sky.
- **Status**: VERIFIED. Reproducible directly from the generated ephemeris —
  `helioLonDegrees` for Earth and Mars drive the walk-the-orbits puzzle, so the
  apparent reversal is derived from real geometry rather than asserted.

### Jupiter's Galilean moons

- **Claim**: Io, Europa, Ganymede and Callisto shift position night to night;
  their orbital periods can be deduced from watching them.
- **Status**: NEEDS SOURCE for the specific periods used in the puzzle. The
  four names and Galileo's discovery are uncontroversial; the numbers the puzzle
  depends on must come from a cited source (JPL) and not from memory.

### Orion's Belt — the "one dot is really several stars" moment

- **Claim** (from the brief): the belt's _brightest-looking_ point resolves into
  multiple stars as you zoom in.
- **Status**: **DISPUTED — do not ship until resolved.**
- **Problem**: the belt's brightest star is Alnilam (ε Orionis), the middle one,
  generally treated as a single blue supergiant. The belt stars that are
  genuinely multiple systems are Alnitak (ζ Orionis) and Mintaka (δ Orionis).
  As written, the "wow" fact appears to be attached to the wrong star.
- **Required action**: `astronomy-accuracy-checker` verifies which belt star the
  claim should name, against a cited catalogue, before any `zoom-split-star`
  content is written. The mechanic is sound; the star may be misidentified.

---

## Bulgarian folklore claims

Folklore claims are factual claims too. Getting Bulgarian folklore wrong in a
game for Bulgarian children is a real defect, and the audience is exactly the
audience that will notice.

### Zornitsa and Vechernitsa

- **Claim** (`fact.zornitsa`): Зорница (morning star) and Вечерница (evening
  star) are traditionally treated as two different stars, but are the same
  object — the planet Venus.
- **Status**: The astronomical half is VERIFIED (Venus is the morning and
  evening star; the "two stars" identification is a widespread historical one).
  The **specific kinship detail** from the brief — Зорница as sister of the sun,
  Вечерница as sister of the moon — is **NEEDS SOURCE**. It must be traced to a
  named Bulgarian ethnographic source before it ships, not asserted from a
  general impression of the folklore.

### Kumova Slama

- **Claim** (`fact.kumova-slama`): Кумова слама is the Bulgarian folk name for
  the Milky Way.
- **Status**: The name itself is NEEDS SOURCE (widely reported, not yet cited
  here). The **accompanying folk tale** — its literal gloss and the story of a
  groom and his best man — is **NEEDS SOURCE**; several variants exist and the
  game should tell one and know which one it is telling.

---

## Terminology

Standard Bulgarian astronomy terms, not literal translations from English.

| English                        | Bulgarian                       | Status   |
| ------------------------------ | ------------------------------- | -------- |
| Solar System                   | Слънчева система                | VERIFIED |
| Milky Way                      | Млечен път                      | VERIFIED |
| Mercury / Venus / Earth / Mars | Меркурий / Венера / Земя / Марс | VERIFIED |
| Jupiter / Saturn               | Юпитер / Сатурн                 | VERIFIED |
| Moon / Sun                     | Луна / Слънце                   | VERIFIED |
| morning star / evening star    | Зорница / Вечерница             | VERIFIED |

---

## Data sources

| What                    | Source                            | Notes                                                                                                              |
| ----------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Planetary positions     | JPL DE440s ephemeris via Skyfield | Downloaded to `data/ephemeris/`, gitignored. Covers 1849–2150.                                                     |
| Planet and moon imagery | NASA                              | Public domain. Real Mars must look like real Mars — imagery is never AI-generated.                                 |
| Star catalogue          | NEEDS SOURCE                      | Constellation lines and magnitudes for `connect-the-dots` are not yet sourced. HYG / Hipparcos are the candidates. |
