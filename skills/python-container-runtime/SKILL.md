---
name: python-container-runtime
description: "Use when a Python service is packaged or started in a container: a Dockerfile for a Python app built with uv (multi-stage, dependency layer before source, lockfile install, bytecode, non-root user, no dev dependencies, a host virtual environment leaking into the image, interpreter path matching between stages) and how the process starts (exec-form command so the termination signal reaches the app, dev server versus production server, one process per container versus worker processes, proxy headers)."
---

# python-container-runtime

Step 6 of the pipeline (`WORKFLOW.md`), for the layer between the code and the machine: the image that
carries a Python service and the command that starts it. The two sections share one premise: **the image is
built from the lockfile and nothing else, and the process that runs in it is the one that receives the
orchestrator's stop signal**. It is the Python counterpart of `node-container-runtime`; image policy and
scanning beyond the points here are in `devops-conventions` and `security-hardening`.

## When
- Writing or reviewing a Dockerfile or compose service for a Python service.
- An image ships development dependencies, is much larger than it should be, or starts with
  "no such file" on the interpreter.
- `docker stop` takes the full grace period, or shutdown code in the app never runs.
- Choosing how many worker processes a container runs.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Image build: multi-stage, dependency layer, lockfile, bytecode, non-root, `.dockerignore`, interpreter match | a Dockerfile is written or reviewed; the image is large or fails to start | [`01-image-build.md`](./references/01-image-build.md) |
| 2 | Process start: exec form, dev versus production server, one process per container, proxy headers | a start command, a worker count or a shutdown behaviour changes | [`02-process-start.md`](./references/02-process-start.md) |

## Output / checkpoint
Each rule was exercised: the image was built from a clean checkout with no host virtual environment present,
the container ran as the non-root user, the dependency list inside it matched the lockfile without the
development group (§1), and `docker stop` returned well inside the grace period with the app's shutdown code
having run (§2). A Dockerfile that was only linted is not verified.

## Guardrails
- Never copy a host virtual environment into the image (§1.4).
- Never start the service through a shell string or a wrapper script that does not hand over the process
  (§2.1).
- Never ship the development server in a production image (§2.2).
- Never change the lockfile inside the build: the build fails if it is stale (§1.2).
- Facts here are as of the uv and FastAPI documentation read on the date in
  [`references/origin.md`](./references/origin.md); check an option against the versions in use. Nothing was
  built or run while writing this block.
- Installing uv or Docker plugins is the user's step; this block names them and stops.

## Origin
Rewritten from the uv Docker integration guide and the uv Docker example repository (MIT or Apache-2.0) and
the FastAPI deployment documentation (MIT), read 2026-10-08. This block is meant to be folded into the
same-topic container or deployment block when PR 118 lands. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
