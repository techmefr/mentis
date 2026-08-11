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

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

## When
As soon as a widget, a screen, a state holder, a repository or a route is written or modified, during
`code` (6) or `tdd` (5).

## Steps

### 1. The two mistakes that crash in production
**After any `await`, the `BuildContext` is suspect.** Navigation, snack bars, dialogs, theme or media-query
reads, provider lookups — anything `context.` — needs a guard before it's touched again.
1. It fails in two ways, and the second is worse: it **throws** ("this widget has been unmounted", "looking up
   a deactivated widget"), or it **silently misfires** — the snack bar appears on a scaffold nobody can see,
   the dialog opens on a dead navigator, the lookup resolves against a disposed scope. And it's **invisible in
   review**, because the code reads as straight-line; the bug only appears when the user navigates away
   mid-request.
2. **Three correct shapes, by where you are.** In a stateful widget: check `mounted` **between the await and
   the context use** — a check placed before the await is useless, since the widget unmounts *during* it, and
   the plain `mounted` getter is the right one there. In a stateless widget: **capture what you need before
   the await** — the navigator or messenger object, not the context. In a state holder (cubit/bloc): don't
   touch context at all — emit, and let the widget listen.
3. **Never store a `BuildContext` in a field** to use later: a stored context is stale by definition. Store
   the derived object instead.
4. **Never silence the analyzer's async-context lint with an ignore comment.** It's a latent crash, not a
   style nit — satisfy the lint.

**Every disposable resource a widget creates, that widget releases.** Text/scroll/page/tab/animation
controllers, focus nodes, stream subscriptions, sinks, timers, tickers, and any state holder it created
itself.
5. Why it matters beyond tidiness: a controller registers listeners and an animation drives a ticker off the
   scheduler, so neither is collected; an uncancelled subscription **keeps invoking its callback after the
   widget is gone**, and that callback often calls `setState` on a dead widget; and several of these assert on
   leak in debug builds, so the report arrives far from the cause.
6. **Store the subscription handle.** Fire-and-forget `stream.listen(...)` cannot be cancelled, which is the
   same bug as not cancelling it.
7. **`super.dispose()` goes last** — release your own resources first.
8. **Never dispose what you didn't create.** A controller passed in through the constructor belongs to the
   caller, and a state holder owned by a provider is closed by that provider — disposing either is a
   double-dispose crash in a different file.
9. **Never create a controller, future or stream in `build`**: a fresh instance every rebuild, none of them
   disposed. Hoist it to `initState` or a late final field.
10. When you add a resource to an existing widget, **wire its teardown in the same edit** — never "for later".
    And if you're already editing a `dispose()` and spot a created-but-unreleased resource, fix it there:
    that's bundled cleanup, not a drive-by.

### 2. Widgets and rebuilds
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

### 3. Layout
1. Unbounded-constraint errors are **constraint** problems, not styling problems: read what the parent passes
   down before adding a fixed size. A hardcoded height that makes the error go away is the bug moving to
   another device.
2. **The messages map to specific causes**, which is what makes them fast to fix rather than mysterious: a
   *scrollable given unbounded height* means it sits inside another unconstrained scrollable or an
   unconstrained column — give it a bounded slot (`Expanded`) rather than a fixed height; an *input that
   cannot have unbounded width* is the same shape horizontally; *flex overflowed* means a child asked for more
   than the parent allotted — make the child flexible or let it wrap; *incorrect use of a parent-data widget*
   means a positioning widget isn't a direct child of the ancestor that reads it; and **a "not laid out" error
   is a cascade, so ignore it and look further up the stack for the real constraint failure**.
3. `Expanded`/`Flexible` inside a flex, `ConstrainedBox` where a bound is genuinely needed.
4. Adapt to the available window size (a layout builder, a size query, width breakpoints) rather than
   assuming a phone: tablets, desktop windows and foldables all arrive as "the same app".
5. Lay out around system UI explicitly: safe areas for notches, status bar and home indicator, and know the
   difference between the padding a system inset reserves and the inset the keyboard adds.
6. Touch targets meet the platform's minimum size. An icon wrapped in a bare gesture detector is usually
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
   is stream processing, debouncing or event replay to do — loading a list, submitting a form, deleting an
   item are all a plain method call, not an event: reach for the event queue only when calls genuinely need
   ordering (a search box, a stream, anything that must drop or replace an in-flight call).
2. **The event-driven form's actual reason to exist is controlling a burst of rapid calls**, not ceremony: a
   plain method call can't be cancelled once made, so three fast calls make three requests, full stop. An
   event queue can apply a policy on what arrives while one is already in flight — process in parallel
   (the default), one at a time in order, drop what arrives while busy, or abandon the in-flight one and
   restart on the newest. A live-search field is the canonical case: only the latest keystroke's result
   matters, so the earlier in-flight calls are abandoned, not merely ignored on arrival (which would still let
   a slow early response overwrite a fast late one).
3. State classes are immutable and exhaustive: the widget maps a state to a UI, and every state has a
   rendering (see §4). Prefer one status enum over independent booleans (`isLoading`/`hasError`) that can
   contradict each other; equality on the state class must hold, or the widget won't rebuild on a genuinely
   new state and appears to ignore an emitted change — mutating a list in place before re-emitting it is the
   common way to break that equality by accident, since the "old" and "new" state then hold the same instance.
4. View logic (formatting, deriving a label) belongs to the state holder or a pure function, not inside
   `build`.
5. No business logic in a widget, and no widget import inside a state holder: the state layer must be
   testable without the UI — including no `BuildContext` and nothing UI-owned (a text controller, a
   `GlobalKey`) inside it. Those belong to the widget that created them and are disposed there (§1); the state
   holder receives their derived value, not the controller itself.
6. **Check whether the state holder is still alive before emitting after any `await`** — the same shape as
   the `BuildContext`/`mounted` guard in §1, one layer down: a screen closed mid-request must not crash the
   next emit.
7. **A one-time reaction (navigation, a snackbar, a dialog) belongs to a listener, never to the builder that
   renders the UI.** A builder can be re-invoked at any time for reasons that have nothing to do with the
   state changing (a parent rebuild, a rotation) — code in it that reacts instead of rendering re-fires on
   every one of those, and a listener condition must compare the previous and current state, not just inspect
   the current one, or the same one-time reaction re-fires every time that state is revisited.
8. Guard the double-submit case in the state holder, not the button: a status already "in flight" makes the
   next call to the same method a no-op, and that status is what disables the button too — one source of
   truth for both.

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
3. **Widget tests** for a component's behaviour: pump it, locate by key or type rather than by rendered text
   where the text is translated, drive the interaction, then assert. Match the pump to what you're testing —
   pump once for static rendering; pump again after an interaction for a state change; advance time explicitly
   for animations and async updates; and scroll an off-screen item into view before expecting to find it,
   because a lazy list hasn't built it yet.
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
**Deepened 2026-08-06.** The first pass wrote this block from the catalogue skills' descriptions. This pass
read the **bodies**, which is where the reasons, the exclusion lists, the carve-outs and the anti-pattern
catalogues live — a description states the rule, a body states when it doesn't apply. What that added here: the two failure modes of a stale
`BuildContext` (throwing versus silently misfiring on an invisible scaffold), the three correct shapes by
context, the check-between-not-before rule, never storing a context, why disposal matters mechanically
(tickers, callbacks outliving the widget, debug leak assertions), never disposing what you didn't create, why
a helper method can never be skipped while a widget class can, and the mapping from each constraint error
message to its actual cause — including that a "not laid out" error is a cascade to be ignored in favour of
the one above it. Stamped 2026-08-06.

**Fills a real gap**: `faramir` was written deferring entirely to an org catalogue, on the explicit basis
that
mentis wrote no mobile block. That basis no longer holds — this block is the mentis-side default for a
project with no catalogue installed.

**§7 deepened 2026-08-11** from the real house doc (doc.stacktim.com, `/developer/nos-methodes/flutter/bloc`,
read that date) — unlike the rest of this block, that page is written from the company's own real production
use of `flutter_bloc`, not from a catalogue description. It sharpened three things this block only had
generically: **why** the event-driven form exists at all (a plain method can't be cancelled once made; the
event queue's point is choosing a policy — parallel, ordered, dropped, or restarted — for calls that arrive
while one is already in flight, a live-search field being the case that actually needs "abandon the in-flight
one"), the **liveness check before an emit after `await`** as the direct analogue of §1's `mounted` guard one
layer down, and the **listener-must-compare-transitions-not-states** rule (comparing only the current state
re-fires a one-time reaction every time that state is merely revisited, not just when it's newly reached).
Kept generic per rule C — no internal package name, `flutter_bloc` itself is the framework's own chosen
library, not a company one.
