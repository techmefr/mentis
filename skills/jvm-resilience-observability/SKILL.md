---
name: jvm-resilience-observability
description: "Use when a Java or Spring Boot service calls another system or must be operated: timeouts on HTTP clients and the connection pool, Resilience4j retry, circuit breaker, bulkhead and time limiter and the order they wrap each other, fallbacks, and then the operating side on Spring Boot with Micrometer: a correlation id in the logging context and whether it survives a thread hand-off, meter tag cardinality, liveness versus readiness probes, graceful shutdown, structured JSON logs."
---

# jvm-resilience-observability

Step 6 of the pipeline (`WORKFLOW.md`), for what a JVM service does when something it depends on is slow or
down, and for what it must expose so a person can tell. The two sections share one premise: **a dependency
that fails slowly is more dangerous than one that fails fast, and a failure nobody can trace or count is one
you learn about from a customer**. The first section bounds how long and how often a call may try; the
second makes the result visible. `observability-instrumentation` §1 to §3 carry the generic rules (the
question first, structured logs, metric cardinality); `devops-conventions` §3 covers monitoring and alerting;
this block adds the JVM and Spring Boot specifics.

## When
- Adding or reviewing an outbound HTTP, database or queue call, or wrapping one in a retry or a breaker.
- A service hangs under a slow dependency, retries into an outage, or takes every instance out at once.
- Adding a metric tag, a log field, a health indicator or a Kubernetes probe, or changing shutdown.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Outbound calls: timeouts, retry, circuit breaker, bulkhead, time limiter, fallback, decorator order, Resilience4j | a call to another system is added or changed, or a dependency outage spreads | [`01-outbound-calls.md`](./references/01-outbound-calls.md) |
| 2 | Operating on Spring Boot: correlation id and thread hand-offs, metric tags, probes, graceful shutdown, structured logs | a log field, a metric, a probe or the shutdown behaviour is added or changed | [`02-operating-the-service.md`](./references/02-operating-the-service.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the dependency was made slow in a test or an environment and
the call returned an error within the configured timeout (§1), the failing dependency was made to fail
repeatedly and the breaker opened and the metric for its state changed (§1), a request's correlation id
appeared in a log line written from an asynchronous task (§2), the probes were queried with the database
stopped and the liveness probe stayed up (§2), and the service received a termination signal during a
request and finished it (§2). Configuration that was only read is not verified.

## Guardrails
- Never leave a call without an explicit timeout, and never rely on a library's default for one (§1.1).
- Never retry an exception that is a business outcome (§1.2).
- Never put a check of an external system in the liveness probe (§2.3).
- Never use an unbounded value (an id, a raw URL, a user input) as a metric tag (§2.2).
- This block states Resilience4j 2.2, Micrometer 1.17 and Spring Boot 4.1 behaviour as of the documentation
  read on the date in [`references/origin.md`](./references/origin.md); defaults moved between releases, so
  check a number against the version in use. Nothing was run while writing it.
- Adding Resilience4j or a Micrometer registry is the user's step, in their own terminal; this block names
  them and stops.

## Origin
Rewritten from the Resilience4j user guide (retry, circuit breaker, bulkhead, time limiter, Spring Boot
starter), the Spring Boot actuator, logging, observability and graceful-shutdown pages, the Micrometer naming
page and the HikariCP readme (read 2026-10-08). 🟡: never run by us; meant to be folded into the same-topic
blocks (`spring-boot-conventions` actuator reference, and `observability-instrumentation` for the
operating part) when PR 118 lands; open points are in [`references/origin.md`](./references/origin.md).
