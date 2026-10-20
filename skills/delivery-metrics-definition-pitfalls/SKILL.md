---
name: delivery-metrics-definition-pitfalls
description: "Use when defining, computing or reading software delivery and developer-experience metrics (deployment frequency, lead time for changes, change failure rate, time to restore, cycle time, review wait, toil, developer survey scores): a start or end event nobody pinned, a failure that is not counted because nobody linked it to a change, an average that hides the tail, a team comparison that measures process differences, and a target that gets gamed. Own guidance plus one framework guide read for definitions, no benchmark and no threshold."
---

# delivery-metrics-definition-pitfalls

A delivery metric is a definition plus a data source plus a decision. Most of the damage is done in the definition:
two teams count "deployment" differently, a lead time starts at a moment nobody can query, failures that no
one connected to a change never reach the rate, and the number then becomes a target and stops describing
anything. The premise is that **a metric is only comparable with itself, under one written definition, for one
system**. This block fixes definitions and reading mistakes; it carries no benchmark, no "elite" band and no
target value, because none was read from a source.

Product and SaaS metrics are `skills/saas-metric-definition-pitfalls` and `skills/semantic-layer-metric-pitfalls`;
a metric that moved is `skills/metric-movement-diagnosis-pitfalls`; reliability objectives are `skills/slo-design`;
the incident process that produces restore times is `skills/blameless-incident-review-pitfalls`; the regulation
that shares the acronym DORA is `skills/dora-ict-risk-and-incident-pitfalls` and is unrelated.

## When
- A dashboard of delivery speed or stability is built, or a leader asks for "our DORA numbers".
- A number is compared across teams, quarters or against an outside figure.
- A target is attached to a delivery metric, or developer-experience feedback is being measured.

**Skip when** no delivery or developer-experience metric is defined anywhere in the repository or its documents (no dashboard, no target, no report, no stated figure). Say "not applicable: no metric defined" and stop; never derive a lead time or a deployment frequency from a short commit history to have something to review. Product analytics events and a bundle-size budget are not delivery metrics.

## Steps

**Read only the part the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Definitions: event boundaries, what counts as a deployment, a failure and a restore, data sources, the tail | a metric is defined or computed | [`01-definitions-and-data.md`](./references/01-definitions-and-data.md) |
| 2 | Reading and using them: comparison, targets and gaming, cycle-time breakdown, toil, developer-experience surveys | a number is compared, targeted or acted on | [`02-reading-and-using.md`](./references/02-reading-and-using.md) |

## Output / checkpoint
For each metric: a one-line definition with its start and end events, the source system for each event, what is
excluded and why, the statistic used (a percentile or median, never a bare mean alone), the unit of analysis (a
service or a team, never "the company"), the decision it informs, and the date of the last review of the
definition. A number without its definition is not published.

## Guardrails
- Write the start and end event of every duration before computing it. Never publish a lead time whose start is
  "when work began" with no queryable event (§1.1).
- Link failures to changes by a recorded rule. Never report a failure rate from incidents nobody traced to a
  release (§1.4).
- Report a distribution or percentiles beside the central value. Never let one mean stand for a skewed duration
  (§1.6).
- Compare a service with its own past. Never rank teams on a raw number when their systems differ (§2.1).
- Use a metric to find a constraint, not to grade people. Never attach a bonus or a target to one without a
  paired counter-metric (§2.3).
- Review only a metric that exists. Never invent one to fill a report (see the Skip when line).
- No benchmark, band or threshold is stated in this block. Never quote one from memory: read it from the
  framework's current publication and date it (`skills/source-freshness`).

## Origin
Own craft knowledge, flagged as such, with the metric names, grouping and cautions checked on 2026-10-20 against the
framework's own metrics guide (read for facts only, licence not verified, no text taken, credited to dora.dev). The
benchmark bands were not read. Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
