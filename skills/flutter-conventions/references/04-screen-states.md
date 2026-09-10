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
16. **A superseded request must lose, even if it answers last.** Typing into a search field fires one
    request per keystroke; if the third one resolves before the first, and the state holder just overwrites
    on every response, the screen can show results for a query the user already changed away from. The state
    holder needs to know which request is current and discard an answer that isn't — a sequence number or
    the request itself compared against the latest one sent, not just "a response arrived."
17. **Debounce the trigger, not just the request.** A search-as-you-type field wired straight to the state
    holder fires a request per keystroke regardless of point 16's discard logic, so the network and the
    backend pay for every intermediate value the user never meant to search for. Waiting for a short pause
    in typing before firing cuts the request count without changing what the user experiences as instant.
18. **A batch of independent items can partially fail**, and collapsing that into a single success/error
    verdict either hides the ones that failed behind a green screen or discards the ones that succeeded
    behind a red one. Point 2's "one set of states per data source" generalises here: a bulk action reports
    per-item outcome, so the user can see which three of ten uploads actually went through and retry only
    those.
19. **An error announced only visually is not announced to a screen reader user.** A red banner or an icon
    change carries nothing through the semantics tree unless the error text sits in a live region, so the
    same failure that a sighted user notices instantly passes silently for someone using assistive tech —
    the accessibility half of point 12's loading announcement applies just as much to the state it leads to.
20. **The last known-good data outlives the request that fetched it.** Persisting the previous successful
    response (even briefly, even just in memory across a screen re-entry) means a cold start with no
    connectivity yet can show that data marked as possibly stale (point 10) instead of the loading state of
    point 1 with nothing behind it — the difference between "reopening the app shows something" and
    "reopening the app on a train shows a spinner forever."
21. **The end of a paginated list and a failure mid-scroll are not the same footer.** Point 6's loading
    footer, the end-of-list marker and the error state need to be three distinguishable things: a marker
    that reads "no more results" when the real cause was a failed page load sends the user away thinking the
    data is complete, and a retry control that only appears on the very first page's failure leaves every
    later page silently stuck.
22. **A confirmed empty result and a filter that matched nothing look the same on screen and need to say so
    differently in the state.** Extending point 4: the state holder distinguishes "loaded zero rows" from
    "still loading page one," since a screen that renders both as the same empty illustration briefly shows
    "nothing here, try creating one" to a user whose first page just hasn't arrived yet.
23. **`ConnectionState.none` and `ConnectionState.waiting` are not the same absence of data.** A
    `FutureBuilder` given no future yet — the common shape when the request is triggered by user action
    rather than fired at construction — reports `none`, not `waiting`; a screen that only checks
    `snapshot.connectionState == ConnectionState.waiting` for its loading state renders as if nothing were
    happening at all until the request is actually issued, which is point 1's "never a blank screen" failing
    from the state machine's own vocabulary rather than from the widget ignoring it.
24. **An automatic retry and a user-initiated one are different policies, not the same button fired
    twice.** Point 7's retry answers "the user asked again"; a transient failure — one dropped packet on an
    otherwise fine connection — is worth one or two automatic attempts with a short backoff before ever
    showing the error state at all, and conflating the two means either the user waits through retries they
    never asked for, or the app gives up after one flaky response it could have silently absorbed.
25. **A shimmering skeleton is an animation, and point 9's off-screen-cost rule applies to it too.** A
    content-shaped placeholder (point 11) that shimmers continuously while its data source is unreachable —
    a stalled background sync, a screen left open on a dead connection — keeps a ticker running for a
    loading state that may never resolve; a static skeleton after a short delay, or the timeout of point 8,
    is what stops "loading forever" from also being "animating forever."
26. **An optimistic write can be rejected with a different final value, not just rejected outright.** Point
    14's rollback assumes the server either confirms or refuses the exact change shown; a rate limit that
    clamps a quantity, a price that changed underneath the order, or a server-side default overriding a
    client guess means the honest recovery is reconciling the screen to what actually got written, not only
    reverting to what was there before the optimistic update.
27. **The same failure retried immediately produces the same error, and the user does not need to see it
    announced twice in a row.** A snack bar or a live-region announcement (point 19) fired on every retry
    attempt against an outage that hasn't cleared restates information the user already has; suppressing a
    repeat of the identical error within a short window keeps the channel meaningful for when something
    actually changes, without silencing point 6's per-failure wording the first time it appears.
28. **A degraded success is a fifth thing the four-state model doesn't name.** A response that returns data
    alongside a partial-failure flag — half the widgets on a dashboard loaded, half timed out — is neither
    the success of point 1 nor the error of point 5; treating it as success hides what didn't load, and
    treating it as error discards what did. Point 18's per-item outcome generalises to a single response that
    is itself mixed: render what came back, and say plainly which part didn't.
29. **Point 10's "keep the old content, mark it stale" is a policy for a pull-to-refresh, not for every
    request that happens to reset the page cursor to zero.** Dogfooded 2026-09-10: a list's state holder used
    one boolean to mean both "go back to page one" (needed by a pull-to-refresh *and* by §6.8's filter-change
    reset) and "this is a refresh whose failure should keep showing the old page marked stale." With one flag
    doing both jobs, typing a filter that the backend rejects landed on point 10's stale-content branch
    instead of point 5's error state, because the previous filter's results were still sitting in state and
    looked, to that one check, exactly like a refresh with something to fall back on. The two need to be
    threaded as separate signals — "reset the cursor" and "this is a refresh, not a fresh query" — because a
    failed reload triggered by a changed filter has no honest "old content" to fall back to: the old content
    belongs to a search the user has already abandoned, and showing it marked merely "stale" hides a failure
    behind data that no longer answers the question being asked. Found by a widget test that entered a new,
    failing filter after a successful first load and got the stale banner instead of the retry button.
