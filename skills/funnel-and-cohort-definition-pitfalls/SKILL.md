---
name: funnel-and-cohort-definition-pitfalls
description: "Use when a funnel or a cohort retention analysis is defined, built or read: steps that are sequential and counted once, page views mistaken for intentional actions, the first step as the denominator, step-over-step versus overall conversion, open-ended versus time-bounded versus cohort-based windows, segmenting before concluding, the choice of the retention event, cohorts that are too recent to compare, averages dominated by large cohorts, small cohorts, user retention versus revenue retention, and several events per user inflating retention."
---

# funnel-and-cohort-definition-pitfalls

Not a step of the pipeline: a craft block for the definitions behind a funnel chart or a retention table. The two
sections share one premise: **a funnel or cohort chart is only as comparable as its definition is explicit, so a
number that looks precise is worthless until it is clear who is counted, from when, within what window and on
which event**. Defining the events themselves is in `event-tracking-plan-pitfalls`; checking a computed result
is in `analysis-validation-pitfalls`; explaining why a metric moved is in `metric-movement-diagnosis-pitfalls`;
experiments are in `experiment-design-pitfalls`.

## When
- Defining the steps and the window of a conversion funnel, or reading a drop-off chart.
- Building a retention or cohort table, or choosing what "active" means.
- Two funnels or two cohort charts disagree, or a period-over-period comparison looks unfair.
- A cohort chart is about to be averaged, or its most recent rows compared with older ones.

## Steps

**Read only the section the task meets.** They are independent.

| Ref | Covers | Read it when | File |
|---|---|---|---|
| 01 | Funnel definition: steps, denominator, counting unit, conversion types, time window, segments, prioritising a drop-off | a funnel is designed or its drop-off is being interpreted | [`01-funnel-definition.md`](./references/01-funnel-definition.md) |
| 02 | Cohort definition: grouping, the retention event, immature cohorts, averages, small cohorts, revenue versus users, repeated events | a cohort or retention analysis is built or read | [`02-cohort-definition.md`](./references/02-cohort-definition.md) |

## Output / checkpoint
A funnel is done when the reader can say who enters at step one, what each step is (an action, not a page view),
the unit counted at every step, the window and its type, and which segment split was looked at before a
conclusion was drawn. A cohort analysis is done when the grouping rule, the retention event and its owner, the
cohort sizes, and which cells are incomplete are all on the chart or beside it. Read the output once looking
for a comparison between cells that have a different number of periods behind them, and for a retention rate with
no count of people under it. Nothing here was verified on real data: the check is a read of the text.

## Guardrails
- Never leave the first step undefined; every rate is relative to it (reference 01).
- Never define a step by a page view when an intentional action is available (reference 01).
- Never mix session-level and user-level counts across steps (reference 01).
- Never conclude from an aggregate funnel before splitting by the most relevant segment (reference 01).
- Never compare cohorts at periods one of them has not reached; mark incomplete cells (reference 02).
- Never pick the retention event after seeing the curve; a wrong event gives a curve that looks right and
  misleads (reference 02).
- Never report retention without the number of people behind it, and set a minimum cohort size in advance; the
  source's suggested value is a recommendation, not a rule, and is not carried here (reference 02).
- Never count a user once per event in a retention measure; one active or inactive signal per user per period
  (reference 02).

## Origin
Rewritten from nimrodfisher's data-analytics-skills, the funnel-analysis reference `funnel_design_guide.md` and
the cohort-analysis reference `cohort_definition_patterns.md` (MIT), read 2026-10-16. A young 2026 repository,
one author's practice and not consensus. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
