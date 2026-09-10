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
16. **A queued job's `failed()` method runs after every retry is exhausted, and it is for the side effect
    the retries themselves cannot cause** — notifying an operator, marking the parent record as needing
    attention, releasing a lock the job was holding. It is not a second chance to fix the job's error: by the
    time it runs, `$attempts` is spent and the exception is already what it is. A job with no `failed()`
    fails silently into the `failed_jobs` table (or the configured failed-job store), where nothing short of
    someone querying it will ever notice — point 12's "the tracker has to know the difference" has a queue
    equivalent, and it is this table.
17. **A retried job re-dispatches the whole job, not a resumed continuation** — `$job->release()` and an
    automatic retry both put the job back on the queue from its `handle()` entry point, so point 10's
    idempotency requirement is not optional for anything that retries more than zero times. A job that
    charges a card, then fails on the email that follows, retries the charge too unless the charge step
    itself checks whether it already ran.
18. **`Http::fake()` intercepts every outbound call in the test process, and a test that forgets a stub for
    one route doesn't skip it — it gets a generic empty response** that can pass a test which never
    asserted on the actual response body, and only fails once the code starts reading a field the fake never
    provided. Asserting the request was sent (`Http::assertSent(...)`) is what makes the fake prove point 11
    was implemented, rather than merely prove the code compiles.
19. **A `ValidationException` and a bespoke domain "field is wrong" exception are not interchangeable**, even
    though both eventually render as a 422. The framework's own class already carries the per-field
    structure point 7 requires and is what a FormRequest throws automatically — reaching for a generic
    exception to report a validation-shaped failure from inside a service class means re-implementing that
    structure by hand, and a caller expecting the standard error-bag shape gets something else instead.
20. **A rate-limit failure (`ThrottleRequestsException`) is an expected outcome, not an incident** — the same
    distinction point 12 draws for a 422 or a stale-link 404, and reporting it at the same volume as a real
    defect drowns the signal for the same reason. It is also where `Retry-After` matters: a client that
    retries an HTTP 429 without reading that header is fighting the limiter with the same request that
    tripped it, and a `catch` that swallows the exception and retries immediately just does the same thing
    server-side.
21. **A test that expects a throw asserts it, and asserting the exception type is not enough on its own.**
    `expectException(DomainException::class)` alone lets a refactor swap in any exception of that class and
    still pass — pairing it with `expectExceptionMessage()` or reading the exception's own data (point 7) is
    what proves the failure carries what point 7 requires, not merely that *something* was thrown from
    somewhere in the method under test.
22. **An exception can carry its own `report()` and `render()` methods instead of routing every case through
    `bootstrap/app.php`.** The framework calls them automatically when they exist, which is the right place
    for handling that belongs to one specific exception class and nowhere else — a `withExceptions()` closure
    stays for the handling that spans several exception types (a shared log channel, a shared status mapping)
    and would otherwise be copied onto every class that needs it.
23. **`report()`'s closure can call `stop()` to suppress the default logging without suppressing the custom
    handling.** Point 2 says a `catch` that reports and continues is not handling; the same trap exists one
    layer up if a custom `report()` closure both sends the exception somewhere of its own choosing and lets
    the framework log it a second time. `stop()` names which one happened — the exception was reported, just
    not by the default channel — instead of leaving two log lines for one failure.
24. **`respond()` customises the whole response the handler produces, which is a different job from
    `render()` on one exception.** `render()` answers "what does *this* exception look like"; `respond()`
    answers "what does *every* response coming out of this handler look like" — adding a header, wrapping
    every error body in one envelope. Reaching for `render()` on every exception class to add the same
    wrapper is point 18's per-caller duplication wearing a different shape.
25. **`dontReportDuplicates()` collapses one exception reported twice in the same request into one entry.**
    A validation failure re-thrown after being caught and re-raised with context (point 3), or a job that
    reports a failure and then rethrows it for `failed()` to see, doubles the tracker volume for a single
    real event — the same signal-versus-noise concern as point 12 and point 20, but caused by the
    application's own code path rather than by an expected outcome.
26. **`Context` added before a throw travels with the exception into the report,** because the report payload
    is built from whatever `Context` held at the moment the exception was reported, not at the moment it was
    constructed. Point 13's "attach identifiers, not payloads" is what to put there — a request id, a tenant,
    a job id — set once near the entry point rather than threaded as a constructor argument through every
    exception class that might need it.
27. **A `Fiber`-based concurrent call (the `Concurrency` facade, or several `Http::pool()` requests) fails
    per-branch, not for the whole call** — one slow or erroring branch does not by itself abort the others,
    so a failure has to be checked per result rather than assumed to have stopped everything else. Point 11's
    "an external call fails in five ways" multiplies by the number of concurrent branches, and a single
    `try/catch` wrapped around the whole `Concurrency::run()` call only ever reports the first one it meets.
28. **A middleware that throws during termination (`terminate()`) fails after the response has already been
    sent to the client**, so point 1's "throw, don't hand-build a response" has nothing left to render —
    the only audience left for that exception is the tracker. Code with a side effect that must still be
    visible to the caller belongs in the request cycle proper, not in `terminate()`, precisely because a
    `terminate()` failure is invisible to whoever made the request.
29. **`rescue()` wraps a call, reports the failure, and returns a fallback value — the same "committed
    degraded default" point 3 already allows a `catch` to be, never a shortcut around one.** Reaching for it
    on a call whose failure the caller genuinely needs to react to swaps a thrown error nobody can miss for
    a fallback value indistinguishable from a real result, which is exactly the silent swallow point 3 warns
    a null/false return becomes; `rescue()` earns its place only where the fallback is a correct answer, not
    merely a convenient one.
