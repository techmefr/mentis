# production-readiness-review: origin and source stamps

> Provenance of `skills/production-readiness-review`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a published checklist repository, one open review process and own craft knowledge, never run
as a real review by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| mercari/production-readiness-checklist: README.md, docs/references/production-readiness-level.md, production-readiness-checklist.md, design-checklist.md (listing), pre-production-checklist.md, docs/guides/check-production-readiness.md (LICENSE file read: MIT, Copyright 2020 Mercari, Inc.; repository last pushed 2021-11-22) | MIT | Levels by criticality tied to the objective; design checklist then pre-production checklist; the areas and their individual checks; evidence per item; not-applicable explained; deploy to production without live users before the review; an independent reviewing team |
| MicrosoftDocs/architecture-center, page "Continuous validation with Azure Load Testing and Azure Chaos Studio" (LICENSE file read: Creative Commons Attribution 4.0 International; repository pushed 2026-10-20) | CC BY 4.0 | Load and fault validation in a production-like environment as part of delivery |
| kubernetes/enhancements, keps/sig-architecture/1194-prod-readiness/README.md (LICENSE read 2026-10-20) | Apache-2.0 | Why an outside review exists (operators' views missing), CI-enforced gate and named approver per stage, review tied to a release deadline, playbook creation as a criterion (§3.3, §3.5, §3.6, §3.10) |

Credit as the licences require: Kubernetes enhancements, Apache-2.0 (https://github.com/kubernetes/enhancements); Mercari production readiness checklist, MIT, Copyright 2020 Mercari, Inc. (https://github.com/mercari/production-readiness-checklist); Microsoft Azure Architecture Center, CC BY 4.0 (https://github.com/MicrosoftDocs/architecture-center). The text was rewritten, not reproduced; no endorsement by either author is implied.

## Removed
1. **Every threshold and figure**: the objective ranges per level, coverage, CPU and disk alert limits, recovery
   times and intervals, session counts and replication lag limits.
2. **All product and platform items**: the named monitoring, paging, profiling, error-tracking, container
   orchestrator and database services, and the service-specific database sections.
3. **The three-letter level names and emoji conventions**; levels are described, not labelled.
4. **The team names and review routing** of the source's organisation.

## Not verified
1. The source is one company's internal practice, published as a reference; the repository has not been updated
   since 2021-11-22 and its items may have aged. Check each area against current practice before relying.
2. §3 points on rehearsal, deciding authority between reviewer and owner, ordering by risk, the three-bucket
   sort, pilots and learning from incidents are own guidance; the reviewer's right to hold, the outside reviewer,
   timing and the record are now backed by one open project's process. The Swisscom questionnaire and the
   site-reliability handbook were not read (no licence file checked).
3. The area list in §2 is a restatement of a microservice checklist; its fit for monoliths, mobile or data
   products is our judgement.
4. No review was run in writing this block.

## Related blocks
`skills/slo-design`, `skills/observability-instrumentation`, `skills/load-and-capacity-testing-pitfalls`,
`skills/backup-restore-drill-pitfalls`, `skills/chaos-experiment`, `skills/feature-flag-lifecycle`,
`skills/threat-modeling-lite`, `skills/security-hardening`, `skills/ship`, `skills/documentation-craft-pitfalls`,
`skills/blameless-incident-review-pitfalls`, `skills/source-freshness`.
