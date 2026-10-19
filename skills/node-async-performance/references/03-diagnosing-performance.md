# node-async-performance §3 — Diagnosing Node performance and CPU-bound work

Node serves many clients from one thread running your JavaScript, plus a small pool for some I/O and
cryptography. The Node documentation's own summary of the model is that Node is fast when the work
associated with each client at any moment is small. Almost every Node performance problem is either a piece
of work that is not small, or a wait that was never bounded. This section is how to tell which, and what to
do, in an order that stops you from fixing the wrong thing.

## 3.1 Define the experiment before touching code

Write down, before any change: the route, message or job under test; the payload size distribution; the
concurrency and arrival pattern; warm-up and duration; data volume and cache state; and the metrics, with
latency as percentiles (p50, p95, p99), throughput, and error rate. Same workload, same machine class, same
data afterwards.

1. **One variable at a time.** Two simultaneous changes (a flag and a query rewrite) make the result
   unattributable, and a net gain can hide one change helping and another hurting. Change one, measure, keep
   or revert.
2. **The load generator can be the limit.** A generator on the same machine competes for the same CPU; a
   generator that is single-threaded saturates before the service does; a generator that waits for each
   response before sending the next under-reports latency during stalls (coordinated omission). What a reader
   sees: throughput that plateaus at the same number whatever the service change, and the generator's own
   CPU at 100 percent. Run it elsewhere, check its CPU, and prefer an open-model generator (fixed arrival
   rate) when measuring tail latency.
3. **Compare distributions, not averages.** A mean hides the stalls; one 400 ms event-loop block every second
   barely moves the mean and ruins p99. Report percentiles and the maximum, and look at the shape over time,
   not one summary number.
4. **Say what the measurement cannot show.** A microbenchmark of one function with a warmed cache does not
   prove the endpoint is faster; a benchmark with a diagnostic attached carries that tool's overhead.
5. **Captures can hold sensitive data.** A heap snapshot contains request bodies, tokens and personal data
   that were live in memory, and a CPU profile may carry file paths. Store them like a database dump and do
   not attach them to a ticket.

## 3.2 Event-loop delay is not CPU, and neither is latency

Separate three things that all show up as "slow":
- time spent executing JavaScript on the main thread (CPU-bound, blocks every other request);
- time spent waiting on a dependency, a pool, a queue or the network (the loop is idle, the request is not);
- time spent waiting for the loop itself because something else is running (a symptom, not a cause).

The instruments:
- **Event-loop delay**: `perf_hooks.monitorEventLoopDelay({ resolution })` returns a histogram, in
  nanoseconds, of how late the loop's timer fires; the default resolution is 10 ms. Enable it, read
  `percentile(99)` and `max`, and export them. Rising delay means something is holding the loop: it tells
  you the loop is blocked, not what blocked it.
- **Event-loop utilization**: `performance.eventLoopUtilization()` (Node 14.10 and 12.19) returns `idle`,
  `active` and `utilization`, the ratio of active time over active plus idle. Pass an earlier result to get
  the delta over an interval, which is how to export it as a gauge. High utilization means the loop is
  busy; it is not CPU utilization of the process, which also counts garbage collection, native threads and
  the libuv pool.
- **Process CPU**: from the operating system or the container metrics. Low CPU with high latency points at
  waiting (a pool, a lock, a dependency); high CPU with high loop delay points at computation on the main
  thread; high CPU with low loop delay points at work off the main thread (workers, the pool, garbage
  collection).

Cross-reading the three is the first diagnostic move. A service with loop utilization near 100 percent and
loop delay in hundreds of milliseconds is CPU-bound on the main thread; one with utilization at 10 percent
and slow responses is waiting on something else, and adding workers will not help.

## 3.3 RSS is not heap; a CPU profile is not a heap snapshot

- `process.memoryUsage()` reports `rss`, `heapTotal`, `heapUsed`, `external` and `arrayBuffers`. The
  documentation defines `rss` as the physical memory the process holds, including the heap, the code
  segment and the stack. It also includes native allocations that no JavaScript heap number sees. A buffer
  heavy service, a native addon, allocator fragmentation or a worker's own heap can raise RSS while
  `heapUsed` stays flat. `process.memoryUsage.rss()` is the cheaper call when only RSS is needed.
- Rising RSS alone therefore does not establish a JavaScript leak. Check `heapUsed` after garbage collection
  settles (a growing floor across several cycles), then `external` and `arrayBuffers`. Raising
  `--max-old-space-size` delays the failure of a real leak; it does not repair it.
