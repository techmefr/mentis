---
name: customer-email-review-pitfalls
description: "Use when a customer-facing email draft is reviewed before sending: checking it against the source (transcript, thread, notes) for accuracy before tone, a dropped concern, owner or date, one ask near the top, length judged by ease of replying, bad news that leads with the customer's impact, the forwardable note, the executive email, the third chase, no numeric score, no commitments added in the rewrite, and a rewrite whose own advice is executable."
---

# customer-email-review-pitfalls

Not a step of the pipeline: a craft block for reading a drafted customer email the way a careful colleague
would before it is sent. The two parts share one premise: **a draft that is checked for tone and never for
truth is the failure**, because a wrong date, an invented commitment or a person who has left becomes the
customer's record of what was agreed, and polish does not make it less wrong. Writing the email from scratch is
out of scope; wording rules for interface text are in `business/ux-writing`, and the situation of an
outage or a security notice is in `business/incident-communication` and `security-advisory-comms-pitfalls`.

## When
- Someone pastes or points at a draft and asks whether to send it.
- A draft "feels off", or someone wonders how the customer will take it.
- A recap, a chase, an escalation, a note meant to be forwarded or an executive email is about to go out.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Review against the source, the checks, the verdict, the rewrite rules, the executable-advice check | any draft is reviewed | [`01-review-against-the-source.md`](./references/01-review-against-the-source.md) |
| 2 | What each email type owes and how each fails: recap, follow-up, bad news, forwardable note, executive email, intro request | the draft's type is known | [`02-checks-by-email-type.md`](./references/02-checks-by-email-type.md) |

## Output / checkpoint
A review is done when it states first whether to send, send with small changes, rework, or not send; names, for
each problem, the sentence and the fix; says which facts were checked against which source and which could not
be checked; and, where a rewrite is given, changes only what was named. Read the review once looking for a
numeric score, a commitment that was not in the original, and a recommendation that depends on something nobody
has confirmed. Nothing here was verified on real correspondence: the check is a read of the text. No pipeline
checkpoint; the sender owns the email.

## Guardrails
- Never judge a draft against itself; get the transcript, the thread or the notes, or say the facts were not
  checked (part 1).
- Never add a commitment, concern or next step in a rewrite (part 1).
- Never give a numeric score to a draft (part 1).
- Never manufacture criticism: a good draft gets "send it" (part 1).
- Never launder an unverifiable claim into cleaner prose; pull it out and flag it (part 1).
- Never recommend an action whose precondition was not checked (part 1).
- Put a note about missing data at the sentence it affects and list both candidates when two records match.
  Never bury a gap in a footer or pick the latest of two matches (part 1, §1.2b).
- Never send a forwardable note with a claim about the product that was not flagged for checking (part 2).
- This block is one small MIT repository's practice, never run by us on real correspondence; a second human read
  is warranted. Sources and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from the email-critic skill of a small customer-success skills repository (MIT), read 2026-10-16. 🟡:
never dogfooded; details in [`references/origin.md`](./references/origin.md).
