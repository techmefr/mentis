---
name: flutter-conventions
description: Use when writing or reviewing Flutter/Dart, BuildContext across async gaps, disposing controllers and subscriptions, widget decomposition, const and rebuild scope, layout constraints and overflows, responsive layout, the four async UI states, navigation and back handling, lists and pagination, forms and keyboard, gestures and touch targets, safe areas, state management, secure storage and runtime permissions, on-device storage, i18n, crash reporting, naming and layered structure, widget and integration tests. Self-contained, it assumes no plugin, UI kit or catalogue installed.
---

# flutter-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Flutter/Dart code. **Special
status**: no production mobile experience behind this block — content comes from the framework's own
documentation, its analyzer lints and an org catalogue for the stack. The matching reviewer (`faramir`) asks
questions rather than asserting, for the same reason.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue and a shared UI
kit, both are the authority — **its** components, its SDK, its structure — and override this block wherever
they differ. A shared UI kit in particular inverts several rules below: where one exists, its component is
preferred over the raw framework widget, and the generic advice here applies only to what the kit doesn't
cover. Internal package names are deliberately absent (rule C).

## When
As soon as a widget, a screen, a state holder, a repository or a route is written or modified, during
`code` (6) or `tdd` (5).

## Steps

### 1. The two mistakes that crash in production
1. **`BuildContext` after an `await` is not guaranteed valid.** Navigation, snack bars, dialogs, theme or
   media-query reads, provider lookups — anything `context.` — after an asynchronous gap must be guarded by a
   mounted check, or the context captured before the gap where that's sound. The widget may be gone by the
   time the future resolves, and the crash lands in a completely unrelated place.
2. **Every disposable resource held by a widget is disposed**: text/scroll/page/tab/animation controllers,
   focus nodes, stream subscriptions, timers, platform listeners. Created in `initState`, released in
   `dispose`, one for one. This is the single most common leak, and it doesn't show up in a test that never
   unmounts the widget.

### 2. Widgets
1. **Split a long `build` into small widget classes**, each in its own well-named file under the feature's
   widgets folder — not into private `_buildXxx()` methods. A method returning a widget rebuilds with its
   parent and can't take a `const` constructor; a class can do both and can be tested.
2. `const` constructors wherever the widget's inputs are compile-time constant: it lets the framework skip
   rebuilding that subtree entirely.
3. Keep the rebuild scope small: the state that changes lives as close as possible to the widgets that read
   it, rather than at the top of the screen where every change repaints everything.
4. A reusable presentation widget is **dumb**: it renders its parameters and calls its callbacks, with no
   business knowledge and no data fetching. Where a shared UI kit exists, check it first — a hand-built
   equivalent of a kit component is a visual divergence plus a maintenance cost.

### 3. Layout
1. Unbounded-constraint errors (`RenderFlex overflowed`, a viewport given unbounded height, infinite width)
   are **constraint** problems, not styling problems: read what the parent passes down before adding a fixed
   size. A hardcoded height that makes the error go away is the bug moving to another device.
2. `Expanded`/`Flexible` inside a flex, `ConstrainedBox` where a bound is genuinely needed.
3. Adapt to the available window size (a layout builder, a size query, width breakpoints) rather than
   assuming a phone: tablets, desktop windows and foldables all arrive as "the same app".
4. Lay out around system UI explicitly: safe areas for notches, status bar and home indicator, and know the
   difference between the padding a system inset reserves and the inset the keyboard adds.
5. Touch targets meet the platform's minimum size. An icon wrapped in a bare gesture detector is usually
   too small and has no ripple feedback; prefer a real button widget (or the kit's).

### 4. Screen states
1. **An async view renders all four states explicitly: loading, success, empty, error.** Never a blank
   screen, never stale content presented as fresh. This is the rule that makes a mobile app feel finished.
2. A useful empty state: an illustration or icon, a short explanation, and the primary action that would
   fill it. "No data" alone tells the user nothing to do.
3. A friendly error state with a **Retry** — a raw exception string on screen is a bug report shown to a
   customer.
4. Prefer content-shaped skeleton placeholders over a centred spinner for content that has a known shape:
   the layout doesn't jump when the data lands.

### 5. Navigation
1. **Centralised declarative routing**, one place that maps routes to screens, rather than imperative pushes
   scattered across widgets. Arguments are typed, not passed as an untyped map.
2. Guards/redirects (auth, onboarding) declared with the route, not checked in each screen's `initState`.
3. Deep links and notification taps are entry points into the same route table, including the cold-start
   case — the tap that launches the app is the one that's usually forgotten.
4. Back handling is explicit where it matters: confirm before leaving a screen with unsaved changes,
   intercept the system back deliberately, and never trap the user with no way out.
5. Tabbed/bottom navigation **preserves each tab's state and scroll position** across switches — losing a
   half-filled form on a tab switch reads as a broken app.

### 6. Lists and forms
1. A long list uses the lazy builder, never a fully materialised children list.
2. Paged list: load the next page near the end, show a loading footer, mark the end of the list, and handle
   the error-mid-scroll case. Pull-to-refresh resets to the first page.
3. A form field validates through the form's own validator mechanism, showing **inline per-field errors**,
   not one global message.
4. Choose the validation timing deliberately (on submit, or as-you-type after first interaction); validating
   from the first keystroke flags an empty field the user is still typing into.
5. Disable the submit control while a submission is in flight — a double tap is one order twice.
6. Keyboard: avoid covering the focused field, scroll it into view, set the right keyboard type and action
   (next/done), and let a tap outside dismiss.

### 7. State management
1. Prefer the **simplest state holder** the framework's chosen library offers for ordinary UI state (a
   Cubit-style holder over a full event/stream Bloc). Reach for the event-driven form only when there really
   is stream processing, debouncing or event replay to do.
