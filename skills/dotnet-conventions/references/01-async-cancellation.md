# § 1 — Async, cancellation, threading

> Section 1 of `skills/dotnet-conventions`. Read it when an `async` method, a cancellation token or any
> concurrency is written or modified.

1. All I/O, concurrent and long-running work goes through `async`/`await` + `Task`/`Task<T>`. Raw threading
   primitives (`new Thread`, `Thread.Sleep`, `ThreadPool.QueueUserWorkItem`, `BackgroundWorker`, APM
   `Begin*`/`End*`, `Task.Factory.StartNew`) don't appear in new code. The point is not elegance: a thread
   blocked on I/O cannot serve another request, so under load the app stops accepting work while the CPU is
   idle.
2. An async method is named with the `Async` suffix, takes a `CancellationToken` as its **last** parameter,
   and **propagates that token to every downstream await**. A token accepted and then dropped is worse than
   no token: the signature promises cancellation the implementation doesn't deliver.
3. Never sync-over-async (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`): a classic deadlock on a
   synchronisation context, and it burns a thread while it waits. It works in a console app and in the
   tests, and hangs in a hosting model that has a context — so it ships.
4. `async void` is reserved for event handlers. Elsewhere its exceptions can't be caught and it doesn't
   compose with `await`. An exception from it is raised on the synchronisation context and takes the process
   down rather than reaching the caller's `try`.
5. A `Task` never awaited or stored (implicit fire-and-forget) silently swallows its exceptions. If
   fire-and-forget is genuinely wanted, it's explicit, logged, and its failure path is written down. The
   analyser will not always see it (a returned task whose result is discarded looks like a statement), so
   check by eye at review.
6. `Task.Run` is for **CPU-bound** work only — wrapping I/O in it adds a thread hop and buys nothing.
   Wrapping *synchronous* I/O is worse: the blocked thread just moves to the pool, which grows one thread at
   a time under load.
7. Independent async work is composed with `Task.WhenAll`, not awaited one after another in a loop. The loop
   costs the sum of the latencies: ten 200 ms calls take two seconds.
8. `ConfigureAwait(false)` in shared library code (CA2007); less critical on the ASP.NET Core server side
   (no synchronisation context) but worth being explicit rather than accidental.
9. `CancellationToken.None` is a real value with a real meaning — "this genuinely cannot be cancelled" —
   not a placeholder to make a signature compile.
10. **Cancellation arrives as an exception, and it is not a failure.** A cancelled await throws
    `OperationCanceledException`, so a broad `catch (Exception)` on a shutdown path turns an orderly
    cancellation into a logged error, an alert, and often a retry of work the caller no longer wants.
    Catch it separately, or let it propagate.
11. **Cancellation is cooperative: a token does nothing unless something checks it.** A tight CPU loop, a
    long computation or a `while` over a queue keeps running after the caller has given up. Inside such a
    loop, check the token explicitly; between awaits, the awaited call checks it only if the token was
    actually passed to it (point 2).
12. **The request's token dies with the request, which is wrong for work that must outlive it.** An HTTP
    request's token is cancelled when the client disconnects, so a background continuation reusing it stops
    halfway through a write when the reader closes the tab. Work that has to finish gets its own token from
    the host's lifetime.
13. **`Task.WhenAll` reports one exception and hides the rest.** Awaiting it rethrows only the first faulted
    task's exception; the others sit on the task's `AggregateException`, which nobody reads. Three failures
    out of five calls produce one log line. Where each outcome matters, collect the results and inspect them.
14. **`WhenAll` over a collection whose size you don't control is unbounded parallelism.** A thousand-row
    import becomes a thousand simultaneous HTTP calls or database connections, exhausting the pool and
    failing calls that would have succeeded. Bound it explicitly — the parallel-foreach API with a maximum
    degree, or a semaphore — from what the dependency can take.
15. **A timeout cancels your waiting, not the remote work.** The server carries on and may complete the
    operation, so a retry after a timeout can duplicate the effect (a second charge, a second row) unless
    the operation is idempotent. Decide that before adding the retry.
16. **You cannot `await` inside a `lock`, and a `lock` around async work is the wrong primitive.** A `lock`
    is thread-affine and the continuation may resume on another thread. Where async work needs mutual
    exclusion, use the async-aware semaphore, released in a `finally`: an exception between acquire and
    release deadlocks everything after.
17. **An async iterator's token is not the caller's until you say so.** A method returning an async sequence
    gets its `CancellationToken` from *two* places — its own parameter and the one `await foreach` passes
    when enumeration starts — and they differ. Without the enumerator-cancellation annotation on the
    parameter (and a `default` so it stays optional), the consumer's cancellation reaches nothing: the loop
    keeps producing, the compiler warns, nobody reads it, and the stream ignores a disconnected client. This
    is point 2's broken promise in the one shape where propagating the token by hand is not enough.
18. **The dedicated lock type is a different primitive wearing the old syntax.** Where the language version
    supports it, a field of the lock type used in a `lock` statement compiles to that type's own enter and
    exit — cheaper uncontended and properly scoped. The trap: behaviour is chosen by the *static* type, so
    assigning it to an `object`, or passing it as one, silently reverts to monitor semantics on a boxed
    reference, a second lock nobody meant to take. The compiler warns on the cast; treat the warning as an
    error.
19. **A timeout is a second token linked to the caller's, not a replacement for it.**
    `CancellationTokenSource.CreateLinkedTokenSource(callerToken, timeoutSource.Token)` cancels on whichever
    fires first and keeps both reasons distinguishable. The linked source is disposable and easy to forget
    because it is short-lived — wrap it in a `using` at the call site (point 16's semaphore needs the same
    discipline in `finally`), or the handle leaks for the life of whatever owns the method.
20. **`ValueTask`/`ValueTask<T>` is a single-use optimisation, not a drop-in `Task`.** It avoids an
    allocation on the synchronous-completion path, and that is what makes it unsafe to treat like `Task`:
    awaiting it twice, calling `.Result` on it, or storing it to await later is undefined behaviour the
    compiler won't catch. Await it once, immediately; convert to `Task` first if the caller must hold it or
    await it from several places.
21. **`AsyncLocal<T>` flows forward through `await` and into a child `Task.Run`, never back.** A correlation
    id set before a call is visible to everything that call awaits or spawns, which suits a request id
    threaded through a log scope. A value a child sets afterwards is invisible to code the parent already
    started, so it is the wrong tool for reporting a result back through ambient state — use a return value
    or an `out` parameter.
22. **`IProgress<T>.Report` posts back to the context that created the `IProgress<T>`, not the thread that
    calls it.** `Progress<T>` captures the synchronisation context at construction and marshals every
    `Report` onto it, so background work can drive a UI update with no manual dispatch — but only if the
    `Progress<T>` was constructed on the thread that should receive the callback. Constructing it inside the
    background work silently loses that guarantee.
23. **Thread-pool starvation looks like a slow dependency and is actually a thread shortage,** in the shape
    points 3 and 6 describe: enough blocked or CPU-bound work queued at once that the pool's injection rate
    — one new thread every couple of hundred milliseconds once the minimum is exhausted — cannot keep up, so
    requests that don't block queue behind ones that do. Raising `ThreadPool.SetMinThreads` only masks it;
    the fix is removing the blocking calls, and the honest metric is queue length, not CPU.
24. **`Parallel.ForEachAsync` is point 14's explicit bound, built into the API.** It takes a
    `CancellationToken` and `ParallelOptions.MaxDegreeOfParallelism` directly, runs at most that many bodies
    concurrently and observes cancellation between iterations. Its limit: it fits "run a bounded number of
    async bodies over a sequence" and is wrong when per-item results must be collected, where point 13's
    `WhenAll` critique applies equally.
25. **A `TaskCompletionSource` without `RunContinuationsAsynchronously` runs the continuation on the thread
    that calls `SetResult`.** Bridging a callback API to `Task` with the default constructor runs the
    awaiter's continuation inline inside the driver or socket callback, which can reenter the caller or
    violate a threading assumption of the callback API. `TaskCreationOptions.RunContinuationsAsynchronously`
    posts it to the thread pool: the safe default for a bridge that doesn't control what continuations get
    attached.
26. **A `PeriodicTimer` is awaited, and that is the whole reason it replaces `System.Timers.Timer` in new
    async code.** The older timer fires on a thread-pool thread unrelated to the scheduling `async` method,
    so overlapping ticks run concurrently unless the handler guards itself. `WaitForNextTickAsync` is called
    in a loop from the method that owns the cadence, so the next tick waits for the previous iteration, and
    its token stops the loop like any other cancellation point (point 11).
27. **A synchronisation context is what makes `.Result` deadlock in one host and merely block a thread in
    another, and the failures are diagnosed differently.** An ASP.NET Core server has no context to resume
    on, so blocking only wastes a thread; WPF, WinForms and the older ASP.NET pipeline have a context that
    lets one thread run continuations, so the blocking call and the continuation that would unblock it queue
    for the same thread. That is why point 3's "worked in the console app and the tests" is no coincidence:
    those hosts have no context either, so only the least representative environment catches the bug before
    it ships.
28. **A bounded `Channel<T>` is backpressure with the writer as the one who waits; an unbounded one is
    point 14's unbounded-parallelism failure moved into a queue.** `WriteAsync` on a bounded channel with
    `BoundedChannelFullMode.Wait` suspends the producer once full, so a fast producer can't outpace a slow
    consumer. An unbounded channel accepts every write and defers the cost to memory, growing until the
    process runs out of it rather than failing where the mismatch began. Choose the full mode deliberately:
    `Wait` for a producer that can slow down, `DropOldest`/`DropNewest` only where losing an item is
    acceptable.
29. **`Task.Yield` forces a hop through the scheduler where `await` on an already-completed task would
    not.** A CPU-bound loop that never awaits holds its thread until it returns, starving queued work as in
    point 23; `await Task.Yield()` periodically lets other work run between chunks without a real
    asynchronous operation. It does not replace point 6 — genuinely CPU-bound work still belongs on
    `Task.Run`; it stops a long synchronous loop already on a shared thread from monopolising it.
30. **`SemaphoreSlim.WaitAsync` has a timeout overload, and skipping it turns point 16's primitive into an
    indefinite wait.** A caller that gives `WaitAsync` no `TimeSpan` or token blocks as long as the semaphore
    stays held — point 16's deadlock shape if the holder throws between acquire and release, but visible
    only as a hang with no exception. Pass a timeout and treat the `false` return as "could not acquire in
    time", distinct from cancellation.
31. **`IHostedService.StartAsync` runs before the host reports ready, so a long-running body there instead
    of in `BackgroundService.ExecuteAsync` blocks startup.** The host awaits every `StartAsync` before
    accepting traffic, so a subscription or poll that belongs in the ongoing loop, placed in `StartAsync`
    instead of kicked off and left running, makes every deploy wait for its first iteration — and a slow
    first run reads as the whole application failing to come up.
32. **A `Task` from an event handler or fire-and-forget dispatch that the framework does not await completes
    on its own schedule, and downstream code that assumes it already ran is wrong.** This is point 5's
    hazard from the caller's side: even a logged, intentionally unawaited task races whatever runs next, so
    a value it was meant to set can be read before it is set. Where the caller needs the result, it needs the
    await; a comment justifying why not is no substitute for the ordering only `await` provides.
33. **A `CancellationTokenSource.CancelAfter` timer is disposed with its source, and forgetting it leaks like
    point 19's linked source, with one extra trap.** `CancelAfter` schedules an internal timer; disposing
    the source before it fires cancels the callback, but a source never disposed keeps the timer (and its own
    resources) alive as long as anything references it. It is point 24's disposal rule applied to a source
    with a timer.
34. **`Task.WhenEach` streams completions instead of collecting them, which changes point 7's "compose,
    don't loop" advice.** `WhenAll` (point 13) and a manual loop both wait for the slowest item;
    `await foreach (var task in Task.WhenEach(tasks))` yields each task as it finishes, in completion order,
    so acting on the fastest results first (cancel the rest once one succeeds, stream partial progress) no
    longer needs the `WhenAny`-in-a-loop pattern that removed finished tasks by hand. It is still a
    collection of already-created tasks, not a bound — point 14's warning applies to what you hand it.
35. **`Task.WaitAsync(TimeSpan)` or `Task.WaitAsync(CancellationToken)` times out the *wait*, not the
    operation: point 15's warning with less code around it.** It replaces a hand-built linked source (point
    19) at each call site, throwing `TimeoutException` (or `OperationCanceledException` for the token
    overload) without cancelling the underlying task, so point 15's duplicate-effect risk and
    idempotency question still apply.
36. **`ConfigureAwaitOptions` replaces the bare boolean with independent flags, and `SuppressThrowing` is the
    one that changes behaviour.** `ConfigureAwait(ConfigureAwaitOptions.None)` and its siblings compose
    `ContinueOnCapturedContext`, `ForceYielding` and `SuppressThrowing` instead of point 8's true/false.
    `SuppressThrowing` observes a faulted or cancelled task without raising, a narrow, explicit alternative
    to point 5's silent fire-and-forget — narrow because it must still be paired with inspecting the task's
    status, or it is the same swallowed failure spelled differently.
37. **LINQ over `IAsyncEnumerable<T>` takes its cancellation on the operator chain, not on the source.** The
    `System.Linq.AsyncEnumerable` operators (.NET 10) accept a token through `WithCancellation` applied to
    the chain, as `await foreach` always has (point 17). A token passed only to the method that built the
    sequence, with none applied to the `Where`/`Select` pipeline consuming it, stops nothing mid-pipeline:
    the wiring point 17 describes depends on where `WithCancellation` sits, not on who iterates.
38. **A synchronous `lock` and an async wait are not interchangeable just because both block, and
    `System.Threading.Lock`'s `TryEnter` with a timeout is only the synchronous half of point 30's
    problem.** `Lock.EnterScope()` (point 18) is thread-affine like the `lock` statement — right for a
    short synchronous critical section, wrong for anything that awaits inside it. Its timeout-bearing
    `TryEnter` avoids an indefinite wait only for callers that never await, and does nothing for the
    async-aware case the semaphore exists for.
39. **A `CancellationToken` captured in a closure passed to `Task.Run` is frozen when the closure is built,
    not re-read from the field that held it.** A method that stores its token in a field and later starts
    background work through a lambda closes over the field access only if the lambda reads it fresh each
    time; assigning the token to a local first captures its value at that line, so a token replaced or
    linked (point 19) afterwards cancels a copy nothing downstream holds — point 12's mismatch, reached
    through capture semantics instead of scope.
40. **A delay, timeout wait or timed cancellation read against the wall clock directly is the ambient read
    point 06.4 forbids for business logic, and `Task.Delay`, `Task.WaitAsync` and `CancellationTokenSource`
    now have `TimeProvider` overloads that remove the excuse.** Pass the injected time abstraction into
    `Task.Delay(delay, timeProvider, token)`, `Task.WaitAsync(timeout, timeProvider)` or the
    `CancellationTokenSource(TimeSpan, TimeProvider)` constructor, so a test advances a fake clock and sees
    the delay, timeout or cancellation fire instantly and deterministically. Code that still calls the
    two-argument overloads on a path a test must control sleeps for real in that test.
41. **A primitive chosen for scheduling is a different question from point 18's, and
    `System.Threading.Lock` answers only mutual exclusion.** `Lock.EnterScope()` (point 18) replaces a
    `Monitor`-based `lock` for a short synchronous critical section and is cheaper uncontended because it
    skips the object-header sync block a plain `object` needs. Using it to "make this faster" in code that
    spends its time waiting on I/O optimises a cost that was never the bottleneck: whether the problem is
    CPU-bound synchronisation or I/O-bound waiting (point 6) decides between a faster lock and an
    `async`-aware wait.
42. **`Task.Factory.StartNew` does not unwrap a delegate that returns a `Task`: an async lambda produces a
    `Task<Task>` that no longer represents the work.** Awaiting the outer task only waits for the delegate's
    synchronous prefix (up to its first `await`) and observes neither the exceptions nor the completion of
    the inner task unless the caller calls `Unwrap()`. `Task.Run` unwraps automatically, one more reason
    point 6's `Task.Run`-not-`StartNew` is the safer default rather than a style choice.
43. **`TaskCreationOptions.LongRunning` only affects the delegate's synchronous prefix; on an async delegate
    it hints about the shortest part of the work.** The flag asks for a dedicated thread instead of a pool
    thread — right for work that would hold a pool thread for minutes — but for an `async` delegate that
    thread runs only until the first `await`, after which the continuation resumes on an ordinary pool
    thread, so the hint covers code that finished before the long-running part (the awaited I/O) began.
44. **A type implementing `IAsyncDisposable` in a hierarchy meant to be extended needs a protected
    `DisposeAsyncCore` beside the public `DisposeAsync`, as `Dispose`/`Dispose(bool)` does for the
    synchronous pattern.** Without that seam a derived class either hides the base's public `DisposeAsync`
    (a caller holding a base reference skips the derived cleanup) or has nowhere correct for its own async
    cleanup. A type offering only `IAsyncDisposable` also forces synchronous callers, who cannot
    `await using`, to block on `DisposeAsync().AsTask()` — point 3's hazard through a missing `Dispose()`
    overload.
45. **`System.Threading.Lock` (point 18) is gated by the target framework, not the C# language version, so
    "where the language version supports it" is the wrong test.** The type does not exist on `net8.0` or
    earlier — it ships in .NET 9's BCL — so a project on the current LTS with a recent `LangVersion` gets
    `CS0246` when `Lock` is used as a field type: the compiler understood the pattern-based dispatch; there
    was no type to resolve. Check the target framework moniker, not only the language version; on `net8.0`
    a plain `object` remains the field for a `lock` statement.
