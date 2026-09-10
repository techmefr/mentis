# flutter-conventions §7 — State management

> Section 7 of `skills/flutter-conventions`. Read it when a cubit, a bloc, any state holder. The other sections and the guardrails stay in `SKILL.md`.

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
4. **The initial state is a real state, not an absence.** A nullable state, or one that stands for "nothing
   has happened yet" without saying so, forces every widget to invent a rendering for it — and they invent
   different ones. Name it, and give it a layout like the other four (§4.15).
5. **A failure is part of the state, not an exception the widget catches.** A holder that lets an exception
   escape makes every call site responsible for a `try` it will forget, and the screen ends up with no
   error rendering at all. Catch at the boundary, emit a failure state carrying what the UI needs to say
   (§4.6), and report the diagnosis separately (§9.12).
6. **Never put a `Future` or a stream in state; put its result.** A state holding an unresolved future
   cannot be compared, cannot be rendered without a second builder inside the first, and re-triggers itself
   on every rebuild — which is §2.16's side effect in `build` arriving through the state layer.
7. View logic (formatting, deriving a label) belongs to the state holder or a pure function, not inside
   `build`.
8. No business logic in a widget, and no widget import inside a state holder: the state layer must be
   testable without the UI — including no `BuildContext` and nothing UI-owned (a text controller, a
   `GlobalKey`) inside it. Those belong to the widget that created them and are disposed there (§1); the state
   holder receives their derived value, not the controller itself.
9. **The holder receives its dependencies; it does not build them.** A holder that constructs its own HTTP
   client or opens its own database cannot be exercised without one, so the tests either hit the network or
   do not exist. Injected, the same holder is tested against a fake in milliseconds — which is the whole
   claim of point 8 made operational.
10. **The network and the cache belong below the holder.** A repository owns where data comes from and how
    long it is kept; the holder orchestrates and decides what the screen sees. Collapsed into one, the
    caching policy is duplicated by the next screen that needs the same data, and the two disagree.
11. **One owner per piece of data.** Two holders that both load and hold the same record are two sources of
    truth: an edit through one leaves the other stale, and which one the user sees depends on which screen
    they opened first. Share the repository, not the state.
12. **Scope is a decision, not a default.** Provided above the navigation stack, a holder survives leaving
    the screen — which is what you want for a session and what you do not want for a form, where the next
    visitor finds the previous one's half-typed data. Created with the screen, it dies with it. Neither is
    right in general, and the wrong choice reads as either "it forgets" or, on a shared device, as a leak
    between users.
13. **Create it once.** A holder instantiated in `build`, or in a builder that re-runs, is a new holder with
    a fresh initial state on every rebuild — the same class of mistake as creating a controller in `build`
    (§1.14), and it presents as a screen that resets itself at random moments.
14. **Check whether the state holder is still alive before emitting after any `await`** — the same shape as
    the `BuildContext`/`mounted` guard in §1, one layer down: a screen closed mid-request must not crash the
    next emit.
15. **A one-time reaction (navigation, a snackbar, a dialog) belongs to a listener, never to the builder that
    renders the UI.** A builder can be re-invoked at any time for reasons that have nothing to do with the
    state changing (a parent rebuild, a rotation) — code in it that reacts instead of rendering re-fires on
    every one of those, and a listener condition must compare the previous and current state, not just inspect
    the current one, or the same one-time reaction re-fires every time that state is revisited.
16. Guard the double-submit case in the state holder, not the button: a status already "in flight" makes the
    next call to the same method a no-op, and that status is what disables the button too — one source of
    truth for both.
17. **Test the sequence, not the destination.** Asserting only the final state passes whether or not the
    loading state was ever emitted, so the spinner that never appears — or the error state skipped on the
    way to a stale success — is invisible to the suite. Assert the ordered emissions, which is the one thing
    a holder is uniquely able to prove about itself.
18. **Point 5's catch is `on Object`, not `on Exception`.** Half of what the framework throws is an
    `Error` rather than an `Exception` — a missing asset, a failed assertion, a bad cast, a
    `late` field read before it was assigned — so the narrow catch that reads as the careful one lets the
    platform's own failures straight past the layer whose whole job is turning them into a state, and the
    user gets the framework's error screen where point 5's failure state was meant to be. That boundary is
    the one place the broad catch is right; everywhere else it hides a bug.
