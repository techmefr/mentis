---
name: gdpr-breach-notification-and-dpia-pitfalls
description: "Use when a personal data breach is suspected or confirmed, a breach-handling runbook is written or audited, or a feature or system is about to start processing personal data in a way that may need a data protection impact assessment: the awareness timestamp and the clock, what the authority notification and the communication to the people concerned must contain, the processor-to-controller hand-off, the breach register, the DPIA trigger check, its content, its consultation steps and its review, and what stays a question for the DPO or counsel."
---

# gdpr-breach-notification-and-dpia-pitfalls

A defensive block for two GDPR duties that engineering teams meet as an emergency or as a late surprise:
telling the authority and the people concerned about a breach (Articles 33 and 34), and assessing a risky
processing before it starts (Article 35, with the consultation step of Article 36 where the assessment says so).
The failures are mechanical: nobody recorded when the team became aware, the processor's message sat in a
mailbox, the notification waited for complete facts, the register was never written, the assessment was
started after launch, the DPO was never asked. The legal text read for this block is Regulation (EU) 2016/679
(the GDPR), Articles 33 to 36, as published in the Official Journal; it applies to that regulation only. Whether
an incident is a breach, whether it is likely to result in a risk or a high risk, and whether an exception
applies, are decisions for the DPO or counsel, never for this block or for an engineer alone. What a product must
provide is in `business/data-protection`; the contract side with a processor is in `skills/dpa-review-pitfalls`
(part 3); the engineering side of an incident is in `skills/incident-comms-pitfalls` and
`skills/blameless-incident-review-pitfalls`. This block is a working method for qualified people, not legal
advice.

## When
- A security incident touches personal data, or may have (lost device, misdirected export, exposed bucket,
  compromised account, a processor reporting a problem).
- A breach runbook, a register or an on-call escalation path is written or audited.
- A feature, a system or a change of use is planned that processes personal data in a new way, on a large scale,
  with new technology, or that evaluates people.
- An existing assessment is older than the processing it describes.

## Steps

**Read only the part the task meets.** Part 1 first during an incident; part 3 first during a design.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Awareness, clock and register: who may declare awareness, the timestamp, the delay reasons, the processor hand-off, the breach register | an incident may involve personal data, or a runbook is written | [`01-awareness-clock-and-register.md`](./references/01-awareness-clock-and-register.md) |
| 2 | What is sent, to whom: the authority notification, phased information, the communication to the people concerned, the conditions that are the DPO's call | a notification or a message to people is drafted or a template is built | [`02-notifications-and-communication.md`](./references/02-notifications-and-communication.md) |
| 3 | The assessment: trigger check, content, DPO advice, views of the people concerned, prior consultation, review | a new or changed processing is planned, or an assessment is written or audited | [`03-dpia-trigger-content-and-review.md`](./references/03-dpia-trigger-content-and-review.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). For an incident: the awareness timestamp and who set it, the computed
deadline with the reason for any delay, the facts known and unknown, the notices drafted or sent with dates, the
register entry, and the questions routed to the DPO with a named owner. For an assessment: the trigger check with
its result and who decided, the four content items present or missing, the DPO advice and its date, the review
trigger. Evidence for a runbook is a drill on dummy data that produced a register entry and a draft notice.
Every output ends with: not legal advice, escalate to the DPO or counsel.

## Guardrails
- Not legal advice. This block does not replace the DPO or a qualified lawyer; escalate to the DPO or counsel
  before any notice leaves the company and before any "no assessment needed" conclusion is recorded.
- It never states that an incident is or is not a breach, that a risk is low, likely or high, or that an
  exception applies; those are the DPO's calls (parts 1 and 2).
- Never compute a period from memory: it comes from the text read, with its start event recorded (part 1).
- Never wait for complete facts before escalating: the text allows information in phases (part 2).
- Never paste real personal data into a prompt, a ticket or a fixture; use dummy data.
- Never decide that an assessment is unnecessary by silence: record the check and its decision (part 3).
- Article 36 was read for the consultation step only; other articles, national law, authority lists and later
  amendments were not checked: say so and ask the DPO.

## Origin
Article 33 to 36 text from Regulation (EU) 2016/679 on EUR-Lex, read 2026-10-19, restated in our words. The
method (awareness record, drill, trigger check as a recorded decision) is our own guidance. Full provenance,
what was removed and what was not verified: [`references/origin.md`](./references/origin.md). 🟡: never run by us.