30. **`Http::retry($times, $sleep, $when)` retries automatically, and without the `$when` closure it retries
    every non-2xx response — including a 404 or a 422 that will never succeed no matter how many times it's
    asked.** Point 11's "an external call fails in five ways" is what the `$when` closure has to encode:
    retry the timeout, the connection failure, the 5xx and the rate limit, and let the client fail fast on
    anything shaped like "this request itself was wrong," or the retry loop spends its budget hammering an
    endpoint that already answered.
31. **A job's `$backoff` property (or `backoff()` method) declares the delay before each retry without the
    worker blocking for it**, which is the difference between a job that releases itself back to the queue
    for another worker to pick up later and one that calls `sleep()` inside `handle()` before failing,
    holding that worker idle for the whole delay. An array of increasing values (`[10, 30, 60]`) is
    exponential backoff declared once, read by the framework, rather than a manual counter reimplementing
    the same schedule inside the job body.
32. **`Sleep::fake()` makes a retry loop's delay fakeable in a test, the same way `Http::fake()` (point 18)
    fakes the network call it's waiting on.** A retry helper written around PHP's own `sleep()`/`usleep()`
    forces its test to either wait out the real delay (slow) or have the sleep stripped out for the test and
    reintroduced for production (untested) — calling `Sleep::for(...)->seconds()` instead keeps the same
    production code path fast under `Sleep::fake()` and asserts on the number of times and how long it slept,
    the delay equivalent of point 21's "assert what the failure carries," applied to timing.
33. **Rethrowing with only a new message and no previous-exception argument discards the original stack
    trace**, which is the detail a tracker needs to find where the failure actually happened. Point 3's
    "adding context and rethrowing" as a legitimate reason for a `catch` only holds if the new exception is
    constructed with the caught one passed as `$previous` (`throw new DomainException($msg, previous: $e)`);
    without it, `getPrevious()` returns null and the report shows the rethrow site as the origin, one layer
    removed from where the code actually failed.
34. **`report_if()`/`report_unless()` guard a report call inline with the exact condition point 12's
    "expected failure, not a defect" already asks for**, and using them instead of a bare `if (...) {
    report($e); }` keeps that condition searchable as one of the tracker's own entry points — a search for
    every `report_if(` call surfaces every place the app decided a failure was conditionally worth flagging,
    where the same logic spelled out as a plain `if` around `report()` blends into ordinary application
    branching and stops being an inventory anyone can run.
35. **The `Exceptions` facade's `->stopIgnoring()`, `->dontReport()` and `->report()` closures registered from
    `bootstrap/app.php` are one central file, and a project still keeping an `App\Exceptions\Handler` class
    from before that change is running two competing registration surfaces at once.** Point 15 already names
    `withExceptions()` as the one place this is configured — the trap is a leftover `Handler::register()` from
    an upgraded project still holding half the rules, so a `dontReport()` entry added to `bootstrap/app.php`
    looks like it should work and does nothing, because the class-based handler never delegates to it.
36. **A `reportable()` closure that returns `false` stops the exception from reaching the default log channel,
    the same way `stop()` (point 23) does on a `report()` method — but only for the report it was registered
    for.** A project registering more than one `reportable()` for overlapping exception types has each one's
    return value checked independently, so an earlier closure returning `false` to suppress the default log
    does not silence a later closure that still wants its own copy reported; the two are not short-circuiting
    each other, they are each answering their own "did I already handle this."
37. **A `renderable()` closure only runs when the request expects the rendered format it returns — it is not
    a blanket override of point 5's negotiation.** Registering `renderable(fn (DomainException $e) => response()->view(...))`
    still lets the framework's own JSON negotiation take over for an API client, because the closure's return
    value is used for the request that reaches it, and a request that never reaches a renderable-eligible path
    (a console command, a queued job) never calls it at all — the closure is a per-exception-type render rule,
    not a second exception handler running instead of the first.
38. **`Context::hidden()` attaches data to the report the same way `Context` (point 26) does, without that
    data leaking into a log line built from the visible context.** Point 13's "identifiers, not payloads" still
    governs what goes in either — the hidden variant exists for data the report needs (an internal trace id
    correlating with an upstream system) but that a structured log statement reading the whole context
    shouldn't print verbatim into every ordinary log entry for the request.
39. **PHPUnit's own assertion failure and a domain exception are not the same kind of throw, and treating an
    assertion failure as "just another exception" to catch in test-support code breaks the test silently.** A
    `try { $this->assertTrue(...); } catch (Throwable $e) { report($e); }` pattern written to "gracefully
    continue" a flaky assertion swallows the one throw PHPUnit relies on to mark the test failed — point 3's
    "an empty catch is a swallow in costume" applies with more consequence here, because the costume is worn
    around the test framework's own failure signal, not around application code.
40. **A job's `failed()` method (point 16) itself can throw, and a second exception raised while handling the
    first one is not retried — it is simply lost unless the queue driver logs it separately.** Code inside
    `failed()` that reaches for the database, an HTTP call, or anything else that can fail needs its own
    guard, because by the time `failed()` runs there is no more retry budget (point 17) for either the
    original failure or a new one thrown while reacting to it — an unguarded `failed()` is where point 12's
    "the tracker has to know the difference" quietly stops being true, for exactly the failures the job most
    needed someone to see.
