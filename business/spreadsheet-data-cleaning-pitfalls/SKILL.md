---
name: spreadsheet-data-cleaning-pitfalls
description: "Use when a spreadsheet or CSV is cleaned, merged, analysed or handed on: an identifier that lost its leading zeros, a long number shown in scientific notation, a date read in the wrong order or as a serial number, a decimal comma parsed as text, a duplicate removed on the wrong key, a lookup that matched the wrong row, a formula that stopped at the last row, a hard-coded figure inside a formula, a cleaned file with no trace of what changed. Type coercion, identifiers, dates and locale, deduplication and joins, formula drift, provenance and a change log."
---

# spreadsheet-data-cleaning-pitfalls

Business layer (`business/README.md`), data. A spreadsheet changes data silently: on open, on paste, on save, on
sort. Most cleaning errors are not wrong formulas but a tool that guessed a type, a key that was not unique, or a
step nobody wrote down. This block is the check to run on a table before and after it is cleaned. Reviewing an
analysis result is `skills/analysis-validation-pitfalls`; the meaning of a business metric is
`skills/saas-metric-definition-pitfalls`; metric tables and a semantic layer are `business/data-analytics`;
quality rules inside a data contract are `skills/data-contract-quality-rules-pitfalls`; personal data in a file is
`business/data-protection`.

It states method only, written from general practice, with no source behind it. It names behaviours that differ
by program, version and locale as things to check on the file in front of you, not as facts to assume.

## When
- A CSV or workbook arrives from someone else and is about to be used.
- A table is merged, deduplicated, reshaped or enriched before a report or an import.
- A workbook with formulas is handed on, extended or audited.
- A cleaned file is about to be loaded into another system.

## Steps

**Read only the section the task meets.** §1 and §2 when opening or importing; §3 before removing or joining rows;
§4 before handing a file on.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Type coercion: identifiers as text, leading zeros, long numbers, codes read as numbers or dates, opening a CSV without a guess | a file is opened, imported or saved | [`01-types-and-identifiers.md`](./references/01-types-and-identifiers.md) |
| 2 | Dates, numbers and locale: day-month order, serial dates, time zones, decimal and thousand separators, currency and unit columns | a column holds dates, amounts or mixed formats | [`02-dates-numbers-and-locale.md`](./references/02-dates-numbers-and-locale.md) |
| 3 | Duplicates, keys and joins: choosing the key, near-duplicates, lookups that fan out or miss, blanks and spaces | rows are removed, matched or merged | [`03-duplicates-keys-and-joins.md`](./references/03-duplicates-keys-and-joins.md) |
| 4 | Formulas and provenance: range drift, hard-coded values, hidden rows, work on a copy, change log, reconciliation totals | a workbook is handed on or relied on | [`04-formulas-and-provenance.md`](./references/04-formulas-and-provenance.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the raw file kept unchanged, a cleaned file, a short change
log (what was changed, how many rows, by which rule) and a reconciliation line (rows in, rows out, rows removed
and why, a control total before and after). The person who owns the data decides what counts as an error; the
cleaner reports what was changed and what was left unresolved.

## Guardrails
- Keep the raw file untouched and clean a copy. Never overwrite the only copy of a source (§4).
- Import identifiers, codes and phone numbers as text, and check them against the original after opening. Never
  let the program guess a type and trust the result (§1).
- State the date order, the time zone and the separators of the source before parsing. Never convert a date or an
  amount on the assumption that the file uses your locale (§2).
- Name the key before removing duplicates and look at the rows it would remove. Never delete duplicates on a key
  that is not unique by definition (§3).
- Check what a join did to the row count and to the unmatched rows. Never accept a lookup that returns a plausible
  value without testing a row that should not match (§3).
- Put constants in labelled cells, extend ranges on purpose and check the totals. Never bury a rate inside a
  formula or trust a total that stops at a hidden last row (§4).
- Write the change log and a before and after control total. Never hand on a cleaned file that nobody can
  compare with its source (§4).
- Leave the unresolved rows listed, not guessed. Never fill a blank with a value you invented (§4).
- This block is a method written from general practice and never run by us on a real file; there is no external
  source. Status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Written from general spreadsheet and data-cleaning practice; no licensed source was read for it (the review found
none to use). 🟡: never run by us. Details in [`references/origin.md`](./references/origin.md).
