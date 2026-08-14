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
