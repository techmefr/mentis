---
name: email-campaign-measurement-and-testing-pitfalls
description: "Use when an email campaign or lifecycle flow result is being read or reported, a subject-line or send-time test is planned, a segment is built from engagement (active, lapsed, never opened), or a benchmark is quoted: an open is a fetch not a reader, a click can be a fetch too, conversion from the system of record with its window, unsubscribe and complaint rates as guardrails, a holdout as the baseline for an always-on flow, tests on a metric that survives, and benchmarks ranked own history first."
---

# email-campaign-measurement-and-testing-pitfalls

Business layer (`business/README.md`), marketing. The recurring failure in email reporting is reading a
fetch as a person: an open count is quoted as readership, a subject-line test is won on opens, a "lapsed"
segment is defined by opens, and a vendor average stands in for the audience's own history. This block says
what a campaign metric can and cannot support, and what email adds to the general test discipline.

Test design is `skills/experiment-design-pitfalls` (one hypothesis, one primary metric fixed before sending,
sample size by formula, no peeking); this block does not restate it. Tagging, the single conversion and its
system of record, and why platform numbers differ are `business/ad-measurement-pitfalls`; two numbers that
disagree is `skills/metric-movement-diagnosis-pitfalls`; events and their privacy are
`skills/event-tracking-plan-pitfalls`; whether mail arrives at all is
`business/email-deliverability-and-sender-requirements-pitfalls`; consent and tracking law is
`business/data-protection`.

It carries no benchmark, no sample size, no test duration and no best send time: the sources disagree and
those figures are folklore. Platform facts it mentions were read on 2026-10-20 and are marked
`re-read before relying`. Not legal advice.

## When
- A campaign or flow result is being summarised, or a report says "open rate".
- A subject-line, content or send-time test is planned or its winner is being picked.
- A segment is defined by engagement, or contacts are about to be removed as inactive.
- A benchmark or an industry average is about to be quoted as pass or fail.
- An always-on flow's conversion rate is being called good.

## Steps

**Read only the section the task meets.** §1 before any engagement number is used.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What an open and a click are: a fetch of a resource, what privacy relays do, what to use instead, the click hypothesis | an open or click count is about to support a statement or a rule | [`01-opens-and-clicks.md`](./references/01-opens-and-clicks.md) |
| 2 | Conversion from the system of record, guardrails from the same send, holdout baseline, benchmark ladder | a result is reported, a flow is judged, or a benchmark is quoted | [`02-conversion-baselines-and-benchmarks.md`](./references/02-conversion-baselines-and-benchmarks.md) |
| 3 | What email adds to testing: metric first, the recipient as unit, the winner as a second decision, send time, engagement segments | a test is planned or read, or a segment is built | [`03-testing-and-segments.md`](./references/03-testing-and-segments.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: for a report, the metric the program is judged on, the
count behind it with its window and source system, the guardrails of the same send, the baseline used and
what kind it is (holdout, own history, vendor average labelled as such), and what is unknown. The owner of
the program reads it and decides.

## Guardrails
- Name the human action a program is judged on (a click that led to a session, a reply, a purchase, a login).
  Never use an open for segmentation, a sunset rule, a subject-line winner or an engagement score (§1.2).
- Treat a click as a possible fetch until a session on the destination backs it. Never present the scanner
  explanation as established: it is a hypothesis here (§1.3).
- Read conversion from the system of record with the attribution window written beside the number, and add
  the unsubscribe and complaint rates of the same send. Never call a lift in clicks a win when the
  unsubscribe rate rose with it (§2.1, §2.2).
- Use a holdout of eligible recipients as the baseline of an always-on flow. Never compare it with the
  organic rate or with last month (§2.3).
- Rank benchmarks: own history in a comparable window, own holdout, vendor averages last and labelled. Never
  quote a vendor average as pass or fail (§2.4).
- Fix the metric before the test and make the recipient the unit. Never test a subject line on opens, or on a
  segment built from opens (§3.1, §3.2).
- Treat a send-time or weekday claim as a hypothesis until it was run on this audience. Never carry the
  sources' "best days and hours" (§3.4).
- State which signal defined an engagement segment and over what window. Never call someone lapsed on opens
  (§3.5).
- This block is a method written from vendor guides and one primary page read through a digest, and never run
  by us on a real programme. Source status and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the analytics, testing and lifecycle notes of several MIT-licensed marketing
skill repositories, with Apple's Mail Privacy Protection page and RFC 8058 as primaries, read 2026-10-20.
🟡: never run by us, written without email-marketing expertise. Details in
[`references/origin.md`](./references/origin.md).
