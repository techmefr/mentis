# § 1 — Measure before touching anything

> Section 1 of `skills/webperf`. Read it before changing anything for speed.

1. **Reproduce the slowness and get a number.** Which page, which interaction, how long, on what
   connection and what device class. "The list is slow" isn't actionable; "the list takes 4s to first
   render with 500 rows" is.
2. **Find where the time actually goes** before forming a theory: network waterfall (how many
   requests, which ones block), main-thread work, render count. The bottleneck is regularly not
   where it feels like it is.
3. **Write the number down.** Without a before, there's no after, and "it feels faster" is how a
   change that made things worse gets shipped.

