---
name: contract-review-pitfalls
description: "Use when an incoming or outgoing commercial contract (service, SaaS, licence, supply, partnership) is to be reviewed before signature: checking that the document is complete and in what state, fixing which side we are on, reading all of it before flagging, a question per clause category answered with quoted text, internal consistency, triage as acceptable, negotiate or escalate against a written playbook, and the output a reviewer can hand to counsel."
---

# contract-review-pitfalls

Business layer (`business/README.md`), legal. A review of a contract is a list of questions answered from the
text of that document, never from what such contracts usually say. The failure modes are known: reading the
contract through a default lens (always the customer's, always the vendor's), findings that quote nothing,
blank amounts and missing schedules found after signature, a "market standard" invented on the spot and a
redline with no fallback. This block is the method for avoiding them. It states no legal rule and no number;
thresholds come from the organisation's own written playbook. Public documents a product publishes are in
`business/legal-documents`; the personal-data clauses of a contract are handed to `skills/dpa-review-pitfalls`;
a short confidentiality agreement goes to `skills/nda-triage-pitfalls`; a regulation or a deadline cited inside
a contract goes through `business/regulatory-watch`.

## When
- A contract, an order form or terms of service from a supplier or a customer arrives for review.
- Someone asks "is this contract fine to sign" or "what should we push back on".
- A negotiated draft comes back and its changes must be compared with what was agreed.
- A contract is already signed and someone asks what it says (information only, see part 3).

## Steps

**Read only the section the task meets.** Part 1 comes first on every review; parts 2 and 3 follow in order.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Before reading: state and completeness of the document, which side we are on, the playbook | a contract is about to be analysed | [`01-before-reading.md`](./references/01-before-reading.md) |
| 2 | Reading: whole document first, clause categories as questions, quoted evidence, internal consistency | the completeness check is done and the text is being analysed | [`02-reading-the-clauses.md`](./references/02-reading-the-clauses.md) |
| 3 | Triage and output: acceptable, negotiate or escalate, the redline record, the acceptable section, the closing line | findings must be turned into a deliverable | [`03-triage-and-output.md`](./references/03-triage-and-output.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a header stating the document, its state, our side and
whether a playbook or a labelled generic baseline was used; the completeness findings first; per clause
category a status (present, absent, unusual) with the quoted text; a triage level per finding; the negotiation
items with their record; an acceptable-terms section; the escalations with who decides; and the closing line
that this is a working review for qualified counsel.

## Guardrails
- This review does not replace legal advice. The decision to sign and the final reading belong to a qualified
  lawyer, who also decides what is enforceable, in which jurisdiction.
- Never state that a clause is enforceable or unenforceable, and never state what is "market standard" or
  "typical". Any number goes in the organisation's playbook, not in the review.
- Never flag from a clause alone before the whole document has been read (part 2).
- Never write a finding without the exact text it rests on, or the statement that the text is absent.
- Never review a document that is visibly incomplete as if it were whole: say what is missing first (part 1).
- Never assume which side we are on (part 1).
- An executed contract is reviewed for information only; do not propose redlines on it (part 3).
- Do not paste a real contract, a party name or a price into a public prompt, ticket or log beyond what the
  review needs.

## Origin
Rewritten from two practitioner skills, each Apache-2.0 or MIT licensed, read 2026-10-16; the provenance, what
was removed and what is our own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never
dogfooded.
