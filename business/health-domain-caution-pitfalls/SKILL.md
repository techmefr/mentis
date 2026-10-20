---
name: health-domain-caution-pitfalls
description: "Use when content, a feature or a message touches health, medicine or wellbeing: copy that tells a reader what is wrong with them, a claim that a product treats or prevents something, a symptom checker or chatbot that answers like a clinician, health data collected for convenience and kept forever, an anecdote used as evidence. Scope of what may be said, claims and evidence, escalation and disclaimers, health data handling as method. Never medical advice, never a clinical claim; legal status of a product as a medical device or health data law is for the qualified owner, not legal advice."
---

# health-domain-caution-pitfalls

Business layer (`business/README.md`). Health is where a plain mistake in wording or data handling can hurt a
person, so the default is narrower than elsewhere: say less, source more, hand off sooner. This block is a method
for the people who write, build or review such material. It gives no medical advice and states no clinical claim.
Personal-data rules are `business/data-protection`; claim checking in general is
`business/marketing-claim-substantiation-pitfalls` and `business/product-marketing` §2; disclosure of generated
content is `business/ai-content-disclosure-and-provenance-pitfalls`; privacy of a person in a file is
`business/data-protection`.

Whether a product counts as a regulated medical product, what a regulator allows to be claimed, and which health
data law applies are decided by a qualified owner (regulatory, legal, clinical). Not legal advice, not medical
advice. This block never answers them.

## When
- Copy, a page, an email or a post mentions a condition, a symptom, a treatment, a supplement or a result on the
  body or mind.
- A feature or a conversational agent receives health questions or health data.
- A health claim from a vendor, a study or a customer is about to be repeated.

## Steps

**Read only the section the task meets.** §1 for words; §2 for evidence and claims; §3 for data and features.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What may be said: informing versus advising, no diagnosis, escalation and emergency wording, disclaimers that do not replace the rule | content or a script is written | [`01-what-may-be-said.md`](./references/01-what-may-be-said.md) |
| 2 | Evidence and claims: reading a study, anecdotes, risk wording, before and after, claims from vendors and customers | a claim is made or repeated | [`02-evidence-and-claims.md`](./references/02-evidence-and-claims.md) |
| 3 | Data and features: why a datum is health data, minimum collection, access, retention, assistants and symptom tools, a human who reviews | a feature or a data flow touches health | [`03-data-and-features.md`](./references/03-data-and-features.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: for content, a list of every health statement with its
source and date and the name of the qualified reviewer; for a feature, a note of what health data is touched, why,
for how long, who sees it, and where a person is sent when the tool cannot answer.

## Guardrails
- Inform in general terms and point to a qualified professional. Never tell a reader what they have, what to take
  or what to stop taking (§1).
- Write the emergency path first for any feature that may meet an urgent case. Never rely on a disclaimer alone (§1).
- Source each health statement to a primary document read and dated, and have a qualified person review it. Never
  repeat a headline, a vendor line or a customer story as evidence (§2).
- Say what the evidence does not show. Never turn an association into a cure or a prevention (§2).
- Collect the minimum health data, keep it for a stated time and limit who sees it. Never collect it for convenience
  (§3).
- Keep a human in the loop for anything a person might act on with their body. Never let a generated answer stand
  as clinical guidance (§3).
- Send regulatory status, health data law and liability to the qualified owner. Never settle them here.
- This block is a method from general practice, with claim-substantiation points checked against public US agency
  guidance; it has had no clinical or regulatory review and was never run by us on a real health product. Status and
  open points are in [`references/origin.md`](./references/origin.md).

## Origin
Written from general practice in health communication and health-data handling; claim-substantiation points checked
against US Federal Trade Commission, FDA and CDC public pages (facts only, read 2026-10-20). 🟡: never run by us. Details in [`references/origin.md`](./references/origin.md).
