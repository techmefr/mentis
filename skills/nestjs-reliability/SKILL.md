---
name: nestjs-reliability
description: "Use when a Node or NestJS service has to survive retries, several replicas and slow dependencies: idempotency keys on a request or a message handler, scheduled jobs or locks across replicas (leases, fencing tokens), a transactional outbox with a consumer inbox, and outbound call policy (timeouts, retries, circuit breaker, bulkhead, unknown outcome after a timeout)."
---

# nestjs-reliability

Step 6 of the pipeline (`WORKFLOW.md`), for the failure modes that only appear once the service runs on
more than one instance, behind a network that loses packets, next to dependencies that stall. The four
sections share one premise: **a request, a tick or a message will be delivered more than once, and a call
that timed out may have succeeded**. Every rule states the principle first, so it holds for any Node
service; the Nest mapping is noted where one exists. It complements `background-jobs-conventions`
(which covers what a job must do once it runs) and `nestjs-node-conventions` (module layout, DTOs).

## When
- A write endpoint a client may retry (payment, order, shipment, anything a customer would notice twice),
  or a message/event handler a broker may redeliver.
- A cron, interval or startup task in a service deployed as more than one replica, or any code that must
  be the only one doing something at a time.
- A database write and a message, event, email or queue entry that must agree.
- A call to another service or SDK: its timeout, its retry, what to do when it is down or when it did not
  answer.

## Steps

**Read only the sections the task meets.** The sections are independent but chain naturally: an outbound
call (§4) usually needs the receiver's idempotency (§1); a relay on several replicas (§3) reuses the lease
and fencing of §2.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Idempotency keys | a client or broker may repeat a request or message; a write must happen once | [`01-idempotency-keys.md`](./references/01-idempotency-keys.md) |
| 2 | Locks, leases, fencing tokens, scheduled jobs on replicas | a job or critical section must not run twice at once, or the service has more than one replica | [`02-locks-and-scheduled-jobs.md`](./references/02-locks-and-scheduled-jobs.md) |
| 3 | Transactional outbox and consumer inbox | a database write and a publish/enqueue/email have to agree | [`03-outbox-and-inbox.md`](./references/03-outbox-and-inbox.md) |
| 4 | Outbound resilience policy and unknown outcomes | the code calls another system, sets or changes a timeout/retry/breaker, or handles a timeout on a write | [`04-outbound-resilience.md`](./references/04-outbound-resilience.md) |

## Output / checkpoint
The section's own verification list was run, and its evidence is attached: the duplicate was actually
sent (twice in sequence and twice concurrently for §1), the second instance was actually started (§2), the
transaction was actually rolled back after the message was written (§3), the dependency was actually made
to hang (§4). A diff that adds one of these mechanisms and was only exercised on a single instance with a
healthy dependency is not verified.

## Guardrails
- Never add an in-memory store to a path whose job is to survive restart or coordinate instances. It
  excludes callers inside one process and forgets everything on deploy; the only legitimate use is a
  single-instance development run.
- Never retry a write without an operation identity the receiver deduplicates on; never report a timed-out
  write as "failed" without having checked.
- Never fix a duplicate-run bug by adding a second mechanism on top (a flag, a sleep, a "run only on
  instance 1" variable) before reading §2: those fail during exactly the rolling deploy where they are
  needed.
- Never write the message with the database handle, the pool or an autocommit client: it removes the
  atomicity the outbox exists to give (§3.2).
- Dependencies named here (the Nest packages for idempotency, locks, outbox, resilience and the HTTP
  client) are named, not installed, by this block: whoever adds one runs the install themselves, with the
  project's package manager.
- The Nest packages are described from their documentation only. No package was installed or run while
  writing this block, and the minimum Nest core version each one needs was not verified: check it against
  the version the project is on before relying on a mapping.
- Replaying, purging or requeueing dead letters, and force-releasing a lock, re-execute real side effects
  or break an exclusion in a shared environment: a human decision.

## Origin
Rewritten from the reliability and scheduling chapters of the NestJS documentation repository (MIT, read
2026-10-08, the Nest 12 docs), cross-checked against three MIT agent-skill repositories (one NestJS
catalogue's failure-resilience reference and outbox concept page, a NestJS standards catalogue's
scheduling skill, a Fastify/TypeScript integrations skill, each read 2026-10-08). The mechanisms are
re-explained in our own words and ordered by what a reader sees when each one is missing. 🟡: written from
documentation and reading, never run on a real service by us; the rules marked as unverified in
[`references/origin.md`](./references/origin.md) are the first to confirm.
