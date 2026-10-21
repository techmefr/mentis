# python-async-no-blocking-calls: origin and source stamps

> Provenance of `skills/python-async-no-blocking-calls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us: no event loop was started and no
debug-mode run was made. The block was first extracted from `skills/python-conventions` §4.4–§4.5 with no
external source; it was sourced on 2026-10-20. Overlaps with `skills/python-conventions`, cross-referenced, not merged.

## Sources (all read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Python documentation: `asyncio` development page, tasks (`to_thread`, `create_task`, `TaskGroup`), event loop (`run_in_executor`, default executor, `getaddrinfo`, debug mode, `slow_callback_duration`), subprocess page | Python documentation licence (PSF); official product documentation, read for facts only | One blocking call delays everything, `run_in_executor` and `to_thread`, process pool for CPU work and the main guard, GIL caveat, default executor shared with DNS, slow-callback threshold 100 ms, blocking log handlers, `communicate()` against `wait()` deadlock, weak task references |
| FastAPI documentation, "Concurrency and async / await" | MIT (repository LICENSE read: copyright Sebastián Ramírez) | `def` runs in a threadpool, blocking code inside `async def` runs on the loop |
| AnyIO documentation, working with threads | MIT (repository LICENSE read: copyright Alex Grönholm) | Worker-thread offload, an abandoned thread keeps running after cancel, 40-thread default limiter that does not govern asyncio's own executor |
| aiofiles README | Apache-2.0 (LICENSE read) | File methods are coroutines over a thread pool executor, default executor unless one is passed |
| HTTPX async page | BSD-3-Clause (LICENSE read) | Async client for async code, reuse one client; nothing on the blocking effect of the sync client |

## Verification pass 2026-10-20
- **Sourced (7 points):** the blocking effect (step 1), the executor choices and the process-pool conditions
  (step 4), the GIL caveat, the shared default executor and DNS queueing (step 5), debug mode and the 100 ms
  threshold (step 6), FastAPI `def` against `async def` (step 7), the subprocess `wait()` deadlock and weak task references.
- **Corrected (2):** the earlier text named "a thread/process pool" as equivalent isolation; the sources say
  a thread does not speed up pure-Python CPU work, so the block now separates I/O from CPU work. The "DNS
  lookup" item now means a direct blocking socket call, since the loop's own `getaddrinfo` already runs on a thread pool.
- **Added:** subprocess, logging handler, executor saturation, debug mode, FastAPI rule, task references.
- **Deleted:** nothing.
- **Still unsourced (3):** the story sentence in step 2 (our wording of an observed failure); that a
  synchronous HTTP client blocks the loop (follows from the sources, no page states it for a named client);
  the "async-compatible label is not proof" guardrail (supported only in part, by the aiofiles design).
  Not read: Starlette, uvloop and Trio documentation.

## Not verified
1. Nothing was run; every statement of behaviour is the documentation's.
2. Version gates (`to_thread` 3.9, `TaskGroup` 3.11) are the pages' statements; free-threaded builds were not read.
3. The AnyIO limiter figure concerns AnyIO's own pool only.

## Related blocks
`skills/python-conventions`, `skills/python-sqlalchemy-fastapi-pitfalls`, `skills/python-hygiene-pitfalls`.
