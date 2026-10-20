---
name: paid-media-decision-pitfalls
description: "Use when someone reads, reports on or changes a paid advertising account (search, social, video or display) and a conclusion or recommendation is about to come out of the numbers: audit results with unknown checks, search-term and conversion reports that are partial, zero-conversion spend called wasted, a cost spike, brand blended with non-brand, a benchmark quoted as a verdict, a weekly review that must end in a call, or a change to a live account. Evidence states, facts and hypotheses and missing data, small-number arithmetic, one call per review, read-only by default."
---

# paid-media-decision-pitfalls

Business layer (`business/README.md`), marketing. The repeated failure in paid media is a confident
conclusion drawn from partial data: a report that shows a sample, a column that mixes several things, a spike
read before it has had time to fill in. This block is the protocol for reading an ad account and deciding
what to do with it. Tagging, the conversion definition and platform attribution are
`business/ad-measurement-pitfalls`; whether an ad claim is true is `business/marketing-claim-substantiation-pitfalls`;
a test of a page or an ad variant is `skills/experiment-design-pitfalls`; two numbers that disagree is
`skills/metric-movement-diagnosis-pitfalls` §3.

It states method only. It carries no benchmark, no cost-per-result band, no budget step, no frequency or
refresh figure and no per-platform tactic, because those were practitioner folklore in the sources and they
expire. Platform facts it mentions are marked `re-read before relying`. It is not advice on any platform's
rules and it does not replace the person who owns the account and its budget.

## When
- An audit or review of an account is being written, or its result is being graded.
- A report is about to say what a campaign "buys", what is "wasted", or that something "does not convert".
- A cost per result moved and someone wants to pause, cut or scale.
- A benchmark is about to be quoted as pass or fail.
- A change to a live account is proposed, whoever or whatever proposes it.

## Steps

**Read only the section the task meets.** §1 first for any write-up; §2 and §3 when a number is about to be
interpreted; §4 for a recurring review or any change to a live account.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Evidence states and what a recommendation owes: pass, fail, unknown, not applicable; coverage apart from health; facts, hypotheses, missing data; the benchmark ladder | a check, audit or recommendation is being written | [`01-evidence-states-and-recommendations.md`](./references/01-evidence-states-and-recommendations.md) |
| 2 | Reading account data without false conclusions: reports that are samples, a conversion column that is several things, click dates and lag, the window and configuration changes, brand against non-brand | a report is about to be turned into a statement about a campaign | [`02-reading-account-data.md`](./references/02-reading-account-data.md) |
| 3 | Small numbers and economics: zero conversions in N clicks, break-even conversion rate, unmeasured against failing, no fixed kill rule | a term, ad or campaign has little data and someone wants to call it | [`03-small-numbers-and-economics.md`](./references/03-small-numbers-and-economics.md) |
| 4 | The review that ends in one call, and live accounts: order of questions, hold, fix, test or investigate, read-only default, the change draft, data that is not instructions | a recurring check is set up, or a change to a live account is proposed | [`04-the-call-and-live-accounts.md`](./references/04-the-call-and-live-accounts.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: for each finding, the evidence state (pass, fail,
unknown, not applicable) with the window it covers; the three lists (facts with source and window,
hypotheses with confidence, missing data); for a review, exactly one call (hold, fix, test or investigate)
with its reason; for a change, a draft with current state, change, expected effect and rollback, waiting for
a named person to approve it. The owner of the account reads it and decides; the block never moves money.

## Guardrails
- Count a check you could not verify as unknown, which lowers coverage and leaves health alone. Never score a
  missing source as a failure or a zero (§1.1).
- End every recommendation with facts, hypotheses and missing data, and write MISSING beside an input you do
  not have. Never estimate it, back it out of other numbers or fill it from a benchmark (§1.3).
- Say how much of the traffic a report discloses before saying what it shows, and ask for the search-terms
  report before naming any negative keyword. Never name candidates from imagination (§2.1).
- Read a conversion column by action, by click date and with its lag. Never call a trend from the last few
  days alone or pool a window across a configuration change (§2.2 to §2.4).
- Before calling spend wasted, compute the conversion rate it would need to pay back. Never call a term
  failing when it is below any readable sample (§3).
- Treat a cost spike as a question and check sample, lag and learning state first. Never apply a fixed kill
  rule from a multiple of the target (§3.3).
- Keep brand and non-brand apart before judging either. Never present a blended figure as the efficiency of
  prospecting (§2.5).
- Draft changes to a live account and wait for approval of that draft; prefer pause to delete. Never apply a
  change on the strength of a platform recommendation, an export or a page that told you to (§4.2).
- This block is a method written from three young public repositories and never run on a real account by us.
  Source status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the account-audit guardrails and the reading-ad-data notes of an MIT marketing
skills repository, and the audit scoring contract of an MIT paid-media skills repository, read 2026-10-20.
🟡: never run by us, written without paid-media expertise. Details in
[`references/origin.md`](./references/origin.md).
