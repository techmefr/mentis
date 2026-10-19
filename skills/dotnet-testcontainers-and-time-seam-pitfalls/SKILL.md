---
name: dotnet-testcontainers-and-time-seam-pitfalls
description: "Use when writing or reviewing .NET tests that start containers with Testcontainers, or tests of code that reads the clock, delays, reads files or uses randomness: random ports, container host name, resource mapping, Resource Reaper, pinned images, reuse, wait strategies, TimeProvider with FakeTimeProvider, scoped ambient overrides."
---

# dotnet-testcontainers-and-time-seam-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for .NET tests that need a real dependency or control over an ambient one.
The premise: **a test that names its container, binds a fixed port or waits on the wall clock passes alone and
fails in CI, on a colleague's machine or on the second run**; each of those is a decision that looks free when
written. Generic test smells are `testing-anti-patterns`; .NET code conventions are `dotnet-conventions`; the
build-file side of a test project is `dotnet-msbuild-and-nuget-publish-pitfalls`.

## When
- A test starts a container, a network or a volume through Testcontainers, or a fixture is shared between tests.
- Code under test calls the current time, a delay, a timer, the file system, the environment or a random source.
- A test sleeps, or its assertions are computed with the production code they check.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Testcontainers: names, ports, host name, mounts, reaper, image pin, readiness, reuse, fixture scope | a container is started from a test | [`01-testcontainers.md`](./references/01-testcontainers.md) |
| 2 | Time and ambient seams: TimeProvider, fake time, scoped overrides, minimal seams | production code reads time, delays, files, environment or randomness | [`02-time-and-ambient-seams.md`](./references/02-time-and-ambient-seams.md) |

## Output / checkpoint
Every container in the change has a random name and port, is reached through its host name property, has a pinned
image and a readiness wait that matches what the test needs. Every time-dependent test advances a fake clock and
asserts before and after the boundary. A claim that tests are "deterministic" without saying which clock, which
files and which ports they touch is not verified.

## Guardrails
- Never assign a static name or a static host port to a container, network or volume (part 1).
- Never disable the Resource Reaper on a machine that has no other cleanup (part 1).
- Never wait on wall-clock time in a test; advance a fake one (part 2).
- Never reset a scoped override to null on exit; restore the value that was active before it (part 2).
- No block and no agent installs a tool or a package: the blocks name it and the user installs it
  (`CONVENTIONS.md`).
- Versions: rules come from the Testcontainers for .NET documentation and the dotnet/skills repository at the
  commits stamped in `references/origin.md`. Nothing was run while writing this block.

## Origin
Rewritten from the Testcontainers for .NET documentation (MIT) and the dotnet/skills testability skill (MIT),
read 2026-10-16. Overlaps with `skills/dotnet-conventions` (2026-10-19); cross-referenced, not merged. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
