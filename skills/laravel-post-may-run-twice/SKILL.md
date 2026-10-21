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
1. **A `POST` may run twice.** Assume it will, not that it might. HTTP defines `PUT`, `DELETE` and the safe
   methods as idempotent and `POST` as not; a client may repeat an idempotent request after a lost connection,
   and the specification says a client should not retry a non-idempotent one automatically unless it can tell
   the request is effectively idempotent or was never applied (RFC 9110 section 9.2.2; the same section says a proxy
   must not). Real clients, users and scripts retry anyway.
2. **The fix is a natural uniqueness constraint in the database**, or an idempotency key the caller
   supplies and the server checks before creating the row.
3. **A check-then-insert in PHP loses the race it was written for.** The window between the check and
   the insert is exactly where the second concurrent request lands. The framework's `unique` validation rule
   and `firstOrCreate` are both a lookup followed by an insert (the Eloquent documentation describes `firstOrCreate`
   as locating the record and inserting if absent; the `unique` rule is a lookup by definition): they
   reduce duplicates, they do not rule them out without a unique index underneath (own reasoning, not a
   documented statement).
4. **If the caller supplies an idempotency key, the server decides what a repeat means.** Public API practice
   (Stripe's idempotent-requests page; the expired IETF draft `draft-ietf-httpapi-idempotency-key-header-07`,
   sections 2.2 to 2.7): the key is unique per operation and not reusable with a different payload (the draft says
   respond 422), a retry after completion returns the stored outcome, success or error, a repeat while the
   first call is still running gets a conflict (the draft says 409), keys expire after a stated period (Stripe
   prunes them after at least 24 hours), and a missing required key is a 400. The key and its stored result
   belong in the database next to the row, written in the same transaction.
5. **A cache lock narrows the window, it does not replace the constraint.** Atomic cache locks (framework
   documentation, Cache, Atomic Locks; they need a shared central store) can serialise concurrent identical
   requests, but a lock that expires or a store that is flushed lets the second request through: keep the
   database constraint as the last line (own reasoning).

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
Extracted from `skills/laravel-conventions` §6.15 (2026-09-09). Sourced on 2026-10-20: RFC 9110 section 9.2.2 (idempotent
methods and automatic retry; IETF text, facts only); the expired Internet-Draft
`draft-ietf-httpapi-idempotency-key-header-07` sections 2.2 to 2.7 (a draft, not a standard: its status codes are
SHOULD-level and may change); Stripe's "Idempotent requests" API page (facts about keys, storage and expiry;
vendor documentation, facts only); the framework's documentation for the `unique` rule, `firstOrCreate` and
atomic locks (12.x). Independent verification 2026-10-21: 12 checked, 11 matched, 1 corrected (step 3 credited the documentation for the race statement, which is our reasoning), 0 unverified.
Not found in a source, so our policy: that the guarantee must be a database constraint and
never application logic (the documentation neither says the unique rule alone is racy nor recommends a
constraint), and step 5's reasoning. Mechanisms only, rewritten in our words.
