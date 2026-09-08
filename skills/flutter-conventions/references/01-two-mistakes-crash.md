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
