---
name: testcontainers-node-pitfalls
description: "Use when Node or TypeScript tests start real services in containers with Testcontainers for Node (GenericContainer and its modules): reading the mapped host port and host instead of hard-coding them, choosing a wait strategy and a startup timeout so tests do not begin before the service is ready, copying files in instead of bind mounts, container names and networks, stopping, removal and the cleanup container, container reuse and the state it leaks, pull policy, and rootless or remote runtimes."
---

# testcontainers-node-pitfalls

A block for the plumbing under integration tests that start their own dependencies. The premise is the one in
`skills/jvm-test-infrastructure`: a test is only as good as the environment it ran in, and a real engine in a
container beats an embedded stand-in; this block is the Node counterpart, from the Testcontainers for Node
documentation read at the commit in `references/origin.md`. Names and defaults are version-bound: the cleanup
container's image tag, the reuse variable and the wait defaults change between releases, so re-read the
configuration page before a design depends on one. What the tests assert, mocks and polling are in
`skills/testing-anti-patterns`; the Java side is in `skills/jvm-test-infrastructure`.

## When
- A test starts a database, broker, cache or any service with `GenericContainer` or a module.
- A suite passes locally and fails on CI with a connection refused, a port clash, a mount that is empty or a
  container that is not ready.
- Containers are left running after a run, or tests influence each other through a shared container.
- The suite runs against a remote Docker daemon, Docker in Docker, Podman or a rootless runtime.

## Steps

**Read the part for the failure you see.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ports, readiness and wiring: mapped ports and host, wait strategies and timeouts, files in, names and networks | a test cannot reach the service, starts too early, or needs files or other containers | [`01-ports-readiness-wiring.md`](./references/01-ports-readiness-wiring.md) |
| 2 | Lifecycle: stopping, removal, the cleanup container, reuse, pull policy, rootless and remote runtimes, debugging | containers leak, tests share state, or CI differs from a laptop | [`02-lifecycle-reuse-runtimes.md`](./references/02-lifecycle-reuse-runtimes.md) |

## Output / checkpoint
For each container in the diff: which ports are exposed and where the test reads the mapped port and host, the
wait strategy and its timeout, how files get in, whether it is reused and what is cleaned between tests, and
which runtime the CI uses. Evidence is the suite run twice at the same time without a port clash, a container
list after the run showing nothing left from it, and a run on a pipeline runner that is not the laptop.

## Guardrails
- Never hard-code a host port or the host name; read both from the started container (point 1.1).
- Never replace a wait with a sleep; pick the strategy that tests readiness (point 1.3, point 1.4).
- Never mount a host path to give a container a file; copy it in (point 1.6).
- Never give a container a fixed name or a fixed host name to find it (point 1.7).
- Never turn off the cleanup container and automatic removal together (point 2.3).
- Never reuse a container without cleaning what a test wrote to it (point 2.4).
- Do not put a real credential or production data in a container image, environment or copied file.

## Origin
Rewritten from the Testcontainers for Node documentation (MIT), read 2026-10-16. The full provenance, library
settings that are version-bound, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
