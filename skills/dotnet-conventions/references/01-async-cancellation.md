# § 1 — Async, cancellation, threading

> Section 1 of `skills/dotnet-conventions`. Read it when an `async` method, a cancellation token or any
> concurrency is written or modified.

1. All I/O, concurrent and long-running work goes through `async`/`await` + `Task`/`Task<T>`. Raw threading
   primitives (`new Thread`, `Thread.Sleep`, `ThreadPool.QueueUserWorkItem`, `BackgroundWorker`, APM
   `Begin*`/`End*`, `Task.Factory.StartNew`) don't appear in new code. What the modern form buys is not
   elegance: a thread blocked on I/O is a thread the server cannot use for another request, so under load
   the app stops accepting work while the CPU is idle.
2. An async method is named with the `Async` suffix, takes a `CancellationToken` as its **last** parameter,
   and **propagates that token to every downstream await**. A token accepted and then dropped is worse than
   no token: the signature promises cancellation the implementation doesn't deliver.
3. Never sync-over-async (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`): a classic deadlock on a
   synchronisation context, and it burns a thread while it waits. The deadlock is the visible half; the
   invisible half is that it works in a console app and in the tests, and hangs in the hosting model that
   has a context — so it ships.
4. `async void` is reserved for event handlers. Elsewhere its exceptions can't be caught and it doesn't
   compose with `await`. An exception from an `async void` method is raised on the synchronisation context
   and takes the process down rather than reaching the caller's `try`.
5. A `Task` never awaited or stored (implicit fire-and-forget) silently swallows its exceptions. If
   fire-and-forget is genuinely wanted, it's explicit, logged, and its failure path is written down. The
   analyser will not always see it — a task returned from a method whose result is discarded looks like a
   statement — so this is one to check by eye at review.
6. `Task.Run` is for **CPU-bound** work only — wrapping I/O in it adds a thread hop and buys nothing.
   Wrapping *synchronous* I/O in it is worse than nothing: it moves the blocked thread to the pool, where
   it still blocks, and the pool grows one thread at a time under load.
7. Independent async work composed with `Task.WhenAll`, not awaited one after another in a loop. The loop
   is not slow by a constant — it is the sum of the latencies, so ten 200 ms calls take two seconds and
   the reader waits for all of them.
8. `ConfigureAwait(false)` in shared library code (CA2007); less critical on the ASP.NET Core server side
   (no synchronisation context) but worth being explicit rather than accidental.
9. `CancellationToken.None` is a real value with a real meaning — "this genuinely cannot be cancelled" —
   not a placeholder to make a signature compile.
10. **Cancellation arrives as an exception, and it is not a failure.** A cancelled await throws
    `OperationCanceledException`, so a broad `catch (Exception)` on a shutdown path turns an orderly
    cancellation into a logged error, an alert, and often a retry of work the caller no longer wants.
    Catch it separately, or let it propagate — it is the mechanism, not an incident.
11. **Cancellation is cooperative: a token does nothing unless something checks it.** A tight CPU loop, a
    long computation or a `while` over a queue keeps running to the end after the caller has given up,
    holding whatever it holds. Inside such a loop, check the token explicitly; between awaits, the awaited
    call does it for you only if the token was actually passed to it (point 2).
12. **The request's token dies with the request, which is exactly wrong for work that must outlive it.**
    An HTTP request's cancellation token is cancelled when the client disconnects, so a background
    continuation that reuses it stops halfway through a write the moment the reader closes the tab. Work
    that has to finish gets its own token from the host's lifetime, not the request's.
13. **`Task.WhenAll` reports one exception and hides the rest.** Awaiting it rethrows the first faulted
    task's exception only; the others are on the task's own `AggregateException`, which nobody reads. So
    five parallel calls where three failed produce one log line, and the incident looks smaller than it
    is. Where the outcome of each matters, collect the results and inspect them.
14. **`WhenAll` over a collection whose size you don't control is unbounded parallelism.** A thousand-row
    import becomes a thousand simultaneous HTTP calls or database connections, which exhausts the pool and
    fails the ones that would otherwise have succeeded. Bound it explicitly — the parallel-foreach API
    with a maximum degree, or a semaphore — and pick the bound from what the dependency can take.
15. **A timeout cancels your waiting, not the remote work.** Cancelling after a delay stops the caller; the
    server carries on and may well complete the operation. So a retry after a timeout can duplicate the
    effect — a second charge, a second row — unless the operation is idempotent. Decide that before adding
    the retry, not after the duplicate is reported.
16. **You cannot `await` inside a `lock`, and reaching for one around async work is the wrong primitive.**
    A `lock` is thread-affine and the continuation may resume on another thread. Where async work genuinely
    needs mutual exclusion, use the async-aware semaphore — and release it in a `finally`, because an
    exception between acquire and release deadlocks everything that comes after.
17. **An async iterator's token is not the caller's until you say so.** A method returning an async sequence
    takes its `CancellationToken` from *two* places — its own parameter and the one the `await foreach`
    passes when it starts enumerating — and they are not the same token. Without the enumerator-cancellation
    annotation on the parameter (and a `default` so it stays optional), the consumer's cancellation reaches
    nothing: the loop keeps producing, the compiler says so in a warning nobody reads, and the symptom is a
    stream that ignores a disconnected client. This is point 2's promise-you-don't-keep, in the one shape
    where propagating the token by hand is not enough.
18. **The dedicated lock type is a different primitive wearing the old syntax.** Where the language version
    supports it, a field of the lock type used in a `lock` statement compiles to that type's own enter and
    exit — cheaper on the uncontended path and scoped properly. The trap is that the behaviour is chosen by
    the *static* type: assign it to an `object`, or pass it as one, and the statement silently goes back to
    monitor semantics on a boxed reference, which is a second lock nobody meant to take. The compiler warns
    on the cast; treat that warning as an error rather than a style note.
19. **A timeout is a second token linked to the caller's, not a replacement for it.**
    `CancellationTokenSource.CreateLinkedTokenSource(callerToken, timeoutSource.Token)` cancels on whichever
    fires first and keeps both reasons distinguishable if the caller checks which token requested it. The
    linked source is disposable and easy to forget precisely because it is short-lived — wrap it in a
    `using` at the call site, the same discipline point 16's semaphore needs in `finally`, or the handle
    leaks for the life of whatever owns the method.
20. **`ValueTask`/`ValueTask<T>` is a single-use optimisation, not a drop-in `Task`.** It exists to avoid an
    allocation on the common synchronous-completion path, and that saving is exactly what makes it unsafe to
    treat like the type it replaces: awaiting it twice, calling `.Result` on it, or storing it to await later
    are all undefined behaviour the compiler will not catch, where the equivalent on a `Task` merely returns
    a cached result. Await it once, immediately, and convert to `Task` first if the caller needs to hold onto
    it or await it from more than one place.
21. **`AsyncLocal<T>` flows forward through `await` and into a child `Task.Run`, never back.** A correlation
    id set before a call is visible to everything that call awaits or spawns, which is what makes it useful
    for a request id threaded through a log scope without passing it as a parameter everywhere. The direction
    is one-way: code the parent already started cannot see a value a child sets afterwards, so it is the
    wrong tool for anything that looks like "let the callee report a result back through ambient state" —
    that is what a return value or an `out` parameter is for.
22. **`IProgress<T>.Report` posts back to the context that created the `IProgress<T>`, not the thread that
    calls it.** The standard `Progress<T>` implementation captures the synchronisation context at
    construction and marshals every `Report` call onto it, so a long-running async operation can report
    progress from a background thread straight into a UI update with no manual dispatch — but only if the
    `Progress<T>` was constructed on the thread that should receive the callback. Constructing it inside the
    background work itself silently loses that guarantee and the callback runs wherever `Report` happened to
    be called.
23. **Thread-pool starvation looks like a slow dependency and is actually a thread shortage,** and it
    arrives in the shape point 3 and point 6 both describe: enough blocked or CPU-bound work queued at once
    that the pool's injection rate — one new thread every couple of hundred milliseconds once the minimum
    is exhausted — cannot keep up with demand, so requests that don't block at all queue up behind ones
    that do. Raising `ThreadPool.SetMinThreads` masks the symptom for a while; removing the blocking calls
    that caused the queue in the first place is the actual fix, and the metric that shows the problem
    honestly is the queue length, not CPU.
24. **`Parallel.ForEachAsync` is point 14's explicit bound, built into the API instead of hand-rolled with a
    semaphore.** It takes a `CancellationToken` and a `ParallelOptions.MaxDegreeOfParallelism` directly,
    running at most that many bodies concurrently and observing cancellation between iterations without the
    caller wiring either by hand — which is also its limit: it is the right tool for "run this bounded
    number of async bodies over a sequence," and the wrong one to reach for when what's actually needed is
    collecting per-item results, which point 13's `WhenAll` critique applies to just as much here.
25. **A `TaskCompletionSource` without `RunContinuationsAsynchronously` runs the continuation on the thread
    that calls `SetResult`, not on a thread pool thread of its own.** Bridging a callback-based API to
    `Task` with the default constructor means whatever code calls `SetResult` — often deep inside a driver
    or a socket callback with its own constraints — now also runs the awaiter's continuation inline, on that
    thread, which can reenter the caller or violate a threading assumption the callback API depended on.
    Passing `TaskCreationOptions.RunContinuationsAsynchronously` posts the continuation to the thread pool
    instead, which is the safe default for a bridge that doesn't control what continuations get attached.
26. **A `PeriodicTimer` is awaited, and that is the entire reason it replaces `System.Timers.Timer` in new
    async code.** The older timer fires its callback on a thread-pool thread with no relationship to
    whatever `async` method scheduled it, so overlapping ticks under load run concurrently unless the
    handler guards itself; `PeriodicTimer.WaitForNextTickAsync` is called in a loop from the method that
    owns the cadence, so the next tick genuinely waits for the previous iteration to finish and the token
    passed to `WaitForNextTickAsync` stops the loop the same way any other cancellation point does (point
    11).
27. **A synchronisation context is what makes `.Result` deadlock in one host and merely block a thread pool
    thread in another, and the two failures are diagnosed differently.** Point 3 states the rule; the
    reason it's absent from an ASP.NET Core server (no context to resume on, so blocking merely wastes a
    thread) but present in WPF, WinForms and the older ASP.NET pipeline (a context that only lets one thread
    run continuations at a time, so the blocking call and the continuation that would unblock it queue for
    the same thread) is why "it worked in the console app and the tests" in point 3 is not a coincidence —
    those hosts have no synchronisation context either, so only the least representative environment
    catches the bug before it ships.
28. **A bounded `Channel<T>` is backpressure with the writer as the one who waits, and an unbounded one is
    point 14's unbounded-parallelism failure moved into a queue instead of a fan-out.** `WriteAsync` on a
    bounded channel with `BoundedChannelFullMode.Wait` suspends the producer once the channel is full,
    which is what keeps a fast producer from outpacing a slow consumer without either side polling; an
    unbounded channel accepts every write immediately and defers the cost to memory, so a producer faster
    than its consumer for any sustained period grows the queue until the process runs out of it rather than
    failing at the point the mismatch started. Choose the full mode deliberately too — `Wait` for a
    producer that can tolerate slowing down, `DropOldest`/`DropNewest` only where losing an item is
    genuinely acceptable — because the default silently picked is not obviously either.
29. **`Task.Yield` forces a hop through the scheduler where an `await` on an already-completed task would
    not, and that difference is the entire reason to reach for it.** A CPU-bound loop that never awaits
    anything holds its thread until it returns, which starves everything else queued on that thread pool the
    same way point 23 describes; inserting `await Task.Yield()` periodically gives other queued work a
    chance to run between chunks without introducing an actual asynchronous operation to wait for. It is not
    a substitute for point 6's rule — genuinely CPU-bound work still belongs on `Task.Run` — it is what keeps
    a long synchronous loop that already runs on a shared thread from monopolising it.
30. **`SemaphoreSlim.WaitAsync` takes a timeout overload, and skipping it turns point 16's mutual-exclusion
    primitive into an indefinite wait with no way out.** A caller that never provides a `TimeSpan` or a
    token to `WaitAsync` blocks for as long as the semaphore stays held — which is exactly the deadlock
    shape point 16 already warns about if the holder throws between acquire and release, except now visible
    only as a hang with no exception raised anywhere. Passing a timeout and treating the `false` return as a
    genuine "could not acquire in time" case, distinct from cancellation, gives the caller a path out that a
    bare `await WaitAsync(token)` does not.
31. **`IHostedService.StartAsync` runs before the host reports itself ready, and a long-running body placed
    there instead of in `BackgroundService.ExecuteAsync` blocks startup itself.** The host awaits every
    registered service's `StartAsync` before accepting traffic, so code that belongs in the ongoing loop —
    a subscription that runs for the app's lifetime, a poll that never returns — placed in `StartAsync`
    instead of kicked off and left running makes every deploy wait for that first iteration to finish, which
    for a job whose first run happens to be slow reads as the whole application failing to come up rather
    than as one background task being slow.
32. **A `Task` returned from an event handler or a fire-and-forget dispatch that the framework does not await
    completes on its own schedule, independent of whatever triggered it — and code downstream that assumes
    it already ran has assumed wrong.** This is point 5's fire-and-forget hazard from the caller's side
    rather than the callee's: even a properly logged, intentionally unawaited task still races whatever runs
    next in the calling method, so a value the task was supposed to have set is read before it's guaranteed
    to be set. Where the caller needs the result, it needs the await; a comment justifying why it doesn't is
    not a substitute for the ordering guarantee only `await` provides.
33. **A `CancellationTokenSource.CancelAfter` timer is disposed with the source it belongs to, and forgetting
    it leaks the same way point 19's linked source does — with one extra trap.** `CancelAfter` schedules an
    internal timer against the token source it was called on; disposing the source before the timer fires
    cancels the pending callback, but a source that outlives its useful life because nothing ever calls
    `Dispose` on it keeps that timer (and the source's own resources) alive for as long as whatever holds the
    reference does. It is point 24's disposal rule applied to a source with a timer attached rather than a
    plain linked one.
