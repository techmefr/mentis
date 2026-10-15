# elasticsearch-query-and-triage-pitfalls §3 — Reading a yellow or red cluster

Sources: the `elasticsearch-cluster-health` skill of elastic/agent-skills at baa5111 (`SKILL.md`), read 2026-10-16. The source states compatibility with Elasticsearch 8.x or 9.x, self-managed or Elastic Cloud Hosted, and says it does not apply to Elastic Cloud Serverless, where cluster, shard and allocation APIs are managed internally.

## 3.1 Status and where the problem is
1. **Read `GET /_cluster/health` first.** Green: every primary and replica is assigned. Yellow: every primary is assigned and at least one replica is not, so data stays readable and redundancy is degraded, which is not data loss. Red: at least one primary is unassigned, so the data of that shard is unavailable and the case is urgent.
2. **Read the shard counters too.** With `initializing_shards` above zero and `unassigned_shards` at zero the cluster is recovering by itself: confirm progress with `GET /_cat/recovery`, wait and re-check before escalating.
3. **Localise to one index with `GET /_cluster/health?level=indices`.** A red index outranks every yellow one; among equals take the index with the most unassigned shards; a red system index (`.security`, `.kibana*`, `.fleet-*`) outranks application indices because the rest of the stack depends on it. `GET /_cat/shards/{index}?h=index,shard,prirep,state,unassigned.reason` shows whether the failures are primaries (`p`) or replicas (`r`).

## 3.2 Trigger against cause
1. **Call `POST /_cluster/allocation/explain`, with no body or with `index`, `shard` and `primary`, and read the fields in this order:** `primary`, `can_allocate`, `unassigned_info.reason`, `allocate_explanation`, then `node_allocation_decisions[].deciders[]`. A `primary` of false is an unassigned replica (the usual yellow); true is an unassigned primary (the usual red).
2. **`unassigned_info.reason` (for example `NODE_LEFT` or `INDEX_CREATED`) is the trigger, not the root cause, when `can_allocate` is `no`.** The decider with `decision: "NO"` names the cause class (for example `disk_threshold`, `filter`, `awareness`). Prefer it over the trigger when reporting.
3. **Map the decider to a cause class:**

| Signal | Cause class | Remediation, applied by the operator |
|---|---|---|
| `disk_threshold`, `decision: NO` | a disk watermark is exceeded | free disk on the named node, add data-node capacity, or adjust `cluster.routing.allocation.disk.watermark.*` after checking `GET /_cat/allocation` |
| `filter` or `awareness`, `decision: NO` | allocation filtering or zone awareness | add a node that satisfies the `index.routing.allocation.*` or awareness attributes, or adjust those settings |
| `throttling`, or recovery in progress | transient recovery | wait, watch `GET /_cat/recovery`, re-check health |
| `can_allocate: no_valid_shard_copy` | no surviving shard copy | the data-loss case (§3.3) |
| `can_allocate: yes` but the shard is still unassigned | delayed allocation or cluster-state catch-up | check the delay in `unassigned_info.at`, wait, re-check |

4. **The common yellow after a node leaves is disk pressure on the survivor.** Replicas relocate to the remaining nodes; a survivor above the high watermark (`cluster.routing.allocation.disk.watermark.high`, 90 percent as the source's text states it for Elasticsearch 8.x or 9.x) has its replica allocation blocked while the primaries stay assigned. The fix is capacity or watermark relief, not deleting the index and not forcing an empty primary.

## 3.3 Remediation and the data-loss case
1. **Triage is read-only.** Use the explain and health reads, report the single most likely cause (decider class plus the `allocate_explanation` text) and one primary remediation. Reroutes, snapshot restores and settings changes are performed by the operator, not during triage.
2. **Yellow with an unassigned replica:** say that all primaries are assigned and nothing is lost, and name the real decider (a disk watermark on a named node), not only "a node left". Do not recommend deleting the index, `allocate_empty_primary`, force-allocating over a healthy primary, or restarting the whole cluster without evidence.
3. **Red with `no_valid_shard_copy`:** the only copy was on the departed node and no remaining node holds a valid one, so queries and routing for that shard fail. Recovery paths in order: bring the departed node back if its data directory is intact; restore from a snapshot into the index, or into a new index followed by a reindex; and only as a last resort `POST /_cluster/reroute` with `allocate_empty_primary`, which creates an empty primary and **permanently loses every document of that shard**. State the loss explicitly and never present it as the first or a casual fix. Do not recommend deleting the index without discussing the loss either.
4. **One index, one cause.** Pick the highest-impact index and the strongest `NO` decider instead of listing every shard.
5. **On Serverless this procedure does not apply**, because the cluster, shard and allocation APIs are managed internally.

## 3.4 Checks (own guidance)
1. The report separates the trigger (`unassigned_info.reason`) from the decider that blocks allocation.
2. The report says whether the unassigned shard is a primary or a replica, and whether data is lost.
3. No write call was made during triage; every remediation is addressed to the operator.
