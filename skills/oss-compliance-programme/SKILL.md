---
name: oss-compliance-programme
description: "Use when a company that ships or offers software must set up or audit how it handles open-source licence obligations as a standing programme, not dependency by dependency: a written policy with named roles and resources, scope, a decision log, a component list per release, a compliance bundle per release, a list of known licences, an intake path for outside questions, contribution clearance, training records and a review interval."
---

# oss-compliance-programme

Business layer (`business/README.md`), legal. `business/licence-compliance` answers the question for one
dependency at the moment it is added; this block sits above it and answers "who does this, what is written down
and what can we show". Its premise: compliance that depends on one person's memory fails on the day that person
is away, a customer or an acquirer who asks for a component list cannot be answered, and a licence question
with no recorded decision gets argued again. A programme is people, then a process, then evidence. This block
is a structure to adapt, not a statement of what any licence or standard requires; the reading of a licence and
the choice of which obligations apply stay with counsel (`business/licence-compliance`).

## When
- A company starts to ship or host software that contains open-source components and has no written way of
  handling them.
- A customer, an investor or an auditor asks for a component list, a policy or proof of how licences are managed.
- A licence question was answered in a chat and cannot be found again.
- The existing process is reviewed after an incident, a reorganisation or a change in how software is delivered.

## Steps

**Read only the section the task meets.** Part 1 first for a new programme; parts 2 and 3 can be read alone to
audit an existing one.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | People and policy: the written policy, the roles, resources, scope, the list of known licences | a programme is being set up or its ownership is unclear | [`01-people-and-policy.md`](./references/01-people-and-policy.md) |
| 2 | Evidence: the decision log, the component list, the compliance bundle per release, retention | the question is what can be shown for a given release | [`02-evidence-per-release.md`](./references/02-evidence-per-release.md) |
| 3 | Intake and upkeep: outside questions, contributions to other projects, training, review, conformance claims | the programme must handle questions or be kept alive | [`03-intake-and-upkeep.md`](./references/03-intake-and-upkeep.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a short written policy with named roles; the scope;
the decision log with its fields; the rule for producing a component list and a compliance bundle at each
release and for keeping them; the list of known licences and the path for an unknown one; the intake path; and
the review date. When auditing, the output is the gap list against these items, each with who owns closing it.

## Guardrails
- This block does not replace legal advice. Which obligations a licence creates, which licences are acceptable
  and whether a given release complies belong to a qualified lawyer.
- Never record a licence decision without the decider, the date and the reason (part 2).
- Never accept a component whose licence is not on the known list without a review by counsel (part 1).
- Never claim conformance to a standard or a certification until it has been checked against that standard's
  own text, which this block does not reproduce (part 3).
- A product that is only hosted may not owe some of the distribution artifacts (source offers, for example);
  whether it does is a question for counsel, not an engineering default (part 2).
- Do not copy retention periods or review intervals from a template without the decision of the owner of the
  programme and counsel (parts 2 and 3).

## Origin
Rewritten from the generic company open-source policy text of the OpenChain Reference-Material repository
(CC0-1.0), read 2026-10-16; provenance, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
