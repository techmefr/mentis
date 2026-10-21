# monorepo-task-graph-and-cache-pitfalls: origin and source stamps

> Provenance of `skills/monorepo-task-graph-and-cache-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files and our own experience, never run by us against a
repository: no orchestrator, package manager or build was executed while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| wshobson/agents at commit 0874a27: `plugins/developer-essentials/skills/turborepo-caching/SKILL.md`, `monorepo-management/SKILL.md` (best practices and pitfalls lists) | MIT, Copyright (c) 2024 Seth Hobson (`LICENSE` read 2026-10-20). The repository aggregates skills; these two files carry no separate licence notice and were treated as covered by it | Task concepts (dependencies, outputs, inputs, environment, long-running), global inputs, public-prefix variables as inputs, affected filter in CI, remote-cache token as a secret, pitfalls list (cycles, phantom dependencies, wrong cache inputs, over- and under-sharing), change-record versioning |
| Turborepo documentation (turborepo.dev): configuration reference, run reference | product documentation, facts only, rewritten, read 2026-10-20 | Task map key, caret, outputs, inputs, env lists, strict default, affected mode and shallow clones, dry run and summary |
| pnpm documentation: workspaces | product documentation, facts only, rewritten, read 2026-10-20 | Workspace protocol resolution and rewrite on publish |

## Removed (stated in the sources, not carried)
- Every configuration and workflow sample, the self-hosted server code, the directory layouts and package-manager command lines.
- The Nx workspace skill (`nx-workspace-patterns`): its files were listed, not read, and nothing here is credited to it.
- Hosted-service login and linking steps.
- The source's version numbers of tools and runtimes.

## Not verified
1. **Key names.** Checked 2026-10-20 for the one tool: current task map key, strict default, affected and force flags. Not checked for other tools. No key or flag was executed.
2. **Official documentation** of Turborepo and pnpm was read for facts (above); Nx and Bazel were not opened. Mechanism statements not marked as checked are own guidance.
3. **Own guidance, labelled in the text:** the isolation and workspace-protocol points, boundary enforcement, shallow-clone behaviour, cross-machine cache validity, the Makefile section, every "Checks" section.
4. **No command, flag or configuration key was executed.**

## Related blocks
`package-manager-supply-chain-pitfalls`, `vite-bundler-conventions`, `ci-workflow-hardening`,
`cpp-build-and-lifetime-pitfalls`, `dart-pub-workspace-and-publish-pitfalls`, `source-freshness`.
