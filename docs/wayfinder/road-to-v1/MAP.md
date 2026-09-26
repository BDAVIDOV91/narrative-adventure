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
- The book ends on a back cover (ticket 009):
  - it unlocks when the last world page is completed;
  - it is not tappable;
  - it points at nothing unbuilt.
- The whole book fits without scrolling down to 360px portrait, and its text never falls below the floor (ticket 009).
- No stubs.
  - No storybook **world** page has `sceneKey: null`. The back cover is not a world.
  - There is no coming-soon marker.
  - No off-roster world has a `level.<world>.*` key or a storybook page.
  - A fact string rewarded by a roster beat may mention any solar-system body (ticket 001).
- Placeholder art is allowed.

## Notes

- **Fixed inputs, not tickets.** Do not reopen these:
  - Earth's ten beats and grilling rounds 1–4 (`docs/handoffs/2026-09-09-session-handoff.md`), less
    `earth-gravity-drop`: the ADR 0006 trigger deletes `gravity-drop` (ticket 004, applied by 005; owner-accepted
    2026-09-25). Its facts move to the Moon's completion line and a Jupiter candidate (ticket 005).
  - The five-type set left by ticket 005, and the ADR 0006 trigger. Saturn (added by ticket 009) designs on these
    five only, and its uses do not count toward the trigger.
  - The rule 1/2/8 walls:
    - `drives` has no `rotation`;
    - Saturn is absent from any drop or pull comparison;
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
- **Hints and nudges (ticket 008, ADR 0007):** every level build follows these.
  - A nudge only points.
  - The hint step narrows _what_ to try, never _how far_.
  - Nothing is ever shown as a count, in digits or in words.
- **Premise corrected at charting:** no Mars scene exists.
  - `src/scenes/mars/` and `src/scenes/moon/` are empty.
  - Mars and Moon are storybook stubs (`sceneKey: null`) with a name and a blurb.
  - Jupiter and Saturn have names only.
  - The ephemeris covers Mercury through Saturn plus the Moon.

## Decisions so far

- [What each candidate world can teach through the seven types](tickets/002-what-each-world-can-teach.md) — Moon and Mars have honest beats on existing types; Neptune has none; `zoom-split-star` lives only if Jupiter does.
- [Which worlds make the v1 roster, and in what order](tickets/001-v1-roster.md) — Earth, Moon, Mars, Jupiter, plus Saturn (added by ticket 009, if ticket 010 finds three honest beats); the rest of the solar system is post-v1; Jupiter comes after the ADR 0006 anchor, so `zoom-split-star` goes.
- [What Jupiter can teach, deep](tickets/007-what-jupiter-can-teach.md) — spine of moons ladder, moving moons, Sirius and fast spin; viable only if `telescope-focus`, `trajectory-match` or `parallax-compare` survive 005.
- [Moon level design: beats, types and the required spine](tickets/003-moon-level-design.md) — spine M1 → M3 → M2 on `orbitAngle`; optional eclipse, near/far (`parallax-compare`) and seas & craters (`telescope-focus`); 2 companion tiers.
- [Mars level design: beats and types](tickets/004-mars-level-design.md) — five required beats, spine R1a: retrograde as see-it (`connect-the-dots`) then why (`trajectory-match`), telescope disc, never Moon-sized, blue sunset; `gravity-drop` gets no Mars use.
- [Apply the ADR 0006 trigger to the designed levels](tickets/005-adr-0006-verdict.md) — five types kept, `zoom-split-star` and `gravity-drop` deleted; air+Apollo becomes the Moon's completion line, the pull comparison a Jupiter candidate; sources gain a RETIRED status.
- [Jupiter level design: beats, types and the required/optional split](tickets/006-jupiter-level-design.md) — five required beats, 4 of 5 to pass, spine J1: the eye → binoculars → telescope ladder (`telescope-focus`), then moons that move (`trajectory-match`), Ganymede vs Mercury and a binocular peek at Jupiter vs Sirius (`parallax-compare`), and a fast spin timed by one Earth turn (`rotate-match`); the pull fact becomes the completion line.
- [What makes a child want to keep playing](tickets/008-what-makes-a-child-keep-playing.md) — the book's pages come alive as markers are solved, with no counter; hints are free (a pointing nudge, then a visual hint step, plus „Спомни си“ cards), never earned; second ideas move from nudges to the album card (ADR 0007).
- [The book's ending and navigation](tickets/009-book-ending-and-navigation.md) — a non-tappable back cover after the last world, derived from `completed`, whose companion lines send the child to find the worlds in the real sky; wrap-and-fit grid down to 360px with a text floor; bookmark on the newest open page; Saturn joins v1 if 010 finds three honest beats.

## Not yet specified

- ~~**Designs for levels after Mars**~~ — graduated to ticket 006 (Jupiter), backed by research ticket 007.
- ~~**The book's through-line, ending and navigation**~~ — page display settled by ticket 008 (a page comes alive as
  its markers are solved); the ending and narrow-width layout graduated to ticket 009.
