# flutter-conventions §1 — The two mistakes that crash in production

> Section 1 of `skills/flutter-conventions`. Read it when always, before anything else on this stack. The other sections and the guardrails stay in `SKILL.md`.

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
3. **One guard per await, not one per method.** Two awaits mean two windows in which the widget can go away,
   so a check after the first proves nothing about the second — and the same applies to the code after a
   `Future.wait`, after a loop that awaits per item, and after an awaited navigation that returns a result
   (§5.12). Every resumption point is its own gap.
4. **A callback is a resumption point too.** Anything that runs later — a stream listener, a timer, a
   platform callback, a `then` — is on the far side of the same gap even though no `await` appears on the
   line. If it touches context or calls `setState`, it needs the guard for the same reason.
5. **The guard stops the crash; it does not stop the work.** A `mounted` check makes the resumption safe and
   the request still ran to completion, still cost the user's data, and still holds whatever it captured
   until it finishes. Where the work is expensive or the screen is left routinely, cancel it rather than
   only discarding its result.
6. **Never store a `BuildContext` in a field** to use later: a stored context is stale by definition. Store
   the derived object instead.
7. **Never silence the analyzer's async-context lint with an ignore comment.** It's a latent crash, not a
   style nit — satisfy the lint. The ignore is also self-concealing: it makes the one tool that finds this
   class of bug stop reporting the line, so the next reader has no signal that anything was ever wrong here.

**Every disposable resource a widget creates, that widget releases.** Text/scroll/page/tab/animation
controllers, focus nodes, stream subscriptions, sinks, timers, tickers, and any state holder it created
itself.
8. Why it matters beyond tidiness: a controller registers listeners and an animation drives a ticker off the
   scheduler, so neither is collected; an uncancelled subscription **keeps invoking its callback after the
   widget is gone**, and that callback often calls `setState` on a dead widget; and several of these assert on
   leak in debug builds, so the report arrives far from the cause.
9. **A leaked closure holds the whole screen.** A timer or a listener that captures `this` keeps the state
   object alive, and through it the widget tree, the images it decoded and whatever the state holder was
   caching — so the memory cost of one forgotten subscription is not the subscription. On a device already
   under pressure, that is the difference between a screen that reopens and one the OS kills.
10. **Store the subscription handle.** Fire-and-forget `stream.listen(...)` cannot be cancelled, which is the
    same bug as not cancelling it.
11. **`super.dispose()` goes last** — release your own resources first.
12. **Release in the reverse order of the dependency.** Cancel the subscription before disposing the
    controller it writes into, or the last callback in flight arrives at a disposed object and the crash
    names the controller instead of the listener that was still running.
13. **Never dispose what you didn't create.** A controller passed in through the constructor belongs to the
    caller, and a state holder owned by a provider is closed by that provider — disposing either is a
    double-dispose crash in a different file.
14. **Never create a controller, future or stream in `build`**: a fresh instance every rebuild, none of them
    disposed. Hoist it to `initState` or a late final field.
15. **`dispose` runs even when `initState` didn't finish.** If setup threw halfway, the teardown still
    executes against half-initialised fields, so a `late final` that was never assigned throws from
    `dispose` — and that second exception is the one reported, hiding the original failure completely.
    Anything created conditionally is released conditionally.
16. **A resource created outside `initState` still needs the same treatment.** One allocated lazily on first
    use, or in a callback, has no obvious teardown site, which is exactly why it is the one that leaks —
    give it a field and release it with the rest.
17. When you add a resource to an existing widget, **wire its teardown in the same edit** — never "for later".
    And if you're already editing a `dispose()` and spot a created-but-unreleased resource, fix it there:
    that's bundled cleanup, not a drive-by.
18. **`WidgetsBindingObserver` is a subscription like any other.** A widget that overrides
    `didChangeAppLifecycleState` or `didChangeMetrics` must call `addObserver` in `initState` and
    `removeObserver` in `dispose` — omitted, the binding keeps calling back into a widget that no longer
    exists, and because the callback runs on an app lifecycle event rather than a rebuild, the crash surfaces
    on backgrounding a screen that was closed minutes earlier, far from the code that forgot the removal.
