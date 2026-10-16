---
name: dpa-review-pitfalls
description: "Use when a data processing agreement or addendum (or a service agreement with scattered data-protection clauses) from a supplier or a customer is to be reviewed: classifying the document before reviewing it, fixing our role and the review posture, checking for missing annexes, a data-processing overview before the terms, a term-by-term pass against the processor-contract content of GDPR Article 28, subprocessing, the processor-side boundary, and a signing gate that gives no comfort while role, annexes or transfer facts are unknown."
---

# dpa-review-pitfalls

Business layer (`business/README.md`), legal. `business/data-protection` part 4 says that a service which
receives personal data needs a processing agreement and leaves the content to the DPO or counsel; this block is
the method for reading the agreement itself. The failure modes are known: a privacy notice reviewed as if it
were a DPA, a role mix-up that flips every finding, an agreement accepted whose annexes were never seen, and a
document called "approved" while the schedules that matter were missing. The article-level checks rest on
Article 28 of Regulation (EU) 2016/679 as read on EUR-Lex on 2026-10-16 (original Official Journal text of
4.5.2016, not a consolidated version); the reader is told to read the current consolidated text before
relying on any of it. Other regimes were not read and are not covered. The block makes no legal conclusion
about any particular agreement.

## When
- A supplier sends its processing agreement, or a customer sends theirs, and someone must give a view.
- A service agreement contains data-protection clauses and someone asks whether a separate DPA is needed.
- A page about telemetry, product improvement or AI training is cited as the data terms of a service.
- Someone asks "can we sign this DPA".

## Steps

**Read only the section the task meets.** Part 1 first on every review; the others follow in order.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The material: user-provided source, classifying the document, completeness | a document is handed over for review | [`01-the-material.md`](./references/01-the-material.md) |
| 2 | Posture and overview: our role, jurisdiction, data, context, leverage, hard constraints; the data-processing overview | the document is a processing agreement and the review is about to start | [`02-posture-and-overview.md`](./references/02-posture-and-overview.md) |
| 3 | The terms against Article 28: processor-contract content, subprocessing, the processor-side boundary | the term-by-term review is run | [`03-terms-against-article-28.md`](./references/03-terms-against-article-28.md) |
| 4 | Signing gate: what to answer when asked whether to sign | someone asks to sign, approve or countersign | [`04-signing-gate.md`](./references/04-signing-gate.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the document class and its state; the posture, with each
assumption labelled; the completeness findings; the data-processing overview; a table of terms with status
(present, absent, unusual or unclear), the quoted text and the effect given our role; which findings are for
counsel; and the signing gate when asked. Every output ends by saying that a qualified lawyer reviews it
before anyone signs.

## Guardrails
- This review does not replace legal advice. The decision to sign, the reading of any clause and the final
  review belong to a qualified lawyer and, where the company has one, its data protection officer.
- Never review a document that is not a DPA as if it were one; say what it is and what to collect next (part 1).
- Never invent a hard constraint, a negotiating position, a party, a date or a subprocessor (part 2).
- Never take our role from a label such as "Company" or "vendor": read the definitions (part 2).
- Never mark a processor-side gap as a defect when it is a controller duty (part 3).
- Never give signing comfort while the role, the key annexes or the transfer facts are unknown (part 4).
- Never state a breach-notification delay, a transfer mechanism or a deletion period as law: those provisions
  were not read for this block and sit with counsel (part 3).
- Do not paste a real agreement, a party name or personal data into a public prompt, ticket or log.

## Origin
Rewritten from a DPA-review skill (Apache-2.0) and a contract-review skill (Apache-2.0), and checked against
Article 28 of Regulation (EU) 2016/679 read on EUR-Lex 2026-10-16; provenance, what was removed and what is our
own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
