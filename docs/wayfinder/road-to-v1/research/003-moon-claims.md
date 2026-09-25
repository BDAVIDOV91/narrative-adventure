---
ticket: "003"
title: Moon level design: the claims the design adopts, and their sources
status: done
---

# Research 003: Moon claims and their sources

Produced by the `astronomy-consultant` agent on 2026-09-25 from search excerpts, not full-page reads. It is a
hand-off to `astronomy-accuracy-checker`, which fetches each page and records the status in `docs/sources.md`.
**Nothing here is VERIFIED until that happens.**

| #   | Claim | Source | Consultant verdict | Wording guard |
| --- | ----- | ------ | ------------------ | ------------- |
| 1 | The maria are plains of solidified lava (basalt), not water | <https://science.nasa.gov/moon/facts/>; <https://science.nasa.gov/moon/composition/>; <https://science.nasa.gov/moon/viewing-tips/> | Sourced; which sentence sits on which page is uncertain | No ages. Never "no water on the Moon" (polar ice) |
| 2 | Relief shows best near the terminator; full Moon is the worst time for shadows | <https://skyandtelescope.org/observing/observing-the-fullmoon/> (likely page); <https://science.nasa.gov/moon/viewing-tips/> | Sourced | Never "full Moon is useless" |
| 3 | A solar eclipse happens only at new Moon, and not every new Moon (orbit tilt) | <https://science.nasa.gov/eclipses/geometry/>; <https://science.nasa.gov/resource/why-dont-we-have-a-solar-eclipse-every-month/>; <https://science.nasa.gov/moon/eclipses/> | Sourced | Tilt "a little", never a steep ramp; no 5°. Moon's shadow on Earth drawn as a small patch, but no "seen only there" |
| 4 | A lunar eclipse happens only at full Moon; most full Moons miss Earth's shadow | <https://science.nasa.gov/moon/eclipses/>; <https://spaceplace.nasa.gov/eclipses/en/>; <https://svs.gsfc.nasa.gov/4158> | Sourced | Shadow always points straight away from the Sun. Shadow ≠ phase, but Earth's shadow on the Moon *is* a lunar eclipse |
| 5 | The Sun and Moon look *almost* the same size; annular eclipses happen when the Moon is farther and looks slightly smaller | <https://science.nasa.gov/eclipses/geometry/>; <https://science.nasa.gov/eclipses/types/> | Sourced for "almost". "Exactly" stays NOT ATTESTED | No 400× on screen |
| 6 | Eclipse safety: never look straight at the Sun; sunglasses, however dark, are not safe; use certified eclipse glasses or pinhole projection with your back to the Sun, never looking through the hole; never through binoculars, a telescope or a camera, even with eclipse glasses | <https://science.nasa.gov/eclipses/safety/>; <https://eclipse.aas.org/eye-safety>; <https://eclipse.aas.org/eye-safety/projection> | Sourced, except "with an adult" and the optics line (added after the challengers) | Nothing about totality. No "ISO 12312-2" in child text. "With an adult": sourced or dropped |
| 7 | Earthshine: sunlight reflected off Earth faintly lights the dark part of a crescent | <https://apod.nasa.gov/apod/ap250403.html>; <https://science.nasa.gov/earth/earth-observatory/earthshine-83782/> | Sourced | Described without naming it; „пепелява светлина" is not used |
| 8 | A perigee Moon looks up to about 14% wider than an apogee Moon; hard to notice by eye | <https://science.nasa.gov/moon/supermoons/>; <https://www.jpl.nasa.gov/edu/resources/teachable-moment/whats-a-supermoon-and-just-how-super-is-it/> | Sourced | Closest vs farthest, never "huge"; no percentage. Don't lift the NASA "double-take" rising-Moon line (horizon illusion) |
| 9 | The Moon turns once per orbit, so one face always points at Earth (tidal locking) | <https://science.nasa.gov/moon/tidal-locking/> (research 002 M1) | Sourced | Never "doesn't rotate"; phase wording never uses „лице" |
| 10 | The far side is not dark; it is fully lit at new Moon | <https://science.nasa.gov/moon/top-moon-questions/> (research 002 M2; `docs/sources.md:64-66` has no URL yet) | Sourced | No "тъмна страна" |

**Earth overlap check.** Earth's `earth-telescope-focus` (`src/scenes/earth/earth-data.json:149-159`) rewards
`fact.telescope-saturn`. No Earth telescope target is the Moon, so M9 is not a duplicate.
