# runbook-writing-and-maintenance-pitfalls: origin and source stamps

> Provenance of `skills/runbook-writing-and-maintenance-pitfalls`. Read it when a rule has to be traced to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No runbook was written, executed or audited with this block. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| PagerDuty/incident-response-docs at commit 464fc9d (`docs/oncall/alerting_principles.md`, `docs/oncall/being_oncall.md`, `docs/crisis/operations.md`) | Apache-2.0 (`LICENSE` read 2026-10-20) | An alert needs context and either steps or a runbook link; an untested alert is as good as none; test threshold, no-data and auto-resolve; runbook links belong on the service; on-call writes down hard-to-find information; backup person and stated escalation timeout |
| PagerDuty/incident-response-docs at commit 464fc9d, files re-fetched raw and re-read 2026-10-20 (same files; `LICENSE` Apache License 2.0, Copyright 2016 PagerDuty, Inc.) | Apache-2.0 | Alert definition and four-level priority scheme, alert content rules, runbook-or-steps rule, testing of threshold, no data and auto-resolve, escalation and backup shifts, handover summary, writing down hard-to-find information, runbook links attached to the service (§1.3.5, §2.2.5) |
| prometheus/docs (`docs/practices/alerting.md`, `LICENSE` Apache-2.0 read) and prometheus/prometheus at commit d10622d (`docs/configuration/alerting_rules.md`, `docs/configuration/unit_testing_rules.md`, `LICENSE` Apache-2.0 read), read 2026-10-20 | Apache-2.0 | No pages without an action, link alerts to consoles, annotations for runbook links and templating, pending delay, keep-firing clause against flapping and missing-data resolutions, rule unit tests (§1.3.5, §1.3.6, §2.1.1, §2.1.5, §2.3.7) |
| Google Cloud Architecture Framework, operational excellence, managing incidents and problems, <https://cloud.google.com/architecture/framework/operational-excellence/manage-incidents-and-problems>, read 2026-10-20 | Page footer states CC BY 4.0 for content, Apache-2.0 for code samples | Incident runbook content per stage, tools, contacts, regular review (§1.4.1b) |
| MicrosoftDocs/architecture-center at commit 8efa267 (AKS baseline backup note; ransomware-resilient backup architecture) | CC BY 4.0 (`LICENSE` read 2026-10-20) | Define recovery in a team runbook and practise it; runbooks, templates and approval flows make recovery repeatable; runbooks degrade as the environment changes |

## Own craft, not from a source
The tired-reader design, page structure, step form, expected results and branches, danger marking, copy-outside-the-failure, ownership, review triggers, executing as the test and its rules, stale-step detection techniques, inventory and retirement, and the checkpoint.

## Removed
Alert design (`skills/slo-design`, `skills/prometheus-rules-and-promql-pitfalls`), incident roles and communication (`skills/incident-comms-pitfalls`), the review (`skills/blameless-incident-review-pitfalls`), restore drills (`skills/backup-restore-drill-pitfalls`), runbook-automation products. Google's SRE books were not opened (CC BY-NC-ND); the Azure repository's other runbook mentions (certificate automation, hybrid monitoring) are about the Azure Automation product and were not used.

## Not verified
1. **Most of the block is own craft**; the two sources only cover alert content, testing alerts, practising recovery and degradation of runbooks. No external claim about reader behaviour was checked.
2. **Source facts were read from repository files at the commits above**, not the live published pages; wording there may have moved. Re-read before relying. Second pass 2026-10-20: every cited claim re-checked in the raw files (PagerDuty three files, the Azure ransomware article and the AKS baseline file where the team-runbook sentence actually sits, the hybrid AKS file only mentions an automation product); 8 points added or credited, 1 attribution made precise (the degradation sentence is in the ransomware article, not the AKS baseline), 0 deleted.
3. **No numbers** (cadences, timeouts, run times) are given as advice; PagerDuty's escalation timeout is described but not quoted.
4. **Stale-step detection techniques** are recalled practice, not tested on a real inventory.
5. **Written by us:** the output/checkpoint paragraph and the guardrails.

## Related blocks
`documentation-craft-pitfalls`, `production-readiness-review`, `backup-restore-drill-pitfalls`, `incident-comms-pitfalls`, `blameless-incident-review-pitfalls`, `slo-design`, `chaos-experiment`.

Independent verification 2026-10-21: 19 checked, 19 matched, 0 corrected, 0 unverified
