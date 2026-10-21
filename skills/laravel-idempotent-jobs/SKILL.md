---
name: laravel-idempotent-jobs
description: "Use when writing or reviewing a queued job: assume it may run twice (timeout, redeploy, manual retry) — assert the end state rather than applying a delta, upsert don't insert, set the flag don't increment."
---

# laravel-idempotent-jobs

Narrow trigger extracted from `skills/laravel-conventions` §8.2, so a queued job's `handle()` routes
here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a queued job — its `handle()` method, specifically the part that mutates state.

## Steps
1. **A job is idempotent where it can be, because a queue retries.** Assume every job may run twice:
   on a timeout that already succeeded, on a redeploy mid-run, on a manual retry after a fixed bug.
2. **Assert the end state rather than applying a delta.** Set the flag, don't increment the counter;
   upsert, don't insert.
3. **Where a side effect genuinely cannot be repeated** (a payment, an email), the guard is explicit
   — a dedupe key, a status check before the side effect fires — rather than hoping the job never
   retries.

4. **Know the framework's own duplicate sources.** A worker timeout equal to or above the connection's
   retry-after window lets the job be picked up again while the first run is still going; keep the timeout
   several seconds below it. Blocking I/O may ignore the worker timeout, so set client timeouts too. Every
   release, timeout and even a clean finish consumes an attempt.
5. **Choose the right guard.** Making a job unique stops a second dispatch while one is queued or running; it
   is not a correctness guarantee, because its lock expires and needs a store with atomic locks. To stop two
   runs of the same key overlapping, use the overlap middleware with an expiry, and raise the attempts: each
   release spends one, and with one attempt the overlapped job is not retried. The overlap middleware's defaults (framework source, 2026-10-20): a job that cannot get the lock goes back to the queue at once, so set a release delay; the "do not release" option skips the job without re-queueing and without recording a failure, which silently drops work; and the lock is freed in a finally block when the job throws. Neither replaces the
   end-state rule of step 2.
6. **Fail a non-repeatable job on timeout** (the fail-on-timeout flag) so that a hung payment call is not
   retried blindly.

## Output / checkpoint
Running the job's `handle()` twice with the same payload leaves the same end state as running it
once — no doubled counter, no duplicate row, no second email sent for an already-processed record.

## Guardrails
- A job that fails silently and leaves a row half-updated is worse than one that never ran — nothing
  distinguishes it from success. Combine this with `laravel-throw-dont-return-errors`'s rule: swallow
  the exception to keep the queue green and the only signal anyone had is gone.
- The queue-what-is-slow-or-fragile question and realtime broadcasting authorisation live in
  `skills/laravel-conventions` §8 — read it for the neighbouring rules this one sits beside.

## Origin
Steps 1 to 3 are `skills/laravel-conventions` §8.2 extracted to its own trigger (written 2026-09-09), our own
guidance: the manual never states that a job should be idempotent, and the "redeploy mid-run" case was not found
in it. Steps 4 to 6 added 2026-10-20 from the queues page (12.x) of the Laravel documentation repository (MIT,
`license.md` read), facts only, rewritten: timeout against retry-after, unique jobs, overlap middleware,
attempts, fail-on-timeout; and from the overlap middleware's source in `laravel/framework` (MIT, LICENSE read). 🟡: nothing was run, 13.x not read.
