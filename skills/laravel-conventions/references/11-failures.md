# laravel-conventions §11 — Failures

> Section 11 of `skills/laravel-conventions`. Read it when an operation can fail — any layer, not just a
> controller. The other sections and the guardrails stay in `SKILL.md`. `code-baseline` §3 governs what an
> exception *is* (a named class, never a built-in with a message); this section governs what happens to it.

1. **Throw. Never build and return the error response yourself.** The framework's exception handler is the
   one place that turns a failure into a status, a body and an error-tracking event, and it only sees what
   is thrown. A hand-returned 500 is **invisible to error tracking** — the endpoint fails in production, the
   error rate stays flat, no alert fires. That is strictly worse than letting it crash, because an uncaught
   exception would at least have been reported. This holds for every layer that can fail (controller,
   action, job, command): the success response is the return value, every failure leaves as a throw.
2. **Reporting is not handling.** Catching an error, sending it to the tracker (`report()`, a
   `captureException`, a house `reportSilently()` helper) and then continuing or returning makes the
   operation *look successful* to everything upstream. An error's job is to stop the current unit of work
   and travel to a layer that can decide about it. A tracker entry next to a 200 is a monitoring artefact,
   not error handling.
3. **A `catch` earns its place by doing something.** Retrying, converting to a domain failure, adding
   context and rethrowing, or committing a genuine fallback whose degraded result is correct — those are
   handling. An empty `catch`, a `catch` holding only a log line, and a `catch` returning a null/false/empty
   collection that the caller cannot distinguish from a real result are the same swallow in three costumes.
4. **Where a failure always means one HTTP status, make the exception HTTP-native** — extend the
   framework's own HTTP exception for that status rather than mapping the domain exception to a response in
   a render callback. The exception then *is* the contract and the handler renders it. The reason is
   mechanical: a render callback's return value is used verbatim, so the callback is forced to
   re-implement content negotiation by hand, and that hand-rolled branch silently contradicts the app's own
   negotiation policy. Keep a mapping layer for the failures whose status genuinely depends on the caller.
5. **Never hand-roll JSON-versus-HTML negotiation.** A branch on "does this request expect JSON" that
   builds two responses carrying the same status and message in two formats is a copy of what the handler
   already does internally, and it drifts from the app's configured policy the moment that policy changes.
   Throw the exception (or the framework's abort helper for an anonymous status) and let the handler
   negotiate.
6. **A guard that only narrows a type is not an error path.** Where middleware has already rendered the
   failure, the check downstream is unreachable at runtime and exists for the static analyser — keep it if
   the narrowing is needed, but its body throws rather than returning a response. The guard was never the
   problem; the `return` was.