19. **A resource owned through a constructor parameter that can change needs `didUpdateWidget`, not just
    `initState`.** A widget that builds something from `widget.someId` and only does so once, in `initState`,
    keeps the old resource alive under the new identifier when the parent passes a different id — the same
    stale-copy failure as §2.10, but for a disposable rather than a plain value. `didUpdateWidget` is where
    the old one is disposed and the new one created, in that order.
20. **A `ChangeNotifier` asserts, in debug builds, if it is disposed while listeners remain attached.**
    `removeListener` has to run before the notifier's own `dispose`, in the reverse order of point 12 —
    otherwise the assertion fires from the notifier's teardown, naming it as the culprit, when the real bug is
    a widget that never detached.
21. **A broadcast `StreamController` still needs `close()` even with several listeners.** Each `listen` call
    needs its own cancellation (point 10), and the controller itself is a separate resource on top: closing
    it without cancelling every subscription first still leaves stale listener callbacks queued if the
    controller had buffered events, and a controller never closed keeps its underlying sink — and whatever it
    was writing into — reachable for the life of the isolate.
22. **A network call has a lifetime independent of the widget that started it**, and `mounted` only guards
    what happens with the result — it does not stop the request. Where the client supports it (a cancellation
    token, an abortable request), cancelling on `dispose` frees the connection and, for anything that
    mutates server state, avoids a write completing after the user believed they had left the screen; this is
    the concrete version of point 5's "cancel rather than only discard."
23. **Cleanup that must run regardless of how the method exits belongs in `finally`, not after the last
    line.** An early return from a caught exception, or an exception the method doesn't catch at all,
    skips whatever teardown was written after the code that could throw — a lock never released, a temporary
    file never deleted, a loading flag never cleared. `try`/`finally` runs the release on every exit path,
    including the one nobody was thinking about when the method was first written.
24. **A `Future` or `Stream` built inline as an argument to `FutureBuilder`/`StreamBuilder` is a fresh one
    every rebuild.** The builder widget compares the instance it was given to the one from the previous
    build, and a new instance — even one that resolves to the same data — reads as a brand-new async
    operation: the widget drops back to `ConnectionState.waiting` and the screen flashes its loading state
    on every unrelated rebuild instead of once. The future belongs to a field created outside `build`, the
    same hoisting point 14 already requires for a controller.
25. **`setState()` after `dispose()` throws its own assertion, distinct from the `BuildContext` failures of
    point 1.** The two are easy to conflate because both are triggered by the same root cause — a
    resumption point firing after the widget is gone — but the `mounted` guard that protects a context read
    protects a late `setState` call for exactly the same reason and needs to be checked independently if the
    callback does both; guarding one and assuming the other is covered is how half the fix ships.
26. **Pausing a subscription is not the same decision as cancelling it.** A widget kept alive off-screen by
    `AutomaticKeepAliveClientMixin` (§2.19) still doesn't want its subscription's callback running while
    nobody can see the result — `StreamSubscription.pause()` on becoming invisible and `resume()` on
    becoming visible again keeps the subscription intact for when the tab is swiped back to, instead of
    cancelling and re-subscribing from scratch and possibly missing what happened while it was away.
27. **A passing test suite is not proof nothing leaks.** Leak detection for controllers, streams and other
    disposables is opt-in per test rather than a property of the app, and a resource created outside the
    widget tree the test actually pumps — a singleton, a background isolate, a static subscription — is
    invisible to it either way. The absence of a reported leak means the checked paths were clean, not that
    the screen was.
28. **`Timer.periodic` started in a method that can throw before reaching its own cancellation needs the
    same `finally` treatment as point 23.** A retry loop that schedules a periodic timer and only cancels it
    on the success branch leaves the timer running forever the one time the method exits through its catch
    block — the ticking callback then fires against a widget that already tore down everything else.
29. **A `compute()` call or a spawned `Isolate` outlives the widget that started it unless told otherwise.**
    Unlike a future awaited in place, an isolate keeps running its work — and holding its memory — after the
    screen that requested it is gone, because nothing about disposing a widget signals the separate isolate
    to stop; a long-running background computation needs its own explicit kill switch stored and called from
    `dispose`, not an assumption that leaving the screen ends it.