2. State classes are immutable and exhaustive: the widget maps a state to a UI, and every state has a
   rendering (see §4).
3. View logic (formatting, deriving a label) belongs to the state holder or a pure function, not inside
   `build`.
4. No business logic in a widget, and no widget import inside a state holder: the state layer must be
   testable without the UI.

### 8. Data, storage, permissions
1. **Sensitive data on device goes in secure storage**: auth and refresh tokens, passwords, API secrets,
   biometric-gated secrets, personal data. Plain preferences storage is not encrypted — anything in it should
   be safe to read.
2. Ordinary preferences (flags, last-selected filter) go in the preferences API, keys centralised as
   constants rather than typed as literals at three call sites.
3. On-device SQL: migrations handled explicitly on version upgrade, writes batched or wrapped in a
   transaction, conflict behaviour stated rather than defaulted.
4. **Runtime permissions handle every branch**: granted, denied, permanently denied (which needs a route to
   the system settings), and restricted. Requesting a permission at app start, before the feature needing it
   is visible, is how a user learns to deny it.
5. Remote images go through a caching image widget with a placeholder and an error widget, and a decode size
   bounded to what's displayed — a full-resolution image decoded into a thumbnail is the classic memory
   spike.
6. Where the backend is a known REST convention, generate or centralise the client once; each screen calling
   the HTTP layer by hand is where the contract drifts.

### 9. Text, motion, monitoring
1. No user-facing string hardcoded in a widget: text, dates, numbers and currency go through the
   localisation layer with typed keys. Currency and date formats are locale rules, not string formatting.
2. Implicit animations by default; an explicit animation controller only where the motion genuinely needs
   driving — and it's disposed (§1.2).
3. Crash and error reporting initialised once at startup, with the environment and release stamped, sampling
   configured deliberately, and payloads scrubbed of personal data before they leave the device.
4. Prefer hand-written code over code generation where the project has taken that position, and don't
   introduce a generation step (and its generated files, its build config, its watch mode) for one model.

### 10. Naming, structure, tests
1. House casing per artefact kind (files, folders, classes, widgets, state holders, states, events, entities,
   gateways, use cases, data sources, variables, constants, enums, tests), applied without exception.
2. Separate **technical/shared** layers from **functional/business** ones, one folder per feature, and no
   technical layer importing a functional one.
3. **Widget tests** for a component's behaviour: pump it, find by key or type rather than by rendered text
   where the text is translated, drive the interaction, assert the four states of §4.
4. **Integration tests** for the journeys that must not break, run on a real device or emulator.
5. A test that awaits a frame settles deliberately: an unconditional settle on a screen with a repeating
   animation never returns.
6. For *what* to test — plan first, exhaustive rather than happy-path, the permission matrix, the coverage
   floor — see `skills/tdd`.

## Output / checkpoint
Code compliant with the sections above, analyzer clean, no new lint introduced by the diff. Checked by
`gate` (7) and by `faramir` at review time in the `review` step (8).

## Guardrails
No comments in the code produced. Where a shared UI kit exists, **its component wins over a raw framework
widget** — and over the generic advice here. This block has never been confronted with a real production
Flutter project: if a rule diverges from a real observed need, fix this block rather than treating it as
settled, and prefer a question to an assertion when reviewing (that's `faramir`'s register too). Where an org
catalogue is installed and disagrees, **it wins**.

## Origin
Ideas taken from: **an org skill catalogue for this stack (37 skills: BuildContext across async gaps, resource
disposal, widget decomposition, const and rebuild scope, layout constraint diagnosis, responsive layout, safe
areas and insets, the four async UI states, empty and error states, skeleton loading, centralised declarative
routing, deep links, back handling, tab state preservation, lists and pagination, form UX, keyboard handling,
gestures and touch targets, Cubit-first state management, secure storage, preferences, on-device SQL, runtime
permissions, cached network images, i18n, motion, crash reporting, code-generation stance, naming, layered
structure, generic widgets, user feedback, widget tests, integration tests)** — rules extracted, de-identified
and rewritten generically, with the internal UI kit, SDK and third-party product names deliberately left out
(rule C); the framework's own documentation for the mechanisms cited. Mechanisms rewritten, no copied text.
Stamped 2026-08-06.

**Fills a real gap**: `faramir` was written deferring entirely to the plugin, on the explicit basis that
mentis wrote no mobile block. That basis no longer holds — this block is the mentis-side default for a
project with no catalogue installed.
