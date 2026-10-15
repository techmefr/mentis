---
name: redis-client-and-cluster-pitfalls
description: "Use when writing or reviewing code that talks to Redis: choosing a data type (Hash against a serialised String), naming keys, connection pooling or multiplexing, pipelines, SCAN against KEYS, blocking pops, client-side caching, timeouts, and Redis Cluster (CROSSSLOT, hash tags, replica reads)."
---

# redis-client-and-cluster-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the client-side and keyspace traps of Redis. The premise: **the
server accepts almost anything, and the cost arrives later**: as a connection storm, a stalled server, a
`CROSSSLOT` error that only a cluster raises, or a stale read used as truth. Locks, idempotency keys and
queue limits that sit on top of Redis are in `nestjs-reliability`; this block is about the client and the keys.

## When
- A value is stored in Redis, or a key name is chosen.
- A Redis client is created or configured (pool, timeouts, client-side cache).
- A command that touches many keys, or a whole container, is written.
- The deployment is, or will become, a Redis Cluster, or reads are sent to replicas.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Data type by access pattern, key naming | a value is modelled or a key is named | [`01-keys-and-types.md`](./references/01-keys-and-types.md) |
| 2 | Pools and multiplexing, pipelines, SCAN, blocking pops, client-side cache, timeouts | a client is created, a loop of commands or a scan is written | [`02-client-connections.md`](./references/02-client-connections.md) |
| 3 | CROSSSLOT, hash tags, replica reads | the target is a cluster, or reads go to replicas | [`03-cluster.md`](./references/03-cluster.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: the client is built once, the
timeouts are set, no unbounded container is read whole, every multi-key operation names the hash tag that
puts its keys in one slot, and no read that needs freshness goes to a replica.

## Guardrails
- Never create a client or connection inside a request handler (§2.1).
- Never call `KEYS`, or read a large container whole, on a production instance (§2.3).
- Never tag every key with the same hash tag, or tag with a bare number (§3.2).
- Never read idempotency state or a balance from a replica (§3.3).
- Client behaviour is given for the clients named in the source (redis-py, Jedis, Lettuce, NRedisStack,
  go-redis) at the stamped commit; nothing here was run against a Redis server (🟡).

## Origin
Rewritten from the Redis, Inc. `redis-core`, `redis-connections` and `redis-clustering` agent skills
(MIT, commit a84871d), read 2026-10-15. Version-bound facts and own guidance are listed in
[`references/origin.md`](./references/origin.md).
