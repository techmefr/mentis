# Origin: node-async-performance

🟡 written 2026-10-08, never run on real work. No dogfood, no incident behind any rule: the sections are a
synthesis of sources, and a rule earns more than 🟡 only by catching a real defect in a real review or run.

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

## Not verified in this pass

See the hand-off list below; each item is stated in the text without a page-level check.

- Node 15 as the version where unhandled rejections began terminating the process (2.4).
- `using` / explicit resource management availability by Node version (1.4).
- `signal` support in `stream.pipeline`, `fs.promises`, `events.once`, and in any named database driver (1.2).
- The statement that a heap snapshot roughly doubles memory while written (3.3); stated from experience of
  the V8 snapshot writer, not from a documentation page.
- The stable-release versions given for `--cpu-prof` and `--heap-prof` come from the CLI page as fetched.
