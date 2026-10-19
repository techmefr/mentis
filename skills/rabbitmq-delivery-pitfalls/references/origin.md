# rabbitmq-delivery-pitfalls: origin and source stamps

> Provenance of `skills/rabbitmq-delivery-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us against a RabbitMQ broker. No queue, publisher or
consumer was started.

## Sources (all read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| rabbitmq/rabbitmq-website at commit db23826 (2026-10-14), `docs/reliability.md` | Dual-licensed Apache-2.0 OR MPL-2.0; phrased under Apache-2.0. `LICENSE-Apache-2.0` and `LICENSE-MPL-2.0` exist, the README "Copyright and License" section states the dual licence (SPDX `Apache-2.0 OR MPL-2.0`) and excludes the blog; the file carries the Apache-2.0 header. All re-read 2026-10-15 | Ack as ownership transfer, at-least-once, data safety per side, redelivered flag, republish duplicates, `mandatory` |
| same, `docs/consumer-prefetch.md` | same (Apache-2.0 header in the file) | Per-consumer prefetch against the AMQP definition, 0 as unlimited, default prefetch setting |
| same, `docs/confirms.md` | same (Apache-2.0 header in the file) | Auto-ack unsafety, prefetch, quorum cap of 2,000, double ack and unknown tags, requeue loops, publisher confirms, confirm latency and ordering, persistence scenario |
| same, `docs/dlx.md` | same (Apache-2.0 header in the file) | Dead letter triggers, policy against arguments, silent drop on a missing exchange, unconfirmed republish, cycle detection |
| same, `docs/production-checklist.md`, section "Application Considerations" (plus the memory-alarm sentence in the resource section) | same (Apache-2.0 header in the file) | Connection management and churn, separate connections, heartbeat floor, automatic recovery, channels, polling |

The documentation website blog is excluded by the README and was not read. The `docs/` folder is the
development tree of the site; `versions.json` at the same commit lists 4.3, 4.2, 4.1, 4.0 and 3.13, and
`package.json` is at 4.3.0. The pages themselves state no version, so no rule is tied to a RabbitMQ version.

## Removed (in the sources, not carried)
- Everything on the broker operator side: memory and disk watermarks, file descriptor limits, storage and
  filesystem choice, clustering, partition handling, TLS, users and permissions, monitoring. The block is
  about application code; the operator pages were not the subject of the review item.
- Code samples (Java, .NET), management and CLI commands: replaced by prose.
- The `x-death` header table beyond one sentence (§3.1.3), and federation and shovel material.
- The review's "keep heartbeat timeouts at 5 seconds or more" is carried as "do not go below 5 seconds", which is
  what the page says.

## Not verified
1. **Quorum queues and streams pages** (`quorum-queues`, `streams`) were not read. The 2,000 prefetch cap, the
   delivery limit and at-least-once dead lettering are stated as the pages read state them (confirms.md,
   dlx.md); the behaviour of quorum queues themselves was not checked.
2. **Published numbers** (a few hundred milliseconds of confirm latency, throughput cut by 250 for
   transactions, prefetch 100 to 300) are quoted from the pages and not measured.
3. **Defaults and client support** (automatic recovery in the Java, .NET and Ruby clients) were not checked
   against client documentation.
4. **Own guidance, labelled in the text:** the single-owner remark on acks (§1.3.2), not looping on channel
   reopen (§4.3.2), counting redeliveries in a cycle that contains a rejection (§3.3.4), and every "Checks"
   section.
5. **The page's own caveats** are kept: the `redelivered` flag is a hint in one direction only, and publisher
   confirms and consumer acknowledgements are independent.

## Related blocks
`background-jobs-conventions` §1 to §5 (at-least-once and dead letters in general), `nestjs-reliability` §1 and
§3 (idempotency keys, outbox), `observability-instrumentation` §4 (alerting on queue depth), `source-freshness`.
