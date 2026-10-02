# § 2 — Expiry, eviction, memory limit, persistence

> Section 2 of `skills/redis-conventions`. Read it when a cache is introduced, a value is stored with no
> expiry, or a server configuration is written. Expiry is the application's decision; eviction is the
> server's emergency; persistence is the answer to a restart. Mixing them up is how a cache becomes a
> source of truth by accident.

1. **Every key that is a copy gets an expiry, set in the same command that creates it.** Use the write
   command's own expiry option rather than a second `EXPIRE` call: between the two calls a crash or an
   error leaves a key that never expires. A key without an expiry is a statement that it lives until someone
   deletes it, so it needs a named owner and a deletion path. Expiry has millisecond resolution, is
   replicated, and is persisted as an absolute date, so time passes for a key while the server is stopped.
2. **Pick the lifetime from the freshness the reader can tolerate, and add jitter when many keys are created
   together.** Keys filled by one batch with the same lifetime expire together and send the whole read load to
   the source at once. A random spread on the lifetime turns a cliff into a slope. For a hot key whose
   recomputation is expensive, let one caller rebuild while others serve the previous value or wait briefly;
   never let every caller rebuild.
3. **Set a memory limit on every instance that holds a cache, and choose the eviction policy on purpose.**
   With no limit the dataset grows until the operating system intervenes. Reaching the limit applies the
   configured policy. `noeviction` rejects commands that would add data and keeps what exists: right for an
   instance holding data you must not lose, wrong for a cache, which then fails on write instead of
   forgetting. The `allkeys-*` policies consider every key and need no expiry to work; the `volatile-*`
   policies consider only keys that carry an expiry and behave like `noeviction` when none do. A least
   recently used policy over all keys is the documented sensible default for a cache whose accesses are
   skewed towards a hot subset; the least-frequently-used and random variants fit other access patterns.
   Judge the choice with the hit ratio and the eviction counters, not by feel (§7).
4. **Do not mix cache keys and must-keep keys in one instance.** Policies that evict only keys with an expiry
   exist for that mixed case, and the vendor's own guidance is to run two instances instead where possible.
   Separate instances also let a cache be flushed, resized and evicted without touching the durable data.
5. **Leave room for the buffers when you set the limit on a replicated or persisted instance.** The memory used
   by the replication and append-log buffers is not counted against the limit, so a limit set equal to the
   machine's free memory is exceeded in practice. Subtract an estimate of those buffers (the server reports the
   amount that is not counted) from the memory you can spend.
6. **Choose persistence from the loss you can accept, then test the restore.** Point-in-time snapshots are
   compact, good for backups and restart speed, and lose everything written since the last snapshot. The
   append log records every write and syncs on a policy (never, every second, every write), so a crash loses
   at most what the policy allows, at the cost of a larger file and, with the strictest policy, speed. They
   combine. A pure cache may turn persistence off, accepting a cold start, which is then a load event on the
   source (§2.2). A backup that has never been restored is not a backup.
7. **Never read the existence of a key as the truth of a business fact.** A key can be absent because it
   expired, was evicted, was never set or the instance restarted; the code path for "absent" is the path to
   the source of truth, not a conclusion. An idempotency record, a lock or a deduplication marker kept only in
   a store that evicts will be forgotten at the worst moment, so those need either an instance with no
   eviction and persistence on, or the database.
8. **Hot keys and big-bang invalidation are designed, not discovered.** Prefer invalidating one key to
   deleting by pattern; a pattern delete needs a keyspace walk (§4.3). When many keys depend on one change,
   put a version segment in the key (`catalogue:v7:item:12`) and bump the version rather than hunting the
   keys, and let the old ones expire.

**Sources:** the vendor's documentation on key eviction, keys and expiration, and persistence (read
2026-10-02, version latest at that date; the compare-and-set commands cited in §3 appear from 8.4).
Points 2, 7 and 8 are reasoning of ours (jitter, absence is not truth, versioned keys), not statements of a page.
