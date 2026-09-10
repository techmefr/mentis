# flutter-conventions §5 — Navigation

> Section 5 of `skills/flutter-conventions`. Read it when a route, back handling, a deep link. The other sections and the guardrails stay in `SKILL.md`.

1. **Centralised declarative routing**, one place that maps routes to screens, rather than imperative pushes
   scattered across widgets. Arguments are typed, not passed as an untyped map. The map is the version that
   fails at run time in a language that would have caught it at compile time, and it fails on the device of
   whoever opens that screen from the one call site nobody tested.
2. **A route's arguments are reconstructible from a URL.** Passing a fully loaded object down means the
   screen only works when it is reached from the list that already had it — a deep link, a notification tap
   or a cold start has an id and nothing else, so the screen either cannot be built or is built with a
   half-empty stand-in. Pass identifiers; let the screen load what it needs.
3. **Route paths and names live in one place as constants.** A path typed as a literal at the call site is a
   runtime failure the compiler cannot see, and it is the kind that survives review because the string looks
   right.
4. Guards/redirects (auth, onboarding) declared with the route, not checked in each screen's `initState`.
   Checked per screen, the guard is a list that grows: the screen added next month is the one that forgets,
   and the check in `initState` runs after the screen has already been built and, briefly, shown.
5. **A guard remembers where the user was going.** Redirecting to sign-in and then landing on the home
   screen throws away the intent — which for a link opened from an email or a chat is the whole reason the
   app was launched. Carry the target through the redirect and return to it.
6. Deep links and notification taps are entry points into the same route table, including the cold-start
   case — the tap that launches the app is the one that's usually forgotten. It behaves differently by
   construction: nothing is initialised, no session is loaded, and the link arrives before the first frame.
7. **A deep link into a detail screen builds a back stack.** Landing directly on a leaf with an empty stack
   means the first back gesture leaves the application, from the middle of a flow, which reads as a crash.
   The declarative router can synthesise the parents — which is another reason the route table is the one
   place this belongs.
8. Back handling is explicit where it matters: confirm before leaving a screen with unsaved changes,
   intercept the system back deliberately, and never trap the user with no way out.
9. **A confirm-before-leaving covers every exit, not the button.** The app bar's back arrow, the Android
   system back, the iOS edge-swipe and a programmatic pop are four different paths to the same departure,
   and guarding only the one in the layout means the guard is bypassed by the gesture most people actually
   use.
10. **A dialog and a bottom sheet are routes.** They sit on the stack, so a back gesture dismisses them and
    a `pop` from the screen underneath can close the wrong one — the classic version is a confirmation
    dialog whose "no" pops the screen behind it. Be explicit about which navigator is being popped,
    especially where there is a nested one under a tab.
11. **Two taps push two screens.** A navigation control tapped twice before the first transition completes
    pushes the destination twice, so the user backs out of the same screen they just left — the same class
    of failure as the double submit of §6.14, and it is solved the same way: the control is inert once it has
    fired.
12. **Navigation belongs to the widget layer.** A state holder that navigates has a dependency on the UI it
    was supposed to be testable without (§7.8), so the transition is expressed as a state or a one-shot
    signal and performed by a listener, never a builder (§7.15). And a push that is awaited for its result
    is an `await` like any other: the context after it is suspect (§1).
13. Tabbed/bottom navigation **preserves each tab's state and scroll position** across switches — losing a
    half-filled form on a tab switch reads as a broken app. It also loses the requests: a tab rebuilt from
    scratch refetches everything it had, which on a metered connection is the user paying for the same data
    twice.
14. **The route table survives the process being killed.** A backgrounded app is terminated routinely,
    especially on Android, and the user returning to it expects to be where they left. A router that can
    rebuild any screen from a path and its identifiers restores that for free; one that depends on objects
    held in memory cannot, and reopens on the home screen.
15. **Screen tracking hangs off the router.** An analytics call in each screen's `initState` is a list that
    goes stale the same way the guards in point 4 do, it double-counts on every rebuild, and it silently
    stops covering whatever was added last. One observer on the route table sees every transition, once.
16. **Push, replace and reset are three different intentions.** Pushing a sign-in screen leaves it on the
    stack, so the first back gesture after signing in returns the user to the login form they just cleared;
    pushing the home screen after a logout leaves the authenticated screens underneath it, reachable by
    going back. A transition that ends a flow replaces or resets, and choosing between the three is part of
    declaring the route rather than a detail of the call site.
17. **`PopScope` replaces `WillPopScope`, and it changes what "intercepting back" means.** `canPop: false`
    stops the pop before it happens, and `onPopInvokedWithResult` runs *after* the framework has already
    decided whether the pop occurred — code written for the old callback that assumed it could still prevent
    the pop from inside the handler silently stops working on the current framework version, which is why
    point 9's "confirm before leaving" needs `canPop` set to false and the confirmation dialog itself
    triggering the real pop, rather than a handler that tries to cancel one already in flight.
18. **On the web, the platform back button is not optional to support.** A router that does not integrate
    with browser history either does nothing on back or leaves the address bar showing a URL the app is not
    actually on, and a path-based URL strategy (rather than the default hash) is what makes a deep link,
    a bookmark and a shared link resolve to the same route point 1 already centralises — without it, every
    link into the app has to go through the home screen first regardless of what point 6 says about entry
    points.
19. **A redirect guard can loop against another guard's redirect.** An auth check that sends an
    unauthenticated user to sign-in, from a sign-in screen that itself redirects somewhere else under some
    condition, bounces the user between two routes with no frame in between to interact with — the app
    appears to hang on launch. The guard has to know it is already on the redirect target and stop, which is
    a condition worth testing directly rather than trusting each guard in isolation.
20. **Each tab in a bottom navigation owns its own navigator when point 13's preserved state includes a
    pushed stack.** A single shared navigator means a push from one tab is still on the stack when the user
    switches tabs and back, and the system back gesture pops whatever is on top regardless of which tab is
    showing — nested navigators keep a tab's back stack local to that tab, so leaving and returning to a tab
    shows exactly what was pushed there.
21. **A dialog meant to survive a tab switch, or one opened from inside a nested navigator, needs the root
    navigator explicitly.** `Navigator.of(context, rootNavigator: true)` reaches past whatever nested
    navigator point 20 introduced; the default lookup finds the nearest one, which for a dialog opened from
    deep in a tab is the tab's own navigator — and a dialog living there disappears when the user switches
    tabs, rather than staying on top of the whole app the way a global confirmation or an error overlay is
    expected to.
22. **A transition duration ignoring the platform's reduce-motion setting is a motion-sensitivity problem
    dressed as a style choice.** The same accessibility signal that governs whether an animation should
    play at all (§9.8) applies to route transitions: a user who has asked the system for less motion still
    gets a full slide or fade on every navigation unless the router checks the same flag and either shortens
    the transition or removes it.
23. **State restoration is a stronger promise than the route table rebuilding from a path.** Point 14 gets
    the user back to the right screen after a process kill; `RestorationMixin` and a `RestorationBucket` get
    them back to the right scroll offset, the right selected tab and the right half-filled field within that
    screen — the difference between reopening the app to the list and reopening it exactly where the user's
    thumb was.
