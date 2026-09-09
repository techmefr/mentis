---
name: laravel-post-may-run-twice
description: "Use when writing or reviewing an endpoint that creates a row on POST: assume it runs twice — a natural uniqueness constraint in the database or a caller-supplied idempotency key, never a check-then-insert in PHP."
---

# laravel-post-may-run-twice

Narrow trigger extracted from `skills/laravel-conventions` §6.15, so a row-creating `POST` endpoint
routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing an endpoint whose second execution would create a second row — clients retry,
users double-click, proxies replay.

## Steps
1. **A `POST` may run twice.** Assume it will, not that it might.
2. **The fix is a natural uniqueness constraint in the database**, or an idempotency key the caller
   supplies and the server checks before creating the row.
3. **A check-then-insert in PHP loses the race it was written for.** The window between the check and
   the insert is exactly where the second concurrent request lands.

## Output / checkpoint
The endpoint's second execution with the same request either fails on a real database constraint or
returns the already-created result — never a second row created by a PHP-level check that ran before
the first insert committed.

## Guardrails
- This is a database-level guarantee, not an application-level one — a unique index or a stored
  idempotency-key record, not an `if` checking whether the row already exists.
- Content negotiation and the additive-then-remove API-contract rule sit right beside this one in
  `skills/laravel-conventions` §6 — read it for the neighbouring HTTP-surface rules.

## Origin
No external source: this is `skills/laravel-conventions` §6.15 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
