---
name: financial-model-integrity-checks-pitfalls
description: "Use when a spreadsheet financial model (three-statement, budget or forecast workbook) is about to be shared or relied on and its arithmetic must be checked: formula-level scan for errors, hardcodes inside formulas, pasted-over values, off-by-one ranges, broken links, unit mix-ups and hidden sheets; structure review; the checks that must hold every period (balance sheet balances, cash ties out, roll-forwards, sign of working-capital movements); circular references; a findings table by severity."
---

# financial-model-integrity-checks-pitfalls

A craft block for checking whether a spreadsheet model **adds up**, not whether it is **right about the
world**. It audits the arithmetic and the wiring of a workbook: formulas, structure and the identities that
must hold in every period. It does not judge assumptions, forecasts or valuations, and it carries no rule about
discount rates, terminal values, deal structures or what a reasonable margin is: those are investment and
accounting judgement and are out of scope. The general pre-delivery review of a computed result is in
`skills/analysis-validation-pitfalls`; this block is the model-specific layer on top of it. Nothing here
replaces a chartered accountant, an auditor, or a legal, compliance or financial adviser, and nothing here is
investment advice.

## When
- A workbook is about to go to a manager, a bank, a board or a client and nobody has checked it end to end.
- A model "will not balance" or a total has moved for no visible reason.
- Someone else's model is inherited and needs to be trusted before it is extended.
- A formula was edited and the downstream sheets must be rechecked.

## Steps

**Read the part the scope needs.** Part 1 applies to any range, sheet or workbook; part 2 to a whole model.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Formula-level scan and structure: error values, hardcodes, pattern breaks, ranges, pasted values, links, units, hidden cells, input separation | any range, sheet or workbook is audited | [`01-formula-scan-and-structure.md`](./references/01-formula-scan-and-structure.md) |
| 2 | Integrity identities, circular references, edge cases and the findings report | a whole model is audited or will not balance | [`02-identities-and-report.md`](./references/02-identities-and-report.md) |

## Output / checkpoint
A findings table with one row per finding: sheet, cell or range, severity (critical, warning, info), category,
the issue and a suggested fix, plus a one-line summary of how many of each. The balance and cash checks come
first and are reported per period. Evidence is that the identities in part 2 were recomputed for every period
and the gap, if any, is quantified rather than described as "small". Nothing is changed in the workbook
without the owner asking: the audit reports first and edits only on request. Nothing here was run against a
real model: the check is a read of the text.

## Guardrails
- Never edit the workbook as part of the audit; report, then fix on request (part 2).
- Never trust any downstream figure while the balance check fails: quantify the gap per period and trace it
  first (part 2).
- Never accept a hardcoded number inside a formula or a value pasted over a formula without flagging it
  (part 1).
- Never treat an intentional circular reference as acceptable unless its iteration switch exists and works
  (part 2).
- This block checks arithmetic and wiring only; it says nothing on whether assumptions or valuation are sound.
- This block does not replace a chartered accountant, an auditor, or a legal, compliance or financial
  adviser, and it is not investment advice.

## Origin
Rewritten from the audit-xls skill of anthropics' financial-services plugins (Apache-2.0), read 2026-10-16.
A vendor-authored practice guide for one tool. 🟡: never run by us; the valuation-specific rules that were
removed and the open points are in [`references/origin.md`](./references/origin.md).
