# redis-security-and-observability-pitfalls §2 — What to watch and what to run

Sources: the `redis-observability` skill of redis/agent-skills at a84871d (`SKILL.md`, `references/metrics.md`, `references/commands.md`), read 2026-10-16. The files give no Redis version. Their thresholds are examples.

## 2.1 Metrics to export
1. **The metrics come from `INFO` and belong in the monitoring system,** not in a one-off print. The source lists seven, each with the condition it alerts on:

| Metric | What it tells you | The source alerts when |
|---|---|---|
| `used_memory` | current memory use | above 80 percent of `maxmemory` |
| `connected_clients` | open connections | sudden spikes or drops |
| `blocked_clients` | clients waiting on blocking commands | above zero, sustained |
| `instantaneous_ops_per_sec` | current throughput | significant drops |
| `keyspace_hits` and `keyspace_misses` | cache hit ratio | the ratio is below 80 percent |
| `rejected_connections` | the `maxclients` cap was reached | above zero |
| `rdb_last_save_time` | the last persistence snapshot | too old against the recovery point objective |

2. **The ratio is hits divided by hits plus misses,** and the source's code guards the denominator against zero so an instance with no lookups yet does not divide by zero.
3. **Cross-check with a managed service's own definitions** (AWS ElastiCache metrics page, read 2026-10-20): its memory percentage is `used_memory` over `maxmemory`; its hit rate is hits over hits plus misses, and the page itself says a value below about 0.8 means many keys are evicted, expired or absent, so the 80 percent figure is a rule of thumb; rejected and blocked connection counts come from the same `INFO` fields as the source's. It adds signals the source lacks: evicted keys (memory pressure shows here before the clients fail), engine-thread CPU (the engine is single-threaded, so host CPU can look idle while the engine is saturated; on hosts of two vCPUs or fewer watch the host figure too, since management processes share it), a memory fragmentation ratio, which the page says should stay above 1.0, and failed-authentication counters (see §1.5).
4. **The 80 percent figures are examples, not limits.** Own guidance: a hit ratio only describes a cache, so an instance used as a queue or a primary store is not judged by it, and a threshold is set from the instance's own history (`observability-instrumentation` §4).
5. **The alert rules for these signals, written against an exporter, are in `datastore-broker-alerting-signals`.**

## 2.2 Commands for an incident
1. **Reach for the built-ins when something looks off:**

| Topic | Command |
|---|---|
| slow commands | `SLOWLOG GET 10`, `SLOWLOG LEN`, `SLOWLOG RESET` |
| server snapshot | `INFO all`, or `INFO memory`, `INFO stats`, `INFO clients`, `INFO replication` |
| memory | `MEMORY DOCTOR`, `MEMORY STATS`, `MEMORY USAGE <key>` |
| connections | `CLIENT LIST`, `CLIENT INFO` |
| Redis Query Engine | `FT.INFO <index>`, `FT.PROFILE <index> SEARCH QUERY "..."` |

2. **The two the source ranks first for triage:** `SLOWLOG GET`, which lists the commands that took longer than the `slowlog-log-slower-than` threshold (10 ms by default in the source) with the exact command and its duration in microseconds; and `MEMORY DOCTOR`, which returns a one-paragraph summary of what is unusual about memory use right now.
3. **`FT.PROFILE` is how the source profiles a slow `FT.SEARCH`.**
4. **Own guidance:** `SLOWLOG RESET` clears the log, so record the entries before resetting it, and read `CLIENT LIST` when the connection count or the blocked clients number is the symptom.

## 2.3 A GUI is not monitoring
1. **Redis Insight is the official GUI for interactive work** (running queries, browsing keys, profiling indexes), and shows the same `SLOWLOG`, `INFO` and `FT.PROFILE` data visually. The source says it is useful in development and during an incident, and not a replacement for exporting metrics to the monitoring system.

## 2.4 Checks (own guidance)
1. Every metric of §2.1 reaches the monitoring system, and the threshold next to each was chosen from the instance's own data.
2. The on-call can run the commands of §2.2 against the instance, with the right user (a user that cannot run them is a result of §1.2, and is decided on purpose).
3. A cache and a non-cache instance are not given the same hit-ratio alert.
