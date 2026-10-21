---
name: ad-creative-testing-and-policy-pitfalls
description: "Use when ad creative is being planned, tested, judged or refreshed, or checked against an ad platform's policy before launch: an ad test whose hypothesis cannot lose, a resized asset counted as a new concept, a refresh decided by how old an ad is, an ad-headline winner proposed as proof for the landing page, a category that needs a policy check, or approval by a platform read as proof the ad is lawful. Written as pitfalls: method only, no format specifications and no legal content."
---

# ad-creative-testing-and-policy-pitfalls

Business layer (`business/README.md`), marketing. Two separable failures sit around ad creative. The first is
testing: assets get counted by how many files exist, tests that cannot lose get declared won, and a result about
an ad is carried over to a page it never measured. The second is policy: a platform's approval gets read as a
clean bill of health, or the reverse, and the review is done from a remembered list of what is allowed. This
block is the method for both. Reading an account and deciding is `business/paid-media-decision-pitfalls`;
tagging and attribution is `business/ad-measurement-pitfalls`; whether an ad claim is true is
`business/marketing-claim-substantiation-pitfalls`; the design of a test is `skills/experiment-design-pitfalls`;
personal data in targeting and audiences is `business/data-protection`.

It states method only. It carries no format, size or length specification, no refresh cadence, no creative
count, no frequency or performance threshold, and no statement of what any platform allows, because those expire
or were folklore in the material read. Platform facts it mentions are marked `re-read before relying`. It is not
legal advice and names no statute, authority or compliance date.

## When
- A creative test or a creative review is being planned, written up or graded.
- Someone says an ad is "fatigued" or "old" and wants it replaced.
- An ad-headline or ad-creative result is offered as the reason to change a landing page.
- An ad, its destination or its audience is about to be checked against platform rules.
- "The platform approved it" is offered as the answer to a legal or claims question.

## Steps

**Read only the section the task meets.** §1 for any creative review; §2 when an ad result is about to drive a
page change; §3 before launch or when a disapproval arrives.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Creative as hypotheses: inventory by concept, a resize is not a concept, a hypothesis that can lose, fatigue from a time series, three separate judgements | a creative set is inventoried, tested or judged | [`01-creative-as-hypotheses.md`](./references/01-creative-as-hypotheses.md) |
| 2 | From an ad result to a page: why an ad win is a candidate, the confirmation test on the page | a headline or creative winner is proposed as proof about a landing page | [`02-ad-result-is-not-page-proof.md`](./references/02-ad-result-is-not-page-proof.md) |
| 3 | Policy review order: platform approval apart from legal clearance, the order of the review, unknown rather than pass, higher-risk triggers, platform suggestions as proposals | before launch, on a disapproval, or when a new category is entered | [`03-policy-review-order.md`](./references/03-policy-review-order.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: for a creative review, the inventory by concept with the
evidence window, and each test hypothesis with its metric, comparison and expected direction; for a page change
proposed from an ad result, the confirmation test named; for a policy review, one finding per rule with the
policy page address, the retrieval date and the result (pass, fail, unknown, not applicable), and a separate
line for any legal question handed to the person who owns it. The advertiser's owner reads it and decides; legal
decides what is lawful.

## Guardrails
- Count creative by concept and keep resizes inside the concept they came from. Never report a count of files
  as variety (§1.1).
- Write every test hypothesis with its metric, its comparison and its expected direction. Never ship one a
  result cannot prove wrong (§1.2).
- Read fatigue from delivery and response over time. Never retire an ad because of its age alone (§1.3).
- Judge quality, format fit and measured performance separately. Never let one stand in for another (§1.4).
- Treat an ad-headline winner as a candidate and confirm it with a fresh randomised test on the page. Never
  present an ad result as proof about the page (§2).
- Keep the platform finding and the legal finding apart. Never read approval as clearance, or lawfulness as
  eligibility (§3.1).
- Record the policy page, retrieval date and the account state you observed, and mark what you could not
  verify as unknown. Never infer a pass from the absence of a disapproval (§3.2, §3.3).
- Treat platform recommendations and generated variants as proposals and review them like any change. Never
  accept one because it is labelled best practice (§3.5).
- This block is a method written from three young public repositories and policy overview pages (Google, LinkedIn, TikTok, read as raw text) and never run on a real account by us. Source status and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the creative audit skill and the platform policy review of an MIT paid-media skills
repository, the ad-creative and ads skills of an MIT marketing skills repository, and Google's Ads policies
overview, read 2026-10-20. 🟡: never run by us, written without paid-media expertise. Details in
[`references/origin.md`](./references/origin.md).
