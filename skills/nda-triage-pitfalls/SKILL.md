---
name: nda-triage-pitfalls
description: "Use when a confidentiality agreement (an NDA, or a confidentiality section inside a larger agreement) arrives from sales, a partner or a supplier and must be routed before anyone signs: identifying its shape, a question list on the definition, exclusions, recipients, duration, return and remedies, provisions that do not belong in an NDA, and routing to standard approval, counsel review or full legal review."
---

# nda-triage-pitfalls

Business layer (`business/README.md`), legal. A triage is for routing, not for signing: its output is the
answer to "who must look at this before it is signed", with the reasons. The usual failures are a
non-solicitation clause hidden in an NDA signed by sales, a missing exclusion found at the first dispute, and
a commercial agreement approved as if it were an NDA. The method is a short question list answered from the
text, with the organisation's written NDA playbook deciding what is acceptable. It states no legal rule and
no number. A full review of a larger agreement is `skills/contract-review-pitfalls`; personal-data clauses are
`skills/dpa-review-pitfalls`.

## When
- An NDA or mutual NDA arrives from a business contact and someone asks whether it can be signed.
- A larger agreement contains a confidentiality section that needs a quick screen.
- A counter-draft of an NDA comes back with changes.

## Steps

**Read only the section the task meets.** Part 1 first, then part 2.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Shape and question list: the kind of agreement, the playbook, the questions answered from the text | an NDA arrives and must be screened | [`01-shape-and-questions.md`](./references/01-shape-and-questions.md) |
| 2 | Misplaced provisions and routing: what does not belong in an NDA, the three routes, the report | the screen is done and the result must be routed | [`02-misplaced-provisions-and-routing.md`](./references/02-misplaced-provisions-and-routing.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the shape of the agreement and whether it fits the
business reason; the answer to each question with the quoted words (or "absent"); the provisions found that do
not belong in an NDA; the route chosen (standard approval, counsel review or full legal review) with the
reason; whether a playbook or a labelled list of defaults was used; and the standing line that it is a
screening for counsel, not legal advice.

## Guardrails
- This triage does not replace legal advice. The decision to sign, the wording of any counter-proposal and the
  final reading belong to a qualified lawyer.
- Never state that a clause is enforceable or unenforceable, valid or void: that depends on the jurisdiction
  and belongs to counsel.
- Never write counter-terms for the other party without counsel (part 2).
- Never send an NDA to standard approval with a question left unanswered or a flag unresolved (part 2).
- Never treat a duration, a notice period or a list of exclusions as "standard" without a source: the
  carve-out list in the sources is drafting practice, and numbers belong in the organisation's playbook (part 1).
- Do not paste a real NDA or the names of the parties into a public prompt, ticket or log beyond what the
  triage needs.

## Origin
Rewritten from two practitioner skills (Apache-2.0 and MIT), read 2026-10-16; provenance, what was removed
and what is our own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
