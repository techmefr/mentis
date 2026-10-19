---
name: gdpr-international-transfers-pitfalls
description: "Use when personal data may leave the European Union or reach a recipient outside it (a new vendor, a cloud region, a support tool, a group company, a remote-access arrangement, a request from a foreign authority) or when a transfer register is built or audited: inventorying every flow and onward flow, identifying the transfer mechanism claimed for each, asking the questions that prove it, and escalating what is a decision for the DPO or counsel."
---

# gdpr-international-transfers-pitfalls

A defensive block for the engineering and review side of GDPR Chapter V (Articles 44 to 49): where personal data
goes, under which mechanism, and who decided. The failures are mechanical: a flow nobody inventoried because it
is a log shipper or a support tool, a "global" vendor whose real processing location was never asked, a mechanism
cited without checking it covers this recipient and this data, a sub-processor chain left unmapped, a derogation
used as if it were a standing arrangement, a foreign request answered by the first engineer who received it.
The legal text read for this block is Regulation (EU) 2016/679 (the GDPR), Articles 44 to 49, as published in the
Official Journal; it applies to that regulation only. Which mechanism is valid, whether a transfer assessment is
needed and what it concludes, and whether a derogation is available are decisions for the DPO or counsel, never
for this block or for an engineer alone. The contract side with a supplier is in `skills/dpa-review-pitfalls`
(parts 3 and 4); the vendor-level checks are in `business/vendor-management`; what a feature must provide is in
`business/data-protection` (part 4, third parties). This block is a working method for qualified people, not
legal advice.

## When
- A new supplier, SaaS, sub-processor, cloud region, support or monitoring tool will receive or can see personal
  data.
- A group entity, a contractor or a remote team outside the European Union gets access to a system holding it.
- A transfer register is built, a processing record is reviewed, or a vendor's list of sub-processors changes.
- A court order, an authority request or a foreign legal demand arrives asking for personal data.

## Steps

**Read only the part the task meets.** Part 1 first for any new flow; part 3 first when a demand arrives.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Inventory and register: what counts as a flow, the fields to record per flow, onward flows, the access-versus-storage trap | a flow is added, a register built, a vendor reviewed | [`01-inventory-and-register.md`](./references/01-inventory-and-register.md) |
| 2 | Mechanisms and their proof: adequacy, appropriate safeguards (and which need the authority), the questions to ask per mechanism, drift over time | a mechanism is named for a flow, or a register is audited | [`02-mechanisms-and-proof.md`](./references/02-mechanisms-and-proof.md) |
| 3 | Derogations, foreign demands and escalation: the specific situations, why they are not a default, the foreign-judgment rule, what the engineer sends to the DPO | no mechanism is available, a derogation is proposed, or a foreign demand arrives | [`03-derogations-demands-and-escalation.md`](./references/03-derogations-demands-and-escalation.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). For each flow under review: the register row (data categories, sender,
recipient entity and location of the processing and of any remote access, onward recipients, mechanism claimed,
evidence seen, date, owner), the open questions with a named owner, and the decision of the DPO or counsel with its
date. For a process: a dummy flow that went from vendor request to register row to review date. Every output ends
with: not legal advice, escalate to the DPO or counsel.

## Guardrails
- Not legal advice. This block does not replace the DPO or a qualified lawyer; escalate to the DPO or counsel
  before a flow goes live without a mechanism the DPO has accepted.
- It never states that a country, a mechanism or a derogation is valid or sufficient; the lists and the
  conclusions are the DPO's (parts 2 and 3).
- Never rely on a vendor's marketing page for a location or a mechanism: ask for the document and file it
  (part 2).
- Never treat remote access as no transfer: record who can see the data from where (part 1).
- Never use a derogation as a standing arrangement on the engineer's reading (part 3).
- Never answer a foreign demand for personal data from engineering: route it (part 3).
- Never paste real personal data into a prompt, a ticket or a fixture; use dummy data.
- Adequacy lists, standard clauses, authority guidance, national law and later amendments were not read: say so
  and ask the DPO.

## Origin
Text of Articles 44 to 49 from Regulation (EU) 2016/679 on EUR-Lex, read 2026-10-19, restated in our words. The
inventory and review method is our own guidance. Full provenance, what was removed and what was not verified:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
