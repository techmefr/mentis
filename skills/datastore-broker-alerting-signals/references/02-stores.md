# datastore-broker-alerting-signals §2 — Redis and Elasticsearch

Sources: the Redis group (exporter oliver006/redis_exporter) and the Elasticsearch group (exporter prometheus-community/elasticsearch_exporter) of `_data/rules.yml` in samber/awesome-prometheus-alerts by Samuel Berthe at 822af1e, licensed CC BY 4.0 (credit and changes in `references/origin.md`), read 2026-10-16. Rewritten as tables of what fires; metric names are the exporters' as the source writes them.

## 2.1 Redis
1. **Availability and replication.** Hold and severity are the source's.

| Signal | Fires when | Hold, severity |
|---|---|---|
| instance down | `redis_up` is 0 | 1 minute, critical |
| missing master | no instance reports the role master (`redis_instance_info`) | none, critical |
| too many masters | more than one instance reports the role master | 1 minute, critical |
| replicas not all connected | the connected-replica total is lower than the replicas scraped | none, critical |
| replication broken | the connected-replica count fell over one minute | none, critical |
| replica link down | `redis_master_link_up` is 0 on a replica | 2 minutes, critical |
| cluster flapping | the connected-replica count changed more than once in a minute | 2 minutes, critical |
| cluster state not ok | `redis_cluster_state` is 0 (unable to serve queries, typically unassigned hash slots or too many nodes down) | 5 minutes, critical |
| cluster slots failed | `redis_cluster_slots_fail` above 0 (part of the keyspace unreachable, needs a failover or manual intervention) | 5 minutes, warning |
| cluster slots possibly failing | `redis_cluster_slots_pfail` above 0 (an early warning before FAIL) | 5 minutes, warning |

2. **The "too many masters" query counts every master the exporter scrapes.** Own guidance: scope the selector to one replication group, because a Redis Cluster has one master per shard and several masters there are normal.
3. **Saturation.**

| Signal | Fires when | Hold, severity |
|---|---|---|
| out of system memory | used memory above 90 percent of system memory (the exporter must run with its include-system-metrics option) | 2 minutes, warning |
| out of configured maxmemory | used memory above 90 percent of `maxmemory` | 2 minutes, warning |
| too many connections | connected clients above 90 percent of `maxclients` | 2 minutes, warning |

4. **Errors and capacity.**

| Signal | Fires when | Hold, severity |
|---|---|---|
| rejected connections | an increase of more than 5 in one minute of the rejected-connection counter | none, warning |
| missing backup | more than 48 hours since the last RDB save | none, critical |

5. **Not carried:** the source's "not enough connections" rule (fewer than 5 connected clients), because its own comment says non-application connections (monitoring, admin sessions, replication) keep a baseline above zero, and the expected minimum depends on the application. The 5 rejected connections per minute and the 48 hours are the source's rough defaults (`datastore-broker-alerting-signals` §1.5).
6. **When one fires,** the commands to run are in `redis-security-and-observability-pitfalls` §2, and the client-side causes of a connection storm in `redis-client-and-cluster-pitfalls` §2.

## 2.2 Elasticsearch
1. **Availability.**

| Signal | Fires when | Hold, severity |
|---|---|---|
| cluster red | `elasticsearch_cluster_health_status` colour red is 1 | none, critical |
| missing node | fewer than 3 nodes in the cluster | 1 minute, critical |
| missing data node | fewer than 3 data nodes | 1 minute, critical |

2. **Saturation.**

| Signal | Fires when | Hold, severity |
|---|---|---|
| high CPU | OS or Elasticsearch process CPU above 90 percent on a node | 5 minutes, warning |
| heap high | JVM heap used above 80 percent of its maximum | 2 minutes, warning |
| heap very high | JVM heap used above 90 percent of its maximum | 2 minutes, critical |
| disk space low | less than 20 percent of the data filesystem available | 2 minutes, warning |
| disk out of space | less than 10 percent of the data filesystem available | none, critical |

3. **Performance and errors.**

| Signal | Fires when | Hold, severity |
|---|---|---|
| unassigned shards | `elasticsearch_cluster_health_unassigned_shards` above 0 | 2 minutes, critical |
| cluster yellow | colour yellow is 1 | none, warning |
| relocating shards too long | relocating shards above 0 | 15 minutes, warning |
| initializing shards too long | initializing shards above 0 | 15 minutes, warning |
| pending tasks | pending cluster tasks above 0 (the source says the cluster works slowly) | 15 minutes, warning |
| no new documents | no increase of the indexing counter on data nodes over 10 minutes | none, warning |
| high indexing latency | indexing time per operation above 10 ms, while indexing | 10 minutes, warning |
| high query latency | query time per query above 1 second, while querying | 5 minutes, warning |
| thread-pool rejections | rejections above 5 percent of rejections plus completions, per node and pool | 10 minutes, warning |
| circuit breaker tripped | an increase of the breaker-trip counter over 5 minutes (the node rejects operations to avoid an out-of-memory error) | none, warning |
| relocating or initializing shards | the same states, as awareness | none, info |

4. **The shard-state rules come in pairs:** a fifteen-minute `warning` for the state that lasts too long and an immediate `info` for the state itself (§1.1). The unassigned-shards alert itself is held two minutes and is `critical`; the source gives no reason for that hold.
5. **Not carried:** the source's indexing-rate rule (above 10000 operations per second) and query-rate rule (above 100 per second). They alert on traffic volume and not on a failure, and the source's own comment says 100 queries per second is very low for most production clusters.
6. **When red, yellow or unassigned shards fire,** the read-only procedure is `elasticsearch-query-and-triage-pitfalls` §3, and slow queries are §1 of the same block.
7. **Own guidance:** the "fewer than 3 nodes" and "fewer than 3 data nodes" numbers describe a three-node cluster; replace them with your own node counts (§1.5).
