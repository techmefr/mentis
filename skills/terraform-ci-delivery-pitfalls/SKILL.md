---
name: terraform-ci-delivery-pitfalls
description: "Use when a Terraform or OpenTofu pipeline is written or reviewed: apply consuming the exact reviewed plan file instead of re-planning, plan files and JSON exports as sensitive artifacts, plan and apply on different events, policy checks on every path to apply, init without a backend for validate jobs, cloud authentication by OIDC and its trust conditions, protected environments, concurrency and lock timeouts, and drift detection that alerts instead of applying."
---

# terraform-ci-delivery-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the job that runs `plan` and `apply`. The three sections share one
premise: **what a person reviewed must be exactly what runs, the artifacts that carry it are as sensitive as the
state, and the pipeline's own mistakes look like Terraform's**. Pinning actions, token permissions, untrusted
triggers and the required-check aggregator are in `ci-workflow-hardening`; generic pipeline reproducibility is in
`devops-conventions`; state, locks and secrets are in `terraform-state-and-secrets-pitfalls`. Examples are GitLab CI
and GitHub Actions because that is where the sources were read.

## When
- Writing or reviewing a workflow that runs `terraform plan` and `terraform apply` (or `tofu`).
- A pipeline applies on merge, on a manual job or from a pull request comment.
- The CI plan differs from the one run locally, or two runs touch the same state.
- Cloud credentials for the pipeline are chosen, or a trust policy for OIDC is written.
- Drift detection is set up.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Plan and apply: the saved plan, plan artifacts as secrets, different events | the apply job is written, or an artifact leaves the plan job | [`01-plan-and-apply.md`](./references/01-plan-and-apply.md) |
| 2 | Pipeline gates: stages, policy, protected environments, OIDC trust, concurrency | a stage, a gate, the cloud login or the locking is chosen | [`02-pipeline-gates.md`](./references/02-pipeline-gates.md) |
| 3 | Drift and reproducibility: why CI and local plans differ, scheduled drift checks | a plan differs by environment, or drift detection is added | [`03-drift-and-reproducibility.md`](./references/03-drift-and-reproducibility.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the apply job's log shows it applying the stored plan file and no
planning command in it (§1.1), the artifact's retention and access were read in the CI settings (§1.2), a change that
violates the policy was pushed on a branch and the policy stage failed before any apply (§2.1), a second run was
started while the first held the lock and waited (§2.3), and a deliberate out-of-band change produced the drift
alert and no apply (§3.2). A pipeline that was only linted is not verified.

## Guardrails
- Never run a fresh planning command in the job that applies (§1.1).
- Never write a claim about what happens when state changed between plan and apply: the sources do not say (§1.1).
- Never leave a plan file or plan JSON in a broadly readable artifact, log or comment, or with long retention (§1.2).
- Never reach `apply` on a path that skips the policy stage (§2.1).
- Never use static cloud keys where OIDC is available, and never relax `sub` to fix an `aud` mismatch (§2.2).
- Never cancel an in-progress apply to start another (§2.3).
- Never auto-apply on a schedule to "fix" drift (§3.2).
- This block states pipeline behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The Terraform, GitHub and GitLab documentation was not read.
  Nothing was run while writing it.

## Origin
Rewritten from terrashark (MIT, CI drift and CI delivery references) and terraform-skill by Babenko (Apache-2.0,
CI/CD workflows, state management and security references), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
