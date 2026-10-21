---
name: runbook-writing-and-maintenance-pitfalls
description: "Use when a runbook is written, reviewed or audited for an alert, a recurring operation or a recovery: what the page must contain so a tired stranger can act, the first safe action, decision points, rollback and escalation, the link from the alert to the page, ownership and review triggers, testing a runbook by executing it, detecting stale steps, and retiring runbooks that no alert points at."
---

# runbook-writing-and-maintenance-pitfalls

Step 6 and step 10 of the pipeline (`WORKFLOW.md`), for the page somebody opens when a pager goes off. The premise: **a runbook is read once, under stress, by someone who did not write it and may not know the system; every sentence that needs the author's memory is a defect, and the page rots silently because nothing fails when a step goes stale**. Each rule gives the symptom, the check and the fix.

Already covered elsewhere, not repeated: general documentation craft and the short runbook rule in `skills/documentation-craft-pitfalls` §3; the production-readiness question "does every page have a runbook" in `skills/production-readiness-review`; the restore-drill runbook in `skills/backup-restore-drill-pitfalls`; customer messages in `skills/incident-comms-pitfalls`; the review after the incident in `skills/blameless-incident-review-pitfalls`; what makes an alert worth a page in `skills/slo-design`, `skills/prometheus-rules-and-promql-pitfalls` and `skills/datastore-broker-alerting-signals`; deliberate fault injection in `skills/chaos-experiment`. This block holds what those leave out: the page's content, its ownership and its testing.

## When
- A new alert is created and needs its page, or an alert fires and its page is not helping.
- An incident review says "the runbook was wrong or missing".
- A recurring operation (rotate a key, fail over, rebuild an index) is only known by one person.
- A runbook inventory is audited, or a service is handed to a new team.

**Skip when** the task is a one-off migration plan (write a plan, not a runbook) or an alert that should be deleted rather than documented; say so instead of writing a page for a bad alert.

## Steps

**Read the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The page: trigger, first safe action, steps, decision points, rollback, escalation, the three-in-the-morning reader | a runbook is being written or reviewed | [`01-content-and-reader.md`](./references/01-content-and-reader.md) |
| 2 | Alert link, ownership, review triggers, executing the runbook, stale-step detection, retirement | a runbook is about to be trusted, or an inventory is audited | [`02-ownership-testing-and-staleness.md`](./references/02-ownership-testing-and-staleness.md) |

## Output / checkpoint
A runbook is done when: the alert it serves links straight to it; its first block says what the symptom means and the first safe action; a stranger executed it end to end, in a non-production copy or a rehearsal, and the edits that came out of that run are merged; it names an owner, an escalation target and the date or trigger of its next check (§2). Record the last executed date on the page. No checkpoint file is written: a craft block, 🟡, nothing here was run on a real system by us.

## Guardrails
- Open with the symptom, its meaning and the first safe action, and put background after (§1.1). Never open with history or architecture that a reader must wade through before acting.
- Write each step as an action with an expected result and what to do when it differs (§1.2). Never write "check the database" with no command, no expected value and no branch.
- Mark steps that destroy, restart or cost money, and say how to undo them (§1.4). Never leave a destructive command in the middle of a list with no warning.
- Execute the runbook before it is needed and after each change to the system it covers (§2.3). Never count a page as ready because it was reviewed on screen.
- Give every runbook an owner and a review trigger, and every page-level alert a runbook (§2.1, §2.2). Never leave a link that points to a deleted or unowned page.
- Delete or merge a runbook no alert or operation reaches (§2.5). Never keep a stale page "just in case": a wrong page is worse than none.
- Facts quoted from sources are for the date in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with a few facts rewritten from the PagerDuty incident-response documentation (Apache-2.0), the Prometheus documentation (Apache-2.0), Microsoft Azure architecture-center articles (CC BY 4.0) and the Google Cloud Architecture Framework (CC BY 4.0), re-read from the source files 2026-10-20; no text copied. Open points in [`references/origin.md`](./references/origin.md).
