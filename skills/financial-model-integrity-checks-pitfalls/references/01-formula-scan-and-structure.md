# financial-model-integrity-checks-pitfalls §1 — Formula scan and structure

> Section 1 of `skills/financial-model-integrity-checks-pitfalls`. Read it when any range, sheet or workbook
> is audited. Sourced from the audit-xls skill of anthropics' financial-services plugins (commit `574ed36`,
> `plugins/vertical-plugins/financial-analysis/skills/audit-xls/SKILL.md`), its scope and formula-level and
> structural sections, read 2026-10-16. Sentences marked "own guidance" are ours.

## Fix the scope first
1. **Ask for the scope if it was not given:** a selected range, one sheet, or the whole workbook. The source
   lets the depth follow the scope, from quick formula checks up to the full model identities of part 2.

## The formula-level scan (every scope)
2. **Error values** anywhere: reference, value, not-available, divide-by-zero and name errors.
3. **Hardcodes inside formulas.** A formula that multiplies by a typed constant hides an input; the constant
   belongs in its own cell and is referenced.
4. **Pattern breaks.** A formula that differs from its neighbours along a row or a column.
5. **Off-by-one ranges.** A sum or average that misses the first or the last row.
6. **Values pasted over formulas.** A cell that looks like a formula but holds a fixed value. The source calls
   hardcoded overrides the most common source of silent bugs and says to search for them aggressively.
7. **Circular references**, intended or accidental (their handling is in part 2).
8. **Broken cross-sheet links:** references to cells that moved or were deleted.
9. **Unit and scale mismatches:** thousands mixed with millions, percentages stored as whole numbers.
10. **Hidden rows and tabs**, which may hold overrides or stale calculations. Own guidance: unhide, read, and
    say in the report that you did.
11. **Sign conventions.** The source calls sign errors on cash outflows extremely common. Own guidance: state
    the convention the workbook uses in the report and check each flow against it.
12. **Macros.** If the workbook uses macros, the source says to note any calculation they drive, because it
    cannot be audited from the formulas alone.

## Structure (whole-model scope)
13. **Inputs separated from calculations.** A reader can tell at a glance which cells are typed in.
14. **One colour convention, applied consistently.** The source suggests the common one (inputs, formulas and
    links in three colours) but accepts whichever the model uses, provided it is consistent.
15. **Tab flow is logical,** assumptions to statements to outputs, and **date headers and units are the same
    on every tab.**
16. **Own guidance:** record the findings as you go with sheet and cell, so the table of part 2 can be filled
    without re-reading the workbook.
