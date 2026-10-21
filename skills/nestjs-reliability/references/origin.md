# nestjs-reliability: origin and source stamps

> Provenance of `skills/nestjs-reliability`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. Nothing here
has been through production feedback; the rules that lean on mechanisms we did not exercise are listed
under "Not verified" below.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The NestJS documentation repository, content of the Nest 12 docs: the reliability chapters on idempotency, locks, outbox and resilience, and the task-scheduling and HTTP-client chapters (each read in full) | MIT, read 2026-10-08 | The mechanisms of §1 to §4 and the Nest mappings: key fingerprint and record outcomes, owner-conditional writes, lease and fencing token on the store's clock, outbox and inbox semantics, relay claims and ordering, the stage-by-stage resilience policy, retry and timeout defaults of the HTTP client |
| One NestJS agent-skills catalogue: the failure-resilience reference and the "events, queues and outbox" concept page | MIT, read 2026-10-08 | Cross-check of the unknown-outcome rule (§4.7), retry decision by semantics, partial-effect questions, and that the outbox does not give exactly-once side effects |
| One NestJS standards catalogue: its scheduling skill | MIT, read 2026-10-08 | Cross-check that a scheduler runs on every pod and needs a lock; see the discrepancy below |
| One Fastify/TypeScript skills catalogue: its integrations skill | MIT, read 2026-10-08 | Cross-check of the unknown-outcome and budget rules (a lost connection after a write leaves success unknown; budget attempts, time, concurrency together; racing a timer only settles the race) |

The ideas-only repositories listed in the sourcing review (a no-licence NestJS skills repo, the two
share-alike Node best-practice and security repositories) were not used for any phrasing.

## Rewrite notes
- The mechanisms are re-explained principle first, with what a reader actually sees when each one is
  missing. The Nest package names appear only in the "Nest mapping" subsection of each section and in the
  guardrails.
- The documentation's worked example (an online shop) was replaced by generic shapes (an order, a carrier, a
  warehouse feed) and every code listing was dropped except SQL-shaped sentences inline.

## Discrepancy between sources, and what was followed
The standards catalogue's scheduling skill says an uncaught exception in a scheduled handler crashes the
whole Node process. The Nest 12 docs say the opposite for `@Cron`, `@Interval` and `@Timeout`: each method
is wrapped in a try/catch and the exception is logged. §2.6.2 follows the documentation (log and continue)
and treats the real unseen failure as the schedule silently stopping, which is a monitoring rule, not a
crash rule. We did not run either behaviour.

## Verification pass 2026-10-20
Re-opened the Nest documentation repository (MIT, `LICENSE` re-read: Kamil Mysliwiec) pages for idempotency,
locks, outbox, resilience, the HTTP client and task scheduling, each searched for the exact figure or behaviour
the block states. Confirmed against the pages: the 24 hour result lifetime and the 60 second in-flight lock
renewed every third; the 409 with `Retry-After`, the 422 on a changed fingerprint, the 400 for a missing key; results
below 500 stored and 5xx released; the store contract methods and the shipped contract test suite; the 30 second
lease renewed every third, the sequence-based fencing token, expiry on the store's clock, the in-memory store
refusing production start-up, the Redis asynchronous-replica caveat, `@OnOneInstance` skipping other instances'
ticks and the advice to set an explicit key; the outbox relay claim with a lease token and `SKIP LOCKED`, ordering
per key only, 20 attempts doubling from 1 s to 5 min, dead letters with `exhausted` and `rejected` reasons, the inbox
recorded after success, no pruning scheduled for you; the resilience policy order, breaker thresholds (50 percent,
10 minimum calls, window of 20, 30 seconds open), the bulkhead figures, 504 chosen over 408 for the reason the
block gives, 503 with `Retry-After` for an open breaker; the HTTP client's three attempts, default no timeout with
undici's five minute limits, status list, 30 second cap, replaced lists and 502/504 mapping with logging; and
that scheduled handlers are wrapped in a try/catch that logs (§2.6.2 follows the documentation, as stated above).
Corrected: idempotency-file point 12 (an in-memory store does ship; only the interceptor in front of the class serialiser blocks
start-up, other global interceptors give a warning). The four "Not verified" items below about defaults, the
five minute fetch limit, 408 and Redis failover are now **verified against the same pages** (items 2, 3, 4 and
6); item 1 (minimum core versions and release status) and item 5 (ours) stand.

## Not verified
1. **Minimum Nest core version for each package.** The docs repository is the Nest 12 documentation (it
   states "As of NestJS v12" in one recipe), but none of the chapters read states the minimum core version
   of `@nestjs/idempotency`, `@nestjs/locks`, `@nestjs/outbox`, `@nestjs/resilience` or `@nestjs/http-client`,
   nor whether each is published as a stable release. The Nest mappings are therefore documentation-level
   only; nothing was installed or executed.
2. **The in-chapter default values** (24-hour idempotency TTL, 30-second lease, 20 retry attempts, three
   HTTP-client attempts, the example breaker thresholds) are quoted from the docs and not checked against
   the packages' source.
3. **The "fetch has no timeout beyond five-minute limits of the HTTP client inside Node"** statement (§4.1.1)
   comes from the HTTP-client chapter and was not checked against the Node release in use.
4. **The 408-repeated-by-proxies claim** (§4.1.4) is the docs' justification for choosing `504`; not
   independently verified.
5. **Written by us, not sourced:** the alternatives listed in §2.1.6 (dedicated worker replica, a scheduler
   that only enqueues under a deterministic job id) and their stated costs; the dead-letter and queue
   enqueue remarks in §3; the generalisation of a "job silence" alert into a vendor-neutral
   "has not succeeded in N hours" rule (§2.6.2).
6. **Redis failover claims** (§2.4.5) restate the lock chapter's reasoning on asynchronous replicas; not
   tested.

## Related blocks
`background-jobs-conventions` (§1 at-least-once and idempotent jobs, §3 overlap guards, §4 payload
compatibility), `api-design` (the replay and conflict status codes are part of the contract), and
`nestjs-node-conventions` (module and DI layout this block assumes).
