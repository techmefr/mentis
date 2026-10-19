---
name: terraform-state-and-secrets-pitfalls
description: "Use when Terraform or OpenTofu state, a backend or a secret handled by a configuration is written or reviewed: what state holds and who can read it, the remote backend baseline (S3 encryption and locking, a bootstrap root, no credentials in HCL), locks and force-unlock, migrating state between backends (migrate-state versus reconfigure), and secrets in state (sensitive only masks, ephemeral and write-only arguments, data sources and random_password, nonsensitive, rotation)."
---

# terraform-state-and-secrets-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the state file and what flows into it. The three sections share one
premise: **state is the record of live resource identity and often holds secrets, so whoever can read it can read
the secrets, and a backend mistake is invisible until a plan wants to destroy or recreate everything**. Address
changes and refactors are in `terraform-refactor-identity-pitfalls`; the pipeline that runs plan and apply is in
`terraform-ci-delivery-pitfalls`; the response after a secret has already leaked (history, revocation order) is in
`secret-leak-response-pitfalls`. Examples use Terraform syntax and the S3 backend because that is where the
sources were read; the mechanisms hold for OpenTofu, but the version floors below are stated for Terraform only.

## When
- Choosing or changing a backend, or writing the bootstrap that creates the state bucket.
- A configuration passes a password, key or token to a resource, or reads one from a secret store.
- A plan or an apply fails on a lock, or someone proposes `force-unlock`.
- State is being moved between backends, or a backend change makes the state look empty.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | State and backend: who can read it, the baseline, S3 encryption and locking, locks | a backend is written, hardened or debugged, or a lock is held | [`01-state-and-backend.md`](./references/01-state-and-backend.md) |
| 2 | Secrets in state: what keeps a value out, what does not, nonsensitive, rotation | a secret reaches a resource, an output or a plan | [`02-secrets-in-state.md`](./references/02-secrets-in-state.md) |
| 3 | Backend migration: migrate-state versus reconfigure, guardrails, moving and restoring state | state changes backend or must be restored | [`03-backend-migration.md`](./references/03-backend-migration.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: `state list` was compared before and after a migration and a
no-op plan followed (§3), the secret field was searched for in the state and the plan JSON after an apply (§2),
the lock holder was identified before any unlock (§1.4), and the backend credentials were absent from the
checked-in HCL (§1.2). A backend that was only read in review is not verified.

## Guardrails
- Never treat `sensitive = true` as keeping a value out of state (§2.1).
- Never pair a write-only argument with a data source that reads the same secret and call it excluded from state (§2.2).
- Never use `nonsensitive()` on a value that might be a secret to silence a plan (§2.2).
- Never put the backend bucket in the root that uses it as its active backend (§1.2).
- Never commit backend credentials or a state file (§1.1, §1.2).
- Never `force-unlock` without identifying the holder, and never from automation (§1.4).
- Never combine a backend migration with resource changes, and never delete the old backend straight after (§3.2).
- Never answer a secret in state with masking: rotate it (§2.3).
- This block states Terraform behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official Terraform and OpenTofu documentation was not read,
  so check every version floor against the runtime in use. Nothing was run while writing it.

## Origin
Rewritten from terrashark (MIT, backend state safety and secret exposure references) and terraform-skill by
Babenko (Apache-2.0, state management, security and code patterns references), read 2026-10-15. 🟡: never run by
us; open points are in [`references/origin.md`](./references/origin.md).
