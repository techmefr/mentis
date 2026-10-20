---
name: b2b-go-to-market-pitfalls
description: "Use when a B2B product or feature is taken to market: an ideal customer defined as everyone, a launch date with no readiness check, channels chosen because competitors use them, a launch with no owner for the leads it creates, a sales team that learns of the release from the announcement, a launch judged by a day of traffic. ICP definition, launch readiness gate, channel choice by what you own, sales handoff, post-launch review. Method only; revenue forecasts are not made here."
---

# b2b-go-to-market-pitfalls

Business layer (`business/README.md`), marketing. `business/product-marketing` owns positioning and claim
checking; this block owns the plan around it: who the product is for, whether it is ready to be sold, which
channels carry it, and who receives what comes back. Release announcements are `business/release-communication`;
pricing is `business/pricing-and-packaging-pitfalls`; the pipeline after a lead arrives is
`business/outbound-sales-and-crm-hygiene-pitfalls`; discovery conversations are
`business/customer-interview-synthesis-pitfalls`.

## When
- A new product, a new segment or a significant feature is about to be launched to business buyers.
- A launch plan is reviewed, or a past launch is reviewed to decide what to change.
- A team asks who the ideal customer is, in sales or in marketing.

## Steps

**Read only the section the task meets.** §1 when defining the customer; §2 before dating a launch; §3 after it.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ideal customer and buying group: a profile that excludes, disqualifiers, roles in a purchase, evidence from won and lost deals | the target is defined or questioned | [`01-icp-and-buying-group.md`](./references/01-icp-and-buying-group.md) |
| 2 | Launch plan: readiness gate, owned, rented and borrowed channels, enablement, handoff of leads, one owner per task | a launch is planned | [`02-launch-readiness-and-channels.md`](./references/02-launch-readiness-and-channels.md) |
| 3 | After the launch: what to measure and when, attribution limits, review and next steps | a launch has happened | [`03-after-the-launch.md`](./references/03-after-the-launch.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a one-page ICP with disqualifiers and its evidence, a
launch readiness note with a named go or no-go owner, a channel plan listing which channels the company owns, a
handoff agreement between marketing and sales, and a dated review of what the launch produced.

## Guardrails
- Write who the product is not for. Never define the customer as every company in a size band (§1).
- Base the profile on won, lost and churned deals, and label hypotheses as such. Never present a guess as a
  finding (§1).
- Run the readiness gate before fixing the date: the product does one thing completely, support and sales can
  explain it. Never launch to create the pressure to finish (§2).
- Choose channels by which ones you own and your buyer uses. Never copy a competitor's mix (§2).
- Agree who answers a lead, in what time, with what material, before the announcement. Never send traffic to a
  form no one reads (§2).
- Brief sales and support before the public does. Never let them learn of the launch from it (§2).
- Judge on outcomes tied to the goal set beforehand, after a long enough period. Never judge on launch-day traffic
  (§3).
- Make no revenue forecast, and state no benchmark from a source you have not re-read and dated.
- This block is partly built from an MIT source and partly from general practice, and never run by us on a real
  launch. Status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our own words from the launch-planning notes of an MIT marketing skills repository (read
2026-10-20), plus general B2B practice. 🟡: never run by us. Details in [`references/origin.md`](./references/origin.md).
