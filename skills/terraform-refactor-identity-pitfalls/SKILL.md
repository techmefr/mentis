---
name: terraform-refactor-identity-pitfalls
description: "Use when Terraform or OpenTofu resources are renamed, re-keyed, moved, adopted or dropped, or when a module is refactored: count versus for_each identity, for_each keys that must be known at plan time, moved blocks before the first apply, declarative import and removed blocks, targeted destroy, provider and runtime pinning with the lock file, a version floor table for newer features, and what terraform test with mocks does and does not prove."
---

# terraform-refactor-identity-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the address of a resource. The three sections share one premise:
**Terraform identifies a resource by its address, so any edit that changes an address is a destroy and a create
unless something says otherwise, and the plan that shows it looks like a small diff**. State, backends and secrets
are in `terraform-state-and-secrets-pitfalls`; the pipeline that runs the plan is in `terraform-ci-delivery-pitfalls`.
Examples are Terraform syntax; OpenTofu floors are given only where the sources state them.

## When
- A list or map that drives `count` or `for_each` gains, loses or reorders an element.
- A resource or module is renamed, moved into a module, or switched between `count` and `for_each`.
- An existing resource is adopted into Terraform, or a resource must leave management without being destroyed.
- A provider or runtime version moves, or a feature is used that depends on a recent release.
- A module is tested with `terraform test` and mocked providers.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Address identity: count versus for_each, keys known at plan time, targeted destroy | a collection is iterated or an element is added or removed | [`01-identity.md`](./references/01-identity.md) |
| 2 | Moves, imports and removals: moved, import, removed, provider removal | an address changes, or a resource is adopted or released | [`02-moves-imports-removals.md`](./references/02-moves-imports-removals.md) |
| 3 | Versions and tests: the floor table, pinning, the lock file, mocked tests | a version is chosen or bumped, or a module test is written | [`03-versions-and-tests.md`](./references/03-versions-and-tests.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a plan was read after the edit and showed moves, not replace
(§2), an adopted resource produced an empty plan (§2.2), an element was removed from the middle of a collection in
a scratch configuration and only that element changed (§1), and the target runtime was stated before any feature in
the floor table was used (§3.1). A configuration that was only formatted and validated is not verified.

## Guardrails
- Never iterate a long-lived collection with `count` (§1.1).
- Never derive `for_each` keys from attributes of another resource that are known only after apply (§1.2).
- Never rename, re-key or move a resource without a `moved` block in the same change (§2.1).
- Never apply an adoption whose plan is not empty (§2.2).
- Never remove a provider block while resources of that provider are still in state (§2.3).
- Never use a version-bound feature without stating the target runtime and a fallback below its floor (§3.1).
- Never ship a runtime or provider bump together with a functional change (§3.2).
- Never count a mocked-provider test as integration coverage (§3.3).
- This block states Terraform behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official Terraform and OpenTofu documentation was not read.
  Nothing was run while writing it.

## Origin
Rewritten from terrashark (MIT, identity churn and migration references), terraform-skill by Babenko (Apache-2.0,
code patterns, state management and testing references) and the Terramate agent skills (MIT, provider version
constraints rule), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
