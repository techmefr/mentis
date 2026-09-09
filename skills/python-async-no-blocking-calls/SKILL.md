---
name: python-async-no-blocking-calls
description: "Use when writing or reviewing an async function: never mix synchronous I/O or heavy CPU work in without isolating it (run_in_executor) — it blocks the whole event loop."
---

# python-async-no-blocking-calls

Narrow trigger extracted from `skills/python-conventions` §4.4–§4.5, so a blocking call inside async
code routes here directly instead of only through the whole Python block.

## When
Writing or reviewing an `async def` that calls a synchronous HTTP client, reads a file, sleeps, does
a DNS lookup, or runs any CPU-heavy work — anything not itself `await`-able.

## Steps
1. **Never mix blocking code into an `async` function without isolating it** (`run_in_executor` or
   the equivalent). It blocks the whole event loop, not just the caller.
2. **This is the failure mode described as "the whole service got slow while one report was
   generating."** One coroutine stalls every other request in the process, not only its own caller.
3. **The blocking call is usually not obvious.** A synchronous HTTP client, a plain file read,
   `time.sleep`, a DNS lookup — none of these look like I/O at the call site, but none of them yield
   to the event loop either.

## Output / checkpoint
Every synchronous or CPU-heavy operation reached from an `async def` is either replaced by its async
equivalent or explicitly isolated (`run_in_executor`, a thread/process pool) — nothing blocking runs
directly on the event loop's thread.

## Guardrails
- A library labelled "async-compatible" is not proof — check whether its actual I/O call is
  non-blocking, not just whether it exposes an `async def` wrapper.
- The full `gather`/concurrency-bound argument this section opens with lives in
  `skills/python-conventions` §4 — read it before assuming `asyncio.gather` alone fixes a blocking
  call.

## Origin
No external source: this is `skills/python-conventions` §4.4–§4.5 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
