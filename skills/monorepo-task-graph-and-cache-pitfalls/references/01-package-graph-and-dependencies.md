# monorepo-task-graph-and-cache-pitfalls §1 — Package graph and dependencies

Sources: the `monorepo-management` skill of wshobson/agents at 0874a27, read 2026-10-20 (its best-practices and common-pitfalls lists). Most points below are our own guidance and are labelled; the source supplied the topics, not the mechanisms.

## 1.1 Phantom dependencies
1. **A phantom dependency is an import that works because another package installed the module,** not because this package declares it. The source lists it as a common pitfall. Symptom: it builds locally and in a warm CI, and fails after a clean install or when the neighbour drops the module.
2. **Declare every import in the package that makes it,** including development-only tools used by a package's scripts (own guidance).
3. **Prefer a package manager mode that isolates each package's modules** so an undeclared import fails at once instead of months later (own guidance for the general point; pnpm's page states only that a package sees the dependencies declared in its own manifest, and does not discuss phantom dependencies by name; re-read your manager's current default).
4. **Reference sibling packages through the workspace's own protocol,** not a published version number, so the local code is used and a version bump does not decouple it silently (own guidance).
5. **Check with a clean install and a build of one package alone** (own guidance); both must pass without the others' modules.

## 1.2 Cycles and boundaries
1. **The package graph must be acyclic.** The source names circular dependencies as a pitfall. A cycle makes build order undefined and breaks "build my dependencies first".
2. **Break a cycle by moving the shared part into a third package** that both depend on, or by inverting the dependency through an interface (own guidance). Do not break it with a lazy import that hides it.
3. **Do not share code that is not shared yet.** The source warns about both over-sharing and under-sharing. Share after the second real user, not before (own guidance); a package that every other package depends on is expensive to change and invalidates every cache when it does.
4. **Enforce boundaries with a rule, not a convention** (own guidance): applications depend on libraries, libraries do not depend on applications, and a lint or graph check fails the build when that is violated.
5. **Keep package entry points explicit,** one public entry per package, so that deep imports into another package's internals are visible in review (own guidance).

## 1.3 Shared configuration
1. **Centralize lint, formatting and compiler settings** in one config package or root file that others extend, as the source recommends, so a rule change is one commit.
2. **A shared config is an input of every task that uses it.** Declare it as such (§2.1); otherwise changing a lint rule leaves lint results cached.
3. **Share types between a client and its server in a types package** rather than by copying (the source's recommendation), with the generator or schema as the single source.
4. **Lock versions across the workspace** for common tools and libraries, so that two packages do not build with different compilers by accident.

## 1.4 Versioning and release
1. **Use a change-record tool for versioning** (the source names the changesets approach) so that each change states which packages bump, and the bump is reviewed with the code.
2. **Private packages need no version discipline; published ones do.** Mark which are which, and never publish from a package that has a workspace-protocol dependency unrewritten (pnpm workspaces documentation, read 2026-10-20: the workspace protocol refuses to resolve to anything but a local package, and packing or publishing replaces it with the target's real version or range; other managers differ, re-read yours).
3. **Document each package in a short readme** (the source says so): what it is for, who may depend on it.

## 1.5 Checks (own guidance)
1. Draw or print the package graph; it has no cycle and no arrow from a library to an application.
2. A clean install and a single-package build pass.
3. Every import in the changed package resolves to a declared dependency, including the scripts' tools.
