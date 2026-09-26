---
name: back-cover-009
description: Ticket 009 back-cover claims (naked-eye worlds, dark adaptation, near-ecliptic, twinkling) and the Artemis II trap that makes "Apollo 17 was the last crewed lunar mission" false
metadata:
  type: project
---

Resolved 2026-09-26, recorded in docs/sources.md under "Back cover — seeing the worlds with your own eyes (ticket 009)".

- **Artemis II trap (durable).** Crewed lunar flyby, launched 2026-04-01, splashdown 2026-04-10, farthest humans ever (beat Apollo 13). So "last crewed lunar mission was Apollo 17" is FALSE; "beyond the Moon" is ambiguous. Safe: "last people to walk on the Moon = Apollo 17, Dec 1972" (re-check: Artemis III, 2027, is a LEO lander test, not a landing) and "nobody has travelled farther than the Moon".
- Twinkling: absolute "planets don't twinkle" = NOT ATTESTED; "usually steadier, tiny disc not point" = VERIFIED (EarthSky, APOD 2011-04-28, UW-Madison).
- Ecliptic latitudes are NOT in orbital-positions.json; derive from raHours/decDegrees with obliquity 23.4393. Window values: Moon ±5.29, Mars -0.33..+4.47, Jupiter +0.54..+1.07, Saturn -2.72..-2.23.
- Dark adaptation is search-excerpt only (Webvision NBK11525); page not read. Durations not pinned to one URL.

**Why:** the Artemis II change postdates much training data; the old Apollo-17 phrasing looks right and is now wrong.
**How to apply:** any "last/farthest human" claim gets checked against Artemis status first. Fetch note: this session's hook blocked WebFetch and bare curl; context-mode tools were not exposed to the subagent.
