# Road to a finished v1

<!-- wayfinder:map -->

## Destination

A settled v1 spec inside CLAUDE.md rule 6 (Sun, planets, major moons):

- the level roster, in order;
- each level's beats mapped to the existing puzzle types, with required/optional marked;
- the ADR 0006 keep/delete verdict for every type.

Plan mode plus two challengers builds from that spec afterwards; this map decides, it does not build.

**The finish bar the spec is judged against:**

- Every roster level is playable end to end, in `npm run dev` and in `npm run build` + `vite preview`.
- Progress persists across a reload.
- Every shipped claim is VERIFIED in `docs/sources.md`.
- The pedagogy, perf and privacy gates pass, and a Playwright QA pass has run.
- No stubs. That means no storybook page with `sceneKey: null`, no coming-soon marker, and no content key for a world
  that is off the roster.
- Placeholder art is allowed.

## Notes

- **Fixed inputs, not tickets.** Do not reopen these:
  - Earth's ten beats and grilling rounds 1–4 (`docs/handoffs/2026-09-09-session-handoff.md`).
  - The seven-type set and the ADR 0006 trigger.
  - The rule 1/2/8 walls:
    - `gravity-drop` never models mass;
    - `drives` has no `rotation`;
    - Saturn is absent from the drop comparison;
    - no exaggerated orbit ellipse.
  - Gating: `unlockThreshold` is 1.0 for the two guided levels (Earth and Moon) and 0.7 for every open level.
- **Folklore is garnish after Earth** (owner, 2026-09-25):
  - Earth's Зорница beat stays, since it is a fixed input.
  - Later levels get zero folklore beats; at most a sourced folk name inside a fact string.
  - ADR 0005 stands.
  - Check `docs/sources.md` NOT ATTESTED before any name.
- **Sourcing on this map:**
  - Research files hold candidates, never design facts.
  - A claim enters `docs/sources.md` when a design ticket adopts it.
  - That ticket cannot close until `astronomy-accuracy-checker` has VERIFIED the claim.
  - A claim found false goes in as NOT ATTESTED immediately.
- **Beats come from honest astronomy, not from type survival.** Keeping a type alive is never a design goal. A type
  survives only on a solar-system target.
- **Skills per ticket:** `grilling`, plus `astronomy-consultant` for design physics.
- **Build work runs beside the map, not as tickets.** This covers:
  - phase-2 task #3 and the rest of the Earth build;
  - reduced motion (phase-2 task 9).
- **Premise corrected at charting:** no Mars scene exists.
  - `src/scenes/mars/` and `src/scenes/moon/` are empty.
  - Mars and Moon are storybook stubs (`sceneKey: null`) with a name and a blurb.
  - Jupiter and Saturn have names only.
  - The ephemeris covers Mercury through Saturn plus the Moon.

## Decisions so far

- [What each candidate world can teach through the seven types](tickets/002-what-each-world-can-teach.md) — Moon and Mars have honest beats on existing types; Neptune has none; `zoom-split-star` lives only if Jupiter does.

## Not yet specified

- **Designs for levels after Mars**: one ticket per roster level, graduating when the roster ticket closes. Each
  carries its companion tier count as level data.
- **The book's through-line, ending and navigation**: what the final page does, and how the storybook handles N pages.
  The current one-row 200px layout (`src/scenes/storybook-scene.ts:71-80`) overflows beyond about five.
- **Imagery and data per level**:
  - which NASA textures to process;
  - whether Uranus and Neptune need ephemeris if they make the roster (the round-1 pivot bars new pipeline);
  - the Galilean periods (#20, NEEDS SOURCE) if Jupiter makes the roster.
- **Constellation visibility by latitude (#25)**: does any post-Earth level need it?

## Out of scope

- **Interstellar content**: a future version (rule 6).
- **Dwarf planets (Pluto, Ceres)**: rule 6 names the Sun, planets and major moons only.
- **The continent/latitude picker**: deferred to the expansion. v1 fixes Bulgaria's latitude (09-09 handoff, rule 8).
- **English and a worldwide version**: after v1 (ADR 0003 amendment).
- **New folklore work (#21 parked)**: folklore is garnish, and no new folklore research opens.
- **Deploy / delivery to children**: held until the owner says so. It returns as its own effort.
- **Sound**: added only once the owner judges the game worth it. It returns as its own effort.
