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
No external source: this is `skills/laravel-conventions` §8.2 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
