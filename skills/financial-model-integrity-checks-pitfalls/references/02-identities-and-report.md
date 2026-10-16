# financial-model-integrity-checks-pitfalls §2 — Identities, circularity and the report

> Section 2 of `skills/financial-model-integrity-checks-pitfalls`. Read it when a whole model is audited or
> will not balance. Sourced from the same audit-xls skill (commit `574ed36`), its balance sheet, cash flow,
> income statement, circular reference, reasonableness, report and notes sections, read 2026-10-16. The
> source's valuation and deal-specific lists are not carried (see `references/origin.md`). Sentences marked
> "own guidance" are ours.

## Identities that must hold in every period
1. **The balance sheet balances.** Total assets equal total liabilities plus equity, in every period. The
   source puts this first: if it fails, quantify the gap per period and trace where it opens, because
   nothing downstream can be trusted until it is fixed.
2. **Retained earnings roll forward.** The prior balance, plus net income, less distributions, equals the
   current balance.
3. **Cash ties out.** Ending cash on the cash flow statement equals cash on the balance sheet, every period.
4. **The cash flow sections sum.** Operating, investing and financing flows add up to the change in cash.
5. **Cross-statement agreement.** Depreciation and amortisation on the cash flow statement equal those on the
   income statement, and capital spending on the cash flow statement agrees with the movement in the fixed
   asset schedule on the balance sheet.
6. **Working-capital signs follow the balance movements.** A rise in receivables, payables or inventory has
   the sign the balance sheet implies.
7. **Revenue build ties** to its segment or product detail. Own guidance: the same test applies to any total
   that has a breakdown elsewhere in the workbook.

## Circular references
8. **Intentional loops need a working switch.** The source's example is interest feeding the debt balance
   feeding cash feeding interest. If the loop is intentional, check that the iteration toggle exists and
   works; if it is not, trace the loop and say how to break it.

## Edge cases
9. **Run the model off its happy path.** The source asks whether it breaks at zero or negative growth or with
   negative earnings, and whether a balance that should stay positive turns negative. Own guidance: change one
   input at a time and watch which identity above fails first.
10. **Growth that compounds to an absurd size** or out-year ramps with no stated cause are prompts to ask the
    owner, not findings by themselves. Own guidance: this block sets no growth or margin threshold; the source's
    numeric flags and its "industry norms" test were not sourced and are dropped.

## The report
11. **One row per finding:** number, sheet, cell or range, severity, category, issue, suggested fix.
12. **Severity.** Critical means a wrong output (the balance sheet does not balance, a formula is broken, cash
    does not tie); warning means risky (hardcodes, inconsistent formulas, edge-case failures); info means
    style (colours, layout, naming).
13. **A summary line first** for a whole model: overall state (clean, minor issues, major issues) and the count
    of critical, warning and info rows.
14. **Report first, change nothing without being asked.**
15. **Scope of the claim.** Own guidance: end the report by saying it checks arithmetic and wiring, not
    assumptions or valuation, and that a chartered accountant or financial adviser judges those.
