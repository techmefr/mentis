---
name: node-async-performance
description: "Use when writing or reviewing Node.js server code that waits on something (an outbound call, a timer, a batch of promises, a queue consumer) or burns CPU, or when a Node service is slow, stalls under load or grows in memory: cancellation and deadlines (AbortSignal, timer races, unconsumed response bodies), bounded concurrency (Promise.all, allSettled, floating promises, async constructors), and diagnosing performance before changing anything (event-loop delay, RSS versus heap, CPU profile versus heap snapshot, worker thread pools, synchronous APIs, ReDoS). Language-level and framework-neutral; Nest and Express blocks apply on top."
---

# node-async-performance

Step 6 of the pipeline (`WORKFLOW.md`) for Node server code, and a diagnosis step when a Node service is
slow. Sits between `typescript-patterns` (the language: unhandled promises, serial versus parallel awaits)
and `nestjs-node-conventions` (the framework): the part where a promise, a timer or a core API that looks
correct in a diff behaves badly in a running process. Browser-side slowness is `webperf`, not this block.

## When
- Code awaits something that can hang or take long: an HTTP call, a database call, a queue message, a
  lock, a stream. Rules of section 1 apply.
- Code starts several operations at once, or consumes a list of items asynchronously. Section 2 applies.
- A Node service is slow, stalls, times out under load, or its memory grows. Section 3 applies, and it
  applies before any change is made.
- Code on a request path hashes, compresses, parses, matches or reads something that scales with input.
  Sections 3.4 to 3.6 apply.

## Steps

Read the rows whose trigger the task actually meets, not the table. A section read is a section applied.

| § | Covers | Read when | File |
|---|---|---|---|
| 1 | Cancellation and deadlines: a timer race stops waiting not the work, `AbortSignal` propagation, already-aborted signals, cleanup on every exit, unconsumed response bodies | the code awaits anything that can hang or be abandoned by its caller | [`references/01-cancellation-deadlines.md`](./references/01-cancellation-deadlines.md) |
| 2 | Concurrency: `Promise.all` limits, a bounded limiter, `allSettled` scope, floating promises and `void`, async constructors | the code launches several operations at once or loops over async work | [`references/02-concurrency.md`](./references/02-concurrency.md) |
| 3 | Diagnosing Node performance and CPU-bound work: event-loop delay, RSS versus heap, profile kinds, load generator, distributions, one variable, worker pools, synchronous core APIs, ReDoS | a service is slow, stalls or leaks, or request-path code does heavy work | [`references/03-diagnosing-performance.md`](./references/03-diagnosing-performance.md) |

Two rules cut across the three and are kept here because every section leans on them:

1. **A promise is a handle on work already started, not the work itself.** Racing it, ignoring it, or
   awaiting it in a loop changes what the caller observes, never what the process is doing. Every rule in
   sections 1 and 2 follows from this.
2. **Measure before you change, and say what the measurement cannot show.** A theory about where Node
   spends time is wrong often enough that section 3 forbids acting on one. The webperf rule "no
   optimisation without a number" holds here unchanged.

## Output / checkpoint
For code: sections 1 and 2 applied, checked through `gate` (7) and `review` (8) on top of
`typescript-patterns` and the framework block. For a performance task: the baseline, the dominant
constraint with its evidence, one change, the same measurement after, and what remains unverified, in the
format of `references/03-diagnosing-performance.md` §3.8. No checkpoint of its own.

## Guardrails
- No comments in the code produced.
- No performance change without a before and an after taken the same way. A claimed speedup that rests
  on a microbenchmark is reported as a microbenchmark result, not as an endpoint result.
- Nothing is installed to apply these rules. A limiter, a worker pool or a profiler named here may exist
  as a package; the block names it and stops, and the user installs it (`pnpm add <package>`).
- Version and API claims in the references carry the Node version they were checked against (Node 26 docs,
  read 2026-10-08). On a runtime older than the floor stated next to a claim, check the claim before
  relying on it.
- Do not apply section 3.4 as a rewrite order. A synchronous call at startup, in a CLI or in a
  build script is correct; the rule concerns code that runs per request or per message.

## Origin
See [`references/origin.md`](./references/origin.md). Idea and mechanisms rewritten from MIT sources and the
official Node.js documentation, no copied text. 🟡 written, never run on real work.
