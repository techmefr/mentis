---
name: production-readiness-review
description: "Use when a service or feature is about to take real traffic for the first time, or a launch checklist is being written or reviewed: pick the level from how much failure would cost, check each area with evidence rather than assertion, have someone outside the team review it, and record what is accepted as open."
---

# production-readiness-review

A method for deciding, before launch, whether a service can be operated by someone who did not build it. The
usual failures: a checklist ticked from memory, the same bar for a prototype and a payment path, an alert that
pages nobody, a rollback never tried, and a review that happens after the date was promised. The block owns no
checklist tool and no platform, and names none. It ties together blocks that each cover one area:
`skills/slo-design` (the objective), `skills/observability-instrumentation` (what can be seen),
`skills/load-and-capacity-testing-pitfalls` (the headroom), `skills/backup-restore-drill-pitfalls` (recovery),
`skills/chaos-experiment` (failure behaviour), `skills/feature-flag-lifecycle` (a safe ramp),
`skills/threat-modeling-lite` and `skills/security-hardening` (security), `skills/ship` (the release step). It
does not repeat them; it asks whether each was done, and who can show it.

## When
- A new service, a first customer-facing release or a move to a new platform is planned.
- A launch date is set and nobody has listed what "ready" means.
- An existing checklist is audited because an incident showed something it did not ask.
- A service changes tier (an internal tool becomes customer-facing, or handles payments or personal data).

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Choosing the level from the cost of failure, and what a check counts as | a review is scoped or a checklist is written | [`01-level-and-evidence.md`](./references/01-level-and-evidence.md) |
| 2 | The areas to check: delivery, observability, reliability, security, data, ownership | the checklist is being filled in or reviewed | [`02-areas-to-check.md`](./references/02-areas-to-check.md) |
| 3 | Running the review: who, in what order, what a pass means, follow-ups and re-review | a review is organised, held or closed | [`03-running-the-review.md`](./references/03-running-the-review.md) |

## Output / checkpoint
No pipeline checkpoint. A readiness record per service: the chosen level and why, each check with its evidence
(a link, a result, a screenshot) or a written reason it does not apply, the open items with an owner, a date and
who accepted the risk, the reviewer's name and the date, and the trigger for the next review.

## Guardrails
- Choose the level before opening the checklist, from the cost of failure. Never pick it from how much of the
  list is already done.
- Require evidence for each check. Never accept "yes" as a pass; a check without evidence is open.
- Explain every check marked not applicable. Never drop an item silently.
- Have a reviewer outside the build team, with the right to say no. Never let the author sign their own
  readiness.
- Record accepted risks with a name and a date. Never carry an open item into production without the person who
  owns the risk saying so in writing.
- The block never deploys, rolls back or changes configuration itself; the owner of the service acts.

## Origin
A production-readiness checklist repository (MIT) and a hosted-platform guide on continuous validation
(CC BY 4.0), plus the Kubernetes production-readiness review process (Apache-2.0), all read 2026-10-20 and restated, plus own guidance flagged in the references. Provenance, what was
removed and not verified: [`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
