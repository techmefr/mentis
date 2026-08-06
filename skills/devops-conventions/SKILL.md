---
name: devops-conventions
description: Use when writing/reviewing a CI/CD pipeline, infrastructure as code (Docker, Terraform, Ansible) or monitoring/alerting, conventions for reliability and reproducibility, not for application code. No dedicated Xefi production experience at this stage, sourced from established practice (12-factor, DORA metrics).
---

# devops-conventions

Step 6 of the pipeline (`WORKFLOW.md`) on the infra/CI side, complementing `portless-ready` (which
makes a stack portless): here, the reliability and reproducibility of the delivery pipeline itself.

## When
As soon as a CI/CD file (`.gitlab-ci.yml`, `Dockerfile`, `docker-compose.yml`), infrastructure as
code (Terraform, Ansible), or a monitoring/alerting config is written or modified.

## Steps

### 1. CI/CD: reproducible and quick to diagnose
1. Idempotent pipeline: replaying the same job on the same commit produces the same result, never
   dependent on unversioned mutable external state.
2. Every step fails fast and clearly (fail-fast): no step that continues silently after an error
   (`continue-on-error` only if explicitly wanted, never by default).
3. Secrets never hard-coded in the pipeline or logged in clear text: protected/masked variables on the
   CI side, never a forgotten debug `echo $SECRET`.
4. Explicit and versioned dependency cache (cache key tied to the lockfile), never a cache that hides
   a broken dependency.

### 2. Infrastructure as code
1. Versioned and declarative state (Terraform state, Ansible inventory): never a manual change to a
   resource managed by the IaC (silent drift on the next apply).
2. `plan`/`dry-run` always read before an `apply`/real execution on a shared environment: never a
   direct apply without reviewing the infra diff.
3. Infra secrets (keys, tokens) in a vault/secret manager, never committed in clear text even in a
   private repo.

### 3. Monitoring and alerting
1. An alert that fires must be actionable: otherwise it's noise that desensitises the team (alert
   fatigue), to be removed or reworded.
2. Structured logs (JSON or a parsable format), never free text alone for events that have to be
   queryable during an incident.
3. Healthcheck distinct from business monitoring: a service that's "up" (process alive) isn't the same
   as a service that's "healthy" (answers real requests correctly).

### 4. Incident response
1. Rollback always possible and tested before it's needed in an emergency; a rollback discovered
   broken during the incident makes the outage worse.
2. Post-mortem with no individual blame, focused on the systemic cause (what made the incident
   possible), not on who pressed what.

## Output / checkpoint
Pipeline/infra compliant with the sections above, `plan`/`dry-run` read and cited before any real
`apply` on a shared environment.

## Guardrails
- Never an automatic `apply`/deployment on a shared environment without explicit human confirmation
  (consistent with the framework's general doctrine: actions that are hard to undo stay a human
  checkpoint).
- This block has no dedicated Xefi production experience yet: to be confronted with the first real
  infra/CI audit, not to be treated as proven doctrine.

## Origin
Sourced from the 12-factor app (config through environment variables, logs as event streams), DORA
metrics (Accelerate: Forsgren/Humble/Kim: deployment frequency, lead time, MTTR, change failure rate)
and established GitOps/IaC practice. Mechanisms rewritten, no copied text. Market research, no
internal production feedback at this stage.
