---
name: ad-measurement-pitfalls
description: "Use when advertising is being tagged, measured or reported: campaign links and UTM naming, click identifiers lost in redirects, deciding what counts as the conversion and which system holds the count, a platform number that disagrees with analytics or the CRM, two platforms claiming one sale, a double count from two senders, choosing or comparing attribution models, or someone proposing to recover users who declined tracking. Written as pitfalls: method only, no per-platform setup."
---

# ad-measurement-pitfalls

Business layer (`business/README.md`), marketing. Advertising spend is steered by numbers that several
systems each count their own way, and the facts about tagging and attribution are easy to get wrong. This block
lists the places where the measurement of paid media goes wrong, and what to check before trusting a figure.
Reading an account and deciding what to do is `business/paid-media-decision-pitfalls`; naming and firing
events inside a product is `skills/event-tracking-plan-pitfalls` (including that a click is not a successful
submit); two numbers that disagree in general is `skills/metric-movement-diagnosis-pitfalls` §3; a test is
`skills/experiment-design-pitfalls`.

It states method only. It carries no setup steps for any platform, no tag or container recipe, and no
percentage for how much tracking loses or how far platforms normally differ, because those figures were
unsourced or vendor-supplied in the material read. Platform facts it mentions are marked
`re-read before relying`. Whether and how personal data may be used is a legal question this block does not
answer (`business/data-protection`); it is not legal advice.

## When
- Campaign links are being created or a naming scheme for them is being agreed.
- Conversions are missing, doubled or reported differently by the ad platform, analytics and the CRM.
- Someone must say which number is "the conversion count" for a report or a budget decision.
- An attribution model is chosen, or two models are being compared.
- Someone proposes a way to count visitors who refused tracking.

## Steps

**Read only the section the task meets.** §2 first when the question is "which number is right"; the others
are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Tagging: UTM names and values, personal data in links, the click identifier and redirects, testing the final address | links are built, or paid traffic shows up as something else | [`01-tagging-and-click-identifiers.md`](./references/01-tagging-and-click-identifiers.md) |
| 2 | What counts as a conversion: one business conversion, the system of record, claimants, outcomes behind a form fill, double counts, refunds | the count itself is in question or optimisation runs on a weak signal | [`02-what-counts-as-a-conversion.md`](./references/02-what-counts-as-a-conversion.md) |
| 3 | Why platform numbers differ: structural causes, what to line up first, lag, no multiplier | two reports disagree | [`03-why-numbers-differ.md`](./references/03-why-numbers-differ.md) |
| 4 | Attribution models and out-of-model checks: every model is an opinion, first and last side by side, volume, self-reported answers and holdouts, consent | a model is chosen or defended, or consent loss is "recovered" | [`04-attribution-and-consent.md`](./references/04-attribution-and-consent.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the single business conversion written in one
sentence and the system that holds its count; each platform's figure shown beside it with its window and
definition and never summed; the list of structural reasons that explain the gap and the ones still open; for a
model choice, the models shown side by side and the out-of-model check named. A person who owns measurement
and, where personal data is involved, legal, reads it and decides.

## Guardrails
- Set source, medium and campaign on every campaign link, with one lowercase naming convention. Never rely on
  mixed-case values or leave a parameter out and accept "(not set)" in reports (§1.1).
- Keep personal data out of link parameters. Never put an email, a name or an account identifier in a link
  that will land in reports, logs and referrers (§1.2).
- Test the final address after every shortener and redirect and check the click identifier arrives. Never
  assume the first hop is the page (§1.3, §1.4).
- Decide the one business conversion and its system of record before any tooling. Never let a platform
  redefine how many conversions there were (§2.1).
- Treat two platforms claiming one sale as one conversion with two claimants. Never sum platform figures
  (§2.2).
- Line up conversion, date basis, time zone, window and scope before comparing two numbers. Never turn a
  platform-to-analytics ratio into a multiplier (§3.2, §4.1).
- Show first-touch and last-touch side by side on a long cycle, keep the model constant and add a check from
  outside the model. Never switch models to make a channel look better (§4.1, §4.3).
- Treat a refusal of tracking as a decision, never a loss to recover, and send the lawful-basis question to
  `business/data-protection`. Never present server-side delivery as a way round consent (§4.4).
- This block is a method written from three young public repositories and two Google help pages and never
  run on a real account by us. Source status and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the conversion-tracking and attribution skills of an MIT marketing skills
repository, the attribution audit of an MIT paid-media skills repository, and Google help pages (UTM
parameters, auto-tagging, conversion windows and delay, attribution models, adjustments, transaction IDs), read 2026-10-20. 🟡: never run by us, written without
measurement expertise. Details in [`references/origin.md`](./references/origin.md).
