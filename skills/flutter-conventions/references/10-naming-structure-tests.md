# flutter-conventions §10 — Naming, structure, tests

> Section 10 of `skills/flutter-conventions`. Read it when a file is placed or named, or tests are written. The other sections and the guardrails stay in `SKILL.md`.

1. House casing per artefact kind (files, folders, classes, widgets, state holders, states, events, entities,
   gateways, use cases, data sources, variables, constants, enums, tests), applied without exception. The
   value is that a name becomes a type: seeing the symbol tells you what kind of thing it is and therefore
   which rules apply to it, without opening the file.
2. **A convention a person has to remember is a convention that drifts.** The analyzer enforces most of
   this, so it belongs in the project's lint configuration rather than in a reviewer's attention — and the
   same applies to the import boundary of point 3, which a dependency lint can check and a human cannot,
   reliably, on a large diff.
3. Separate **technical/shared** layers from **functional/business** ones, one folder per feature, and no
   technical layer importing a functional one. The direction is the whole point: a technical layer that
   reaches into a feature can no longer be reused by the next feature, and the cycle it creates is
   discovered later as a build error naming neither file.
4. **The deletion test tells you whether the folders are right.** If removing a feature means editing files
   in five places, the tree is organised by technical kind rather than by feature, and every future change
   to that feature pays the same tax. A `utils` or `common` folder is where this begins — it is a name that
   means "no concept", so it accumulates.
5. **Widget tests** for a component's behaviour: pump it, locate by key or type rather than by rendered text
   where the text is translated, drive the interaction, then assert. Match the pump to what you're testing —
   pump once for static rendering; pump again after an interaction for a state change; advance time explicitly
   for animations and async updates; and scroll an off-screen item into view before expecting to find it,
   because a lazy list hasn't built it yet.
6. **A test that has never failed proves nothing.** Write it red, or break the behaviour once and watch it
   go red, before trusting it. A test asserting something already true is worse than no test: it occupies
   the place where the real one would have been, and it reports success for ever.
7. **Fake every boundary the widget does not own** — network, storage, permissions, the clock, the platform
   channels. A widget test that reaches a real network is slow, fails on someone else's connection, and
   fails for a reason that has nothing to do with the widget; a suite with a few of those is a suite people
   learn to re-run rather than read.
8. **Freeze time and randomness.** A test reading the real clock fails at midnight, on the first of the
   month, in a different timezone, or on a leap day — and it fails in CI, where nobody is watching, which
   makes it look like flakiness rather than a dependency on the clock.
9. **Each test stands alone.** A service locator, a global provider or a singleton left registered by the
   previous test makes the order matter, so the suite passes in the order it was written and fails in the
   order the runner chooses. That then reads as infrastructure trouble instead of as the coupling it is.
10. **Assert the refusal, not only the success.** The denied permission, the unauthorised state, the
    validation that must reject — those are the paths that become incidents rather than bugs, and a suite
    that only ever exercises the happy path proves the feature works while saying nothing about who can
    reach it.
11. **Test the states that ship broken.** Each of §4's four states deserves an assertion, and loading,
    empty and error are precisely the ones a developer never sees against a fast local backend. A screen
    tested only in its success state is a screen whose skeleton overflows on the day the network is slow.
12. **A pump that is too short passes for the wrong reason.** Asserting while a transition is still running
    finds the old frame, or finds the new one by luck depending on the machine. Advance the clock by the
    animation's own duration rather than by a number that happened to work.
13. A test that awaits a frame settles deliberately: an unconditional settle on a screen with a repeating
    animation cannot succeed. In a widget test it fails in under a second — the settle advances a *fake*
    clock and gives up after ten minutes of it — and the message names the settle rather than the
    animation, so the obvious move is to allow it more time, which cannot work; on a device, in an
    integration test, the clock is real and it hangs instead. Either way it is the test-side symptom of
    §9.9 — an animation nothing stops — so it is usually pointing at a real defect rather than at itself.