- The container limit and the V8 heap limit are two numbers. A heap limit equal to the container limit leaves
  no room for RSS outside the heap, and the process is killed by the orchestrator without any JavaScript
  out-of-memory message.

Choose the capture for the question:

| Question | Capture | What it shows |
|---|---|---|
| Where does CPU time go? | CPU profile: `node --cpu-prof app.js` (writes a `.cpuprofile`; flag available since Node 12, documented stable in 20.16 and 22.4), or a profiler attached through the inspector | which functions are on the stack when sampled, as a call tree or flame graph |
| What retains memory? | Heap snapshot: `--heapsnapshot-signal=SIGUSR2` for one on demand, `--heapsnapshot-near-heap-limit=N` near the limit, or `v8.writeHeapSnapshot()` | every live object and the path that retains it; diff two snapshots taken minutes apart under load |
| Where is memory allocated over time? | Heap profile: `--heap-prof` (writes a `.heapprofile`) | allocation sites by sampled volume, not what is still retained |
| Why did it stall or die? | Diagnostic report (`--report-on-signal`, `--report-on-fatalerror`) | a point-in-time snapshot of stacks, libuv handles and resource use |

A CPU profile cannot find a leak, and a heap snapshot cannot find a hot function. Taking the wrong one is the
usual reason an investigation produces a convincing graph and no fix. A snapshot pauses the process and
roughly doubles its memory while it is written, so take it from one replica taken out of rotation, not from
the instance serving traffic near its limit. `--diagnostic-dir` sets where these files land.

## 3.4 Synchronous core APIs do not belong on a request path

Anything synchronous on the main thread stops every other request for its full duration. The Node guide on
not blocking the event loop lists the usual offenders: the `*Sync` file-system calls, the synchronous
cryptography (`pbkdf2Sync`, `randomBytes` and `randomFillSync` without a callback), synchronous compression
(`inflateSync`, `deflateSync`) and the synchronous child-process calls (`spawnSync`, `execSync`,
`execFileSync`).

What a reader sees: p99 latency that tracks the work of one slow request, a health probe that times out while
a single large request is processed, and event-loop delay spikes aligned with one route's call volume.

The rule: on a path that runs per request or per message, use the asynchronous form (callback or promise
API). A synchronous call at process start, in a CLI, in a build script or in a migration is fine; the rule is
about code that runs while the process is serving.

The asynchronous forms are not free either: `crypto.pbkdf2`, `scrypt`, `randomBytes`, key generation, and the
asynchronous zlib calls run on the libuv thread pool, which is small by default and shared with file-system
and DNS lookups (`dns.lookup`). A burst of password hashing can queue behind the pool and slow unrelated file
reads, with the main thread idle. If the pool is the bottleneck (loop delay low, latency high, CPU on worker
threads), reduce the work per call, bound the number of concurrent hashes with a limiter (see
`02-concurrency.md` §2.2), or raise `UV_THREADPOOL_SIZE` as a measured, deliberate change.

Large `JSON.parse` and `JSON.stringify` are in the same class: linear in size, but a tens-of-megabytes body
blocks the loop for a perceptible time. Bound request body size at the edge, and for exports stream or page
instead of building one huge string.

## 3.5 CPU-bound work: `await` does not move it, a pooled worker does

Putting CPU-heavy code behind `async` or `await` does nothing for the loop: the function still executes on the
main thread until it finishes; only waiting is deferred. The same goes for wrapping it in `Promise.resolve`
or `setImmediate` once.

The options, in order of how often they fit:
1. **Remove the work.** Cache the result, avoid the repeated computation, bound the input, or push the cost
   to the database.
2. **Partition it** into slices that yield to the loop between them (`setImmediate` between chunks). Fits
   simple iteration over a large array; a slice must stay small relative to the latency you owe other
   requests.
3. **Offload it** to a worker thread, a child process, or a separate service or queue consumer. A queue is the
   right choice when the result is not needed in the same response, or must survive a restart.

On worker threads, the `worker_threads` documentation states that workers are useful for CPU-intensive
JavaScript and do not help much with I/O-intensive work, because Node's built-in asynchronous I/O is more
efficient than workers can be. It adds that you should use a pool, as the cost of creating workers would
otherwise likely exceed their benefit, and its own example of spawning a worker per call is presented as the
thing to avoid.

The rules:
- **A pool, never one worker per request.** Creating a worker starts a new V8 isolate with its own heap and
  event loop; at request rate that startup cost and memory dominate the computation, and an unbounded count
  exhausts memory under a traffic spike. Size the pool near the number of available cores, queue the tasks
  that exceed it, and bound that queue (reject or shed past a limit).
