# Origin: node-async-performance

🟡 written 2026-10-08, never run on real work. No dogfood, no incident behind any rule: the sections are a
synthesis of sources, and a rule earns more than 🟡 only by catching a real defect in a real review or run.
Independent verification 2026-10-21: 17 checked, 17 matched, 0 corrected, 0 unverified

## Sources and licences

- `mcollina/skills`, the `node` rules on async patterns, performance and profiling. MIT, read 2026-10-08.
  Gave the topic list for bounded concurrency, factories instead of async constructors, `AbortController`
  deadlines, worker pools for CPU work, and the profile-then-measure loop. Its code examples were not
  reused; the explanations of failure modes in this block are rewritten.
- `Dankosik/fastify-backend-skills`, the TypeScript async and performance skills. MIT, read 2026-10-08.
  Gave the framing that `Promise.all` neither limits nor cancels, that `void` does not handle a rejection,
  that a timer race stops waiting and not the operation, that already-aborted signals and unconsumed
  response bodies need handling, that event-loop utilization is not CPU utilization, that rising RSS is not
  a heap leak, and that the load generator can be the limit. The mechanisms were rewritten and extended
  with what a reader observes when each one breaks.
- `amirtaherkhani/nestjs-agent-skills`, the performance-diagnosis reference. MIT, read 2026-10-08. Gave the
  experiment-definition checklist, "one variable at a time", the pooled-worker-not-per-request rule and the
  result format of 3.8, rewritten.
- `mkosir/typescript-style-guide`. MIT, read 2026-10-08, consulted for TypeScript conventions only; nothing
  specific to this block comes from it.

## Primary documentation (verified, Node.js documentation, read 2026-10-08)

AbortSignal statics and `throwIfAborted` and `reason` with their version ranges (globals); `timers/promises`
signal option and `AbortError`; `performance.eventLoopUtilization` and `monitorEventLoopDelay` (perf_hooks);
`process.memoryUsage` and the definition of `rss`; `--cpu-prof`, `--heap-prof`, `--heapsnapshot-signal`,
`--heapsnapshot-near-heap-limit`, `--diagnostic-dir` (CLI); `worker_threads` statements on CPU versus I/O,
pooling, `resourceLimits` and `terminate`; the "Don't block the event loop" guide for the synchronous API
list, ReDoS shapes and the libuv pool membership; the undici documentation on unconsumed response bodies.
Section 3.6 was written from the Node guide's description of the mechanism and from engine behaviour, not
from `goldbergyoni/nodebestpractices`.

## Idea-only, never phrased from

`Kadajett/agent-nestjs-skills` (no licence), `goldbergyoni/nodebestpractices` (CC-BY-SA-4.0),
`trailofbits/skills` (CC-BY-SA-4.0): used at most to cross-check that a topic exists. No sentence here
derives from them.

## Source pass 2026-10-20

Official Node.js documentation read as a source of facts only, rewritten in our words, no text copied: CLI
(`--unhandled-rejections` modes and the v15.0.0 default change to `throw`; `--cpu-prof` and `--heap-prof` stable
since 22.4 and 20.16; `--heapsnapshot-signal`), process (`unhandledRejection`), globals (`AbortSignal.timeout`,
`any`, `throwIfAborted`, `reason` with their versions), stream (promise `pipeline` and `finished` accept a
signal), fs (`readFile` and `writeFile` signal is best effort, buffering only), events (`once` signal, default
10 listeners, no warning on `AbortSignal`, `addAbortListener`), v8 (heap snapshot needs about twice the heap and
blocks the loop), the Node 24.0.0 release note (V8 13.6 carries explicit resource management), the "Don't block
the event loop" guide, and the undici `Dispatcher` page (bodies must be consumed or destroyed; `dump`).
Licence of the one permissive repository read this pass: `sindresorhus/p-limit`, licence file read, MIT (named,
not installed).

| Point | Result |
|---|---|
| Node 15 default for unhandled rejections (2.4) | confirmed, wording sharpened |
| `using` by Node version (1.4) | confirmed for Node 24 (V8 13.6); statement kept version-gated |
| `signal` in `stream.pipeline`, `fs.promises`, `events.once` (1.2) | confirmed; fs corrected to best effort |
| Heap snapshot memory (3.3) | corrected: about twice the heap and blocking, not "roughly doubles" from experience |
| `--cpu-prof`, `--heap-prof` versions | confirmed |
| Added: silent signal listener leak, `addAbortListener` (1.4) | from the events page |

## Still unverified

- `signal` support in any named database driver (1.2): no driver documentation read; the block tells the reader
  to check the driver.
- `p-map` `concurrency` option (2.2): the `p-map` page was not read.
- A permissive prose source on the Node event loop beyond the official guide: none found (searched: the
  official guide and the repositories above).
