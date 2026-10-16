# contract-review-pitfalls §2 — Reading the clauses

> Section 2 of `skills/contract-review-pitfalls`. Read it once the completeness check is done and the text is
> being analysed. Sources: the review-contract skill (commit `33eeda1`) and the contract-review skill
> (commit `bca0d2e`), re-read 2026-10-16; the clause categories are the two sources' lists merged and
> reduced. Sentences marked "own guidance" are ours.

1. **Read the whole document before flagging anything.** The first source gives the reason: clauses interact.
   Its own example is an indemnity with no cap that a broad exclusion of liability may soften. The reverse
   also happens (own guidance): a carve-out from a cap can swallow the cap. A flag raised on a clause read in
   isolation is a draft finding, not a result.
2. **Each category is a question, answered present, absent or unusual.** For every category below, say whether
   the document has a provision, has none, or has one that reads out of the ordinary, and quote the exact
   words the answer rests on. When the answer is absent, say it in so many words: the second source
   asks for a table of missing provisions for this purpose.
3. **Liability.** Is there a cap, and on what is it based; is it the same for both parties; which liabilities
   sit outside it; which kinds of loss are excluded and are the exclusions mutual; does the cap apply per
   claim, per period or in total.
4. **Indemnity.** What triggers it; one party or both; whether it is inside or outside the cap; who controls the
   defence and the settlement; how it relates to the liability clause. An indemnity for any breach at all is a
   reason to look at the cap again (first source).
5. **Intellectual property.** Who owns what each party brings and what is made during the work; how far an
   assignment or a work-for-hire clause reaches; the scope of every licence granted (exclusive or not,
   territory, sublicensing); what a clause on feedback gives away; where open-source components matter.
6. **Personal data.** Whether a processing agreement is required and present, and how our party is described in
   it. This block does not review those terms: hand them to `skills/dpa-review-pitfalls`. Whether any rule
   applies is not decided here.
7. **Confidentiality.** Scope, duration, exceptions, what happens to the information at the end. For a stand-alone
   confidentiality agreement use `skills/nda-triage-pitfalls`.
8. **Warranties and disclaimers.** What is promised, what is disclaimed ("as is" included), how long a warranty
   lasts and what remedy it carries.
9. **Term, renewal and exit.** Length; renewal and whether it is automatic; the notice window to stop it, with
   its date written down; termination without cause and with cause, and whether there is a period to cure;
   what is owed on termination: return of data, help with transition, surviving clauses.
10. **Suspension.** Whether a party can suspend service, with or without notice and on which grounds.
11. **Assignment and control.** Who may assign; whether a change of control needs consent; whether the rights
    are symmetrical (second source: one party may assign and the other not).
12. **Money.** Payment terms, late charges, taxes, the way prices may change, minimum commitments, audit rights
    and who bears the cost of an audit.
13. **Disputes.** Governing law, forum or arbitration seat, any waiver of a type of proceeding, who pays costs.
    Whether a given choice is acceptable depends on the jurisdiction: say so and leave it to counsel.
14. **Other.** Insurance (what is required and what proof), force majeure (scope, notice, right to terminate),
    unilateral amendment rights, exclusivity and non-compete, wording such as "sole discretion" that leaves
    a party with no objective standard (second source).
15. **Internal consistency.** Check the document against itself, as the second source does: a term defined in
    one place and used with a different meaning or a different capitalisation elsewhere; a cross-reference
    to a section or a schedule that does not exist; a number or a date given twice with different values; a
    clause that gives with one hand what another takes back.
16. **Quote, do not paraphrase.** Each finding carries the clause number and the exact text. If a finding has
    no quote and is not an "absent" finding, it is removed. This is the one rule that separates a review from
    an opinion.
17. **Leave out what is not in the text.** Do not fill a gap with what the contract "probably" means or with
    what such contracts usually contain. A gap is a finding. Where the meaning is unclear, say it is unclear
    and ask counsel (the second source lists this as a guardrail: only refer to text that is actually in the
    document).
