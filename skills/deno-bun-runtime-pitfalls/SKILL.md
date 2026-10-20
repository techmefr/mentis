---
name: deno-bun-runtime-pitfalls
description: "Use when writing, porting or reviewing a service or script that runs on Deno or Bun instead of Node: permission flags and least privilege, Node compatibility gaps, module resolution and lockfiles, built-in test and bundle tooling, native addons, production images, and how to check a port against the real runtime."
---

# deno-bun-runtime-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for code that looks like Node and is not Node. The premise: **the runtime
accepts the program and still behaves differently**: a Deno script runs with every permission because the
developer typed an allow-all flag, a Bun service passes its tests and fails in a Node-only library at the
first rare call, a lockfile is ignored in CI, an install script that Node's tooling would run is skipped. Node
packaging, containers and TypeScript execution are in `node-container-runtime`; supply-chain rules for installs
are in `package-manager-supply-chain-pitfalls`.

## When
- A project starts on Deno or Bun, or a Node project is ported to one of them.
- A script runs with permission flags, or a Dockerfile changes the runtime.
- A dependency is a native addon, a Node built-in heavy library, or a framework with deep Node assumptions.
- Tests pass locally and fail on the other runtime, or the reverse.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Permissions model, secrets and network scope, imports and lockfiles, tasks and workspaces | a script is started with flags, or dependencies and tasks are set up | [`01-permissions-imports-and-lockfiles.md`](./references/01-permissions-imports-and-lockfiles.md) |
| 2 | Node compatibility gaps, native code, built-in tools, performance claims, production and CI | a port, a native dependency, a benchmark claim or a deployment is the question | [`02-compatibility-tooling-and-production.md`](./references/02-compatibility-tooling-and-production.md) |

## Output / checkpoint
For a change touching this block: the run command lists the narrowest permissions the program needs (or the
Bun equivalent of limiting what runs), the lockfile is committed and enforced in CI, the full test suite ran on
the runtime that ships, and a compatibility claim rests on a run of the real dependency, not on a table.

## Guardrails
- Grant only what the program needs, scoped to paths and hosts (§1.1). Never use the allow-all flag outside a throwaway script.
- Commit the lockfile and install from it in CI (§1.3). Never resolve fresh versions in the pipeline.
- Test on the runtime that ships (§2.1). Never test on Node and deploy on another runtime.
- Treat a speed claim as a hypothesis until you measure your own workload (§2.4). Never choose a runtime on a headline benchmark.
- Runtime flags, command names and compatibility levels move with each release; re-read the documentation of the version in use (🟡, nothing here was run).

## Origin
Written from our own craft knowledge of Deno and Bun usage; behaviour is stated as general facts in our words. No
source text was taken. See [`references/origin.md`](./references/origin.md).
