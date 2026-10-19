# node-async-performance §2 — Concurrency in async code

JavaScript runs your code on one thread, but the operations you start run alongside each other in the
runtime, the network and the database. "Single-threaded" therefore says nothing about how many operations
are in flight, and that number is what saturates pools, sockets and downstream services.

## 2.1 `Promise.all` neither limits concurrency nor cancels siblings

`Promise.all(items.map(fn))` calls `fn` for every item before the first one finishes. If `items` has ten
thousand entries, ten thousand operations start at once. And when one promise rejects, `Promise.all` rejects
immediately, but the other operations are not stopped: they keep running, their results are discarded, and
their own later rejections are swallowed by the combinator.

What a reader sees: a batch endpoint that works with 50 rows and exhausts the connection pool, file
descriptors or the downstream rate limit with 5,000; memory spiking because every payload is in flight at
once; after one failed item, the log still shows the other items' side effects arriving seconds after the
request returned an error.

The rule: `Promise.all` is for a small, statically bounded set of independent operations (two or three
calls the handler makes in parallel). Anything sized by data or by the caller goes through a bounded
limiter (2.2). When siblings must stop after the first failure, give them a shared `AbortController` and
abort it in the failure path (see 1.2); rejection alone does nothing to them.

## 2.2 Bound the work with a limiter

A limiter holds a queue and admits at most N operations at a time; the rest wait unstarted. N is chosen from
the scarcest resource the operations touch: the pool size, the downstream's published rate, the memory each
in-flight item costs. Not from the number of cores: these operations wait on I/O.

- Use a maintained limiter (the `p-limit` and `p-map` packages are the common ones, `p-map` taking a
  `concurrency` option) or a small loop of N workers pulling from a shared iterator. The block names them
  and does not install them.
- Bound the waiting work as well as the active work. A limiter with an unbounded queue only moves the
  overload from "too many in flight" to "too many pending"; for a server fed by requests or messages,
  reject or shed when the queue passes a threshold instead of queueing forever.
- A serial `for ... await` is the limiter with N = 1. It is correct when each step depends on the previous
  one or when order matters. It is wasteful when steps are independent and the downstream can take more, and
  that is a measured trade, not a reflex in either direction (`typescript-patterns` §2.2 covers the serial
  case).
- Pass the signal into the limited function (1.2) and stop admitting new items once it is aborted; the queue
  must not keep draining on a cancelled request.

## 2.3 `allSettled` only where partial failure is tolerated

`Promise.allSettled` never rejects; it returns a status per input. That is the right tool when the caller
can act on a mix: a dashboard assembled from five widgets where one failing renders a placeholder, a
notification fan-out where per-recipient failures are recorded and retried.

It is the wrong tool as a way to avoid handling errors. Used on a unit of work that is supposed to be
all-or-nothing, a transfer, a multi-row write, an order and its stock reservation, it turns a failure into a
silent partial state, because nothing throws and the code proceeds on the fulfilled results.

The rule: after `allSettled`, the code inspects every rejected entry and does something deliberate with it
(record, retry, surface in the response, fail the whole request). A call to `allSettled` followed by only
reading the fulfilled values is a defect to flag. Reasons are untyped (`unknown`): narrow before use.

## 2.4 `void` does not handle a rejection

`void doThing()` and a bare `doThing()` call without `await` both create a promise nobody observes. The
`void` operator only tells the linter you meant it; it attaches no handler. If that promise rejects, the
rejection is unhandled. Node's default for unhandled rejections is to raise them as an uncaught exception
and terminate the process, since Node 15 (stated from the CLI documentation's `--unhandled-rejections`
modes; not re-verified on a page fetch in this pass).

What a reader sees: a process that crashes at a random moment, hours after the request that triggered the
background call returned success; or, where a handler for `unhandledRejection` is installed, a log line with
no request context and a feature that quietly does not work.

The rule: a fire-and-forget call is a deliberate decision with an owner and a failure policy. Either await
it, or attach a handler at the call site that records the failure with its context (`.catch(logAndRecord)`),
or hand the work to a queue that has retry and dead-letter semantics. If the work must survive the request,
or must not run twice, it belongs in a queue, not a floating promise; the process can be stopped at any
moment and the promise goes with it. A global `unhandledRejection` handler is a last-resort diagnostic, not a
substitute for handling at the call site.

Also check floating promises inside callbacks that return nothing useful: `array.forEach(async ...)` starts
all of them and awaits none; the surrounding function returns before any finishes and their errors are
unhandled. Use a loop with `await`, or the limiter from 2.2.

## 2.5 No async constructor

A constructor returns the instance synchronously. It cannot be `async`, and doing asynchronous setup inside
it (kicking off a connection, loading a file) produces an object whose methods may run before it is ready,
plus a promise stored or dropped nowhere, which is a floating promise (2.4).

The rule: construct in two steps. A private or trivial constructor holds already-resolved dependencies, and a
static `create` (or a plain factory function) performs the asynchronous work and returns the instance:
`const db = await Database.create(config)`. Callers cannot obtain an unready object. In a dependency
injection container, express the same thing as an asynchronous provider (a factory provider that returns a
promise) or an initialisation hook the container awaits before accepting traffic, never a constructor that
starts work and hopes. Readiness of a service that is not ready until some work completes belongs in its
readiness probe.

## 2.6 State across suspension points

Between two `await`s, any other callback can run. A read-modify-write on shared state spanning an `await` is
not atomic across concurrent requests, even though no two lines run simultaneously. Check-then-act on an
in-memory map, a counter, or a "does it exist, then create it" against a database all race. Fix it with a
database constraint or atomic statement, a single-flight map keyed by the work, or a serialising queue,
whichever matches where the state lives. Process-local fixes do not hold across several replicas; for that,
the rule moves to the data store.

## 2.7 Review checklist for this section

1. Is every `Promise.all` over a statically small set, with data-sized batches going through a limiter?
2. Is the limiter's N derived from the scarcest resource, and is its queue bounded?
3. After `allSettled`, is every rejected entry handled on purpose?
4. Is every un-awaited promise either handled at the call site or moved to a queue?
5. Any `forEach(async ...)`?
6. Is asynchronous setup done by a factory or an awaited provider, never a constructor?
7. Any read-modify-write spanning an `await` on shared state?
