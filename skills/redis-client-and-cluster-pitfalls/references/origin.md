# redis-client-and-cluster-pitfalls: origin and source stamps

> Provenance of `skills/redis-client-and-cluster-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 24 checked, 24 matched, 0 corrected, 0 unverified

**Status: 🟡.** Written from documentation-style skill files, never run by us against a Redis server. No Redis
instance, cluster or client library was started while writing it.

## Sources (all read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| redis/agent-skills at commit a84871d (2026-09-08): `skills/redis-core/SKILL.md`, `references/choose-data-structure.md`, `references/key-naming.md` | MIT, Copyright (c) 2026 Redis, Inc. (`LICENSE` re-read 2026-10-15; frontmatter `license: MIT`) | Type by access pattern, Hash against serialised String, key naming, tenant prefix, no URL as key |
| redis/agent-skills at a84871d: `skills/redis-connections/SKILL.md`, `references/pooling.md`, `blocking.md`, `pipelining.md`, `client-cache.md`, `timeouts.md` | MIT (same file) | Pool or multiplex, no connection per request, multiplexed connections and blocking commands, pipelining, SCAN family, client-side cache with RESP3, timeouts |
| redis/agent-skills at a84871d: `skills/redis-clustering/SKILL.md`, `references/hash-tags.md`, `references/read-replicas.md` | MIT (same file) | CROSSSLOT, 16,384 slots, hash tags, replica reads |

| redis-py `docs/clustering.rst` and `docs/advanced_features.rst` (repository LICENSE read: MIT, Redis, Inc.), read 2026-10-20 | MIT | Cluster multi-key and non-atomic variants, cluster pipeline grouping, replica reads and retries, pipeline transaction default, thread rules |
| go-redis `README.md` (LICENSE read: BSD 2-Clause), read 2026-10-20 | BSD-2-Clause | Protocol option, experimental client-side caching constraints, autopipelining in the cluster client |

Not read: Jedis, Lettuce (the one documentation path tried returned not found; its LICENSE file was read and reported as MIT, but no Lettuce page was read, so nothing is credited to it), node-redis, StackExchange.Redis. No other permissive documentation was found for those clients in this pass, searched: the clients' repositories.

The redis/docs repository (CC BY-NC-SA 4.0) and valkey-io/valkey-doc (CC BY-SA 4.0) are idea-only for this
programme and were not read for this block. The `redis.io` links that appear in the source files were not
followed.

## Removed (stated in the sources, not carried)
- Field-level expiration for Hashes (`choose-data-structure.md` mentions it in one table cell): no Redis
  version is given in the file, so it is dropped.
- Everything about JSON, Streams, Vector Sets and RQE indexing beyond naming the type in the mapping: the
  files only name them.
- Java, Python and Lettuce code samples: replaced by prose; the one kept code sample (hash tags) is rewritten
  without comments.
- The source's pointer to "redis-core's transactions guidance": that page does not exist in the files read.

## Not verified
1. **Client versions.** The pool, multiplexing, pipeline and `CacheConfig` behaviours are stated for redis-py,
   Jedis, Lettuce, NRedisStack and go-redis as the files name them; the files give no client version, and none
   was checked against a client's own documentation.
2. **RESP3 and client-side caching.** The files state that RESP3 is required and show `protocol=3` with a cache
   configuration; the minimum server version and which clients support it were not given and are not claimed.
3. **Cluster behaviour of pipelines.** The files state that a pipeline over keys in different slots raises `CROSSSLOT`. Checked 2026-10-20: redis-py's cluster pipeline groups commands per node (so the statement is about a plain client, not redis-py); other clients not read.
4. **Own guidance, labelled in the text:** the retry-after-timeout caution on writes (§2, Checks), exercising
   multi-key operations on a cluster before release (§3.1.2), giving idempotency checks the primary client
   (§3.3.3), the pipeline ordering remark (§2.2.3), and every "Checks" section.
5. **Thresholds** in the examples (pool of 50 connections, cache of 1000 entries, 2 and 5 second timeouts,
   `count=100`) are sample values in the files and are not recommendations.

## Related blocks
`nestjs-reliability` (locks, idempotency keys and unknown-outcome rule that sit on top of Redis),
`observability-instrumentation` (what to watch), `source-freshness`. Redis security, observability and
search are not covered here.
