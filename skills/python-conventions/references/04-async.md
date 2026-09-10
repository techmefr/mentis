# python-conventions §4 — Async

> Section 4 of `skills/python-conventions`. Read it when an `async def`, a gather, or a blocking call in an async path. The other sections and the guardrails stay in `SKILL.md`.

1. `asyncio.gather` for independent operations, never a serial `await` in a loop out of reflex. The cost is
   additive and invisible when reading top to bottom: three sequential 200 ms calls are a 600 ms response
   that profiles as "the dependencies are slow", and no amount of tuning on their side will move it.
2. **`gather` needs a decision about failure.** By default the first exception propagates while the other
   tasks keep running unattended, so a partial result is discarded and a background task outlives the
   request that started it. Say whether the failures are collected or the group is cancelled — a task group
   is usually the honest form, because it cancels the siblings.
3. **Concurrency without a bound is a way to take down a dependency.** Gathering over a list whose length
   comes from data opens as many connections as the data says, so the same code is fine on ten rows and a
   denial of service on ten thousand. A semaphore or a chunked batch is part of writing the gather, not a
   later optimisation.
4. Never mix blocking code (synchronous I/O, heavy CPU work) into an `async` function without isolating it
   (`run_in_executor`): it blocks the whole event loop, not just the caller. That is the failure mode people
   describe as "the whole service got slow while one report was generating" — one coroutine stalls every
   other request in the process.
5. **The blocking call is usually not obvious.** A synchronous HTTP client, a file read, `time.sleep`, a DNS
   lookup, a template render, a large JSON parse, a library that quietly opens a socket: none of them look
   like I/O at the call site, and none of them will warn. The rule is about auditing what a dependency does,
   not about spotting the word `sleep`.
6. **An async application is async all the way down.** A synchronous database engine or client in an async
   path either blocks the event loop or fails at runtime with a greenlet/context error; use the async engine
   and session, with an async driver in the connection URL. The driver in the URL is the part that gets
   missed, because the code compiles and the error names a greenlet rather than a URL.
7. A coroutine created but never awaited or stored is a silent bug — the runtime's
   `coroutine was never awaited` warning — and is always checked. It is a warning rather than an error, so
   it scrolls past in a busy log, and the code reads as if the work happened.
8. **Fire-and-forget loses the task.** A task created and not kept is only weakly referenced, so it can be
   garbage-collected mid-flight, and if it raises, the exception surfaces at collection time with no context
   — or not at all. Keep the reference, and attach something that reports the failure.
9. **Cancellation is delivered as an exception, and swallowing it breaks shutdown.** A broad `except` inside
   a coroutine catches the cancellation the runtime uses to stop it, so the task refuses to end and the
   process hangs on shutdown or on timeout. Let it propagate; clean up in `finally`.
10. **Every await on something external gets a timeout.** Without one, a dependency that stops answering
    without refusing the connection holds the coroutine for ever, and the request never completes — a
    spinner with no end from the client's point of view (`code-baseline` §4.5).
11. **`async` does not make shared state safe.** There is no lock, only the absence of pre-emption between
    awaits: a read-modify-write with an `await` in the middle can interleave with another request's, so
    check-then-act on module-level state is a race exactly as it would be with threads. Anything shared
    needs an async lock or no `await` in the critical section.
12. **Module-level mutable state is shared across concurrent requests**, which means across users. A cache
    keyed by "the current user", a client holding the last request's credentials, a counter — each serves one
    request's data to the next, more reliably the more traffic there is. That is why it passes every local
    test (§6.2 is the same bug arriving through a container lifetime).
13. **A context variable, not a global, for per-request context.** It is the mechanism that survives the
    concurrency of point 12: each task sees its own value, so a request id or a tenant set at the boundary
    is readable further down without being threaded through every signature.
14. **A synchronous entry point cannot await.** Calling `asyncio.run` from inside a request handler or a
    library function that may already be running in a loop raises, and the workaround people reach for —
    a nested loop, a thread with its own loop — moves the failure rather than fixing it. Decide at the
    boundary whether the code path is async, and keep it that way (point 6).
15. **An async generator has to be closed.** Abandoned part-way, its `finally` runs whenever the collector
    gets to it, so the connection or transaction it held stays open past the request. Consume it fully, or
    wrap it in something that closes it deterministically (§2.14).
16. **`TaskGroup` is the structured form of point 2's failure-handling decision, not an alternative to
    `gather`.** `async with asyncio.TaskGroup() as tg` cancels every sibling task the moment one raises and
    re-raises through an `ExceptionGroup`, so the group cannot leak a running task the way a bare `gather`
    can — the cancel-the-siblings answer point 2 already recommends is what the construct does by default
    instead of by discipline. It needs `except*`, not `except`, to catch what it raises.
17. **A context manager is not automatically safe under cancellation.** `asyncio.CancelledError` can be
    delivered at any `await`, including one inside a manager's `__aenter__`/`__aexit__`, so a resource
    acquired but not yet recorded as acquired can leak on cancellation — the same shape as point 9's
    swallowed-cancellation bug, arriving from a library's own internals rather than from the calling code.
18. **`asyncio.timeout()` scopes a deadline over a block, not over a single call.** `async with
    asyncio.timeout(seconds):` around several awaits cancels whichever one is running when the clock runs
    out and raises `TimeoutError` at the `with` statement, which is often the more honest place to put
    point 10's obligation than threading a timeout argument through every individual call — and it
    composes: an outer timeout still fires even if an inner one hasn't expired yet.
19. **A producer that outruns its consumer needs backpressure, not a growing list.** `asyncio.Queue(maxsize=n)`
    makes `put` await once the queue is full, so a fast producer is slowed to the consumer's pace instead of
    accumulating an unbounded backlog in memory — the same failure as point 3's unbounded gather, but for a
    long-lived pipeline rather than a single batch of calls.
20. **CPU-bound work still blocks the loop from inside a thread.** `asyncio.to_thread` (the modern spelling
    of point 4's executor call) moves a blocking I/O call off the event loop, but a genuinely CPU-bound
    computation blocks whichever thread runs it — including that one — so it stalls every coroutine
    scheduled on that thread's loop just the same; real parallelism for CPU-bound work needs a process, not
    a thread.
21. **`asyncio.shield` protects the waiter, not the shielded work's own lifetime.** Shielding an awaited
    coroutine stops the *awaiting* task's cancellation from reaching it, but the shielded task can still be
    cancelled directly, and the caller that shielded it still has to decide what happens if its own wait is
    cancelled while the shielded work keeps running unobserved in the background.
22. **A signal handler cannot `await`.** `loop.add_signal_handler` runs its callback synchronously on the
    loop, so a graceful shutdown on `SIGTERM`/`SIGINT` means setting an `asyncio.Event` (or a flag checked
    elsewhere) from the handler and awaiting that event in a coroutine — not running cleanup directly inside
    the handler itself.
23. **A subprocess launched from async code is one more thing to time out and reap.**
    `asyncio.create_subprocess_exec` returns as soon as the process starts; forgetting to await its
    completion after `communicate()` fails, or never applying point 10's timeout to a hung child process,
    leaves a zombie process the same way an unawaited coroutine (point 7) leaves silent work undone.
24. **A retry loop around an awaited call needs its own bound, or it is an unbounded wait with extra steps.**
    Retrying without a cap on attempts or elapsed time turns a slow dependency into a request that never
    completes, which is point 10's timeout rule failing one level up — each individual await can time out
    correctly while the loop around it still runs forever.
