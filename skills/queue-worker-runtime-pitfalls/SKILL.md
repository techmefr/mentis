---
name: queue-worker-runtime-pitfalls
description: "Use when a BullMQ queue (on Redis) or a Graphile Worker queue (on PostgreSQL) is wired into a Node service: opposite connection behaviour for the code that adds jobs and the worker (fail fast versus wait forever, offline queue, per-request retries), the ioredis key prefix, undefined values passed as queue names, custom job ids, throwing Error objects and the unrecoverable error that skips retries, shutdown on SIGTERM and stalled jobs, 'Missing lock' errors, clear-text payloads, and for Graphile Worker the lock window after a hard kill, job keys and their modes, perma-failed jobs, un-awaited promises and splitting non-idempotent jobs."
---

# queue-worker-runtime-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the runtime of one job library once the queue exists. The premise:
**the code that adds a job and the code that runs it want opposite things from the connection, a worker that is
stopped badly leaves its jobs in limbo for a long time, and a deduplication key can swallow the event you
needed**. Residue only: retry limits and backoff, retention, idempotent jobs, dead-letter handling and
deploys with jobs in flight are in `background-jobs-conventions`; idempotency keys, locks, `noeviction` and the
outbox are in `nestjs-reliability`; Redis client pools and cluster slots are in `redis-client-and-cluster-pitfalls`.

## When
- A service adds jobs from a request path and a Redis outage turns into hanging HTTP calls.
- A worker dies on connection errors, or logs 'Missing lock for job'.
- A job fails with a permanent cause and is still retried, or a custom job id is silently ignored.
- Workers are deployed or killed and jobs stay locked, or run twice.
- A Graphile Worker task is written, a `job_key` is chosen, or perma-failed jobs pile up.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | BullMQ connections: adder versus worker, key prefix, undefined arguments, error events | a queue or worker is created, or a Redis outage is being designed for | [`01-bullmq-connections.md`](./references/01-bullmq-connections.md) |
| 2 | BullMQ jobs: thrown errors, unrecoverable errors, job ids, payloads, shutdown, stalled jobs, lost locks | a processor, a job id or a deploy of workers is written | [`02-bullmq-jobs-and-shutdown.md`](./references/02-bullmq-jobs-and-shutdown.md) |
| 3 | Graphile Worker: failure and shutdown, hard-kill window, job keys, perma-failed jobs, task executors | the library runs on PostgreSQL | [`03-graphile-worker.md`](./references/03-graphile-worker.md) |

## Output / checkpoint
Each rule was exercised, not read off the page: Redis was stopped while the adding endpoint was called and the
caller got an error quickly (1.1), a worker survived the same outage and resumed (1.1), a processor threw the
unrecoverable error and the job was not retried (2.2), a worker was sent SIGTERM with a job running and the
job finished or was seen to stall (2.4), and for Graphile Worker a worker was killed hard and the locked job
was found (3.2). A queue that was only read is not verified.

## Guardrails
- Never share one connection setting between the code that adds jobs and the worker (1.1).
- Never use the ioredis `keyPrefix` option with BullMQ (1.2).
- Never pass a possibly undefined or empty value as a queue name or job argument (1.3).
- Never throw a non-Error value from a processor (2.1).
- Never put a colon in a custom job id, or make it all digits (2.3).
- Never put secrets in a job payload (2.3).
- Never use the `unsafe_dedupe` job key mode unless losing the triggering event is acceptable (3.3).
- Never run a bulk delete of perma-failed jobs without reading why they failed (3.4).
- This block states library documentation as of the commits in [`references/origin.md`](./references/origin.md);
  behaviour is version-bound, and nothing here was run against a queue (🟡).

## Origin
Rewritten from the BullMQ documentation (taskforcesh/bullmq, MIT) and the Graphile Worker documentation
(graphile/worker, MIT), read 2026-10-16. 🟡: never run by us; open points and own guidance are in
[`references/origin.md`](./references/origin.md).
