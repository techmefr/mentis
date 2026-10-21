# serverless-edge-worker-pitfalls §2 — Request lifetime and state

Sources: `references/runtime-patterns.md` and the anti-pattern table of the `workers-best-practices` skill in cloudflare/skills at 86505e4, read 2026-10-20. The shared-process and floating-promise points are general to function platforms.

## 2.1 State shared between requests
1. **The platform reuses one process (an isolate, a container) for many requests, so module-level variables are shared by all of them.** A variable assigned inside the handler from request data leaks one user's value to the next request and can raise a "cannot perform I/O on behalf of a different request" error.
2. **Pass request state through function arguments.** Read-only module constants and caches keyed by an id are fine; a mutable "current user" is not.
3. **A cache in module memory is per process, not global:** it may be empty on any request, and two requests can see different copies. Use it as an optimisation, never as the source of truth.

## 2.2 Promises that outlive the response
1. **A promise that is not awaited, returned or handed to the platform's background hook is floating: its result is dropped, its error swallowed and the platform may stop the process before it finishes.** Await it when the response needs the result; hand it to the background hook when it does not.
2. **Call the background hook as a method of the context object; do not destructure it.** Detaching the method loses its receiver and throws an "illegal invocation" error at run time.
3. **Background work after the response has its own short time limit:** the platform's limits page (read 2026-10-20) gives up to 30 seconds after the response on both plans; re-read it, figures change. Anything longer goes to a queue or a workflow (§3.1).
4. **Use the floating-promise lint rule the project already has,** or inspect each async call on the changed path. Adding lint tooling is a separate change.
5. **On other function platforms: AWS Lambda freezes the execution environment once the handler and extensions finish, and unfinished background work resumes only if that environment is reused** (Lambda developer guide, execution environment lifecycle). So work started and not awaited may run late, in the middle of another request, or never; finish or enqueue it before returning.

## 2.3 Memory, CPU and streaming
1. **A function has a small fixed memory budget.** Reading an unbounded body into memory (`text()`, `json()` or an array buffer on a large payload) crashes it; stream the body through, or pass the upstream body straight into the response.
2. **Small, known-size payloads are fine to read whole.** The finding is a body whose size the caller controls.
3. **When streaming several parts into one response, keep the pipeline promise tracked** by the background hook so it does not float.
4. **CPU time is limited separately from wall-clock time,** and a plan can set a low figure (limits page, 2026-10-20: 10 ms per request on the free plan; on the paid plan 30 s by default, raisable to 5 minutes; memory 128 MB per isolate on both): large synchronous parsing, tight loops and heavy crypto hit it. Break the work up, queue it, or move it to compiled code; re-read the limits page for the plan in use.
5. **A validation library that holds a lot of heap per schema can cause out-of-memory errors in a small function:** the source names a minimum version of one such library for that reason; re-read before relying on it.

## 2.4 Errors that fail open
1. **Do not use the "pass through on exception" helper as general error handling.** It forwards the request to the origin when the function throws, so bugs vanish from view and the origin gets traffic it was meant to be shielded from.
2. **Catch at the handler, log a structured error, return a structured error response with the right status.** The response says what failed in generic terms; the log carries the detail.

## 2.5 Secrets and randomness
1. **Use the platform's cryptographic random source for tokens and ids,** not `Math.random()`, which is predictable.
2. **Compare secrets in constant time:** hash both values to a fixed size first, then use the constant-time compare. A plain equality check leaks timing, and a length check before the compare leaks the length.

## 2.6 Checks (own guidance)
1. Search the module scope for `let` and `var` assigned in a handler: none.
2. Search for async calls whose result is discarded, and for destructured context methods: none.
3. Send a response larger than the memory budget through the function in a test: it streams.
