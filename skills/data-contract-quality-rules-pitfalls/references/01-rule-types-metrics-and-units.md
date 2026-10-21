# data-contract-quality-rules-pitfalls §1 — Rule types, metrics and units

> Part 1 of `skills/data-contract-quality-rules-pitfalls`. Version-bound: ODCS v3.2.0. Read it when a rule is
> chosen or its numbers are questioned. Source: the standard's data-quality page (Apache-2.0); points marked own
> guidance are ours.

## 1.1 Four rule types
1. **A rule has one of four types**: `text`, `library`, `sql`, `custom`. The documented default is `library`,
   and the type may be left out when a `metric` is given.
2. **`text` is a human-readable statement.** The page says it may later become an executable check, a library
   metric or an AI check. Until then nothing runs it, so a contract made of text rules records an intent and
   enforces nothing (own guidance: do not report text rules in a coverage count).
3. **`library` rules name a maintained metric** and compare its numeric result with an operator, so no query
   has to be written. Some metrics take `arguments`.
4. **Pick the lowest type that says it.** A library metric is portable across engines; `sql` is bound to one
   dialect and `custom` to one vendor (part 2).

## 1.2 The library metrics
1. **The page lists six**: `nullValues`, `missingValues`, `invalidValues` and `duplicateValues` at property
   level, `duplicateValues` again at schema level, and `rowCount` at schema level. A metric used at the wrong
   level is a rule that does not mean what it says.
2. **`nullValues` counts nulls only.** `missingValues` counts the values the author lists as missing, with the
   `missingValues` argument (the page's example lists null, the empty string and two spellings of "not
   available"). A column filled with empty strings or placeholder text passes a null check and fails a
   missing-values check; write the sentinel list down, because the contract is the only place it lives.
3. **`invalidValues` takes a `validValues` list or a `pattern`.** Both go under `arguments`, as the
   arguments table says. Correction 2026-10-20: an earlier reading of this block said the page's pattern example
   put `pattern` beside `arguments`; at the commit recorded in `origin.md` the example nests it under
   `arguments`, so that warning is withdrawn. Validating a copied example against the schema is still sensible
   (own guidance).
4. **`duplicateValues` at schema level takes a `properties` list**, the way a compound key is checked: the
   combination must be unique, not each column. At property level it counts duplicates in one column.
5. **`rowCount` compares the object's total rows**; a value range (the page's example gives a lower and upper
   bound) is the usual shape.

## 1.3 Units and operators
1. **The unit is `rows` by default, or `percent`.** The page comments "rows (default) or percent", and the
   v3.2.0 schema says any other value is accepted. A threshold of 1 with no unit means one row; the same 1
   with `percent` means one percent of the rows. State the unit on every threshold (own guidance, a consequence
   of the default).
2. **A unit the engine does not know is accepted by the schema and meaningless to the engine** (the schema
   leaves the value open). Use the two documented ones.
3. **Operators**: `mustBe`, `mustNotBe`, `mustBeGreaterThan`, `mustBeGreaterOrEqualTo`, `mustBeLessThan`,
   `mustBeLessOrEqualTo`, `mustBeBetween` and `mustNotBeBetween`. The page says `mustBeBetween` is equivalent
   to greater-than plus less-than, which are strict operators. Do not rely on a bound being included; if the
   edge matters, use the or-equal operators explicitly (own guidance; the page does not discuss the edge).
4. **A rule can carry two operators.** The page's own equivalence example writes a greater-than and a
   less-than on one rule; check that the pair describes a non-empty range (own guidance).
