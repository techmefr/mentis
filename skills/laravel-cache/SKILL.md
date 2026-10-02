---
name: laravel-cache
description: "Use when writing or reviewing Laravel code that reads, writes, invalidates or locks through the cache: cache-aside reads, falsy values, stale-while-revalidate, atomic writes and locks, tags, flushing, failover. Version-sensitive APIs are marked and re-read against the installed framework."
---

# laravel-cache

Step 6 of the pipeline (`WORKFLOW.md`). The cache decisions that look harmless and fail under load or in
production: a falsy value read as a miss, two requests computing the same expensive value, a tag on a store
that ignores it, a flush that empties someone else's keys. Sits next to `skills/laravel-conventions` §12
(which only picks the store) and §4 (queries).

**Special status.** New block, 🟡: written from the framework's own documentation and the rule files the
Laravel team ships for its tooling, never run on real work in house. A base to confront with the first
real caching change, not settled doctrine. Several APIs here are recent (`flexible`, `memo`, `funnel`,
`failover`): re-read the page of the installed version before relying on one (`skills/source-freshness`).

## When
A `Cache::` call, the `cache()` helper, `once()`, a lock, a tag, a cache-store setting, or a "slow, let's
cache it" change.

## Steps
1. **Read through the store's own primitive, not a hand-written truthiness test.** `Cache::remember($key,
   $ttl, fn () => ...)` is the cache-aside read. The manual `get`, `if (! $value)`, `put` shape treats a
   legitimately cached `0`, `false` or empty array as a miss and recomputes it on every call.
   `rememberForever` is for values with an explicit invalidation path, never a default: without one it is a
   permanent stale answer.
2. **`remember` does not stop two requests computing the same missing value.** When duplicate computation
   is expensive or unsafe, wrap the computation in a lock (step 5) or use stale-while-revalidate (step 3).
3. **Stale-while-revalidate is `Cache::flexible($key, [$fresh, $stale], fn () => ...)`.** Fresh window:
   served as is. Stale window: served stale and refreshed after the response by a deferred function that
   lives in the same process, not in a durable job. Past the stale window: recomputed synchronously for
   that caller. Use it for hot keys where a slow recompute hurts; do not use it where serving a stale value
   is wrong (balances, permissions).
4. **Atomic conditional write is `Cache::add`**, which returns whether it wrote. A `has` followed by a `put`
   is a race. The documentation initialises a counter with `add` before calling `increment`.
5. **A lock when ownership matters**: `Cache::lock($name, $seconds)` with `get`, `block($wait)` (throws
   `LockTimeoutException` when it cannot acquire) or the closure forms that release for you. To release in
   another process, pass `$lock->owner()` to it and use `Cache::restoreLock($name, $owner)->release()`;
   `forceRelease()` ignores ownership and is an operator tool, not a code path. Locks need a store that
   supports them and every server must reach the same one. `Cache::funnel` caps concurrency (a limit, a
   release-after safety timeout, a block wait) and needs a lock-capable store.
6. **Repeated reads of one key in a single request or job** go through `Cache::memo()->get(...)`, which holds
   resolved values in memory for that execution and forgets one on any write through it. `once()` memoizes a
   callback in process and never touches a store; use it for repeated computation, `memo()` for repeated reads.
7. **Tags only on a store that supports them.** The file, database, storage and DynamoDB drivers do not.
   A tagged item is readable only with the same ordered tags it was stored with. Flushing a tag removes every
   item carrying it. Confirm the store before designing invalidation around tags; on a store without tags,
   name the keys and `forget` them.
8. **Never `Cache::flush()` for an application-level reason.** It ignores the configured prefix and empties
   every key in a shared store, other applications' included. Invalidate by key or by tag.
9. **Invalidation is part of the change.** A new cached value names what makes it wrong (which write, which
   event) and where that is cleared. A cache with a TTL and no invalidation path is a stale-data bug with a
   delay. Key names are built in one place from the inputs that change the value, tenant and locale included,
   or two tenants share a key.
10. **Production uses a failover store deliberately.** The `failover` driver tries the next store when an
    operation on the current one throws; it does not consult a later store on an ordinary miss and does not
    replicate data. It dispatches an event when it fails over: report it.
11. **A cache is not storage.** Anything that must survive eviction, restart or a store swap (a counter that
    bills, a one-time token with legal meaning) lives in the database. Test code uses the array store or a
    fake, never the production store.

## Output / checkpoint
Every cached read uses a primitive from steps 1 to 6, every tag sits on a store that supports it, every cached
value has a named invalidation, and no code calls `flush()`. Checked at `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Apply to new and changed code only (`skills/code-baseline` §0). Do not add
a cache to fix a slow query before measuring it (`skills/laravel-conventions` §4). A project that already
standardises on one pattern keeps it.

## Origin
Rewritten from the Laravel 13 cache documentation (laravel.com/docs/13.x/cache, MIT-licensed framework docs,
read 2026-10-02: remember, flexible, memo, add, touch, locks and owner tokens, funnel, tags support list,
flush and prefix, failover) and the `caching` rule file of Laravel Boost (`laravel/boost`, MIT, cloned
2026-10-02: falsy values, the lock caveat on `remember`, `once` against `memo`). Mechanisms only, rewritten in
our words. Version-sensitive: `flexible`, `memo`, `funnel`, `failover` and the `storage` driver depend on the
installed framework version.