- **Do not move I/O into workers.** A database call or an HTTP request inside a worker adds a copy and a
  scheduling hop and gains nothing; the main thread was already waiting on it for free.
- **Mind the transfer.** Data passed to a worker is copied (structured clone) unless transferred or shared
  (`ArrayBuffer` transfer, `SharedArrayBuffer`). For large payloads the copy can cost more than the
  computation; measure that, and prefer transferring buffers.
- **Set limits on the worker.** `resourceLimits` on the `Worker` constructor (`maxOldGenerationSizeMb`,
  `maxYoungGenerationSizeMb`, `stackSizeMb`, `codeRangeSizeMb`) bounds the worker's JavaScript heap; reaching
  a limit terminates that worker, so the pool must replace a terminated worker and fail the in-flight task
  cleanly instead of hanging. Those limits do not cover external memory such as `ArrayBuffer`s.
- **Cancellation reaches the pool too.** A task whose caller gave up should be dropped from the queue, and a
  running task killed through `worker.terminate()` (a promise since Node 12.5) when it can never finish.
  Terminating stops JavaScript execution as soon as possible, not instantly.
- A maintained pool library is preferable to a hand-written one (Piscina is the common choice); the block
  names it, the user installs it.

## 3.6 Regular expressions on user input: ReDoS

A regular expression engine that backtracks can take exponential time on input crafted to fail near the end
of a match. In Node the match runs on the main thread, so one request with a short crafted string holds the
loop for seconds or minutes, and several requests hold it indefinitely. It needs no volume: a few kilobytes
and a handful of requests take a service down.

The Node documentation names the shapes that cause it: nested quantifiers such as `(a+)*`, overlapping
alternatives such as `(a|a)*`, and backreferences combined with repetition. A pattern that looks like a
reasonable "path or email or list" check, such as repeating a group that can itself match the same characters
as its neighbour, is the usual carrier.

What a reader sees: CPU pinned at 100 percent on one core with request volume low, event-loop delay of tens
of seconds, a health probe failing, and a profile whose top frame is the regular-expression execution.

The rules:
1. **Prefer no regex.** A plain string operation (`startsWith`, `includes`, `indexOf`, a split and a length
   check) cannot backtrack. Parse structured formats (URLs with `URL`, dates with a date parser) rather than
   validating them with a hand-written pattern.
2. **Bound the input first.** Check length at the edge (body-size limit, schema `maxLength`) before any
   pattern sees the string. A cubic pattern on 100 characters is harmless; on 100,000 it is an outage.
3. **Review every pattern applied to external input** for nested quantifiers and overlapping alternatives.
   Make each quantified group unambiguous so that one input has one way to match. Tools that flag unsafe
   patterns statically exist (`safe-regex` is the one the Node guide names); treat them as a prompt to look,
   not as proof of safety.
4. **For patterns that cannot be made safe, use a linear-time engine** such as RE2 bindings (the Node guide
   points to `node-re2`), accepting that it lacks backreferences and lookarounds, or run the match in a
   worker with a deadline and terminate it on timeout.
5. A pattern in a dependency counts. When a profile points at a library's regex, upgrade or replace the
   library; patching the input shape upstream of it is rarely robust.

## 3.7 Where to look first on a slow service

In the order of usual payoff, each only after the measurement of 3.1 to 3.3 points there:
1. Dependency time: slow queries, N+1 patterns, unbounded results, pool waits, missing deadlines (section 1
   of this block). Database latency dominates framework overhead far more often than the reverse.
2. Unbounded concurrency or queues (section 2): saturating a pool or a downstream.
3. Event-loop blockers (3.4 to 3.6): synchronous APIs, large parse and serialise, regular expressions,
   per-request CPU work.
4. Memory: retained request data, unbounded maps and caches, listeners never removed, large buffers, whole
   result sets materialised in memory.
5. Only then: runtime flags, a different framework or HTTP adapter, caching layers. A cache added before the
   cause is known hides a query problem behind stale data, and a framework migration is justified only after
   profiling shows the adapter overhead is the dominant cost; do not quote a generic framework benchmark as
   proof for this application.

## 3.8 Result format

State the outcome in this shape, so the next reader can reproduce or reject it:

```text
Baseline:    workload + p50/p95/p99 + throughput + error rate
Bottleneck:  the evidence (loop delay, CPU profile frame, dependency span) and the dominant resource
Change:      one intervention
Result:      same metrics, same workload, after the change
Limits:      what the measurement does not show (microbenchmark, no production data, generator headroom)
Next limit:  the resource that now saturates first
```

If the evidence is missing or inconclusive, the report says so and proposes the discriminating measurement,
instead of claiming a speedup or adding speculative complexity.
