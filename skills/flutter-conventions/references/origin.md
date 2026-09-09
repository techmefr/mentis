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

**Dogfooded once, 2026-09-09.** A small Flutter app was written against this block as its only reference:
it reads a bundled JSON catalogue of this repo's own blocks and shows each one's source stamp as a
freshness, with a filter, a paged list, a detail screen reached by identifier, a first-run threshold
behind a route guard, and one setting. Cubits for state, declarative routing, the framework's own
localisation generator, platform preferences for the setting. 45 Dart files, 3,419 lines, **63 tests
green**, `flutter analyze` clean under `flutter_lints`, on the `ghcr.io/cirruslabs/flutter:stable` image
(Flutter 3.44, Dart 3.12) with nothing installed on the host. It lives outside this repo, with its
findings beside it.

**The router held up, with one honest exception.** §8's permissions half never applied — the app asks the
platform for nothing — and §1's *first* half never applied either, which turned out to be a finding rather
than an omission (see §7.19). The other eight sections were all touched.

Seven gaps came back, all closed here, and five of the seven were found by a failing test or a failed
build rather than by reading:

- **`on Exception` misses half of what the framework throws.** The boundary that maps a load failure onto
  §4's states, written the disciplined narrow way, let a `FlutterError` for a missing asset straight
  through — `Error` is not `Exception`, and neither are a failed assertion, a bad cast or an unassigned
  `late` read. Found by a test that expected the mapped state and got the raw framework error (§7.18).
- **An awaited call into the holder does not say whether it worked.** Once §7.5 puts the failure in the
  state, the method completes normally either way, so a screen that awaited a save and then left, left on
  a failed save too. Found by a failing test; fixed by moving the reaction to §7.15's listener — which
  also removed the only `await` the widget had, and with it the need for §1's guard (§7.19).
- **A status enum plus a nullable payload keeps the impossible combination representable**, so the widget
  asserts on the payload or invents a rendering for a state that cannot happen. Sealed types remove it;
  the enum was still the right answer for the flags (§7.20).
- **A parse moved off the main isolate (§8.9) is invisible to a widget test.** The result comes back
  outside the harness's zone, so the future never completes and the test hangs to its timeout naming
  nothing. Confirmed both ways: it passes in a plain test, and inside the harness only with the real-async
  escape hatch. The seam a widget test fakes has to sit above the hop (§8.18).
- **The localisation layer is generated code and it pins its own dependency.** §9.1's typed keys come from
  the framework's generator, which is the step §9.15 says not to introduce; and the SDK's localisation
  package pins one exact version of the formatting library, so adding it the ordinary way makes the
  project unresolvable while blaming the SDK. Found by the resolver (§9.16).
- **An unconditional settle does not hang in a widget test, it fails in under a second** — the settle
  advances a fake clock and gives up after ten minutes of it, with a message naming the settle rather than
  the animation. §10.13's mechanism was right and its symptom was wrong, which sends the reader looking
  for the wrong thing; on a device it does hang. Also: `find.byType` matches the framework's own copies of
  a widget (a page transition contributed four extra fades), and a screen with a text field has two
  scrollables, so a scroll helper cannot tell which to drive (§10.13 corrected, §10.17).
- **The composition root has nowhere to live in §10.3's two layers.** A centralised route table imports
  every feature's screens, so it is not technical; it belongs to no feature, so it is not functional. Met
  by construction on the first route (§10.18).

**The status still does not change.** 🟡 — one small app written by the same agent that wrote the block is
not the production mobile experience this file has always said it lacks, and `faramir` keeps asking
questions rather than asserting. What the exercise bought is seven mechanical defects, five of which only
a compiler or a test could have surfaced, and evidence for the rules that held: §4.13's forced-failure
switch made all four screen states reachable, §6.7's in-flight flag turned three triggers in one frame
into one request, and §9.8's reduce-motion fallback is the only reason a settle on the loading screen
returns at all.

**Widened against Riverpod's current codegen surface, 2026-09-09.** Same method as `csharp`/`design-patterns`/
`react`/`python` the same week: checked against the state-management library's current documented behaviour,
not against the catalogue, since §7's Cubit-first guidance predates `@riverpod` code generation becoming the
ecosystem default. Three points added: a generated provider disposes itself the instant nothing watches it
unless `keepAlive: true` says otherwise, which is point 12's scope decision made *for* the author by default
rather than by them; `ref.watch` (rebuild on change, inside `build` only) and `ref.read` (current value once,
outside `build`) are different questions, and `read` inside `build` silently opts a widget out of the
rebuild contract point 3 states; and a family provider's cache key uses the parameter's own equality, so a
parameter without `==`/`hashCode` refetches on every call even for identical values — point 11's
one-owner-per-data rule broken by the provider layer itself. Nothing added here answers the catalogue
comparison a second time.
