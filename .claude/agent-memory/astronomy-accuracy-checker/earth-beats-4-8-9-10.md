---
name: earth-beats-4-8-9-10
description: Sources found 2026-09-09 for Earth beats 4 (year/solstices), 8 (gravity drop), 9 (telescope), 10 (day length) and the planets-outshine-stars claim — including three traps that would silently produce wrong content
metadata:
  type: project
---

Researched 2026-09-09 for `docs/design/earth-level-brief.md`. Values and URLs below
were pulled live that day; re-verify only if a number is challenged.

## The three traps (this is the part worth remembering)

1. **`helioLonDegrees` 0/90/180/270 does NOT map to March/June/Sept/Dec the way it
   looks.** Earth's heliocentric longitude is the Sun's geocentric longitude + 180°,
   so Earth λ = **0 → September equinox**, 90 → December solstice, 180 → March
   equinox, 270 → June solstice. Assuming 0 = vernal equinox mislabels every season
   by six months and the file still validates.
2. **The committed longitudes are J2000-ecliptic, not ecliptic-of-date.**
   `orbital-positions.py` calls `ecliptic_latlon()` with no `epoch=`. Measured
   offset at these epochs: **−0.383°**, i.e. the crossing lands **~0.39 day late**.
   Combined with 1-day sampling the naive crossing date is off by up to a day —
   March 2027 reads 03-21 when the equinox is 03-20. Fix is `epoch=t` in the script,
   or subtract the offset when deriving.
3. **Saturn straddles Earth in the NASA fact sheet.** Saturn "Gravity (mean, 1 bar)"
   = 11.19 m/s² (stronger than Earth) but "Acceleration (eq., 1 bar)" = 8.96
   (weaker). Jupiter 25.92 vs 23.12. The summary table's "Gravity" row publishes the
   _acceleration_ numbers. Any "on Saturn you'd fall slower/faster" claim is
   therefore unsourceable as stated — do not write one.

## NSSDCA fact sheets are redirecting

As of 2026-09-09 every `nssdc.gsfc.nasa.gov/planetary/factsheet/*` URL 302s to
`https://www.nasa.gov/nssdc/`. Last live Wayback captures are Aug 2025. Cite the
archived snapshot with its date, not the bare URL.

## Values captured (all m/s², NASA fact sheets, Aug 2025 snapshots)

Sun 274.0 (eq.) · Mercury 3.70 · Venus 8.87 · Earth 9.82 mean / 9.780 eq. ·
Moon 1.62 · Mars 3.73 mean / 3.69 eq. · Jupiter 25.92 mean 1 bar / 23.12 eq. 1 bar ·
Saturn 11.19 mean 1 bar / 8.96 eq. 1 bar. Earth: sidereal year 365.256 d, tropical
365.242 d, obliquity 23.44°.

## Live sources that worked

- Apollo 15 drop: science.nasa.gov/resource/the-apollo-15-hammer-feather-drop/ plus
  the Apollo Lunar Surface Journal, now at **apollojournals.org/alsj/** (the
  nasa.gov/history/alsj URLs redirect). GET 167:22:06 → 2 August 1971.
- Day length for Sofia: **USNO API** `aa.usno.navy.mil/api/rstt/oneday?date=…&coords=42.6977,23.3219&tz=…`
  returns rise/set JSON with no key. This is the cheapest citable day-length table.
- USNO `aa.usno.navy.mil/faq/seasons_orbit` states the tropical year is the basis of
  the civil calendar AND that solstices are when days are longest — one page covers
  beats 4 and 10.
- Sky & Telescope is 403 to scripts; fetch it through the Wayback Machine.

Related: [[settled-sources]], [[bulgarian-folk-figures]].
