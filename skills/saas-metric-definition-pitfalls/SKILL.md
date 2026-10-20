---
name: saas-metric-definition-pitfalls
description: "Use when a subscription-business metric is defined, calculated or quoted: MRR and its four components, ARR as MRR times 12 and not trailing revenue, ACV, logo churn against revenue churn, net and gross revenue retention (gross capped at 100 percent), LTV and CAC with their inputs and period stated, payback, what counts as an active user before DAU or MAU is quoted, growth rates and the quick ratio."
---

# saas-metric-definition-pitfalls

Not a step of the pipeline: a craft block for writing down what a subscription metric means before a number is
quoted. The two parts share one premise: **a SaaS metric is a formula plus the inputs it takes, and two people
quoting the same name with different inputs are quoting two numbers**. The general discipline (a written
definition, an owner, the decision test) is in part 5 of `business/data-analytics`; explaining why a metric
moved is in `metric-movement-diagnosis-pitfalls`. This block only holds the definitions that go wrong most.

## When
- A dashboard, board update or model quotes ARR, MRR, churn, retention, LTV, CAC or active users.
- Two reports give different churn or retention for the same period.
- A metric is being defined for a new product or a new pricing model.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Revenue and retention: MRR components, ARR, ACV, logo against revenue churn, NRR, GRR | a recurring-revenue or retention figure is defined or checked | [`01-revenue-and-retention.md`](./references/01-revenue-and-retention.md) |
| 2 | Unit economics, engagement and growth: LTV, CAC, payback (per plan and cohort, gross margin, break-even CPA as the ceiling, §2.1), active user, stickiness, growth, quick ratio | a per-customer, per-user or growth figure is defined or checked | [`02-unit-economics-engagement-growth.md`](./references/02-unit-economics-engagement-growth.md) |

## Output / checkpoint
A metric is ready to quote when one line states its name, formula, every input with the period it covers, and
what is excluded, and when a reader can recompute it from that line alone. Read the line once looking for an
input with no period, a ratio whose two sides use different definitions, and a name that stands for two
formulas in the same document. No pipeline checkpoint. Nothing here was verified against a real billing
system: the check is a read of the text.

## Guardrails
- Never call a trailing twelve-month total ARR; ARR is the monthly figure times twelve (part 1).
- Never quote retention without saying whether it is net or gross, and never let gross exceed 100 percent
  (part 1).
- Never quote churn without saying whether it counts customers or revenue (part 1).
- Never quote LTV or CAC without the inputs and the period stated beside it (part 2).
- Never quote DAU or MAU before "active" is defined (part 2).
- Never quote one blended payback, or call a cohort recovered from a single retention figure: compute it per
  plan or cohort with gross margin, and say when a cohort has not recovered (part 2, §2.1).
- Interpretation bands and benchmarks (what ratio is healthy, what payback is good) are not in this block: the
  source's were unsourced and were dropped; a threshold is a decision the team writes down (part 2).

## Origin
Rewritten from one file of nimrodfisher's data-analytics-skills (MIT), read 2026-10-16. A young 2026
repository, one author's practice and not consensus. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
