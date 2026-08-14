# flutter-conventions §2 — Widgets and rebuilds

> Section 2 of `skills/flutter-conventions`. Read it when a widget is written, or a rebuild looks too wide. The other sections and the guardrails stay in `SKILL.md`.

1. **Split a long `build` into small widget classes**, each in its own well-named file under the feature's
   widgets folder — not into private `_buildXxx()` methods. The reason is mechanical, not stylistic: a helper
   method's widgets belong to the **parent's** element, so they rebuild with it and can never be skipped; a
   widget class is its own element and can be. A one-liner returning a single const child is fine.
2. **`const` wherever the subtree is constant.** A const widget is canonicalised and reused, so the framework
   recognises it as identical and skips it. A missing `const` the analyzer would have accepted is a free
   rebuild every frame.
3. **Put `const` on your own widget's constructor** when all its fields are final — omitting it blocks every
   caller from going const, which is the invisible version of the same cost.
4. **Keep `build` free of work.** Sorting, filtering, parsing or formatting inside `build` re-runs every
   frame; move it to where the data changes.
5. **Narrow the rebuild scope**: one builder wrapped around the whole screen rebuilds everything on any state
   change. Split into targeted builders with a rebuild condition, and keep changing state close to the widgets
   that read it.
6. **Profile before claiming a performance win.** If jank is reported, confirm it with the performance overlay
   or the devtools timeline rather than asserting that a const fixed it (`skills/webperf`: diagnose from a
   measurement).
7. A reusable presentation widget is **dumb**: it renders its parameters and calls its callbacks, with no
   business knowledge and no data fetching. Where a shared UI kit exists, check it first — a hand-built
   equivalent of a kit component is a visual divergence plus a maintenance cost.
