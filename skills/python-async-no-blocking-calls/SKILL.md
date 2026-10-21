---
name: python-async-no-blocking-calls
description: "Use when writing or reviewing an async function: never mix synchronous I/O or heavy CPU work in without isolating it (run_in_executor, to_thread, a process pool) — it blocks the whole event loop."
---

# python-async-no-blocking-calls

Narrow trigger extracted from `skills/python-conventions` §4.4–§4.5, so a blocking call inside async
code routes here directly instead of only through the whole Python block.

## When
Writing or reviewing an `async def` that calls a synchronous HTTP client, reads a file, sleeps, does
a DNS lookup, runs a subprocess, logs through a network handler, or runs any CPU-heavy work — anything not
itself `await`-able.

## Steps
1. **Never mix blocking code into an `async` function without isolating it.** A blocking call delays every
   other task and I/O operation on the loop by its whole duration, not just its caller.
2. **This is the failure mode described as "the whole service got slow while one report was
   generating."** One coroutine stalls every other request in the process, not only its own caller.
3. **The blocking call is usually not obvious.** A synchronous HTTP client, a plain file read, `time.sleep`,
   `subprocess.run`, a direct `socket.getaddrinfo`, a log handler that writes to the network — none of these
   look like I/O at the call site, but none of them yield to the event loop either.
4. **Pick the isolation by the kind of work.**
   - Blocking I/O: `asyncio.to_thread(func, ...)` (Python 3.9+, copies the context variables) or
     `loop.run_in_executor(None, func, ...)`, which uses the loop's default thread pool.
   - CPU-bound pure Python: a `ProcessPoolExecutor` through `run_in_executor`. The function and its arguments
     must be picklable and the entry point needs the `if __name__ == "__main__":` guard. A thread does not
     give pure-Python code a real speedup because of the GIL; it helps mainly with I/O, or with extensions
     that release the GIL.
   - Subprocesses: `asyncio.create_subprocess_exec`, and `communicate()` rather than `wait()` when output is
     piped (`wait()` can deadlock once the pipe buffer fills).
   - Files: `aiofiles` or `to_thread`; the loop has no native file API, so both end up on a thread pool.
5. **A thread pool is a shared, finite resource.** The default executor also runs the loop's own `getaddrinfo`
   and `getnameinfo`; when it is saturated, DNS lookups queue and higher layers report timeouts. Give heavy
   blocking work its own executor, or size the default one on purpose.
6. **Find the culprits at run time.** Debug mode (`PYTHONASYNCIODEBUG=1`, `asyncio.run(..., debug=True)` or
   Development Mode) logs any callback slower than `loop.slow_callback_duration`, 100 ms by default. Run it
   in tests or staging, not as a production default.
7. **In a web framework, check what the framework already does.** FastAPI runs a plain `def` path operation
   or dependency in a threadpool and does not do so for an `async def` one; a handler that must call a
   blocking library and has no `await` should be `def`, not `async def`.

## Output / checkpoint
Every synchronous or CPU-heavy operation reached from an `async def` is either replaced by its async
equivalent or explicitly isolated (`to_thread`, `run_in_executor`, a process pool) — nothing blocking runs
directly on the event loop's thread. A test or staging run in debug mode shows no slow-callback warning on the
changed path.

## Guardrails
- A library labelled "async-compatible" is not proof — check whether its actual I/O call is
  non-blocking, not just whether it exposes an `async def` wrapper. Some async file libraries only run the
  blocking call in a thread pool for you: fine, but then the pool size is your concern.
- Do not "fix" CPU-bound code by moving it to a thread and calling it done; see step 4.
- Hold a strong reference to a task you start with `create_task` (a set with a done callback, or a
  `TaskGroup`); the loop keeps only weak ones, and a dropped task can vanish before it finishes.
- The full `gather`/concurrency-bound argument this section opens with lives in
  `skills/python-conventions` §4 — read it before assuming `asyncio.gather` alone fixes a blocking
  call.

## Origin
Extracted from `skills/python-conventions` §4.4–§4.5 (2026-09-09), then checked on 2026-10-20 against the
Python asyncio documentation (facts only) and the FastAPI (MIT), AnyIO (MIT) and aiofiles (Apache-2.0)
documentation. Sources, licences and what stays unsourced are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