- **Imagery and data per level**:
  - storybook page art with one element per marker, lit as it is solved (ticket 008). It is textless, and placeholder
    art is allowed.
  - which NASA textures to process;
  - the Galilean periods (#20): VERIFIED by ticket 006, values in `docs/sources.md`; only the data row remains;
  - radii and other constants, as cited `data/reference/` rows. `dataRef` reaches only `data/generated/` today, so
    these rows need the seam extended or a sibling loader (ticket 006).
  - Jupiter (ticket 006): Galilean periods and orbit radii, Jupiter/Ganymede/Mercury radii and the Jupiter/Earth
    rotation rows; J1 rung-3 telescope-like imagery (the Red Spot pale); the J7 close-up (real imagery, framed as up
    close); Ganymede and Mercury disc images; the J4 wide-sky frame (~50°, both J2000).
  - Mars (ticket 004): a Mars radius row, and the Moon radius row it shares with ticket 003, for R2's true-scale
    panel; the R3 disc frame, public-domain NASA/HST degraded honestly in `process-textures.py` and documented, or a
    licensed amateur image, never AI-generated; PIA19400 for R6.
  - Moon: which frames for M9's quarter/full crater pair (telescope-like, with a `docs/sources.md` imagery entry),
    and whether an annular Sun-vs-Moon disc needs a cited radius row (ticket 003).
  - Back cover (ticket 009):
    - textless storybook vignettes of each completed world, drawn only for a completed world, with no dim placeholder;
    - they are pictures, not the naked-eye view, so Saturn's rings are not promised to the eye;
    - a closed back cover is a plain dim cover;
    - plus the bookmark ribbon.
  - Saturn (tickets 010/011): the ring-opening angle is not in `data/generated/`, so it needs a cited row or a one-off
    computation (`docs/sources.md` "Through a small telescope"); plus the Saturn disc imagery.
- **Constellation visibility by latitude (#25)**: does any post-Earth level need it?

## Out of scope

- **Interstellar content**: a future version (rule 6).
- **Dwarf planets (Pluto, Ceres)**: rule 6 names the Sun, planets and major moons only.
- **The continent/latitude picker**: deferred to the expansion. v1 fixes Bulgaria's latitude (09-09 handoff, rule 8).
- **English and a worldwide version**: after v1 (ADR 0003 amendment).
- **New folklore work (#21 parked)**: folklore is garnish, and no new folklore research opens.
- **Deploy / delivery to children**: held until the owner says so. It returns as its own effort.
- **Sound**: added only once the owner judges the game worth it. It returns as its own effort.
- **Worlds after Saturn** (the Sun, Mercury, Venus, Uranus; Triton waits with its planet): out because the v1
  destination is five worlds (ticket 001, amended by ticket 009). The whole solar system is the owner's post-v1 goal, as
  a fresh map.
  - Input to that map: the owner prefers a Sun + Mercury page.
  - Input to that map: **Pluto** as a fully optional bonus page, near Sun + Mercury and outside the unlock chain, for
    curious children (ticket 009 Q6/Q11). It needs CLAUDE.md rule 6 amended first.
  - Input to that map: the **companion's finale**, a "help the companion" section that unlocks when the whole solar
    system is cleared ([The companion's story](tickets/012-companion-story.md) seeds it).
  - Input to that map: new world pages insert before the back cover, and that map decides how the back cover stays
    open with no new stored state (ticket 009).
  - Neptune has no honest beat (research 002).
- **Phobos, and Mars beat R9**: out because rule 6 covers major moons only, meaning the large round moons, and Phobos
  is not one (ticket 001).
