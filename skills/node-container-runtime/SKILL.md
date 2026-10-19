---
name: node-container-runtime
description: "Use when a Node or NestJS service is packaged or configured to run: a Dockerfile for a Node app (multi-stage, non-root user, signals reaching node, PID 1, build secrets, memory limits and heap size), NODE_ENV and environment configuration (validated at startup, env files, loadEnvFile), and the choice between running TypeScript directly with Node type stripping or building it, including what a Nest app can and cannot do under type stripping and which tsconfig flags to set."
---

# node-container-runtime

Step 6 of the pipeline (`WORKFLOW.md`), for the layer between the code and the machine: the image that
carries a Node service, the configuration it reads at start, and the way its TypeScript becomes something
Node runs. The three sections share one premise: **the process must start the same way in a container as
on a laptop, receive the signals the orchestrator sends, and fail at boot, not at the first request, when
its configuration is wrong**. Graceful shutdown itself (draining requests, closing pools) is in
`nestjs-reliability` and `nestjs-node-conventions`; this block only makes sure the signal arrives.

## When
- Writing or reviewing a Dockerfile, a compose service or an image build for a Node service.
- A container is killed with exit 137 or restarts under load, or `docker stop` takes ten seconds.
- Adding or changing an environment variable, an env file, or a `NODE_ENV` branch.
- Deciding how TypeScript runs: Node directly, a bundler, `tsc`, SWC, or the Nest CLI.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Container image: multi-stage, non-root user, signals and PID 1, build secrets, memory and heap | a Dockerfile is written or reviewed; a container stops slowly or is OOM-killed | [`01-container-image.md`](./references/01-container-image.md) |
| 2 | Runtime configuration: NODE_ENV, validated env, env files, loadEnvFile | an env variable or a mode switch is added | [`02-runtime-config.md`](./references/02-runtime-config.md) |
| 3 | Running TypeScript: Node type stripping versus a build, Nest limits, tsconfig flags | the start command, the build or the tsconfig changes | [`03-typescript-execution.md`](./references/03-typescript-execution.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the image was built and `docker stop` returned in well
under the grace period (§1), the container ran as the non-root user and could not write outside its data
directory (§1), the service was started once with a required variable removed and refused to boot (§2), and
the start command was run exactly as the image runs it (§3). A Dockerfile that was only linted is not
verified.

## Guardrails
- Never put a secret in `ARG` or `ENV`: both persist in the image and its history (§1).
- Never start the app through a package manager script in the image's command: the signal stops at the
  wrapper (§1).
- Never set the heap limit to the container limit: the process needs memory outside the V8 heap (§1).
- Never gate security or correctness on `NODE_ENV` alone (§2.1).
- Never enable type stripping for a Nest app and expect decorators to work (§3.2).
- This block states Node facts as of the Node documentation read on the date below; Node moves quickly, so
  check the flag or version a rule names against the runtime in use before relying on it. Nothing was built
  or run while writing it.
- Image scanning, registry policy and runtime hardening beyond the points here belong to
  `devops-conventions` and `security-hardening`.

## Origin
Rewritten from the Node.js Docker image's best-practices document (MIT), the Docker build-secrets
documentation, the Node.js API documentation (main branch) and the maintained tsconfig base presets (MIT),
cross-checked against one MIT Node-practices note on environment handling (read 2026-10-08). 🟡: never run
by us; open points are in [`references/origin.md`](./references/origin.md).
