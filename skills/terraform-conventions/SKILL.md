---
name: terraform-conventions
description: "Use when writing or reviewing Terraform or OpenTofu: file layout and naming, remote state and locking, resource identity and refactors, module contracts and version pinning, secrets in configuration and state, tests and the plan-review-apply pipeline. Names the failure mode first; the generic IaC principles stay in devops-conventions."
---

# terraform-conventions

Step 6 of the pipeline (`WORKFLOW.md`) on the infrastructure-as-code side. `devops-conventions` §2 holds the
principles that apply to every IaC tool (versioned declarative state, read the plan before an apply, secrets in
a vault, protected shared resources); this block holds what is specific to the Terraform language and its
state, and to OpenTofu, its compatible fork. Every rule holds in a repo with nothing installed
(`CONVENTIONS.md`, rule A).

**Special status.** New block, no in-house production experience: the content comes from the vendor's language
documentation and from two open, expert-maintained guides, read on 2026-10-02. A base to confront with the first
real configuration, not proven doctrine. **Many features exist only from a given runtime version** (§5.1); the
runtime and its exact version are the first thing to establish.

## When
A `.tf`, `.tfvars`, `.tftest.hcl` or lock file is written or changed, a state operation is planned, or a
pipeline that plans or applies infrastructure is built.

## Steps

1. **Capture the context before writing:** the runtime (Terraform or OpenTofu) and its exact version, the
   providers and their versions, the state backend, how a change reaches production (a person at a terminal, a
   pipeline, a hosted service), and how critical the environment is. State the assumption if it is not given.
2. **Name the failure mode the change risks,** because the rules are organised by what goes wrong: *identity
   churn* (addresses shift, resources are destroyed and recreated), *secret exposure* (values in state, plans,
   logs), *blast radius* (one state or one apply reaches too much), *drift between what was reviewed and what is
   applied*, *state damage*, *provider-upgrade breakage*, *untested modules*. Read the rows for the modes in play.
3. **Read the rows the task meets**, not the table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | File layout, naming, block and argument order | any configuration is written | [`01-structure-and-style.md`](./references/01-structure-and-style.md) |
| 2 | State, backends, locking, state operations | a backend is chosen or changed, state is split, moved or repaired | [`02-state-and-backends.md`](./references/02-state-and-backends.md) |
| 3 | Resource identity: repeat arguments, refactors, imports, removals, destroys | `count` or `for_each` is added or changed, a resource is renamed, moved, imported or removed, anything is destroyed | [`03-identity-and-refactoring.md`](./references/03-identity-and-refactoring.md) |
| 4 | Modules, composition, version constraints, the lock file | a module is written or called, a version is bumped | [`04-modules-and-versions.md`](./references/04-modules-and-versions.md) |
| 5 | Secrets, tests, the plan-review-apply pipeline | a secret appears in configuration, tests are written, CI is wired | [`05-secrets-tests-pipeline.md`](./references/05-secrets-tests-pipeline.md) |

## Output / checkpoint
Format and validate pass; the plan was read, and for a shared environment it is the saved plan that is applied
(§5.6); every destroy in the plan was expected (§3.8); the runtime floor of each feature used was checked (§5.1);
and the response states its assumptions (the context of step 1) and how to undo a state-changing step. Nothing
here writes a pipeline checkpoint.

## Guardrails
- Never apply or destroy on a shared environment without a reviewed plan and a human confirmation
  (`devops-conventions` §2, Guardrails).
- Never run a destroy, targeted or not, without first reading the destroy plan in full (§3.8).
- Never force-unlock a state or edit a state file by hand before finding out why it is locked or what is wrong (§2.6).
- Never put a secret in a variable default, a `.tfvars` file committed to version control, or an argument that is
  stored in state when a write-only form exists (§5.2).
- Do not recite a numeric default (a resource-count threshold for splitting state, a timeout) as a rule.
- No comments in the code produced; descriptions on variables and outputs are part of the contract, not comments.

## Origin
The vendor's Terraform language documentation and style guide, plus two open guides maintained by the
community (Apache-2.0), read 2026-10-02 and rewritten. Provenance, licences and the version stamps are in
[`references/origin.md`](./references/origin.md).
