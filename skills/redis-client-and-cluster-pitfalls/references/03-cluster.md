# redis-client-and-cluster-pitfalls §3 — Redis Cluster slots and replica reads

Sources: the `redis-clustering` skill of redis/agent-skills at a84871d (`SKILL.md`, `references/hash-tags.md`, `references/read-replicas.md`), read 2026-10-15.

## 3.1 CROSSSLOT
1. **Redis Cluster spreads keys over 16,384 slots by hashing the key name.** A command that touches several keys (`MGET`, `SDIFF`, `SUNIONSTORE`), a transaction, a pipeline or a Lua script with several `KEYS[]` needs all of them in the same slot. Otherwise the server answers `CROSSSLOT`.
2. **Own guidance:** the source's examples fail "in cluster mode", which implies the same code passes on a non-cluster instance, so exercise multi-key operations against a cluster before release.
3. **Two keys that share a prefix are not in the same slot:** `user:1001:profile` and `user:1001:settings` are hashed as whole names.

## 3.2 Hash tags
1. **Only the part between `{` and `}` is hashed.** Keys that share the tag always land in the same slot, so `{user:1001}:profile` and `{user:1001}:settings` can be read in one pipeline or moved with one `LMOVE`.
2. **Scope the tag to the entity:** `{user:1001}`, never a bare `{1001}`. Unrelated keys such as `purchase:{1001}` and `employee:{1001}` would all be hashed on `1001` and saturate one slot.
3. **Tag only the keys that need multi-key operations.** Tagging every key makes hotspots and removes the point of sharding.
4. **A single-key command on a tagged key works as before,** so adding tags is not a protocol change; but renaming keys on a production dataset is painful, so decide the tags up front for the entities that will be grouped.

```python
redis.set("{user:1001}:profile", "...")
redis.set("{user:1001}:settings", "...")
pipe = redis.pipeline()
pipe.get("{user:1001}:profile")
pipe.get("{user:1001}:settings")
pipe.execute()
```

## 3.3 Replica reads
1. **Replicas are eventually consistent.** Routing reads to them (redis-py `read_from_replicas=True` in cluster mode, or a second client pointed at a replica in a primary/replica setup) frees capacity on the primaries.
2. **Never read your own writes from a replica,** and never use replica reads for anything that needs strict freshness: balances and idempotency state are the source's examples. Good fits are cache layers, analytics, dashboards and recommendation feeds.
3. **Writes go to the primary.** Own guidance: since the choice is made per client, a code path that checks idempotency state is given the primary client.

## 3.4 Checks (own guidance)
1. List every multi-key command, transaction, pipeline and Lua script and name the hash tag that puts its keys in one slot.
2. No tag is a bare number or a short string shared by several entity types.
3. The idempotency and balance reads use the primary.
