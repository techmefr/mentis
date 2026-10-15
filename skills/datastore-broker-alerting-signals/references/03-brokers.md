# datastore-broker-alerting-signals §3 — RabbitMQ and Kafka

Sources: the RabbitMQ group (exporters rabbitmq/rabbitmq-prometheus and kbudde/rabbitmq-exporter) and the Kafka group (exporters danielqsj/kafka_exporter and linkedin/Burrow) of `_data/rules.yml` in samber/awesome-prometheus-alerts by Samuel Berthe at 822af1e, licensed CC BY 4.0 (credit and changes in `references/origin.md`), read 2026-10-16. Rewritten as tables of what fires; metric names are the exporters' as the source writes them.

## 3.1 RabbitMQ
1. **Rules for the rabbitmq-prometheus plugin.** Hold and severity are the source's.

| Signal | Fires when | Hold, severity |
|---|---|---|
| node down | fewer than 3 nodes running (`rabbitmq_build_info` summed) | 1 minute, critical |
| memory alarm active | `rabbitmq_alarms_memory_used_watermark` above 0: the memory watermark was reached and publishers are blocked cluster-wide until memory is freed | 1 minute, critical |
| disk space alarm active | `rabbitmq_alarms_free_disk_space_watermark` above 0: the disk free limit was reached and publishers are blocked cluster-wide | 1 minute, critical |
| predicted low disk watermark | a linear projection of the last 24 hours of available disk puts a node below its alarm threshold within 24 hours | 1 hour, warning |
| memory high | resident memory above 90 percent of its limit | 2 minutes, warning |
| file descriptors | open descriptors above 90 percent of the maximum | 2 minutes, warning |
| too many connections | more than 1000 connections on a node | 2 minutes, warning |
| high connection churn | connections opened plus closed per second above 10 percent of the connection count, with at least 100 connections: clients use short-lived connections, which wastes CPU and descriptors | 10 minutes, warning |
| node not distributed | `erlang_vm_dist_node_state` below 3: the distribution link to a peer is not up | 1 minute, critical |
| different versions | more than one RabbitMQ version in the same cluster | 1 hour, warning |
| too many ready messages | ready messages of a queue above 1000 | 1 minute, warning |
| too many unacknowledged messages | unacknowledged messages of a queue above 1000 | 1 minute, warning |
| no queue consumer | a queue with fewer than 1 consumer | 1 minute, warning |
| unroutable messages | more than 3 returned or dropped as unroutable over 5 minutes | 2 minutes, warning |

2. **Rules for the kbudde exporter use other metric names** (`rabbitmq_up`, `rabbitmq_running`, `rabbitmq_partitions`, `rabbitmq_node_mem_used`). Its `rabbitmq_up` liveness rule (one minute, `critical`) and its fewer-than-3-running rule (`rabbitmq_running` summed, one minute) are its equivalents of the plugin's node count. It adds one signal the plugin group lacks, a cluster partition (`rabbitmq_partitions` above 0, `critical`, no hold; the source says messages may be lost or duplicated), and a stricter no-consumer rule (`rabbitmq_queue_consumers` equal to 0, held five minutes, `critical`; the source's comment says the hold allows a short service restart).
3. **Own reading:** predicted disk is the early version of the disk alarm. The alarm is the state that blocks every publisher and the prediction gives up to a day's notice, so the two belong together, with the `warning` going to the people who can add disk.
4. **The kbudde group also holds rules that hard-code placeholder names, and they are templates, not rules:** a named queue that should have only one consumer, a named dead-letter queue above 10 messages held one minute, a named queue whose head message is more than 60 seconds old held two minutes, a named exchange publishing fewer than 5 messages per second. Copy the pattern with your own queue and exchange names only if the signal means something for them. Own guidance: the dead-letter depth and the head-message age are the two worth adapting. Why messages reach a dead-letter queue is in `rabbitmq-delivery-pitfalls`.
5. **Own guidance:** a queue with no consumer is a valid alert only for a queue that is meant to be consumed all the time; for a queue drained by a scheduled worker it fires on every quiet period.

## 3.2 Kafka
1. **Rules for danielqsj/kafka_exporter.**

| Signal | Fires when | Hold, severity |
|---|---|---|
| in-sync replicas below the replication factor | the minimum of `kafka_topic_partition_in_sync_replica` for a topic is below 3 (data durability is at risk) | none, critical |
| consumer group lag | the summed lag of a consumer group is above 10000 messages | 1 minute, warning |
| consumer group lag increasing | the lag of a group on a topic keeps rising over 15 minutes, although the absolute threshold has not been crossed | 15 minutes, warning |

2. **The in-sync number is the topic's replication factor, not 3.** The source's comment says 3 matches a common replication factor and tells you to adjust it to the topic's configured one. Own reading: a topic whose replication factor is below that number would alert permanently.
3. **The lag has two alerts on purpose.** The absolute one catches a backlog; the trend one catches a slow leak before any threshold is crossed. The trend rule sums the change of lag over 5 minutes per topic and group, excludes the internal offsets topic and empty group names, and holds 15 minutes, which is what makes it a trend and not a spike.
4. **The Burrow group has two more rules, not carried** (§3.3).
5. **Own guidance:** the in-sync alert tells you the set shrank, not what that did to writes. The producer and topic settings that decide that (acks, the minimum in-sync count, unclean leader election) are in `kafka-delivery-semantics-pitfalls`.

## 3.3 What the source does not give
1. **The Kafka group read has no rule for a broker being down** and none for a consumer group that stopped consuming; the Zookeeper group beside it was not read for this block. Own guidance: a lag alert that never fires because a consumer died and the producer stopped too is the absence case of `observability-instrumentation` §4.9, and has to be written for your topology.
2. **The two Burrow rules are not carried:** an offset that decreased in a minute (the source gives no more than that description, so its meaning is not asserted here) and a consumer lag that the source describes as 30 minutes and increasing, built on a comparison of each partition's lag now with 15 minutes earlier and a 15-minute hold. The `kafka_exporter` lag-trend rule above covers the second.
3. **Metric names are exporter-bound** (`kafka_consumergroup_lag`, `kafka_topic_partition_in_sync_replica`), and a Kafka deployment that exposes metrics another way needs the names of that exporter (§1.6).
