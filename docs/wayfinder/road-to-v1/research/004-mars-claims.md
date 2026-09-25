---
ticket: "004"
title: Mars level design: the claims the design adopts, and their sources
status: done
---

# Research 004: Mars claims and their sources

Drafted by the main session on 2026-09-25 from research 002's Mars table (search-excerpt level), then widened after
two `challenger` reviews to one row per player-facing fact **and** nudge. It is a hand-off to
`astronomy-accuracy-checker`, which reads each page in full and records the status in `docs/sources.md`.
**Nothing here is VERIFIED until that happens.**

| #   | Claim | Where | Source | Wording guard |
| --- | ----- | ----- | ------ | ------------- |
| 1 | Mars sometimes appears to move backwards against the stars, then forwards again | R1a | NASA, _Mars Retrograde_ <https://mars.nasa.gov/all-about-mars/night-sky/retrograde/>; APOD 2014-10-28 <https://apod.nasa.gov/apod/ap141028.html>. Upgrades `docs/sources.md` "Mars retrograde motion", which is VERIFIED but cites no external source | "Seems to", "turns back". Never promise a loop: over a short span the track is a hook or Z. No dates |
| 2 | Mars never really turns back; the backwards look comes from Earth catching up with Mars and overtaking it | R1a fact | Same as 1 | Never "Mars stops" or "reverses" |
| 3 | The overtaking happens when Earth passes Mars on the inside (Earth's orbit is the inner one) | R1a nudge | Same as 1 | "Catches up and overtakes on the inside lane", never "passes near Mars" |
| 4 | Earth moves faster around the Sun than Mars does | R1b fact | Same as 1; else NASA, _Mars Facts_ <https://science.nasa.gov/mars/facts/> | No speeds or periods on screen |
| 5 | Mars never looks as big as the full Moon, not even at its closest | R2 fact + nudge | NASA, _Mars Hoax_ <https://mars.nasa.gov/resources/21869/mars-hoax/>; JPL Night Sky Network | No sizes or ratio. 2027 is a small (aphelic) opposition; no drama |
| 6 | Through a small telescope Mars is a small orange disc, sometimes with faint dark markings | R3 | Sky & Telescope, _An Observer's Guide to Mars_; ALPO, _2026-2027 Aphelic Apparition_ | Never the polar cap at small aperture (NOT ATTESTED). Never "like the photos" |
| 7 | Bigger telescopes show more detail on Mars | R3 nudge | Sky & Telescope, _An Observer's Guide to Mars_ | No apertures on screen |
| 8 | Mars is red because of rusty (iron oxide) dust | R3 fact | NASA, _Mars Facts_ | — |
| 9 | Mars is a cold world (placed beside 8, "red from rust"). _Corrected 2026-09-25: "not because it is hot" dropped, no read page states it_ | R3 fact | NASA, _Mars Facts_ | Never assert "not because it is hot". No temperatures on screen |
| 10 | A camera on Mars (Curiosity, Gale Crater) photographed a sunset with a bluish glow around the Sun | R6 fact | JPL, _PIA19400_ <https://photojournal.jpl.nasa.gov/catalog/PIA19400> | "A camera on Mars saw": one image, not every sunset. The blue is near the setting Sun. **Never say or imply the Mars sky is blue**; never "always". No "Mars has no air". _Corrected 2026-09-25: white balance is not a reason to doubt the colour; the caption says Mastcam sees colour much like a human eye_ |
| 11 | A day on Mars is only a little longer than a day on Earth | R6 nudge | NASA, _Mars Facts_ | "A little longer", no hours |

## Verification — `astronomy-accuracy-checker`, 2026-09-25

**Method: full page.** Each source was downloaded, stripped to text and searched for the supporting sentence. No
status below rests on a search excerpt. Quotes and exact URLs are in `docs/sources.md`, "Mars level — the claims
ticket 004 adopts".

| #   | Verifier status | Page that carries it (read in full) |
| --- | --------------- | ----------------------------------- |
| 1 | VERIFIED | NASA _Mars Retrograde_ (Wayback 2022-12-05, the live URL is dead) + APOD 2014-10-28 |
| 2 | VERIFIED | NASA _Mars Retrograde_ (Wayback): „It's an illusion"; „Earth comes up from behind and overtakes Mars" |
| 3 | VERIFIED | NASA _Mars Retrograde_ (Wayback): „Earth has the inside lane" |
| 4 | VERIFIED | NASA _Mars Retrograde_ (Wayback): „moves faster than Mars"; NSSDC fact sheet 29.8 vs 24.1 km/s |
| 5 | VERIFIED | NASA _Close Approach_ (Wayback): hoax recurs „every time Mars makes a close approach". Live _Mars Hoax_ URL is dead |
| 6 | **SUPERSEDED by 6′** (never VERIFIED; old wording NEEDS SOURCE, must not ship) | S&T guide returned 403, unread. ALPO read: „small apparent disk" only; „orange" only in a dust storm; no dark markings |
| 7 | **SUPERSEDED by 7′** (never VERIFIED; old wording NEEDS SOURCE, must not ship) | ALPO ties detail to disc size over the months, not aperture. S&T unread |
| 6′ | VERIFIED (full page, re-check 2026-09-25) | APOD 2003-08-19 <https://apod.nasa.gov/apod/ap030819.html>: „through a small telescope, possibly the most striking part of Mars' appearance is its red color"; ALPO <https://www.alpo-astronomy.org/jbeish/2027_MARS.htm>: „a small apparent disk of 6"". Keep APOD's hedge („possibly"). Guard: never the 2003 view, polar caps or named features for 2027 |
| 7′ | VERIFIED (full page, re-check 2026-09-25) | ALPO: „Views of surface details not well defined" at the 6″ start, „Views of surface details well defined" at opposition; APOD 2003-08-19, near the 2003 closest approach: „Visible through the small telescope are … dark red areas". Guard: no telescope sizes, no promise of what a particular telescope shows |
| 8 | VERIFIED | NASA _Mars Facts_: „oxidization — or rusting — of iron"; ESA 2025 concurs (ferrihydrite; keep „rust") |
| 9 | **Split**: „cold" VERIFIED; „not because it is hot" **NEEDS SOURCE** — drop it | NASA _Mars Facts_: „a dusty, cold, desert world". No read page states the negation |
| 10 | VERIFIED | PIA19400 caption (now at science.nasa.gov/photojournal): blue stays „closer to sun's part of the sky", strongest at sunset; white balance removes camera artifacts and Mastcam sees colour „very similarly to what human eyes see" |
| 11 | VERIFIED | NASA _Mars Facts_: „24.6 hours, which is very similar to one day on Earth (23.9 hours)" |

