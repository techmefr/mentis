# swift-conventions §3 — Concurrency

> Section 3 of `skills/swift-conventions`. Read it when an asynchronous function, a task, a task group, an
> actor, a main-actor annotation or a type shared across tasks is written. Rewritten from the language
> guide's concurrency chapter (`references/origin.md`).

1. **Every possible suspension point is marked with `await`**, and code between two of them runs without
   interruption by other code on the same isolation. Do not read this as "one thread": a function can resume
   on a different thread than it started on, so never rely on thread identity.
2. **Independent asynchronous calls run in parallel, not one after the other.** Awaiting each call in turn
   makes the second wait for the first for no reason; start independent calls together (an `async let`
   binding for a fixed few, a task group for a dynamic number) and await the results.
3. **Prefer structured concurrency.** Child tasks of a group or `async let` have a parent: cancelling the
   parent cancels them, priority escalates through the tree, task-local values propagate. An unstructured
   task has no parent and you are fully responsible for its lifetime, so create one only when no structured
   form fits, keep its handle, and cancel it. A detached task inherits no isolation, priority or task-local
   state; use it deliberately, not as the default way to leave the main actor.
4. **Cancellation is cooperative.** A task must check for it at sensible points, by throwing the cancellation
   check or reading the cancelled flag (use the flag when clean-up is needed before stopping). Responding
   means throwing, returning nothing, or returning the partial work done. In a group, add children with the
   variant that does not start new work after cancellation and stop adding when it reports refusal. A
   cancellation handler gives immediate notice but the task is still running, so do not share state between
   the task and its handler.
5. **Shared mutable state has one of three safe forms**: it is immutable; it is referenced by one task only;
   or it is protected by an actor. A class with unprotected mutable properties shared across tasks is a data
   race the compiler may not find until runtime.
6. **UI state lives on the main actor.** Annotate the type or the specific properties and methods that touch
   the UI. Frameworks usually annotate their protocols and base classes already, so conforming types inherit
   it; do not add redundant annotations. The pattern is: do the long or heavy work off the main actor, then
   hop to it for the UI update. The main actor is not the same thing as the main thread: you interact with
   the actor.
7. **An actor's state is read from outside with `await`; inside it, without.** An actor method with no
   suspension point cannot be interleaved, so a multi-step update that temporarily breaks an invariant is
   safe there. Putting an `await` in the middle reopens the window: restore the invariant before any
   suspension point.
8. **Types crossing concurrency domains are sendable**: a value type of sendable parts, a type with no
   mutable state, or a type that serialises its own access (main-actor-isolated, or queue-confined). Mark a
   type that must not cross as explicitly non-sendable. Do not silence a sendability diagnostic by an
   unchecked escape; fix the shared state.
9. **Adopt concurrency from the top down.** Asynchronous code cannot be called from synchronous code except
   through a task; there is no bottom-up route, and the standard library omits the blocking bridge on
   purpose. Do not block a thread waiting for an asynchronous result.
