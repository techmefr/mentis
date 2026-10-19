# § 7 — Operating it: what to watch, what to run

> Section 7 of `skills/redis-conventions`. Read it when a dashboard or an alert is written, or an incident
> is under way. The questions to ask first are in `skills/observability-instrumentation` §1; this is the
> server-specific half.

1. **Export these, because each one answers a question the on-call will ask.** Memory used against its limit
   (will it start evicting or refusing writes); connected and blocked clients and rejected connections (is
   the pool leaking, has the connection cap been hit); operations per second (did throughput drop); cache hits
   against misses (is the cache earning its place); evicted and expired key counters (are keys leaving for
   the right reason, §2); time since the last snapshot against the loss you accepted (§2.6). Alert on
   symptoms the application feels, a falling hit ratio or a rising rejected-connections count, rather than on
   every internal counter (`skills/observability-instrumentation` §4).
2. **Hit ratio is hits over hits plus misses,** and an existence check that finds nothing counts as a miss. A
   low ratio has two readings that need different fixes: many evictions means the memory limit or the policy
   is wrong; few evictions and many expirations means the lifetime is too short or the wrong keys expire.
   Check the eviction counter before changing anything.
3. **Reach for the built-in diagnostics before guessing.** The slow log lists commands that exceeded a
   threshold, with their duration, which finds the one big command behind a latency spike. The server
   information command, by section, gives memory, clients, stats and replication. The memory report and the
   per-key memory command explain pressure and find the heavy key. The client list shows who holds
   connections. A search module has its own info and profile commands for a slow query.
4. **A latency spike is usually one of three things:** a slow or large command blocking the single worker
   (§1.8, §4.3), persistence work such as forking for a snapshot on a large dataset (§2.6), or memory
   pressure forcing eviction or swapping. Look at the slow log, then at persistence and memory, in that order.
5. **Use a graphical client for looking, not for monitoring.** It surfaces the same data interactively, which
   suits development and an incident, and it is no replacement for exporting the counters of point 1 to the
   monitoring system.

**Sources:** the vendor's development skill on observability (MIT) and its documentation on key eviction
(hit-ratio calculation, eviction and expiry counters) and on latency (slow commands, the mostly
single-threaded design), read 2026-10-02. Point 4 is a synthesis of those pages, not a quotation.
