---
name: variance-analysis-pitfalls
description: "Use when explaining a gap between actual and budget, forecast or prior period: splitting a variance into volume and price and proving the parts sum to the total, extra effects (rate, mix, headcount, timing) only with a checked formula, building a bridge that reconciles, writing a narrative that names, quantifies and explains each driver, narrative anti-patterns (circular, bare timing, one-time, various), which comparison serves which purpose, forecast accuracy and systematic bias."
---

# variance-analysis-pitfalls

A craft block for the write-up of a variance: the arithmetic that splits it, the bridge that proves the split
and the sentences that explain it. The premise is that **a variance is explained only when its parts add up to
the whole and each part has a cause someone can check**. It overlaps with `skills/metric-movement-diagnosis-pitfalls`
(volume, rate and mix of a moving metric) and with `skills/analysis-validation-pitfalls` (checking a result
before it is shared); read those first when the question is "why did this number move" rather than "how do I
report this gap". It carries no materiality threshold and no accounting treatment: the point at which a variance
needs an explanation is the organisation's decision. It does not replace a chartered accountant, an auditor, or
a legal, compliance or financial adviser, and it is not investment advice.

## When
- A budget, forecast or prior-period comparison needs commentary for a manager or a board.
- A revenue, cost or people-cost gap must be split into drivers.
- A bridge or waterfall is being built, or one was built and does not reconcile.
- A forecast has missed repeatedly and the pattern needs reading.

## Steps

**Read the part the task meets.** Part 1 when splitting and bridging; part 2 when writing and comparing.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Decompose and bridge: volume and price, extra effects, proof that parts sum, bridge reconciliation, driver count | a gap is split into drivers or a waterfall is built | [`01-decompose-and-bridge.md`](./references/01-decompose-and-bridge.md) |
| 2 | Narrative and comparisons: what a good explanation contains, anti-patterns, which comparison for which purpose, accuracy and bias | commentary is written or a forecast is judged | [`02-narrative-and-comparisons.md`](./references/02-narrative-and-comparisons.md) |

## Output / checkpoint
A variance write-up is done when the total variance is stated with its comparison basis, each driver has a
signed amount, the drivers sum to the total (shown, not claimed), and each driver has a sentence that names it,
quantifies it, gives the cause and says whether it continues. Evidence is a bridge whose start plus drivers
equals its end, and a worked check of any formula on a small example before it is used on the real figures.
Nothing here was run on a real close: the check is a read of the text.

## Guardrails
- Never publish a split whose parts do not sum to the total variance; an unexplained remainder is shown as a
  line, not absorbed (part 1).
- Never use a decomposition formula you have not checked on a small example (part 1).
- Never write "timing", "one-time" or "various" for a material gap without the item, the date or the
  breakdown (part 2).
- Never read a pattern of always-favourable or always-unfavourable variances as bad luck without asking about
  the plan itself (part 2).
- This block sets no threshold for what is material: take it from your organisation.
- This block does not replace a chartered accountant, an auditor, or a legal, compliance or financial
  adviser.

## Origin
Rewritten from the variance-analysis skill of anthropics' knowledge-work-plugins (Apache-2.0), read
2026-10-16. A vendor-authored practice guide, not a standard. 🟡: never run by us; the formulas that were not
carried and the open points are in [`references/origin.md`](./references/origin.md).