Two wording corrections the reads force: row 10's guard should not lean on "white-balanced" to suggest false
colour, since the caption says the opposite; and _Mars Facts_ says the Mars sky „would be hazy and red", which is
now in the NOT ATTESTED list. Rows 6, 7 and the „not heat" half of 9 must not ship as worded.

**Follow-up, 2026-09-25.** The owner reworded 6 and 7 as 6′ and 7′; both pages were re-read in full and both are
VERIFIED. Row 9 now ships as "Mars is a cold world" beside "red from rust", with "not because it is hot" dropped. Row
10's guard no longer mentions white balance. Two traps on the pages: APOD's caption explains the dark areas as
„relatively smooth lowlands" — do not reuse it; and ALPO's prose says the disc peaks „on July 01, 2027", which its own
table contradicts (13.8″ at closest approach on 2027-02-20) — do not cite that sentence.

**Data check for 1–3, done by challenger A on 2026-09-25 against `data/generated/orbital-positions.json`.**
Mars RA turns back on 2027-01-13 and forward again on 2027-04-04, inside the window 2026-09-08 → 2027-09-07.
Geocentric longitude from the Earth and Mars `helioLonDegrees` agrees within a day. The track crosses itself only over
about six months (Nov 2026 – May 2027); a shorter span draws a hook. It lies beside Regulus, in real background stars.

**Not adopted (ticket 004 "Out"):** falling on Mars (R7), Mars seasons (R8), Phobos (R9). No new claim from them.
