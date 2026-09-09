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
7. **A failure carries what the caller needs in order to act.** A validation failure carries per-field
   detail, not a sentence, because the form has to point at the field the user must fix; a domain exception
   carries the identifiers and values involved, as data on the exception rather than baked into a string.
   A message the caller has to parse is a contract that breaks the first time somebody rewords it.
8. **The exception message is for developers; the user-facing text is the handler's decision.** Putting a
   polished, translated sentence in the throw site mixes two audiences and guarantees the sentence gets
   duplicated, because the next throw site needs the same words. And it goes the other way too: internal
   detail — a query, a path, an upstream body — must not reach the response, which is exactly what §11.1's
   hand-built error response tends to leak.
9. **Inside a transaction, a throw is the rollback.** So do not catch and continue in there: swallowing the
   exception commits a half-finished unit of work, which is the one failure mode a transaction existed to
   prevent. The corollary is that irreversible side effects — mail, a queued job, an outbound HTTP call —
   do not belong inside the transaction, because a rollback cannot recall them (§8 covers dispatching after
   commit).
10. **A retry re-runs everything before the failure point.** So a job or command that can be retried is
    idempotent by construction, or its first steps happen twice: two emails, two charges, two rows (§8).
    "It only fails rarely" is not an answer — rare is exactly when nobody is watching the second run.
11. **An external call fails in five ways, not one.** A timeout, a refused connection, a 5xx, a rate limit
    and a malformed body are different outcomes with different correct responses, and a single
    `catch (Exception)` around an HTTP client treats a rate limit as a bug and a bug as a rate limit. Set
    the timeout explicitly while you are there: several clients default to none, and a dependency that
    hangs becomes your outage rather than theirs.
12. **An expected failure is not a defect, and the tracker has to know the difference.** A 422, a 404 on a
    stale link, a rejected login — these are the application working. Reporting them next to real
    exceptions raises the volume until the real ones are unfindable, which is the same harm as reporting
    nothing, arrived at from the other direction.
13. **Attach identifiers to a report, not payloads.** The tenant, the user, the resource id and the
    operation are what make an exception diagnosable; dumping the request body puts personal data into a
    third-party tool, where it is now retained under someone else's policy and outside the deletion path
    the application promises.
14. **The failure path is asserted.** A throw is behaviour, so a test names it and proves it (§9);
    otherwise the first refactor quietly turns it back into the returned error response point 1 forbids,
    and nothing anywhere goes red.
15. **All of this is configured in one place, `withExceptions()` in `bootstrap/app.php`**, which is where
    point 12's "the tracker has to know the difference" is actually enforced: `dontReport()` names an
    exception class as expected rather than catching it at every throw site to suppress it locally, and
    `throttle()` samples a class that fires legitimately at volume (a flaky upstream, a bot hammering a
    404) so the tracker keeps a representative slice instead of either silence or being flooded into
    unreadability. `stopIgnoring()` is the other direction: a status the framework ignores by default
    (404, a CSRF failure) that this application specifically wants reported, because a spike in one of
    those is itself the signal.
