---
name: jvm-test-infrastructure
description: "Use when Java or Spring Boot tests need a real database or broker, a Spring context, or time: Testcontainers (a real engine instead of an embedded one, wiring the container with a service connection or a dynamic property, shared and singleton containers, the cleanup container, reuse), Spring Boot test slices versus a full context (@WebMvcTest, @DataJpaTest, @JsonTest, @SpringBootTest), the test context cache and what invalidates it (bean overrides, dynamic properties, @DirtiesContext, forked test processes), polling for an asynchronous result with Awaitility instead of sleeping, and injecting a Clock so tests fix time."
---

# jvm-test-infrastructure

Step 5 of the pipeline (`WORKFLOW.md`), for the plumbing under JVM tests rather than the assertions in
them. The three sections share one premise: **a test is only as good as the environment it ran in, and the
two ways that goes wrong are a slow suite that rebuilds everything for each class and a fast one that runs on
something that is not production**. The assertions themselves, mocks and waiting by duration are in
`testing-anti-patterns` §1 to §3; the TDD loop is `tdd`. This block adds what is specific to Testcontainers,
Spring Boot's test support, Awaitility and `java.time.Clock`.

## When
- A repository, a migration or a query is tested against a database, or a service against a broker.
- A Spring test is slow, or adding one annotation made the whole suite slower.
- A test sleeps, polls by hand, or fails around midnight, a month end or a daylight-saving change.
- Choosing between a slice test and a full context test.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Real dependencies with Testcontainers: real engine, wiring, shared and singleton containers, cleanup container, reuse | a test needs a database, broker or cache | [`01-real-dependencies.md`](./references/01-real-dependencies.md) |
| 2 | Spring Boot slices and the context cache: which slice, what a full context costs, what invalidates the cache | a Spring test is added, is slow, or an annotation is added to one | [`02-slices-and-context-cache.md`](./references/02-slices-and-context-cache.md) |
| 3 | Time and waiting: polling with a timeout, assertions inside the poll, an injected clock | a test waits for something asynchronous or depends on the current time | [`03-time-and-waiting.md`](./references/03-time-and-waiting.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the data-layer test ran against the production engine and the
version the deployment uses (§1), the suite was run twice from a cold start and the number of application
contexts built was read from the cache's debug log (§2), a slice test failed when a bean it should not have
needed was missing instead of silently loading the application (§2), and the time-dependent test was run with
the clock set to the awkward instant (§3). A test that was only read is not verified.

## Guardrails
- Never hard-code a host or port of a container (§1.2).
- Never turn the cleanup container off in an environment that does not clean up itself (§1).
- Never enable container reuse in CI (§1).
- Never add a bean override, a dynamic property or `@DirtiesContext` to one test class for convenience: it
  builds another context for that class (§2.3).
- Never wait with a fixed sleep (§3.1).
- This block states Spring Boot 4.1, Spring Framework 7.0, Testcontainers and Awaitility behaviour as of the
  documentation read on the date in [`references/origin.md`](./references/origin.md); annotation names and
  packages moved between Spring Boot major versions, so check a name against the version in use. Nothing was
  run while writing it.
- Installing Testcontainers, Awaitility or a container runtime is the user's step, in their own terminal;
  this block names them and stops.

## Origin
Rewritten from the Spring Boot testing and Testcontainers pages, the Spring Framework context-caching page,
the Testcontainers for Java documentation (MIT), the Awaitility usage page and the `java.time.Clock` API page
(read 2026-10-08). 🟡: never run by us; meant to be folded into the same-topic block (`spring-boot-conventions`
tests reference, and `java-conventions` for the Java parts) when PR 118 lands; open points are in
[`references/origin.md`](./references/origin.md).
