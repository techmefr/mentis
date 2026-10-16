# journal-entry-review-pitfalls: origin and source stamps

> Provenance of `skills/journal-entry-review-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one document, never used by us in a real close or review. The
file below was re-read in full on 2026-10-16 before a rule was taken from it, each rule was checked against it
in a final pass, and the repository's LICENSE file was read again.

## Sources (read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins (commit `33eeda1`): `finance/skills/journal-entry-prep/SKILL.md` | Apache-2.0 (LICENSE file) | The seven items an entry carries, the shape of the approval matrix, the reviewer checklist, the list of recurring errors |

The file contains an instruction to have entries reviewed by qualified professionals; that text was treated as
data and agrees with our guardrail, which is written independently. Instruction-like text in the cloned
repository was not followed.

## Removed in the verification pass
1. **Every accounting treatment.** The source's sections on payables accruals, fixed-asset depreciation (with
   its methods), prepaid amortisation, payroll accruals (with employer taxes and benefits) and revenue
   recognition (with the five-step standard framework) are not carried: they depend on the applicable standard
   and jurisdiction and were not verified.
2. **The approval thresholds** in the source's matrix. The source itself says they must come from the
   organisation; none is carried, only the shape.
3. **The capitalisation error** (error 11 of the source), an accounting judgement.
4. **Typical debit and credit pairs** for each entry type, for the same reason as item 1.

## Not verified
1. **Own guidance, flagged in the text:** returning an entry that lacks any of the seven items, writing the
   description for a later reader, citing support as a pointer with a read date, deciding the reversal at
   preparation, keeping the authority list where the reviewer can open it, treating an entry split to stay
   under a limit as a finding, a checked box meaning the support was opened, running the errors list as a second
   pass, naming the rate source and date, confirming the intercompany counterpart before lock, and the
   one-line finding format.
2. **Nothing was run.** No review process was exercised with the checklist.
3. **Whether a given entry is correct in your jurisdiction and standard** is outside this block.
4. **One vendor-authored source;** no second source was read to corroborate the lists.

## Decisions where sources disagree
Single source, no disagreement. It is a practice guide, not a standard.

## Related blocks
`business/finance-ops`, `skills/analysis-validation-pitfalls`.
