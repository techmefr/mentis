# § 6 — Cluster and replicas

> Section 6 of `skills/redis-conventions`. Read it when the deployment is sharded, or reads are sent to
> replicas. Both change what a single command is allowed to touch and how fresh a read is.

1. **In a sharded deployment the key name decides which node owns a key,** by hashing it into a fixed
   number of slots. Any command that touches several keys (multi-get, set algebra, a transaction, a script
   with several declared keys, a pipeline that reads several of them under one command) needs all those keys on
   the same slot, otherwise the server answers with a cross-slot error. That error appears only when the code
   moves from one node to a cluster, so a test against a single node proves nothing about it
   (`skills/testing-anti-patterns`: a test that cannot fail).
2. **Co-locate keys with a hash tag, scoped to the entity.** Only the text between the braces is hashed, so
   `{user:1001}:profile` and `{user:1001}:settings` share a slot. Tag with the meaningful entity, not a bare
   number: `{1001}` shared by unrelated namespaces puts them all on one slot. Tag only the keys that really
   take part in multi-key operations: tagging everything concentrates load on single nodes and removes what
   sharding was for. Plan tags before keys exist, since renaming keys in production is a migration (§1.6).
3. **No numbered logical databases in a cluster.** Only database 0 exists, and selecting another is refused.
   Code that separates data with database numbers must move to prefixes before it can be clustered (§1.7).
4. **A replica read can be stale.** Replication is asynchronous, so a client that writes and then reads from a
   replica may not see its own write. Use replica reads for caches, dashboards and feeds where staleness is
   tolerable; never for a balance, an idempotency record, a lock or a read-after-write on the same request.
   Enable replica reads per client or per call, not globally.
5. **A failover can lose acknowledged writes,** for the same reason: a write acknowledged by the primary but
   not yet replicated is lost if the primary dies. The data that cannot tolerate this belongs in a store whose
   durability model says otherwise (§1.1).

**Sources:** the vendor's development skill on clustering (hash tags, cross-slot errors, replica reads; MIT)
and its cluster specification (database 0 only), read 2026-10-02. Point 5 follows from asynchronous
replication as the replication documentation describes it and is stated here as a consequence, not quoted.
