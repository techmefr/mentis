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

**§7 deepened 2026-08-11** from the company's own internal house documentation (its Flutter BLoC page,
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

**Depth pass 2026-09-08 — all ten sections.** Same method as the nuxt, laravel and react blocks: every
original point kept verbatim and given the mechanism plus what the user or the next reader actually sees
when the rule is broken, with new points written only where a section was *silent* on a failure mode rather
than terse about one. Before → after: §4 screen states 138 → 951 words, §9 text/motion/monitoring 144 →
892, §5 navigation 157 → 949, §6 lists/forms 168 → 965, §8 data/storage/permissions 217 → 1,045, §10
naming/structure/tests 218 → 955, §3 layout 299 → 993, §2 widgets/rebuilds 316 → 892, §1 the two crashing
mistakes 494 → 921, §7 state management 571 → 1,100. Router plus the ten sections: 3,380 → 10,321.

What this pass added that the block had no line about at all — the mobile-specific failures, since the
generic ones were already here. **The device is not yours**: a secure-storage read can fail because the
platform keystore was cleared by a biometric re-enrolment or a restore, so a token written successfully is
unreadable later and the honest response is "not signed in" rather than a crash loop on launch (§8.2);
logging out has to clear what the session wrote, because the next person holding a shared phone is a
different user (§8.3); the process is terminated in the background as a matter of course, which is why the
route table has to rebuild from a path (§5.14) and why a long form deserves a draft (§6.18); and a
permission can be revoked from the settings app while the app is backgrounded, so it is checked at the point
of use rather than cached at launch (§8.13). **The system prompt is often a one-time chance** per install,
which makes a prompt fired before the user understands why a permanent no (§8.12).

On the UI side: an overflow is silent in release builds, so a layout that only breaks on a small device or
a long translation ships without a word (§3.6); the reader's font-scale setting can make every label
substantially taller, so a row that fits exactly at the default overflows for the users who most need the
app to work (§3.10); a media query answers a question about the *window*, so a widget inside a dialog or a
split view that sizes itself from it is using a number that does not apply — which is the cause of most
"works on the page, not in the modal" reports (§3.8). Clipping an overflow is not fixing it (§3.5). And the
four async states belong to each data source rather than to the screen, or the working half of a screen is
hidden by the failing half (§4.2) — with empty having two causes that need different words, since showing
the first-run invitation to someone with an active filter reads as data loss (§4.4).

On correctness: `initState` runs once, so copying a constructor parameter into state there means the widget
ignores every later value its parent passes (§2.10); inherited state is not available in `initState` at all
(§2.11); a `builder` gets its own context and reaching for the enclosing one is how a dialog opens without
the theme it was supposed to inherit (§2.12); `dispose` runs even when `initState` threw halfway, so a
teardown that assumes everything was created throws a second exception that hides the first (§1.15); and
one guard per `await` rather than one per method, since two awaits are two windows (§1.3). A rebuild is
cheap and a repaint is not — blur and layered clipping inside a scrolling list is the usual jank no amount
of `const` fixes (§2.7).

**A defect found by doing the pass rather than by reading for it**: §9's animation rule cited `§1.2` for
disposal, and §1.2 is the *async-context* rule — the disposal half of §1 starts at point 5. It had been
wrong since the section was written. All thirty-six intra-block `§N.M` references were then re-checked one
by one against the current numbering; ten had been left pointing at the wrong rule and were corrected.
§1 was also restructured so its two halves are 1-7 (async context) and 8-17 (disposal) rather than 1-4 and
5-10, which is what moved most of those.