19. **An awaited call into the holder does not tell the widget whether it worked.** Once point 5 is
    followed the failure lives in the state and the method completes normally either way, so a widget that
    writes `await holder.save()` and then leaves the screen leaves it on a failed save too — with the error
    message the holder emitted rendering for one frame behind the transition. The success is a state as
    well, reacted to by point 15's listener on the transition into it. And once the reaction lives there
    the widget has no `await` of its own left at all, which is why a screen built this way never needs
    §1's context guard rather than merely getting away without it.
20. **A status enum is the right answer for flags and the wrong shape for payloads.** Point 3's single
    enum removes the contradiction between two booleans, and then a status of *failed* carrying no failure
    — or of *ready* carrying no data — is still a value the class allows, so the widget either asserts on
    the payload or invents a rendering for the impossible case, which is the fabricated state §4.15 exists
    to prevent. Where the language has sealed types and exhaustive matching, one class per state carrying
    exactly its own payload removes the combination instead of documenting it, and the widget's `switch`
    has nothing left to assert.
21. **A generated provider disposes itself the moment nothing watches it, unless told otherwise.** Point 12's
    scope decision is made for you by default: leaving the screen that was the only watcher tears the
    provider and its state down immediately, which is right for a form (nothing to remember not to leak) and
    wrong for a session the next screen still needs — `@Riverpod(keepAlive: true)` is that decision made
    explicit, not the framework's opinion about what should persist.
22. **`ref.watch` and `ref.read` are two different questions, not two spellings of the same read.** `watch`
    inside `build` says "rebuild me when this changes" and belongs nowhere else; `read` says "give me the
    current value once" and belongs in a callback or an initializer. `read` inside `build` silently opts the
    widget out of point 3's rebuild-on-new-state contract — it renders the value that was current when the
    widget was first built and never again.
23. **A family provider's parameter is a cache key, and the equality it uses is the class's own, not
    identity.** A parameter object without `==`/`hashCode` defined creates a fresh cache entry — and a fresh
    fetch — on every call even when the values are the same, which is point 11's one-owner-per-data rule
    broken by the provider layer itself rather than by a second holder.
24. **`AsyncValue.guard` is point 5's boundary catch, written once instead of at every mutation.** Wrapping an
    async body in it turns whatever it throws into the failure branch of the same three-state value a
    provider's `build` already returns, so a screen has one shape (`when`/`whenOrNull` over data, loading,
    error) to render regardless of whether the failure came from the initial fetch or from a later mutation —
    the alternative, a bare `try`/`catch` around each mutation that hand-assigns a loading and an error state,
    is the per-call-site `try` point 5 already warns is easy to forget written out as boilerplate instead.
25. **`ref.watch` in a `build` method and `ref.select` in the same spot are answering different-sized
    questions, and skipping `select` rebuilds more than the change warrants.** Watching a provider that
    exposes a whole record or a whole list rebuilds the widget on any field's change; `select` on the same
    provider narrows the subscription to the one derived value the widget actually reads, so a change to an
    unrelated field never reaches it — the same rebuild-scoping question point 3's `Selector`/`context.select`
    equivalent answers in a `Provider`-based tree, asked one layer up, at the provider-consumption site rather
    than at the state-equality site.
26. **A synchronous `notifyListeners` inside a loop calls every listener once per iteration, not once for the
    whole batch.** A `ChangeNotifier`-based holder that mutates and notifies inside a loop over several
    updates triggers a full rebuild of everything that watches it at each iteration; batching the mutations
    and notifying once after the loop is the direct fix, and is the same shape as point 3's equality
    concern — the point being that the *number* of emissions matters as much as their *content*, or a
    screen redraws several times for what the user experiences as a single change.
27. **A `ValueNotifier` is the right granularity for one primitive value, not a substitute for the state
    class of point 3.** Reaching for it to hold a whole screen's state reintroduces the independent-booleans
    problem point 3 already rules out, one `ValueNotifier` per flag, each rebuilding its own listener on its
    own schedule with no shared notion of a coherent state — it is the correct tool for a single slider
    position or a single toggle a widget owns locally, and the wrong one past that scope.
