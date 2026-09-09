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
