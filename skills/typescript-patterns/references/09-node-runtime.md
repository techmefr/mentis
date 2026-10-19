# typescript-patterns §9 — Node runtime: streams, shutdown, a process that will not exit

> Section 9 of `skills/typescript-patterns`. Read it when code runs on Node (a service, a script, a worker, a test
> run) and handles a file or a large flow of data, must stop cleanly, or hangs after the work is done. The other
> sections and the guardrails stay in `SKILL.md`. For a NestJS application the shutdown mechanics are the
> framework's (`skills/nestjs-node-conventions` references/06); this section is the framework-free layer.

## Streams
1. **Compose streams with `pipeline`, not chained `.pipe()`.** `pipeline` gives the composition proper error handling,
   which chained `.pipe()` does not. Use the promise form and `await` it.
2. **Transform with an async generator in the pipeline** for line parsing, filtering and mapping: it receives the
   source as an async iterable and yields results, and back-pressure comes with it. Carry a partial last line across
   chunks (split on newline, keep the tail) and flush it at the end.
3. **Never load a large file or response into memory to process it.** Read as a stream, process in chunks, write as a
   stream. A task that mentions large files, ingestion, CSV or line-by-line processing is a stream task.
4. **Respect back-pressure when writing by hand**: when a write reports that the buffer is full, wait for the drain
   event before writing again, rather than queueing without bound.
5. **Deduplicate and bound the asynchronous lookups inside a transform** (an enrichment call per row): cache by key
   for a short time and limit concurrency, so a million rows do not mean a million identical requests.
6. **Build a stream from an iterable with `Readable.from`**, and use the stream consumers (text, JSON, buffer) for
   small bounded inputs, not as a substitute for streaming.

## Shutdown
7. **One shutdown handler per process, with a bounded delay.** On the termination signals and on an unhandled
   failure: stop accepting work, flip the health and readiness checks to "shutting down" (503) so the orchestrator
   stops routing, drain in-flight work, close the server, then the data connections, in reverse order of opening,
   and exit; if it takes longer than the delay, exit anyway. A small library exists for this (`close-with-grace`);
   without it, a manual handler guards against running twice and clears its own timer.
8. **Size the delay to the platform's termination grace period** (the container orchestrator's), with margin: a
   delay longer than the grace period is cut off by a kill.
9. **Do not hand-write `unhandledRejection` / `uncaughtException` handlers that swallow and carry on.** After an
   uncaught exception the process state is unknown: log, and shut down gracefully through the single handler (the
   library above does this for both events).

## A process or a test run that will not exit
10. **Isolate, bound, identify, fix at the source, repeat.** Reproduce with one file, then one test; run with an
    explicit timeout and a reporter that names the location; list what keeps the loop alive with a handle-listing
    diagnostic (`why-is-node-running`, dev dependency, diagnostic only); fix the teardown in the same scope that
    created the resource; re-run the isolated case many times (30 is a reasonable count) before the full suite.
    Do not call it fixed before the repeated run passes.
11. **The usual handles**: a server started and not closed (await its close), an interval or timer left running (clear
    it, or `unref()` it where it must not hold the process), a database, cache or queue client not disconnected,
    worker threads or child processes still alive, file watchers and readline interfaces left open, a
    fire-and-forget promise never settled, and a teardown hook that throws before reaching the cleanup.
12. **A test creates what it needs and registers its teardown at creation time** (`after` hook of the same scope),
    never in a distant global teardown.

## Mechanical checks

```
grep -rnE "\.pipe\(" src
grep -rnE "readFileSync|readFile\(" src
grep -rnE "process\.on\(['\"](SIGTERM|SIGINT|unhandledRejection|uncaughtException)" src
grep -rnE "setInterval\(" src
grep -rnE "createServer|\.listen\(" src
grep -rnE "closeWithGrace|close-with-grace" src package.json
```

- `.pipe(` between streams is rule 1. `readFile` on a user-sized input is rule 3.
- `setInterval` with no `clearInterval` or `unref` in the same file is a candidate hang (rule 11).
- A `process.on('unhandledRejection', …)` that only logs is rule 9.
