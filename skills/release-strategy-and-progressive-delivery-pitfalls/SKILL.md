---
name: release-strategy-and-progressive-delivery-pitfalls
description: "Use when choosing or reviewing how a web service, application or static site reaches production: branching model, merge-to-release path, progressive rollout (rings, canary, blue-green, stamps), rollback, and schema changes that must survive a rollback: long-lived branches that hide integration pain, a rollout whose abort rule is a feeling, a rollback that the database makes impossible, and a new version validated by nothing but its own health check. Mobile store releases are mobile-release; flag life cycle is feature-flag-lifecycle."
---

# release-strategy-and-progressive-delivery-pitfalls

How a change travels from a merged commit to every user, and how it travels back. The failures are quiet: a branch
that lives for weeks and merges as a surprise, a canary that has no stated condition for stopping, a rollback
that works for the code and fails on the data, and "healthy" meaning only that the process started. The premise is
that **a release strategy is the set of decisions made before the release, not the steps run during it**: what
exposes first, what is measured, who may stop it, and what undoes it.

The block owns no pipeline product, orchestrator or traffic router. Mobile store releases are
`skills/mobile-release`; the life of a flag is `skills/feature-flag-lifecycle`; abort signals are
`skills/slo-design` §3 and `skills/observability-instrumentation`; the go-live gate is
`skills/production-readiness-review`; cutting a package release is `skills/package-release`; the migration of a
schema is `skills/deprecation-migration` and the migration blocks of each stack.

## When
- A team picks or changes a branching model, or a branch has lived long enough to hurt.
- A rollout plan (canary, rings, blue-green, per-tenant) is written or reviewed.
- A release needs a rollback that is proven, not assumed, especially with a schema change in it.
- An incident review finds that the release itself, not the code, was the failure.

**Skip when** the project has one exposure unit (one site, one environment, no tenants, no stored data of its own): rings, canary, blue-green and the data steps of §3 do not apply, say "not applicable: reason" for them rather than invent a finding, and read instead §1.9, §2.10 and §3.9 to §3.11, which hold the minimum for a single-environment deploy.

## Steps

**Read only the part the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Branching and the path to release: short-lived branches, one artefact promoted, environment parity | a branching model or a merge-to-release path is chosen or reviewed | [`01-branching-and-the-release-path.md`](./references/01-branching-and-the-release-path.md) |
| 2 | Progressive exposure: rings, canary, blue-green, stamps, stop rules, what to measure | a rollout plan is written | [`02-progressive-exposure.md`](./references/02-progressive-exposure.md) |
| 3 | Rollback and data: what can be undone, compatible schema steps, the rehearsal | a release carries a schema or contract change, or rollback is claimed | [`03-rollback-and-data.md`](./references/03-rollback-and-data.md) |

## Output / checkpoint
For each release path: the branching rule in one sentence, the artefact that is built once and promoted, the
exposure sequence with who is in each stage and what is read before widening, the stop rule written as a
condition, the rollback procedure with its last rehearsal date, and for any data change the ordered compatible
steps. A staged rollout without a stop condition is not started; a single-environment deploy owes the minimum of §3.11 instead.

## Guardrails
- Merge small and often to the shared line, and keep branches short. Never let integration happen only at the end
  (§1.1, §1.2).
- Build once and promote the same artefact through every stage. Never rebuild per environment and call it the
  same release (§1.3).
- Write the stop rule as a measurable condition before the first user is exposed. Never decide it while watching
  the graph (§2.3).
- Prove rollback on a copy before relying on it. Never claim a rollback that has never run (§3.1).
- Split a breaking data change into steps that each work with the old and the new code. Never ship the schema and
  the code that needs it as one irreversible move (§3.2).
- Choose stage sizes, hold times and branch lifetimes from your own traffic and risk. Never copy another team's
  numbers.
- Nothing here was run; vendor documentation facts are marked "re-read before relying".

## Origin
Rewritten from the Azure Architecture Center articles on tenant update strategies and on blue-green deployment
(CC BY 4.0), the GitHub Actions concurrency page (CC BY 4.0) and the Argo Rollouts documentation (Apache-2.0), read 2026-10-20, plus own craft knowledge flagged in the references. Provenance, what was removed and
not verified: [`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
