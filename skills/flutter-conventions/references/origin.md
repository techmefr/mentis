# flutter-conventions — origin and source stamps

> Provenance of `skills/flutter-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

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
