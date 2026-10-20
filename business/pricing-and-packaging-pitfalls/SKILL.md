---
name: pricing-and-packaging-pitfalls
description: "Use when the price structure of a software product is designed, redesigned or reviewed: what is bundled in which plan, what the price scales with (seats, usage, features), the fences between tiers, a free plan or trial, a first price, a pricing page, or a willingness-to-pay survey whose curve is about to be read as the price. Three separate decisions in order, a value-metric test, an upgrade trigger per tier, segments before numbers, a cost model for free users, a first price as a bet, a page checklist, and the limits of survey methods."
---

# pricing-and-packaging-pitfalls

Business layer (`business/README.md`), marketing and product. The repeated failure in price design is choosing
a number, a metric or a plan shape from a survey curve, a copied competitor page or a remembered benchmark, and
then reading the result as proof. This block is the protocol for designing the structure and for checking it.

Out of scope, handled elsewhere: changing the price of customers who already pay, grandfathering, discounts and
billing mechanics are `business/price-change-and-billing-pitfalls`; tax on prices is
`skills/vat-handling-in-software-pitfalls`; whether a claim on a pricing page is true is
`business/marketing-claim-substantiation-pitfalls`; how a page is positioned is `business/product-marketing`;
the definition of the revenue metrics that follow a model is `skills/saas-metric-definition-pitfalls`; a live
price test is `skills/experiment-design-pitfalls`.

It carries no benchmark: no trial conversion rate, no value-to-price ratio, no discount percentage, no tier
multiple, no sample size, because the sources gave them without a derivation. It is not legal or tax advice, and
the person who owns the pricing decision decides.

## When
- A plan structure, a value metric or a first price is being chosen or reviewed.
- Someone proposes "price per seat", "usage-based", a free plan or a trial.
- A tier table or a pricing page is being written or graded.
- A willingness-to-pay survey result is about to become a number.

## Steps

**Read only the section the task meets.** §1 first for any pricing discussion.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Three decisions in order (packaging, metric, number), competitor and cost as inputs, the first price as a bet | a price is being discussed before the structure is settled | [`01-three-decisions-and-the-first-price.md`](./references/01-three-decisions-and-the-first-price.md) |
| 2 | The value metric: the test, seats, usage and the meter, credit and outcome models | the unit the price scales with is being chosen | [`02-the-value-metric.md`](./references/02-the-value-metric.md) |
| 3 | Tiers and fences: the upgrade trigger, what not to gate, anti-pattern checklist, segments before pricing | a tier table is designed or reviewed | [`03-tiers-fences-and-segments.md`](./references/03-tiers-fences-and-segments.md) |
| 4 | Free plan, trial, reverse trial as cost models; the pricing page checklist | a free-to-paid shape is chosen or a page is written | [`04-free-to-paid-and-the-pricing-page.md`](./references/04-free-to-paid-and-the-pricing-page.md) |
| 5 | Willingness-to-pay research: method follows the question, careful readings of two survey methods, validate with behaviour | a survey is designed or its curve is read | [`05-willingness-to-pay-research.md`](./references/05-willingness-to-pay-research.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the three decisions written separately with who decides
each; for each tier, who it is for and its upgrade trigger; for a metric, the test answered; for a first price,
the hypothesis and a review date; for a survey, a range and a shortlist with the n per segment, never "the
price". The owner of the pricing decision reads it and decides.

## Guardrails
- Decide in the order packaging, metric, number. Never fix the number first and bend the metric to fit it (§1).
- Test the metric: more use must mean more value, the unit must be understandable, predictable and hard to
  game. Never charge per seat on a product whose value does not rise with headcount (§2).
- Give every paid tier one named event that makes the tier below it hurt. Never ship a top tier that is a dump
  of roadmap items (§3).
- Gate what separates casual from serious use. Never gate the capability that delivers the core value (§3).
- Run segments apart before reading any survey or building tiers. Never average across personas (§3, §5).
- Name who pays for users who never convert, and the time to value, before choosing free plan or trial. Never
  pick a free shape by default (§4).
- Treat competitor prices as information about their strategy and cost base. Never use one as the target (§1).
- Publish a first price as an experiment with a hypothesis and a review date. Never present it as a verdict
  (§1).
- Report a survey as a range and a shortlist with n per segment, then check with behaviour. Never quote a
  crossing point as the price or as the revenue optimum (§5).
- Written from three young public repositories and two method pages, never run by us on a real product.
  Source status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the pricing skills of two MIT marketing repositories and the research-method
notes of a third, with survey-method facts from a vendor method page and an encyclopedia article, read
2026-10-20. 🟡: never run by us, written without pricing expertise. Details in
[`references/origin.md`](./references/origin.md).
