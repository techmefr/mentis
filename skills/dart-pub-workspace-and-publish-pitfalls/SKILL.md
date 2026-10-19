---
name: dart-pub-workspace-and-publish-pitfalls
description: "Use when setting up a Dart or Flutter monorepo with pub workspaces or Melos, or publishing a package to pub.dev: shared resolution, stray lock files, workspace-local dependencies, overrides, tag-triggered publishing with short-lived credentials, tag patterns per package, environments, dry runs, retraction and security advisories."
---

# dart-pub-workspace-and-publish-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for Dart packages that live together or ship to pub.dev. The premise:
**a monorepo with one lock file per package drifts into several versions of the same dependency, and a
publish step that anyone with push access can trigger ships a version nobody reviewed.** Flutter conventions are
`flutter-conventions`; the general CI hardening rules are `ci-workflow-hardening`; Flutter release tooling is
`flutter-release-toolchain-hygiene`.

## When
- Several Dart or Flutter packages share a repository, or a workspace is being added to one that has them.
- Melos is proposed or already used on top of a workspace.
- A package is published to pub.dev, a publish workflow is added, or a security advisory shows up at resolution.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Workspaces and Melos: single resolution, members, stray files, local interdependencies, overrides, running commands | a workspace is created, migrated or debugged | [`01-workspaces-and-melos.md`](./references/01-workspaces-and-melos.md) |
| 2 | Publishing and advisories: tag-triggered publish, tag patterns, environments, tag protection, dry run, retraction, advisories | a publish workflow, a first publish or an advisory is handled | [`02-publishing-and-advisories.md`](./references/02-publishing-and-advisories.md) |

## Output / checkpoint
A workspace change shows the root pubspec, the resolution entry in every member and the single lock file that
results. A publish change names the tag pattern on pub.dev, the matching trigger in the workflow, who can push
that tag and whether an environment gate is on. "Publishing is automated" without saying who can trigger it is
not verified.

## Guardrails
- Never leave stray lock files or package configurations next to workspace members after a migration (part 1).
- Never publish a package's first version from automation; the first version is published by hand (part 2).
- Never store an exported service-account key where short-lived federated credentials work (part 2).
- Never ignore a security advisory without reading it (part 2).
- No block and no agent installs a tool or publishes a package: the blocks name the command and the user runs it
  (`CONVENTIONS.md`).
- Versions: pub features have minimum SDK versions stated in part 1; the documentation page changes.
  Nothing was run while writing this block.

## Origin
Rewritten from the Dart website's pub documentation (CC BY 4.0 for prose, BSD-3-Clause for code samples:
workspaces, automated publishing, publishing and security advisories pages) and the Melos documentation
(Apache-2.0, getting-started page), read 2026-10-16. Overlaps with `skills/flutter-conventions` (2026-10-19); cross-referenced, not merged. 🟡: never run by us; open points
are in [`references/origin.md`](./references/origin.md).
