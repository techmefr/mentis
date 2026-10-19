# nda-triage-pitfalls: origin and source stamps

> Provenance of `skills/nda-triage-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two repositories' text, never run by us on a real NDA. Each source
file was opened again on 2026-10-16 before a rule was written and each rule was checked against it in a final
pass. This block states no law and no number.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| `anthropics/knowledge-work-plugins`, commit `33eeda1`, `legal/skills/triage-nda/SKILL.md` (licence file `legal/LICENSE`, read) | Apache-2.0 | Routing instead of signing, playbook then defaults, structure check, the question groups (definition, obligations, exclusions, recipients, term, return, remedies, governing law), provisions to flag, the not-really-an-NDA rule, the report shape |
| `evolsb/claude-legal-skill`, commit `bca0d2e`, `skill.md`, NDA checklist table (LICENSE file read, copyright Christopher Sheehan) | MIT | Direction question, compelled disclosure, no-contact and announcement checks, return certification, injunctive relief wording |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **All numeric terms** from both sources (agreement term in years, survival in years, a marking window in
   days, "typical" years in the second source, a turnaround in business days): market claims with no cited
   source, which also differ between the two sources. They belong in the organisation's playbook.
2. **The numeric ceilings** the first source uses to separate its middle and top levels (a term of ten years
   or more, a longer-than-standard term in examples).
3. **The "narrow residuals" definition** (retained in unaided memory, excluding trade secrets and patentable
   information): a drafting position of the source, not checked; the block only flags any residuals clause.
4. **The redline approaches and standard positions** of the first source (for instance a twelve-month limit
   on a non-solicit offered as a compromise): negotiating advice with no cited basis.
5. **The "Common NDA Issues" list and the report table with pass, flag and fail**: restated as questions.
6. **Colour labels** (green, yellow, red): replaced by three named routes.

## Not verified
1. **Own guidance, flagged in the text:** the number-free defaults, perpetual duties for trade secrets as a
   question for counsel, route higher when in doubt, no drafting of counter-terms, stating the basis of the
   triage and which version was read.
2. **The list of exclusions and of misplaced provisions** is the two sources' drafting practice and was not
   checked against a legal text or a model clause set. It is presented as questions for counsel.
3. **No lawyer has reviewed this block.**

## Decisions where sources disagree
The two sources give different durations and a different wording of what counts as standard; none is carried.
They agree on the list of misplaced provisions, which the second extends with no-contact and announcement
clauses; both extensions are kept as flags.

## Related blocks
`skills/contract-review-pitfalls`, `skills/dpa-review-pitfalls`, `business/legal-documents`,
`business/regulatory-watch`, `skills/source-freshness`.
