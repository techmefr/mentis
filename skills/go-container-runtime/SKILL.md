---
name: go-container-runtime
description: "Use when a Go service is packaged or tuned to run in a container: a Dockerfile or build script for a Go binary (static build, minimal base image, numeric non-root user, trimpath, version stamping, third-party licences), CPU and memory limits (GOMAXPROCS and the cgroup quota, GOMEMLIMIT, GOGC), and signal handling with graceful HTTP shutdown."
---

# go-container-runtime

Step 6 of the pipeline (`WORKFLOW.md`), for the layer between a Go binary and the machine: the image it ships
in, the CPU and memory limits it runs under, and how it stops. The premise: **the Go runtime sizes itself
from the machine unless told otherwise, so the image and the limit are one design, not two**. General Go
code rules are in `go-conventions`; image scanning and registry policy belong to `devops-conventions`; the
equivalent blocks for other stacks are `node-container-runtime` and `dotnet-container-runtime`.

## When
- Writing or reviewing a Dockerfile or a build script for a Go binary.
- A Go container is CPU-throttled, OOM-killed, or drops requests when it is stopped or redeployed.
- Changing `GOMAXPROCS`, `GOMEMLIMIT` or `GOGC`.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Image build: static binary, minimal base, numeric user, trimpath, linker flags, version stamp, licences | a Dockerfile or build script is written or reviewed | [`01-image-build.md`](./references/01-image-build.md) |
| 2 | CPU and memory: GOMAXPROCS and the cgroup quota (by Go version), GOMEMLIMIT, GOGC | a container is throttled, killed or slow, or a limit changes | [`02-cpu-memory.md`](./references/02-cpu-memory.md) |
| 3 | Shutdown: SIGTERM, graceful server stop, long-lived connections | a deploy drops requests, or a `main` is written or reviewed | [`03-shutdown.md`](./references/03-shutdown.md) |

## Output / checkpoint
The image was built and run: the binary started in the final image as the numeric user (§1), it printed the
stamped version, the container ran under its real CPU and memory limits with the Go version's behaviour
confirmed (§2), and a `SIGTERM` sent to the running container ended in-flight requests normally (§3). A
Dockerfile that was only linted is not verified.

## Guardrails
- Never run the container as root, and never name the user by a name the base image may not have (§1.3).
- Never set `GOMAXPROCS` to the host's CPU count by habit: a manual value switches the automatic behaviour
  off (§2.1).
- Never set a memory limit to the container's full limit (§2.2).
- Never leave a server without a shutdown deadline, nor exit `main` before `Shutdown` returns (§3.2).
- Versions: each rule names its Go version. Nothing was built or run while writing this block.

## Origin
Rewritten from a Go build template (Apache-2.0), the automatic-GOMAXPROCS library README (MIT), and the
Go garbage collector guide, release notes and package documentation (CC-BY-4.0 text), read 2026-10-08.
Meant to be folded into `go-conventions` when the extended version of that block lands. 🟡: never run by
us; open points are in [`references/origin.md`](./references/origin.md).
