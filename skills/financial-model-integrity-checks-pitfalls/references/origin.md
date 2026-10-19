# financial-model-integrity-checks-pitfalls: origin and source stamps

> Provenance of `skills/financial-model-integrity-checks-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one document, never used by us on a real workbook. The file below
was re-read in full on 2026-10-16 before a rule was taken from it, each rule was checked against it in a final
pass, and the repository's LICENSE file was read again.

## Sources (read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/financial-services (commit `574ed36`): `plugins/vertical-plugins/financial-analysis/skills/audit-xls/SKILL.md` (the same skill is copied under several agent plugins; only this copy was read) | Apache-2.0 (LICENSE file) | Scope choice, formula-level scan, structure review, the identities by statement, circular reference handling, edge cases, report columns and severities, the "report first" rule |

Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **Valuation-specific rules.** The source's rule about the share of a terminal value in an enterprise value,
   its list of discount-rate and discounting mistakes, and its model-type-specific bug lists for discounted
   cash flow, leveraged buyout and merger models are not carried: they are valuation theory and investment
   territory, and their thresholds are unsourced.
2. **Numeric and benchmark flags:** the revenue-growth flag, the "outside industry norms" margin test and the
   terminal-value share flag. They are arbitrary or unsourced.
3. **The tax-rate and share-count checks** of the income statement section: they depend on the tax rules and
   the instruments in play and were not verified.
4. **Goodwill and intangible flow** from acquisition assumptions: a deal-accounting matter, not read.
5. **The three-statement-specific bug list** was folded into the identities of part 2 where it is arithmetic
   (working-capital signs, depreciation agreement); its debt-maturity and dividend remarks were not carried.
6. **Other copies of the skill** under the agent plugins were not compared with the one read.

## Not verified
1. **Own guidance, flagged in the text:** recording findings with sheet and cell as you go, unhiding and saying
   so, stating the sign convention, changing one input at a time to see which identity fails first, treating
   odd compounding as a prompt to ask, applying the tie-out test to every total with a breakdown, and closing
   the report with the scope of the claim.
2. **Nothing was run.** No workbook was audited with these steps.
3. **Whether a model's assumptions or valuation are sound** is outside this block by design.
4. **One vendor-authored source,** young and written for a specific tool; spreadsheet products differ in how
   they flag circular references and hidden content.

## Decisions where sources disagree
Single source, no disagreement.

## Related blocks
`skills/analysis-validation-pitfalls`, `business/finance-ops`.