14. **Golden tests need their inputs pinned.** A screenshot comparison depends on the font, the device size
    and the platform's text rendering, so an unpinned golden fails on the next machine and gets regenerated
    until it asserts nothing. Use them deliberately, for the few layouts where a pixel difference is the
    thing being protected.
15. **Integration tests** for the journeys that must not break, run on a real device or emulator. Keep them
    few and keep them about journeys: they are the slowest thing in the pipeline, and a slow suite is a
    suite that gets skipped — so its speed is part of its design, not an afterthought.
16. For *what* to test — plan first, exhaustive rather than happy-path, the permission matrix, the coverage
    floor — see `skills/tdd`. Coverage there is a smoke detector and not a target: a line executed is not a
    line asserted, and a high number produced by tests that call code without checking outcomes is more
    dangerous than an honest lower one, because it retires the question.
17. **Locate by key, not by type, for anything the framework also builds.** A finder for a widget type
    matches the framework's own copies of it as well as yours — a page transition contributes its own fade
    to every screen, so a count of four comes back as eight — and a screen with a single text field has
    two scrollables in it, so a scroll-until-visible helper cannot tell which one to drive and fails with
    a framework error naming neither the test nor the widget. Scoping the finder to a key, or to a
    descendant of one, is what makes it mean what it reads as.
18. **The composition root is a third place, and neither layer of point 3 can hold it.** The centralised
    route table of §5.1 imports every feature's screens by construction, so it cannot live in the
    technical layer that point 3 forbids from importing a feature; and it belongs to no single feature, so
    it is not a functional one either. The same goes for the dependency wiring, the crash reporter, the
    localisation delegates and the application widget itself: assembled once at startup, importing both
    layers, imported by neither. Give them their own top-level folder, or the direction point 3 exists to
    protect is broken by the first route added.
19. **A negative assertion is a separate claim from a positive one, and skipping it is how a stub silently
    becomes the behaviour.** Verifying that a call happened is not evidence that it happened *once*, or that
    a related call did not also happen — a mock double that never asserts `verifyNever` on the branch that
    must not fire lets a duplicate write or a duplicate network call through, since nothing in the suite
    would fail if it did.
20. **The test tree mirrors the source tree, one file per file, or a moved source file orphans its test.**
    A test suite organised by kind of test rather than by mirrored path (one flat `widget_tests` folder,
    say) means renaming or relocating a source file leaves its test behind with no build error to catch it
    — coverage tooling still reports the number as if the test were exercising the current file, when it is
    quietly exercising nothing.
21. **A golden file's name and location are part of the contract, not an implementation detail of the
    comparison.** Point 14's golden tests are pinned by rendering inputs; they are also pinned by where the
    reference image lives and what it is called, since a renamed test silently starts comparing against
    nothing and regenerates a fresh "reference" that never questioned the regression it was meant to catch.
    Keep goldens beside the test that owns them and treat a rename of either as a rename of both.
22. **An integration test needs its own entrypoint and driver, and skipping either runs nothing.** Point
    15's device-level journeys are driven through a harness separate from the widget-test one — a runner
    invoked without the integration driver configured reports green having executed zero of the journeys it
    was meant to guard, which is a worse failure than red because nothing about the report says so.
23. **`tester.view` (or `tester.viewOf` for a specific view) is the current seat for what used to be read off
    a single implicit window.** A test that stubs a device size or a text-scale factor through the older
    binding-level window property is pinning a value the multi-view-capable framework no longer reads from
    there by default in the same way; the per-view test properties are what a size- or scale-dependent
    widget test (points 12, 14) actually needs to control, and reaching for the deprecated seat is how such a
    test passes locally and stops controlling anything after an SDK upgrade.
24. **Arrange, act, assert, in that order and visibly separated**, is what makes a failing test's diff
    readable without re-deriving the setup: a test that interleaves stubbing calls between actions makes it
    unclear which piece of the arrangement was in effect when the assertion ran, and unwinding that at the
    moment a test is red is the worst time to be doing it.
