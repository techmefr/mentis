# datastore-broker-alerting-signals §1 — Reading and adapting the signals

Sources: the Redis, Elasticsearch, RabbitMQ and Kafka rule groups of `_data/rules.yml` in samber/awesome-prometheus-alerts at 822af1e (alert rules and content CC BY 4.0, credit in `references/origin.md`), read 2026-10-16. This section states how the rules in the source are built, so that a rule is copied with what makes it work; the signals themselves are in §2 and §3.

## 1.1 Severity and hold go together
1. **Every source rule carries a severity (`critical`, `warning` or `info`) and, where it applies, a hold duration (`for`).** Copy the pairing with the condition: the condition alone fires on every blip, and a hold alone says nothing about urgency.
2. **Liveness and node-count rules hold one minute.** The source's comment on them is that the delay allows a restart without triggering an alert.
3. **Slow-moving states hold longer:** two minutes for memory, connection, heap and replica-link conditions, five minutes for Redis cluster state and failed slots, ten minutes for the Elasticsearch thread-pool rejection ratio and indexing latency and for RabbitMQ connection churn, fifteen minutes for Elasticsearch shards stuck relocating or initializing and for pending tasks and for a growing Kafka lag, and one hour for a RabbitMQ disk prediction or mixed versions in a cluster.
4. **States that are bad on any occurrence hold nothing:** Elasticsearch red, a Redis instance with no master, a lost replica (replication broken), an Elasticsearch circuit breaker trip, a RabbitMQ network partition in the kbudde exporter group.
5. **`info` appears in these four rule groups only for the Elasticsearch shard states relocating and initializing**, as awareness next to their fifteen-minute `warning` twins. A page-level alert is not made of them.

## 1.2 Two tiers on a gradual resource
1. **The source pairs a `warning` and a `critical` threshold on the resources that degrade gradually:** Elasticsearch heap at over 80 percent (warning) and over 90 percent (critical, both held two minutes), disk with less than 20 percent available (warning, held two minutes) and less than 10 percent (critical, no hold).
2. **Own guidance:** the first tier is the one that leaves time to act, so put the person who can free space or add capacity on it, and keep the second for the wake-up.

## 1.3 Ratios against the resource's own limit
1. **The saturation rules compare a value with its own capacity, as a percentage:** Redis memory against `maxmemory` and against system memory, connected clients against `maxclients`, RabbitMQ resident memory against its limit and open descriptors against the maximum, Elasticsearch heap and disk against their totals. That is what lets one rule serve instances of different sizes.
2. **Every ratio rule also requires the denominator to be above zero** (for example that `maxmemory` or the node's heap maximum is set); the connection-churn rule asks for at least 100 connections instead. Own reading: a limit of zero, or an idle period with no operations, would otherwise give a meaningless ratio; add the same condition to a rule of your own.
3. **The same shape is used for per-operation averages:** Elasticsearch indexing and query latency divide time by operation count, only while operations are happening, and the thread-pool rejection ratio divides rejections by rejections plus completions.

## 1.4 Counters
1. **The source reads event counters through a window, never raw:** Redis rejected connections (an increase over one minute above five), RabbitMQ unroutable messages (an increase over five minutes above three, returned or dropped), Elasticsearch circuit breaker trips (an increase over five minutes above zero), and "no new documents" (an increase over ten minutes below one).
2. **Own guidance:** a cumulative counter that has counted once stays above zero until the process restarts, so a raw comparison fires for ever after the first event and never resolves. Wrap any counter you alert on in a window.
3. **Replica loss is also read as a change over a short window:** Redis replication broken is a fall of the connected-replica count over one minute, and Redis cluster flapping is more than one change in that count over one minute, held two minutes.

## 1.5 Thresholds are starting points
1. **The source marks many numbers as rough defaults to adjust:** the Redis rejected-connection volume and the 48-hour backup age; the Elasticsearch ten-minute no-new-documents window, 10 ms per indexing operation and one second per query; the RabbitMQ 1000 connections, 1000 ready messages, 1000 unacknowledged messages and the unroutable threshold of three; the Kafka lag of 10000 messages.
2. **Some numbers encode a cluster size.** "Fewer than 3 nodes" for Elasticsearch and RabbitMQ, and "fewer than 3 in-sync replicas" for Kafka (the source says to match the topic's replication factor), are the source's cluster, not yours.
3. **Set each threshold from your own data and say which window and percentile it came from** (`observability-instrumentation` §4.6), and write the number's origin next to the rule.

## 1.6 Exporter names and versions
1. **The source has a separate rule group per exporter, and the metric names differ between them.** Redis is read through oliver006/redis_exporter, Elasticsearch through prometheus-community/elasticsearch_exporter, RabbitMQ through the rabbitmq-prometheus plugin or through kbudde/rabbitmq-exporter, Kafka through danielqsj/kafka_exporter (and Burrow in a second group). A rule written for one exporter's names does nothing on another's.
2. **Some rules need an exporter option.** The Redis system-memory rule says the exporter must be started with its include-system-metrics flag or the matching environment variable.
3. **Check every metric name against the output of the exporter and version you run,** and re-check on an exporter upgrade (`source-freshness`). The stamp of this block is the commit named above; nothing was run.

## 1.7 Next to symptom alerts (own guidance)
1. **`observability-instrumentation` §4.1 says to alert on a symptom the user can see, and on an infrastructure cause only when the link has been shown to be causal.** The source itself states the link for several signals here: RabbitMQ's memory and disk alarms block publishers cluster-wide, a Redis cluster state that is not ok cannot serve queries, an Elasticsearch red status means a primary shard is unassigned (`elasticsearch-query-and-triage-pitfalls` §3). Those are cause signals worth a page on their own; keep the user-facing symptom alert as the page, and attach these as the cause the responder looks at first.
2. **Signals the source does not tie to a symptom (CPU, heap before it trips a breaker, pending tasks, relocating shards, connection counts) are warnings or dashboard lines until you have seen them precede an outage** (`observability-instrumentation` §4.4).
3. **Two signals here are absences,** an Elasticsearch cluster whose data nodes indexed nothing in ten minutes and a RabbitMQ queue with no consumer, which is the class of failure that a symptom set misses (`observability-instrumentation` §4.9). Decide on purpose whether the engine's normal pattern makes them valid for you.

## 1.8 Checks (own guidance)
1. Each alert copied from §2 or §3 keeps its hold duration and severity, or the change is written down.
2. Each metric name was found in the output of the exporter in use.
3. Each ratio carries its denominator condition, and each counter is wrapped in a window.
4. Each threshold has an origin, and each cluster-size number was replaced by yours.
5. Each alert names what the responder does (`observability-instrumentation` §4.3).
6. Each alert was made to fire once, by simulation or in a test environment (`observability-instrumentation` §4.2).
7. Each rule that needs an exporter option has it enabled, and a rule that returns no data was checked for a missing option or a wrong metric name before being trusted.
