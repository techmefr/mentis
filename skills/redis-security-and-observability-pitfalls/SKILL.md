---
name: redis-security-and-observability-pitfalls
description: "Use when deploying, hardening or monitoring a Redis instance: authentication and TLS, one ACL user per application with command categories, bind and protected-mode and firewall, restricting destructive commands, which INFO metrics to export and alert on, and the built-in commands for triage (SLOWLOG, MEMORY DOCTOR, CLIENT LIST, FT.PROFILE)."
---

# redis-security-and-observability-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for what stands around a Redis server once it leaves a laptop. The
premise: **an instance with no password and an open interface is the usual Redis breach, a leaked application
credential should not be able to wipe the keyspace, and a server nobody exports metrics from is diagnosed by
guessing**. Keys, connections, pools and cluster slots are in `redis-client-and-cluster-pitfalls`; the
alert rules themselves are in `datastore-broker-alerting-signals`.

## When
- A Redis instance is deployed, exposed to a network, or audited against a hardening checklist.
- An application gets its Redis credentials, or credentials leak.
- Monitoring or alerts are set up for Redis, or a latency, memory or connection incident is being diagnosed.

## Steps

**Read only the section the task meets.** They are independent, but §1 comes first on a new deployment.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Authentication and TLS, ACL users and categories, bind and protected-mode, destructive commands | an instance is deployed, exposed or audited | [`01-access-and-network.md`](./references/01-access-and-network.md) |
| 2 | INFO metrics worth exporting, built-in triage commands, GUI against monitoring | monitoring is set up or an incident is diagnosed | [`02-observability.md`](./references/02-observability.md) |

## Output / checkpoint
Each section ends with its own checks. For a deployment: authentication and TLS on, one ACL user per
application with its commands and key patterns, a named interface list with protected-mode on and a firewall,
and no application using the admin user. For monitoring: the INFO metrics exported to the monitoring system,
and the triage commands known to the on-call.

## Guardrails
- Never run a production Redis without authentication (§1.1).
- Never bind to every interface with protected-mode off (§1.3).
- Never give application traffic the admin user, or share one password between applications (§1.2).
- Never rely on `rename-command` without verifying it for the server version in use (§1.4).
- Never treat a GUI as monitoring (§2.3).
- The thresholds in §2 are the source's examples, not limits; nothing here was run against a Redis server (🟡).

## Origin
Rewritten from the Redis, Inc. `redis-security` and `redis-observability` agent skills (MIT, commit a84871d),
read 2026-10-16. Open points and own guidance are in [`references/origin.md`](./references/origin.md).
