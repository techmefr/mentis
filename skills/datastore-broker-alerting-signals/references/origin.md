# datastore-broker-alerting-signals: origin and source stamps

> Provenance of `skills/datastore-broker-alerting-signals`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from a collection of alert rules, never run by us. No Prometheus, no exporter and no
Redis, Elasticsearch, RabbitMQ or Kafka instance was started while writing it, and no alert was made to fire.

## Attribution (CC BY 4.0)

The alert rules in this block are derived from awesome-prometheus-alerts by Samuel Berthe
(https://github.com/samber/awesome-prometheus-alerts, site https://samber.github.io/awesome-prometheus-alerts),
whose alert rules and content are licensed under Creative Commons Attribution 4.0 International
(https://creativecommons.org/licenses/by/4.0/). **Changes made:** the rules were read in the repository's
`_data/rules.yml`, rewritten as prose and tables, regrouped by engine, and selected (see "Removed"); the
PromQL queries are described in words with the exporters' metric names and are not reproduced, and every
sentence marked as own guidance or own reading is ours and not the source's. The licence applies to the source
content and does not extend to the rest of this repository.

## Sources (all read in full 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| samber/awesome-prometheus-alerts at commit 822af1e: `_data/rules.yml`, group Databases, services Redis (lines 1611 to 1716) and Elasticsearch (lines 1962 to 2094) | CC BY 4.0 for the alert rules and content (`_data/rules.yml`, `dist/rules/`, `README.md`), MIT for `site/` (`LICENSE` re-read 2026-10-16; the README licence section says the same) | Redis and Elasticsearch signals, conditions, hold durations and severities, the rough-default comments |
| samber/awesome-prometheus-alerts at 822af1e: `_data/rules.yml`, group Message brokers, services RabbitMQ (lines 2767 to 2949) and Kafka (lines 2989 to 3032) | CC BY 4.0 (same file) | RabbitMQ and Kafka signals, conditions, hold durations and severities, the placeholder-name rules |

The repository's `CLAUDE.md` (guidance for an AI agent contributing rules) is outside the licensed set named
in `LICENSE`, contains instructions to an agent, and was treated as data: it was read but not used as a
source, and none of its content is carried. The other rule groups of the file, the `dist/rules/` copies, the
site and the Zookeeper group were not read for this block.

## Decision: new block, not a reference inside `observability-instrumentation`
The review item allowed either. This is a new block because `observability-instrumentation` is engine-agnostic
application instrumentation whose §4.1 is a symptom-first rule; a catalogue of engine and exporter specific
signals, with metric names bound to exporter versions, would change its premise and its refresh cycle, and a
reader writing alerts for one engine would have to load the whole alerting section. The block links to
`observability-instrumentation` §4 and states in §1.7 how the two fit. No main block was edited.

## Version bounds stated in the sources
None for the products. The source gives no Redis, Elasticsearch, RabbitMQ or Kafka version, nor an exporter
version, for any rule in these groups. Exporter metric names are bound to the exporter that exposes them, and
a Redis rule says it needs the exporter's include-system-metrics flag or the matching environment variable.

## Removed (in the sources, not carried)
- Redis "not enough connections" (fewer than 5 connected clients): low signal, and the rule's own comment says
  baseline non-application connections exist.
- Elasticsearch "high indexing rate" (above 10000 operations per second) and "high query rate" (above 100 per
  second): traffic volume and not failure, and the source's own comment calls the second very low for most
  production clusters.
- The RabbitMQ rules that hard-code `my-queue`, `my-dead-letter-queue` and `my-exchange` are kept only as
  templates (§3.1), not as rules.
- The Burrow rules for Kafka (offset decreased; lag growing), described in §3.3 and not carried.
- Zookeeper, Pulsar and NATS groups, and the rest of the file: out of scope.
- The PromQL expressions themselves, the descriptions' template variables and the exporter documentation links.

## Not verified
1. **Metric names and label names** are as the source writes them for the named exporters; none was checked
   against an exporter's output or documentation, and the exporters' versions are not known.
2. **Rule semantics of the source** (for example what the Redis "disconnected slaves" arithmetic counts, or
   that the "too many masters" query counts every scraped master) are our reading of the source's queries,
   which were not run.
3. **The source's thresholds and hold durations** are its starting points, many labelled rough defaults, and
   are carried as such.
4. **Own guidance and own reading, labelled in the text:** scoping the Redis master count to one replication
   group, the warning going to those who can add disk, the Kafka in-sync threshold reading, the first tier of a
   two-tier alert as the one with time to act, windowing every counter, the queue-with-no-consumer caveat, the
   fit with symptom-based alerting (§1.7), and every "Checks" section.

## Related blocks
`observability-instrumentation` (§4: alerting), `redis-security-and-observability-pitfalls` (Redis metrics and
triage commands), `redis-client-and-cluster-pitfalls`, `elasticsearch-query-and-triage-pitfalls` (non-green
triage), `rabbitmq-delivery-pitfalls`, `kafka-delivery-semantics-pitfalls`, `source-freshness`.
