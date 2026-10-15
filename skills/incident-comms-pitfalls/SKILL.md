---
name: incident-comms-pitfalls
description: "Use when customers have to be told about an incident while it is running: deciding in advance when an incident is communicated publicly, the first message and the scoping message, updates on a stated cadence even with nothing new, long incidents, the resolution message and data loss, wording ('outage', cause speculation), separating the commander from the communicator, individual notice for customers on special contracts, and the first hours of a security incident."
---

# incident-comms-pitfalls

The customer-facing side of an incident, **while it runs**. The premise: **a customer who sees the symptom and
finds no sign that you know about it concludes that you do not, and the fix to that is a message, not a
better fix**. `business/incident-communication` is the short overview of the whole arc; this block holds the
detail that overview leaves out: criteria, cadence, roles, wording and the security case.

Not covered here: the postmortem and its review, internal and engineering-channel communication, how to
diagnose (`skills/debug`), and a reported bug that is not an incident (`bug-triage`).

## When
- Defining or reviewing when, how fast and how often customers are told about an incident.
- Writing a status page message, a customer email or a holding statement for a running incident.
- Splitting who decides, who fixes and who speaks, in a team where one person may hold two roles.
- A suspected security incident that customers will have to be told about.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Deciding what is communicated, severity as input, roles, individual notice, security incidents | the process is being set up, or nobody knows who may post | [`01-decide-and-roles.md`](./references/01-decide-and-roles.md) |
| 2 | First message, scoping message, updates and cadence, long incidents, resolution | a message is about to go out or the updates stopped | [`02-message-sequence.md`](./references/02-message-sequence.md) |
| 3 | Wording, cause speculation, time zone, short templates, a pre-send check | a draft is being reviewed | [`03-wording-and-checks.md`](./references/03-wording-and-checks.md) |

## Output / checkpoint
For the process: written criteria for public communication, a cadence per severity, and the three roles named
for the next incident. For a live incident: every message sent carries a next-update time and a stated time
zone, no message names a cause, and the resolution message says whether data was affected. A draft that was
not checked against the list in §3.3 is not reviewed.

## Guardrails
- Never leave the decision to communicate to the middle of the incident; the criteria exist beforehand (§1.1).
- Never let the first message wait for the scope; send it thin and say scope will follow (§2.1).
- Never go silent because there is nothing new; send "still investigating, next update at HH:MM" (§2.3).
- Never name a cause in public while it is unconfirmed (§3.1).
- Never write "outage" for something that was not a full outage (§3.2).
- Never let more than one voice speak for the incident (§1.2).
- Never leave the resolution message without a statement about data (§2.5).
- Every minute and hour figure in this block is one source's example. Where the sources disagree the
  disagreement is stated; choose your own and write it down. This block makes no claim about legal duties.

## Origin
Rewritten from PagerDuty's public incident response documentation (Apache-2.0), Felipe Guedes's incident
response runbook (Apache-2.0, a young repository) and one comms template from the durrello incident runbooks
(MIT), read 2026-10-15. Details, licences and open points are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
