# dpa-review-pitfalls §1 — The material

> Section 1 of `skills/dpa-review-pitfalls`. Read it first, when a document is handed over for review.
> Sources: `SKILL.md` and `references/source-verification-rules.md` of the dpa-review skill in
> `The-Data-Galaxy/dpa-review-skill` (commit `c225d1f`), and the data-protection points of the review-contract
> skill in `anthropics/knowledge-work-plugins` (commit `33eeda1`), re-read 2026-10-16. Sentences marked "own
> guidance" are ours.

1. **Start from what the user supplied, and say so.** Treat the file or pasted text as the document under review
   and label it user-provided. State whether a version, an effective date or a "last updated" line is visible
   in it, and that the current official version of the vendor's terms was not checked unless it was. Do not go
   looking for a newer version unless the user asks, the file is visibly incomplete or an index page, or the
   conclusion depends on whether this is the binding version (the source's reasons for checking).
2. **Classify before reviewing.** Put the document in one class: a DPA or processing addendum with a full body;
   a service agreement with data-protection clauses scattered through it; a privacy notice or policy; a page
   about telemetry, product improvement, AI training or reuse of customer content; an index, a download page
   or a table of contents; one clause or a few clauses sent alone. The source runs a different review mode for
   each of these, which is the point: the question asked of a notice is not the question asked of a DPA.
3. **Stop when it is not the thing asked for.** For a notice, a marketing page or an index, do not force a review.
   Say what the document is, why it is not enough, which document to collect next, and whether any of its
   content is still useful as background. A download page is not the file it points to; name the file if you can
   guess it, and do not review the page as if it were the file.
4. **Service clauses and product-data clauses get their own question.** For scattered clauses: what do they
   cover and what is missing before they would amount to a processing agreement, and does a separate DPA
   look necessary. For a telemetry or training clause: scope, the right to opt out, retention, onward sharing
   and conflicts with the confidentiality terms or the instructions. For one clause alone: what it does, what
   it assumes, and which neighbouring provisions it depends on.
5. **Check completeness.** List what the text refers to and the file lacks: the main agreement, annexes, the
   description of security measures, the list of subprocessors, the transfer terms or clauses, the lists of
   data categories and of data subject categories, and regional addenda. A missing piece is a finding in its own
   right and it also caps how confident any later conclusion can be.
6. **State a confidence level for the source.** The source uses three: high for official current full text with
   annexes present or irrelevant; medium for a user-provided full text that looks complete, or official
   text with annexes missing; low for excerpts, an unclear version, an unofficial mirror or missing key
   schedules. Say which one applies, and why.
7. **Controller-to-controller is a different document.** If the agreement allocates both parties as
   controllers, or as joint controllers, the processor-contract checks of part 3 do not fit. Say so and stop
   at classification (own guidance).
8. **Do not imply checks that were not made.** A privacy notice, an impact assessment, a prior review or a
   standard template compared against it count only if the user supplied them or asked for the check. If absent,
   write "not checked", not nothing.
