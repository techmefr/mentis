---
name: community-and-social-metrics-pitfalls
description: "Use when community or social numbers are defined, reported or acted on: reading discovery, usage, retention and maintainer response in order, time to first response with its filters, occasional contributors, bursts, harm metrics with severity and delay, choosing social measures that map to a goal, missing versus zero, lifetime snapshots, small samples, and labelling editorial weightings."
---

# community-and-social-metrics-pitfalls

Business layer (`business/README.md`), communication. `business/community-management` and
`business/social-publishing` both say to measure; this block gives the definitions and the reading rules that
stop a number from saying more than it can. Its premise: a metric is useful when a change you make can move it,
and most reporting failures are about reading a number, not collecting it.

Nothing here replaces a statistician or the platform's own definitions. Numbers quoted from sources, such as
sample sizes, are the sources' own choices and are labelled so.

## When
- Setting up or reviewing a community health report or a social media report.
- Someone reads a spike, a drop or a response time and proposes a decision.
- A dashboard mixes bot replies, missing fields or lifetime counts with current activity.
- Choosing which social measures to report for a goal.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The community funnel: discovery, usage, retention, maintainer response, and what each question rules out | a community report is being structured | [`01-the-funnel.md`](./references/01-the-funnel.md) |
| 2 | Definitions that need filters: time to first response, occasional contributors, bursts, harm metrics | a response or activity number is defined or compared | [`02-definitions-and-filters.md`](./references/02-definitions-and-filters.md) |
| 3 | Social measures and honest reading: goal mapping, missing versus zero, snapshots, small samples, weightings | social numbers are reported or acted on | [`03-social-measures-and-reading.md`](./references/03-social-measures-and-reading.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: each metric with its definition and filters, its source
and date, whether missing values were kept apart from zero, the sample size, a note when a spike has a known
cause, and a decision the report supports. A measure that will not change next week's action is labelled a
diagnostic. The person who owns the community or the account decides.

## Guardrails
- Never count bot or automated replies as responsiveness, and never leave the responder role undefined (part 2).
- Never read a spike as growth before asking what event or campaign caused it (part 2).
- Never treat a missing number as zero, nor estimate as fact (part 3).
- Never present a lifetime snapshot as a live window (part 3).
- Never draw a pattern from a handful of posts, or call a correlation a cause (part 3).
- Never hide an editorial weighting inside a score; label it (part 3).
- This block is a method from public guidance and young repositories, never run by us on a real community. A
  second human read is warranted. Sources and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from an open-source community guide on metrics (CC-BY-4.0, attributed), three community health metric
definitions from a community analytics working group (MIT), a social analytics skill and two social post
analysis skills (MIT), and a trust-and-safety teaching deck on metrics (CC0), read 2026-10-16. 🟡: never
dogfooded. Details in [`references/origin.md`](./references/origin.md).
