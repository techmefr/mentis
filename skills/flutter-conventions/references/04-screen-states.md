# flutter-conventions §4 — Screen states

> Section 4 of `skills/flutter-conventions`. Read it when a screen renders async data. The other sections and the guardrails stay in `SKILL.md`.

1. **An async view renders all four states explicitly: loading, success, empty, error.** Never a blank
   screen, never stale content presented as fresh. This is the rule that makes a mobile app feel finished.
   The mechanism behind that impression is that a mobile network fails constantly — a lift, a tunnel, a
   handover between cells — so the three non-success states are not edge cases here, they are the normal
   experience of the same screen over a week of use.
2. **The four states belong to each data source, not to the screen.** A screen with two independent
   requests has two sets of states, and collapsing them into one gate makes the whole screen wait for the
   slowest — including the parts that already have their data. It also produces the version of the bug
   nobody can reproduce: one request fails, the screen shows the error, and the working half is hidden.
3. A useful empty state: an illustration or icon, a short explanation, and the primary action that would
   fill it. "No data" alone tells the user nothing to do.
4. **Empty has two causes and they need different words.** Nothing exists yet — the first-run case, where
   the action is *create* — and nothing matched, where the action is *clear the filter*. Showing the
   first-run invitation to someone who has two hundred records behind an active search reads as data loss,
   and it is the most common way a good empty state becomes a support ticket.
5. A friendly error state with a **Retry** — a raw exception string on screen is a bug report shown to a
   customer. It is also an information leak in the small: a stack frame or a URL in a snack bar tells
   whoever is looking over the user's shoulder more about the backend than the app meant to say.
6. **Say which failure it was, where the user can act on it.** Offline, unauthorised, not found and server
   error lead to four different next steps — wait, sign in again, go back, retry later — and one generic
   sentence for all of them forces the user to guess and support to ask. The wording stays short; the
   diagnosis goes to the crash reporter (§9.10), not to the screen.
7. **Retry has to actually retry the thing that failed.** Wired to re-run the screen's whole
   initialisation, it discards the filter, the scroll position and anything half-entered, so the recovery
   costs more than the failure. And it is disabled while the retry is in flight, or an impatient user
   queues five identical requests behind a network that is already struggling.
8. **A spinner with no deadline is an indefinite wait.** A silently black-holed connection — a captive
   portal, a dropped socket that never resets — never produces an error, so the request never completes and
   the screen spins forever with no way out but killing the app. Every request has a timeout, and the
   timeout resolves into the error state of point 5.
9. **Refreshing is not loading.** Replacing content already on screen with a full-screen spinner throws
   away what the user was reading and moves everything when it comes back. A refresh keeps the content and
   shows progress at the edge — which is also what pull-to-refresh must do (§6.6), rather than returning the
   screen to its initial loading state.
10. **After a failed refresh, the screen says the data is old.** Silently keeping the previous content is
    the "stale presented as fresh" failure of point 1, and it is the expensive one: a balance, a stock level
    or a status that is quietly twenty minutes out of date gets acted on. A discreet marker plus the retry
    is enough; pretending is not.
11. Prefer content-shaped skeleton placeholders over a centred spinner for content that has a known shape:
    the layout doesn't jump when the data lands. The jump is not only cosmetic — a list that reflows under a
    finger already in motion produces a tap on the wrong row.
12. **A loading state announces itself.** A spinner conveys nothing to a screen reader, so a user relying on
    one hears silence and then, without warning, a screenful of new content. Label the progress and announce
    the transition; this is the same rule as §3.15's touch targets, applied to time rather than to space.
13. **A state you cannot reach is a state you have not written.** Loading and error paths are fast or absent
    on a developer's machine against a local backend, so they ship untested — and then a skeleton overflows
    or a retry button is behind the keyboard. Make them reachable deliberately (an injected delay, a forced
    failure switch) and look at them once.
14. **Optimistic success needs the path back.** Rendering the change before the server confirms it is good
    for perceived speed and a lie until the response lands, so the rollback and the sentence explaining it
    are part of the same edit. Without them, a failed write leaves the UI asserting something that never
    happened, and the user finds out from someone else.
15. **The state is decided in the state holder, not by reading nullability in `build`.** `data == null` has
    to stand for loading, empty and failed at once, so one of the three ends up unrepresented — which is why
    §7.3's single status enum exists. A widget's job here is to map an explicit state to a layout, and if it
    cannot do that with a `switch`, the state class is the thing to fix.
