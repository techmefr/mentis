# queue-worker-runtime-pitfalls: origin and source stamps

> Provenance of `skills/queue-worker-runtime-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no Redis or PostgreSQL server was started, no
queue created and no job run while writing it. Every page below was opened in full on 2026-10-16 before a rule
was taken from it, and each repository's licence file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| taskforcesh/bullmq (commit `84e3424`), `docs/gitbook/guide/going-to-production.md` | MIT (LICENSE file: MIT licence text, copyright BullForce Labs AB and contributors, 2018) | Persistence and eviction, reconnect options, error listeners, shutdown signals, clear-text payloads, unhandled exceptions |
| the same repository, `guide/connections.md` | MIT | Producer versus worker connection settings, the `keyPrefix` incompatibility |
| the same repository, `patterns/failing-fast-when-redis-is-down.md` | MIT | Offline queue off, 503 on failure, the startup limitation |
| the same repository, `guide/retrying-failing-jobs.md`, `patterns/stop-retrying-jobs.md` | MIT | Error objects, the unrecoverable error, rate-limit attempts, the two attempt counters |
| the same repository, `guide/jobs/job-ids.md`, `guide/jobs/stalled.md`, `guide/workers/graceful-shutdown.md`, `guide/troubleshooting.md` | MIT | Custom id rules, stalled jobs, `close()`, the lost-lock causes, undefined arguments |
| graphile/worker (commit `4cda192`), `website/docs/error-handling.md`, `job-key.md`, `tasks.md`, `scaling.md`, `index.md` | MIT (LICENSE.md: MIT licence text, copyright Benjie Gillam, 2019) | Failure and retries, shutdown and the four-hour lock, job keys and modes, task rules, perma-failed jobs |

The pages come from documentation directories of the two repositories, whose licence file is the repository's
MIT text; no separate licence for the documentation is stated, so the pages were rewritten, not copied. No
code sample was copied.

## Version bounds stated in the sources
1. BullMQ: the separate scheduler class is not needed from 2.0; the per-request retry default of 20 and the
   30-second lock and stall windows are the pages' defaults at the commit above; the startup limitation is
   described as "currently".
2. Graphile Worker: the 0.16 behaviour on migrations is the only version the pages name; the 25 attempts, the
   four-hour lock, the 8 to 10 minute sweep and the five-second second-signal window are as the pages state them.
3. The BullMQ package version in the clone was not used as a claim anywhere.

## Removed in the verification pass
1. **"Enqueue inside the same database transaction as the business write"** was in the sourcing brief for
   Graphile Worker and was dropped: none of the five pages read says it. They state that jobs do not get lost
   thanks to the database's transactional guarantees, and that the query helper opens no transaction; the
   outbox principle is in `nestjs-reliability`.
2. **The BullMQ Pro documentation** (a commercial product) was not used.
3. **Retention, attempts, back-off and `noeviction` as separate rules** were left to `background-jobs-conventions`
   and `nestjs-reliability`; `noeviction` appears only as a pointer and as one cause of the lost-lock error.
4. **Code samples** (the shutdown handler, the 503 handler, SQL examples) were replaced by prose; the source
   examples use line comments, which this repository does not.
5. **The delete statement for perma-failed jobs** was described, not quoted: it targets a private table.

## Not verified
1. **Nothing was run.** Every behaviour is the documentation's claim.
2. **Whether `close()` waits on a job that never returns** was not tested; the page says it has no timeout.
3. **The current default of the per-request retry count** in the installed BullMQ was not read from code; the
   connections page's figure is quoted.
4. **BullMQ release notes** after the pinned commit, and Graphile Worker releases after 0.16, were not read.
5. **Written by us, not sourced:** all checks sections, the retention-versus-uniqueness remark (2.3 point 2),
   setting the platform grace period above the longest job (2.4), the order of the lost-lock investigation
   (2.5), doing the manual unlock only after confirming the worker is gone and the supervisor restart after a
   migration (3.2), startup-order testing (1.1 point 6), and the advice not to schedule the perma-failed delete.

## Related blocks
`background-jobs-conventions`, `nestjs-reliability`, `redis-client-and-cluster-pitfalls`,
`datastore-broker-alerting-signals`, `rabbitmq-delivery-pitfalls`, `source-freshness`.
