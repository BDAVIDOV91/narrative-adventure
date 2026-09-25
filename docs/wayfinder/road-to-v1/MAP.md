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
- No stubs.
  - No storybook page has `sceneKey: null`.
  - There is no coming-soon marker.
  - No off-roster world has a `level.<world>.*` key or a storybook page.
  - A fact string rewarded by a roster beat may mention any solar-system body (ticket 001).
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
- [Which worlds make the v1 roster, and in what order](tickets/001-v1-roster.md) — Earth, Moon, Mars, Jupiter; the rest of the solar system is post-v1; Jupiter comes after the ADR 0006 anchor, so `zoom-split-star` goes.
- [What Jupiter can teach, deep](tickets/007-what-jupiter-can-teach.md) — spine of moons ladder, moving moons, Sirius and fast spin; viable only if `telescope-focus`, `trajectory-match` or `parallax-compare` survive 005.
- [Moon level design: beats, types and the required spine](tickets/003-moon-level-design.md) — spine M1 → M3 → M2 on `orbitAngle`; optional eclipse, near/far (`parallax-compare`) and seas & craters (`telescope-focus`); 2 companion tiers.

## Not yet specified

- ~~**Designs for levels after Mars**~~ — graduated to ticket 006 (Jupiter), backed by research ticket 007.
- **The book's through-line, ending and navigation**: what the final page does, and how the storybook handles N pages.
  The four roster pages fit the one-row 200px layout (`src/scenes/storybook-scene.ts:71-80`) only at a window of roughly
  900px or wider, and the canvas is `Scale.RESIZE`. Narrow and tablet widths are still open.
- **Imagery and data per level**:
  - which NASA textures to process;
  - the Galilean periods (#20, NEEDS SOURCE), which Jupiter needs;
  - radii and other constants, as cited `data/reference/` rows.
  - Moon: which frames for M9's quarter/full crater pair (telescope-like, with a `docs/sources.md` imagery entry),
    and whether an annular Sun-vs-Moon disc needs a cited radius row (ticket 003).
- **Constellation visibility by latitude (#25)**: does any post-Earth level need it?

## Out of scope

- **Interstellar content**: a future version (rule 6).
- **Dwarf planets (Pluto, Ceres)**: rule 6 names the Sun, planets and major moons only.
- **The continent/latitude picker**: deferred to the expansion. v1 fixes Bulgaria's latitude (09-09 handoff, rule 8).
- **English and a worldwide version**: after v1 (ADR 0003 amendment).
- **New folklore work (#21 parked)**: folklore is garnish, and no new folklore research opens.
- **Deploy / delivery to children**: held until the owner says so. It returns as its own effort.
- **Sound**: added only once the owner judges the game worth it. It returns as its own effort.
- **Worlds after Jupiter** (the Sun, Mercury, Venus, Saturn, Uranus; Titan and Triton wait with their planets): out
  because the v1 destination is four worlds (ticket 001). The whole solar system is the owner's post-v1 goal, as a fresh
  map.
  - Input to that map: the owner prefers a Sun + Mercury page.
  - Neptune has no honest beat (research 002).
- **Phobos, and Mars beat R9**: out because rule 6 covers major moons only, meaning the large round moons, and Phobos
  is not one (ticket 001).
