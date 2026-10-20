# monorepo-task-graph-and-cache-pitfalls: origin and source stamps

> Provenance of `skills/monorepo-task-graph-and-cache-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files and our own experience, never run by us against a
repository: no orchestrator, package manager or build was executed while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| wshobson/agents at commit 0874a27: `plugins/developer-essentials/skills/turborepo-caching/SKILL.md`, `monorepo-management/SKILL.md` (best practices and pitfalls lists) | MIT, Copyright (c) 2024 Seth Hobson (`LICENSE` read 2026-10-20). The repository aggregates skills; these two files carry no separate licence notice and were treated as covered by it | Task concepts (dependencies, outputs, inputs, environment, long-running), global inputs, public-prefix variables as inputs, affected filter in CI, remote-cache token as a secret, pitfalls list (cycles, phantom dependencies, wrong cache inputs, over- and under-sharing), change-record versioning |

## Removed (stated in the sources, not carried)
- Every configuration and workflow sample, the self-hosted server code, the directory layouts and package-manager command lines.
- The Nx workspace skill (`nx-workspace-patterns`): its files were listed, not read, and nothing here is credited to it.
- Hosted-service login and linking steps.
- The source's version numbers of tools and runtimes.

## Not verified
1. **Key names.** The source's example uses an older name for the task map of its tool; the current name, strict-environment behaviour and flag names were not checked. Re-read before relying on any key or flag.
2. **Official documentation** of Turborepo, Nx, pnpm and Bazel was not opened; the review file marked their licences as not checked. All mechanism statements beyond the source's lists are own guidance.
3. **Own guidance, labelled in the text:** the isolation and workspace-protocol points, boundary enforcement, shallow-clone behaviour, cross-machine cache validity, the Makefile section, every "Checks" section.
4. **No command, flag or configuration key was executed.**

## Related blocks
`package-manager-supply-chain-pitfalls`, `vite-bundler-conventions`, `ci-workflow-hardening`,
`cpp-build-and-lifetime-pitfalls`, `dart-pub-workspace-and-publish-pitfalls`, `source-freshness`.
