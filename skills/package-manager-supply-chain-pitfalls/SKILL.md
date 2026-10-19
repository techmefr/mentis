---
name: package-manager-supply-chain-pitfalls
description: "Use when configuring or reviewing how a JavaScript project resolves, installs, updates, runs or publishes packages (npm, pnpm, npx, lockfiles, a private registry, a new dependency): git and exotic sources, lockfile injection, frozen installs, install scripts, trust policy, dependency confusion, evaluating a package, and publishing safely."
---

# package-manager-supply-chain-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the package-manager settings and habits that decide what code
lands on a machine before any review: where a dependency may come from, what the lockfile is trusted to
say, what runs at install time, and how a package is judged and published. `skills/security-hardening`
§4.3, §4.9 and §4.11 state the principles (a dependency is a decision, the lock file is the inventory, the
install step is code), `skills/ci-workflow-hardening` §3 owns the update cooldown for Dependabot and uv and
the audit of the lockfile, and `hooks/block-installs.sh` refuses agent-run installs; this block is the
package-manager layer under them. The worked ecosystem is npm and pnpm; every option name and version
number below is version-bound and dated in `references/origin.md`. Other ecosystems' package managers are
out of scope.

## When
A diff adds or changes an `.npmrc`, a `pnpm-workspace.yaml`, a lockfile, a CI install step, a package
`name` or registry configuration, a publish workflow, or a new dependency, or when someone proposes running
a package with `npx` or `dlx`. Also after a published incident involving a package you use.

## Steps

**Read only the section the change touches.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Resolve and install: git sources, lockfile, frozen installs, updates, scripts, trust policy, cooldown, `npx` | an install configuration, a CI install step or an update policy changes | [`01-resolve-and-install.md`](./references/01-resolve-and-install.md) |
| 2 | Names, evaluation and publishing: dependency confusion, inspecting a package, evaluating a dependency, publisher settings, a compromise | a name, a registry, a new dependency, a publish workflow or an incident is in play | [`02-names-evaluation-publishing.md`](./references/02-names-evaluation-publishing.md) |

## Output / checkpoint
For each project in the diff: whether git and tarball sources are blocked and for which depth of the tree,
how the lockfile is validated and which install command CI runs, what install-time code is allowed and
by name, the trust and cooldown settings with the version of the package manager that supports them,
how internal names are scoped and routed, and for a new dependency the evaluation record of §2.3. Evidence
is the installed package manager's own documentation for each option used.

## Guardrails
- Never set an option from memory: confirm it exists in the installed package manager's version
  (`references/origin.md`).
- Never commit a registry token to an `.npmrc` (§2.1).
- Never install a package to inspect it; fetch and read its archive (§2.2).
- Never run `npx` or `dlx` on an unpinned package name in an unsupervised context (§1.9).
- Never merge a lockfile change that moves a `resolved` host or adds a dependency nobody asked for (§1.3).
- An agent does not install packages; the install is a human act with a named reason
  (`skills/security-hardening` §4.11).

## Origin
Rewritten from the Awesome npm Security Best Practices list by Liran Tal (Apache-2.0), the NPM Security
Best Practices repository by boda (MIT) and the Concise Guide for Evaluating Open Source Software by the
OpenSSF Best Practices Working Group (CC-BY-4.0, credited in the origin file), read 2026-10-15. The full
provenance, the version stamps, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
