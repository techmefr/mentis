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
   frame; move it to where the data changes. `build` is called far more often than the code reading it
   suggests — a parent rebuild, a rotation, a theme change, a keyboard appearing — so anything in it is
   priced per frame rather than per user action.
5. **Narrow the rebuild scope**: one builder wrapped around the whole screen rebuilds everything on any state
   change. Split into targeted builders with a rebuild condition, and keep changing state close to the widgets
   that read it.
6. **`setState` rebuilds the widget it is called on, all of it.** Held at the top of a screen for a value one
   small control owns, it is the same failure as point 5 arriving through the stateful widget instead of the
   state holder: push the state down to the smallest widget that owns it, and the framework does the rest.
7. **A rebuild is cheap; a repaint is not always.** The framework diffs widget descriptions, so a rebuild
   that produces an identical tree costs very little — which is why chasing rebuild counts can miss the
   actual cost. Opacity, clipping with rounded corners, shadows and especially blur force the renderer to
   allocate a separate layer each frame, and one of those inside a scrolling list is the usual cause of jank
   that no amount of `const` fixes.
8. **Profile before claiming a performance win.** If jank is reported, confirm it with the performance overlay
   or the devtools timeline rather than asserting that a const fixed it (`skills/webperf`: diagnose from a
   measurement).
9. **A key decides identity.** Without one, the framework matches children by position, so inserting,
   removing or reordering hands one child's element — and therefore its state, its scroll offset, its
   animation — to a different child. In a list this is §6.4; in a `Stack` or a conditional it is why a
   half-filled field appears under the wrong label.
10. **`initState` runs once, and a widget's fields can change.** Copying a constructor parameter into state
    there and reading the copy afterwards means the widget ignores every later value its parent passes — the
    screen shows the first record it was given for ever. Handle the change in the update callback, or don't
    copy at all.
11. **Inherited state is not available in `initState`.** A theme, a media query or a provider looked up
    there either throws or registers no dependency, so a later change never reaches the widget. That lookup
    belongs in the dependency-change callback, or in `build`, where the framework can track it.
12. **A `builder` gets its own context; use that one.** Reaching for the enclosing context inside a builder
    resolves against a scope that does not contain what the builder introduced, which is how a dialog opens
    without the theme or the localisation it was supposed to inherit, or how a sheet cannot find the
    navigator it is sitting in. The rule generalises: use the innermost context available.
13. **A `GlobalKey` is a global variable with a layout cost.** Moving one across the tree tears down and
    rebuilds the subtree it identifies, and needing one is usually a sign that state is being reached for
    sideways instead of being owned somewhere and passed down (§7.11).
14. A reusable presentation widget is **dumb**: it renders its parameters and calls its callbacks, with no
    business knowledge and no data fetching. Where a shared UI kit exists, check it first — a hand-built
    equivalent of a kit component is a visual divergence plus a maintenance cost, and it will not follow the
    kit when the kit changes.
15. **A widget that fetches cannot be reused and cannot be tested cheaply.** The data-fetching version needs
    a network faked before a single assertion about its layout is possible, while the dumb one is exercised
    by passing parameters — which is the practical reason point 14 is a rule and not a preference.
16. **`build` must be free of side effects.** Starting a request, emitting to a state holder, showing a
    snack bar or creating a controller (§1.9) inside it happens once per frame rather than once per
    intention, and the symptom scales with how often the screen happens to rebuild — a loop that looks like
    a backend problem.
