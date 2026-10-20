---
name: monorepo-task-graph-and-cache-pitfalls
description: "Use when setting up or debugging a repository with several packages and a build orchestrator (pnpm workspaces with Turborepo or Nx, or a Makefile-style graph): task dependencies and outputs, cache keys and stale hits, undeclared environment variables, phantom dependencies, circular packages, affected-only runs in CI, shared configuration and remote caches."
---

# monorepo-task-graph-and-cache-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for repositories where one command builds, tests or lints many packages.
The premise: **the orchestrator is a cache over a dependency graph, and a cache is only as correct as the
declarations it is given**: a task that reads a file nobody declared hits a stale cache, an output nobody listed
is missing on a hit, a package that imports something it does not depend on works only on the machine that
happens to have it installed. Install and publish hygiene is in `package-manager-supply-chain-pitfalls`; Vite is in
`vite-bundler-conventions`; Dart workspaces are in `dart-pub-workspace-and-publish-pitfalls`; C++ builds are in
`cpp-build-and-lifetime-pitfalls`; the CI side is in `ci-workflow-hardening`.

## When
- A repository has several packages with a workspace file and an orchestrator configuration, or the request names Turborepo, Nx, pnpm workspaces or a build graph.
- A build passes locally and fails in CI, or passes in CI after "clean cache", or ships stale output.
- A package is added, split, merged or made to depend on another.
- CI should build and test only what a change affects.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Package graph, phantom dependencies, cycles, internal references, shared configuration, what to share | a package is created or depends on another, or an import fails on a clean machine | [`01-package-graph-and-dependencies.md`](./references/01-package-graph-and-dependencies.md) |
| 2 | Task graph, inputs, outputs, environment keys, stale or empty cache hits, affected runs, remote cache | a task is declared, a cache hit looks wrong, or CI is slow or wrong | [`02-tasks-cache-and-ci.md`](./references/02-tasks-cache-and-ci.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: every import is declared by the package
that makes it, the package graph has no cycle, every task lists its inputs, outputs and environment variables,
a clean checkout with an empty cache builds, and the affected-only run was compared with a full run once.

## Guardrails
- Declare a dependency in the package that imports it (§1.1). Never rely on a copy hoisted by a neighbour.
- Break a cycle by extracting the shared part, never by ignoring the warning (§1.2).
- List the outputs and the environment variables every task depends on (§2.1, §2.2). Never trust a cache hit for a task whose inputs are only guessed.
- Cache only deterministic tasks, and never cache the development server (§2.3).
- Keep a remote cache token in the CI secret store, and grant write to the main branch only (§2.5).
- Configuration key names and flags change between major versions of the tools; re-read the version in use before relying on one (🟡, nothing here was run).

## Origin
Rewritten from the `wshobson/agents` repository (MIT, commit 0874a27), the monorepo, Turborepo and Nx skills,
read 2026-10-20, plus our own guidance, labelled in the text. See [`references/origin.md`](./references/origin.md).
