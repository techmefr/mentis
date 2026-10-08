# jvm-resilience-observability: origin and source stamps

> Provenance of `skills/jvm-resilience-observability`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. No breaker was
configured, no probe was queried and no application was started while writing it.

**Fold-in note.** This block is meant to be folded into the actuator reference of `spring-boot-conventions`
(the Spring parts) and into `observability-instrumentation` (the operating part) when PR 118 lands. It is
standalone only so that it does not depend on a block that is not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Resilience4j user guide, version 2.2 pages: retry, circuit breaker, bulkhead, time limiter, Spring Boot starter | Apache-2.0 (LICENSE.txt read in the repository) | §1.1 (time limiter), §1: defaults, states, fallbacks, aspect order, metrics |
| The Spring Boot 4.1 pages: actuator endpoints (probes), observability (correlation id, propagation), logging (structured), graceful shutdown, REST clients, properties appendix | official docs, read 2026-10-08 | §1.1 point 1, §2.1, §2 |
| The Micrometer 1.17 page on naming meters | official docs, read 2026-10-08 | §2.2 |
| The HikariCP readme | Apache-2.0 | §1.1 point 2: connection timeout default and minimum |

## Rewrite notes
Rules are re-explained principle first; numbers are the guide's defaults at the version read, stated as such.
The "a fallback is a real degraded answer" and "alert on the breaker staying open" lines are our guidance.

## Not verified
1. **Client library defaults.** No page read states the default connect or read timeout of the HTTP clients
   Spring Boot configures, so §1.1 says to set them explicitly rather than claiming a default is infinite.
2. **JDBC and queue timeouts** beyond the pool wait were not read; only the pool's `connectionTimeout` is
   covered. Per-statement and socket timeouts are not.
3. **Resilience4j version.** The guide pages read are the 2.2 pages; the Spring Boot starter page is the one
   for the Boot 3 starter. Whether the same module and property names apply to Spring Boot 4 was not read.
4. **Whether MDC survives a virtual-thread hand-off** was not found in the pages read; only the Boot
   propagation mechanism for `@Async` and reactive pipelines is stated.
5. **Dropped from the source list:** "retry only idempotent calls" as a rule (no page read states it; the
   block points to `background-jobs-conventions` §1 for repeat-safe effects), "no retry inside a
   transaction", "timeout shorter than the orchestrator's grace period", "per-hop timeouts shorter than
   the caller's", and "MDC cleared in a `finally`". None is stated on a page read.
6. **Written by us, not sourced:** the checks lists and the "decide and write it down" advice on readiness.

## Related blocks
`observability-instrumentation` (§1 to §4), `devops-conventions` (§3), `background-jobs-conventions` (§1),
`java-conventions` (§3), `security-hardening` (never log a token).
