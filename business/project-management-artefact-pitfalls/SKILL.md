---
name: project-management-artefact-pitfalls
description: "Use when a project plan, risk log, status report or estimate is written, reviewed or handed on: a risk with no owner, an issue and a risk in the same column, a date given as a single number, a dependency nobody told the other team about, a status that is green until the week it is red, a change that moved the date without anyone deciding it, a project closed with no record of what it learned. RAID log discipline, estimate honesty, dependency tracking, status reporting, change control and closure."
---

# project-management-artefact-pitfalls

Business layer (`business/README.md`), project management. A project artefact is a promise about the future that
other people plan around. Most failures are not missing artefacts but artefacts that say nothing checkable: a log
nobody owns, a date with no range, a status that never turns amber. This block is the check to run on a plan, a
log or a report before it is sent. Code-side planning is `skills/plan`, the handoff between sessions is
`skills/handoff`, the product backlog is `business/product-ownership`, goals and their scoring are
`skills/okr-scoring-pitfalls`, the choice of a vendor is `business/vendor-management`.

It states method only. Any framework named in the field (a certification body's method, an agile flavour) is
proprietary or contested; this block keeps the ideas that survive in all of them and names no mandatory template.

## When
- A plan, a risk or issue log, a dependency list or an estimate is created, or inherited from someone else.
- A status report or steering update is written.
- A change request, a slipped date or a scope trade is on the table.
- A project or phase ends and its record has to be closed.

## Steps

**Read only the section the task meets.** §1 when a log or plan is created or taken over; §2 when a date or a
dependency is committed; §3 when a report, a change or a closure is written.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | RAID log: risks, assumptions, issues and dependencies kept apart, owners, triggers, review rhythm | a log is started, or one is inherited | [`01-raid-log-and-ownership.md`](./references/01-raid-log-and-ownership.md) |
| 2 | Estimates and dependencies: ranges, what the number includes, slip that moves downstream, the critical path | a date or an effort is given or accepted | [`02-estimates-and-dependencies.md`](./references/02-estimates-and-dependencies.md) |
| 3 | Status, change and closure: evidence-based status, trend, decisions asked for, change control, lessons | a report, a change request or a close-out is written | [`03-status-change-and-closure.md`](./references/03-status-change-and-closure.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a log in which every line has an owner, a next review date
and, for a risk, a trigger; each date stated with its range and its assumptions; a report whose colour is backed
by a fact and that ends with the decisions it needs. The project owner decides priorities and accepts risk; the
author reports the state and does not soften it.

## Guardrails
- Give every risk, issue and dependency one named owner and a review date. Never leave a line owned by "the team"
  (§1).
- Keep a risk (may happen) apart from an issue (has happened). Never log an event that already occurred as a risk
  to keep a report calm (§1).
- Give a range and the assumptions behind it. Never promise a single date that hides an unknown (§2).
- Tell the owner of every downstream task when an upstream one slips. Never wait for the plan review to surface it
  (§2).
- Back each status colour with a fact and a trend. Never report green on feeling (§3).
- End a report with the decisions you need and the date they are needed by. Never send an update that asks for
  nothing and leaves the reader to guess (§3).
- Record a date or scope change as a decision with a named decider. Never let a date move by silent edit (§3).
- This block is method written from general practice, never run by us on a real project; no external source was
  taken. Status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Written from general project-management practice; the proprietary certification methods were not read, and the
one MIT skills repository named by the review was not used for text. 🟡: never run by us. Details in
[`references/origin.md`](./references/origin.md).
