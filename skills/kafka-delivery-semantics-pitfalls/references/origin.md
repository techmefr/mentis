# kafka-delivery-semantics-pitfalls: origin and source stamps

> Provenance of `skills/kafka-delivery-semantics-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one documentation page, never run by us against a Kafka cluster. No producer,
consumer or broker was started.

## Sources (read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| apache/kafka-site at commit e6cbeb5 (2026-10-14), `content/en/43/design/design.md`, the "Design" page of the Kafka 4.3 documentation (511 lines, read in two passes) | Apache-2.0 (`LICENSE` re-read 2026-10-15, Apache License Version 2.0 text; the file carries the ASF Apache-2.0 header) | Consumer position, delivery semantics, idempotent producer, ISR and `acks`, `min.insync.replicas`, unclean election, transactions and exceptions, compaction and tombstones |

This is the only source of the block, as the review decided for the Kafka rules.

## Version bounds stated in the source
- The page is the 4.3 documentation (path `content/en/43`). Marks it states itself: idempotent producer and
  transactions since 0.11.0.0; unclean leader election disabled by default since 0.11.0.0; static membership
  from 2.3 (not carried); `delete.retention.ms` default of 24 hours in the compaction section. The standardised
  transactional exception categories are described in the page as current ("are now more precisely defined");
  no earlier version is given.

## Removed (in the sources, not carried)
- Everything on the filesystem, page cache, `sendfile`, batching, compression, push against pull, quotas, static
  membership, quorum theory and replica management: design rationale and operations, not delivery rules.
- Share group details beyond one pointer (§3.4): the page covers them in a few paragraphs and the review marked
  them as a separate model.
- Other sources of the review: the Unknown-333 `building-kafka-consumers` skill (partition cap,
  `max.poll.interval.ms` rebalancing) was not used, as the review decided, since `design.md` does not confirm
  those rules. The Debezium, CloudEvents, AsyncAPI and ODCS clones were not used.
- The `TransactionalMessageCopier` and `TransactionalClientDemo` links of the page were not followed.

## Not verified
1. **Client configuration names** (`isolation.level`, `enable.auto.commit`, `transactional.id`, `acks`,
   `min.insync.replicas`, `unclean.leader.election.enable`, `delete.retention.ms`) are quoted from the page; the
   configuration reference pages (`content/en/43/configuration/`) were not read.
2. **Exception categories** were taken from the page's list; the client library behaviour was not checked.
3. **Which version of the 4.x line an application runs** is not claimed; the page is the 4.3 documentation.
4. **Own guidance, labelled in the text:** the lagging-consumer remark in §4.2.3, and every "Checks" section,
   including the replication factor against `min.insync.replicas` reading in §2.4.
5. **`design.md` operations pages** (monitoring, kraft, hardware, transaction protocol) were not read.

## Related blocks
`background-jobs-conventions` §1 to §5, `nestjs-reliability` §1 and §3, `data-pipeline-conventions` §1
(idempotent re-runs), `source-freshness`.
