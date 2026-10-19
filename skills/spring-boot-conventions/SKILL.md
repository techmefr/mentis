---
name: spring-boot-conventions
description: "Use when writing or reviewing a Spring Boot application: package layout and injection, typed configuration and profiles, error bodies and persistence settings, actuator exposure, shutdown, security filters and test slices."
paths: "**/*Application.java, **/application*.properties, **/application*.yaml, **/application*.yml, **/*Controller.java, **/*Config.java, **/*Configuration.java, **/*Properties.java, **/SecurityConfig*.java"
---

# spring-boot-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Spring Boot code, on top of
`skills/java-conventions` (the language and the persistence points that are not specific to Boot). Every rule
below holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). **Special status**: like
`go-conventions`, no in-house production experience sits behind this block yet. The content comes from the
reference documentation of Spring Boot (docs at 4.2.0-SNAPSHOT when read on 2026-10-02) and of Spring Security;
treat it as a base to confront with the first real Boot project, not as proven doctrine. A property or an
annotation that moved between major versions is flagged in the point; a project on an older line reads the
point as "check the release notes first".

## When
As soon as Spring Boot code is written or modified, during `code` (6) or `tdd` (5): a bean, a configuration
class, a property, a controller or its error handling, a security rule, an actuator setting, a test annotation.

## Steps

**Read only the sections the task touches.** One file per section under `references/`; a section read is a
section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Package layout, injection, typed configuration, profiles | a class is placed, a bean wired, a property read or an environment difference introduced | [`01-structure-config.md`](./references/01-structure-config.md) |
| 2 | Errors, persistence settings, shutdown | an error body, a JPA or datasource setting, or the stop of the service is touched | [`02-web-data-lifecycle.md`](./references/02-web-data-lifecycle.md) |
| 3 | Actuator, security filters, tests | an endpoint is exposed, a request matcher or CORS rule written, a test annotation chosen | [`03-actuator-security-tests.md`](./references/03-actuator-security-tests.md) |

## Output / checkpoint
Code compliant with the sections read; the build and the tests green; no new property read outside a typed
class; no actuator endpoint exposed beyond the ones the diff names. Checked by `gate` (7) and `review` (8).
Where the project cannot run its build (no environment), the checkpoint records it rather than reporting a pass,
and nothing is installed to make it run (`CONVENTIONS.md`: a block names a dependency and stops).

## Guardrails
No comments in the code produced. These rules govern **new** code; existing field injection or `@Value` reads
stay until touched. Never loosen a security rule, an exposure setting or a coverage threshold to get a diff
through. For the error body shape and idempotency, `skills/api-design`; for queues,
`skills/background-jobs-conventions`; for authentication and sessions, `skills/auth-session-conventions`.

## Origin
Rewritten from the Spring Boot and Spring Security reference documentation; the full provenance, licences and
the audit of what was left out are in [`references/origin.md`](./references/origin.md). Read it when checking a
rule's freshness, not when applying one.
