---
name: java-upgrade-and-maven-audit-pitfalls
description: "Use when upgrading a Java project between LTS releases or a Spring Boot major version, or auditing and changing Maven dependencies: removed JDK modules and internal APIs, javax to jakarta, add-opens flags, build-tool toolchain settings, outdated and vulnerable dependencies, tree conflicts, unused or undeclared dependencies, exclusions and pinned versions."
---

# java-upgrade-and-maven-audit-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for Java changes that touch the runtime version or the dependency set.
The premise: **a JDK or framework upgrade that compiles can still fail at run time on a removed module or a
closed internal API, and a dependency bump that Maven resolves silently can pick one side of a version conflict
for the whole application.** Code conventions are `java-conventions`; generic deprecation and migration
discipline is `deprecation-migration`; supply-chain rules for CI are `ci-workflow-hardening`.

## When
- A project moves to another JDK release, or Spring Boot or Hibernate moves a major version.
- A pom or a Gradle build changes its compiler release or toolchain.
- Dependencies are checked, bumped, excluded or pinned, or a security advisory arrives.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | JDK and framework upgrades: path, breaking changes, build settings, `javax` to `jakarta`, runtime flags, test tooling | the Java version or a framework major version changes | [`01-jdk-and-framework-upgrades.md`](./references/01-jdk-and-framework-upgrades.md) |
| 2 | Maven dependency audit: updates, tree conflicts, unused declarations, scans, pinning, exclusions, update policy | dependencies are audited, bumped or excluded | [`02-maven-dependency-audit.md`](./references/02-maven-dependency-audit.md) |

## Output / checkpoint
An upgrade names the source and target release, lists what was found by search (internal API use, `javax`
imports, security-manager use), says which runtime flags were added and why, and shows a green build and test run
on the target JDK. An audit lists security findings first, then major updates needing a changelog read, then
minor and patch updates, then conflicts and unused declarations. "Dependencies are up to date" without the command
that produced it is not verified.

## Guardrails
- Never skip an LTS release in one step when the source calls for the consecutive path (part 1).
- Never leave an `--add-opens` flag without naming the library that needs it (part 1).
- Never treat "omitted for conflict" in a dependency tree as resolved without checking which version won (part 2).
- Never run a bulk "update to latest" on a production project without a revert path (part 2).
- No block and no agent installs a tool or a dependency: the blocks name it and the user installs it
  (`CONVENTIONS.md`).
- Versions: the compatibility tables in the source are a snapshot; each rule names what it came from. Nothing was
  built or run while writing this block.

## Origin
Rewritten from two skills of the claude-code-java repository (MIT: the Java migration skill and the Maven
dependency audit skill), read 2026-10-16. Meant to be folded into the Java language block when the extended
language blocks (the unmerged PR 118) land; until then it stands alone. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
