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
4. View logic (formatting, deriving a label) belongs to the state holder or a pure function, not inside
   `build`.
5. No business logic in a widget, and no widget import inside a state holder: the state layer must be
   testable without the UI — including no `BuildContext` and nothing UI-owned (a text controller, a
   `GlobalKey`) inside it. Those belong to the widget that created them and are disposed there (§1); the state
   holder receives their derived value, not the controller itself.
6. **Check whether the state holder is still alive before emitting after any `await`** — the same shape as
   the `BuildContext`/`mounted` guard in §1, one layer down: a screen closed mid-request must not crash the
   next emit.
7. **A one-time reaction (navigation, a snackbar, a dialog) belongs to a listener, never to the builder that
   renders the UI.** A builder can be re-invoked at any time for reasons that have nothing to do with the
   state changing (a parent rebuild, a rotation) — code in it that reacts instead of rendering re-fires on
   every one of those, and a listener condition must compare the previous and current state, not just inspect
   the current one, or the same one-time reaction re-fires every time that state is revisited.
8. Guard the double-submit case in the state holder, not the button: a status already "in flight" makes the
   next call to the same method a no-op, and that status is what disables the button too — one source of
   truth for both.
