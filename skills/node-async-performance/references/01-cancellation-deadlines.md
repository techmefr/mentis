# node-async-performance §1 — Cancellation and deadlines

A deadline is a promise to the caller that they will hear back by a given time. Keeping that promise and
stopping the work are two different things in Node, and most defects in this section come from treating them
as one.

## 1.1 A race against a timer stops waiting, not the operation

`Promise.race([operation(), timeout(ms)])` settles when the timer fires. The operation is not told. The
query keeps running on the database connection, the outbound request keeps its socket, the file keeps being
read, and whatever side effect it had still lands.

What a reader actually sees: callers get a 504 after two seconds while the downstream service logs a
completed request at eight; the connection pool is full of work nobody is waiting for, so the next
requests queue behind it; a "failed" payment call turns out to have charged the card.

The rule: a deadline is enforced by handing the operation a signal and letting it stop. The race, if kept at
all, is the fallback for an operation that ignores signals, and its result is "outcome unknown", never
"did not happen". Cancellation also does not undo a remote effect: after an abort on a possible write,
reconcile before retrying (an idempotency key, or a read of the resulting state).

## 1.2 Propagate an `AbortSignal` through every layer that waits

Each function on the path that performs or delegates asynchronous work takes a signal (conventionally the
last parameter or an `options.signal`) and passes it on. A layer that drops it silently ends cancellation
for everything below.

- Build the deadline once, at the edge: `AbortSignal.timeout(ms)` yields a signal that aborts after `ms`
  milliseconds (Node 17.3 and 16.14, per the globals documentation). To combine the caller's signal and a
  local deadline, use `AbortSignal.any([callerSignal, AbortSignal.timeout(ms)])` (Node 20.3 and 18.17). The
  reason of the combined signal is the reason of whichever source fired first, which lets a handler tell a
  timeout from a client disconnect.
- Pass it to what accepts one: `fetch(url, { signal })`, `timers/promises` functions, `stream.pipeline`,
  `fs.promises` reads, `events.once`, database drivers that document an abort option. Check the driver
  documentation: a client without signal support needs its own cancel call (a statement cancel, a
  connection destroy), and that call is the cancellation path to wire.
- A budget is shared, not restarted. A request with a five-second deadline that makes three sequential
  calls gives each the time left, not five seconds each. Passing one signal down the whole path does this
  for free; wrapping each call in its own fresh `AbortSignal.timeout(5000)` multiplies the worst case by
  the number of calls.
- Tie the signal to the inbound side: when the client disconnects, abort the work started on its behalf.
  Without that link, an abandoned request keeps consuming a connection and a worker for nobody.

## 1.3 Handle an already-aborted signal

A signal can be aborted before the function starts. Event listeners for `abort` never fire in that case,
because the event already happened, so a function that only registers a listener runs to completion on a
cancelled request.

The rule: check at entry with `signal.throwIfAborted()` (Node 17.3 and 16.17), which throws the signal's
`reason`, and check again after each long suspension point where continuing would be wasteful or unsafe.
When a function registers an `abort` listener, it first checks `signal.aborted` and settles immediately if
true. Settle with the signal's `reason`, not a new generic error, so the caller can classify it.

What a reader sees when this is missing: cancelled jobs that still send their email; a retry loop that
starts one more attempt after its deadline passed; a test that aborts first and then asserts the operation
never started, failing intermittently.

## 1.4 Clean up on every exit

Anything the operation acquired is released whether it completed, threw, or was aborted: timers, abort
listeners, locks, pooled connections, open files, child processes, temporary files.

- Timers: a `setTimeout` started for a deadline is cleared when the operation wins the race. A forgotten
  timer holds a closure alive until it fires and, without `unref`, keeps the process from exiting; in a
  test runner it is the "did not exit one second after the tests" message. The signal-based forms above
  avoid hand-managed timers, which is a reason to prefer them.
- Listeners: a listener added to a long-lived signal or emitter per call and never removed accumulates. The
  runtime eventually prints a possible-leak warning for emitters, and memory grows linearly with traffic.
  Pass `{ once: true }` where one firing is the contract, and remove the listener in the `finally` path.
- Put release in `finally` (or `using` where the runtime supports explicit resource management), never only
  after the success path. Await the release when its completion matters, for example a connection returned
  to the pool before the next request needs it. Close only what this scope opened; a handle received as a
  parameter belongs to its owner.
- A `finally` that can itself throw hides the original error. Keep cleanup simple, or catch and log inside
  it.

## 1.5 Consume or cancel every outbound response body

With `fetch` in Node (undici), receiving the status line is not the end of the exchange: the body is still
attached to the connection. Reading only `response.status` and returning leaves the body unread, and the
connection is not released for reuse until the body is consumed, cancelled, or the garbage collector
eventually collects the response. The undici documentation says leaving this to the collector can lead to
excessive connection usage, reduced connection reuse, and even stalls or deadlocks when the pool runs out of
connections.

What a reader sees: latency creeping up under steady load with CPU idle; connection counts per host climbing;
a service that works in a test and stalls in production after a few thousand calls, recovering when garbage
collection happens to run.

The rule, for every outbound response on every path including the error branches:
- need the body: read it (`await response.json()`, `.text()`, `.arrayBuffer()`) or iterate it fully;
- do not need it (a status check, a redirect, a rejected response you are about to throw on): cancel it
  with `await response.body?.cancel()` before returning or throwing;
- only headers needed: use a `HEAD` request so no body exists.

Check the early-return branches first: the `if (!response.ok) throw ...` line is the usual place a body is
abandoned, because the happy path two lines below does read it. The same logic applies to any streaming
HTTP client: an unread stream holds a socket. For client libraries other than the built-in `fetch`, read
their documentation for the equivalent of "dump" or "destroy" on an unused response.

## 1.6 Review checklist for this section

1. Does every function that waits take and forward a signal, or is there a stated reason it cannot?
2. Is the deadline built once at the edge and shared, or restarted per call?
3. Does an already-aborted signal stop the function at entry?
4. Does every acquired timer, listener, lock and connection have a release in `finally`?
5. Is every outbound response body consumed or cancelled on every branch?
6. After a timeout on a possible write, does the code treat the outcome as unknown?
