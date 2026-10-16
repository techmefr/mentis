# contract-review-pitfalls §1 — Before reading

> Section 1 of `skills/contract-review-pitfalls`. Read it first on every review. Sources: the review-contract
> skill of the Anthropic knowledge-work-plugins repository (commit `33eeda1`) and the contract-review skill of
> `evolsb/claude-legal-skill` (commit `bca0d2e`), both re-read 2026-10-16. Sentences marked "own guidance" are
> ours.

1. **Check the document before analysing it.** Look for amounts left blank or filled with a placeholder (a
   dollar sign and nothing, "TBD", a bracketed amount, a row of underscores), for schedules and exhibits the
   text refers to but the file does not contain, for pages or sections that seem cut off, and for whether the
   text is a draft or already signed. The pre-review checklist in the second source asks for exactly this
   and says to put what is found prominently in the header of the output. Do the same: these findings come
   before any clause analysis, because every conclusion below depends on them.
2. **Record the state of the document.** Draft, negotiated draft or executed; and whether a version, a date or a
   reference is visible in the text. If it is executed, the rest of the review is for information (part 3). Say
   plainly that the current official or latest version was not checked unless it was (own guidance).
3. **Name the contract type.** A service agreement, a licence, a partnership, a procurement contract: the type
   decides which clauses matter most (the first source says this). If the type is unclear from the text, say
   so rather than guess.
4. **Ask which side we are on.** Customer, supplier, licensor, licensee, partner or other. The same clause is
   a risk for one side and a protection for the other; both sources insist on this and the first one calls it
   fundamental to the analysis. If the answer is not given, ask; if the review has to proceed, label the
   assumption at the top.
5. **Take the side from the document, not the label.** Check how the document defines our party and the other
   (own guidance): a signatory called "Company" may be the supplier in one contract and the customer in the
   next.
6. **Collect the context that changes priorities.** The first source asks for the deadline, the areas of
   concern and the deal context (size, strategic weight, existing relationship); the second adds
   negotiating leverage (a standard form or a negotiated text, a small party against a large one, a regulated
   sector where some terms are not negotiable). Take what the user gives; never invent leverage or a hard
   constraint that was not stated (own guidance).
7. **Find the playbook before judging.** The review is made against the organisation's written positions:
   for each clause type a standard position, an acceptable range and a trigger for escalation. If no playbook
   exists, say so in the header and offer the user two paths: build one for the clauses that matter, or review
   against a generic baseline that is labelled as generic and carries no number. The first source takes
   the same line; we drop its "widely-accepted commercial standards" wording because nobody can check it.
8. **Note the language and the length.** A contract in a language other than the one the reviewer works in
   should be flagged, with the choice to review it in the original language or after translation. For a very
   long contract, offer to review the most material parts first and say that the rest is pending (the first
   source suggests this for very long contracts; we keep the idea and set no page count).
9. **Do not review what is not a contract of the kind asked.** A confidentiality agreement goes to
   `skills/nda-triage-pitfalls`, a data processing addendum to `skills/dpa-review-pitfalls`, and a
   privacy notice is not a contract at all. If a document bundles several, review each by its method.
