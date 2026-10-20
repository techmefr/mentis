---
name: collation-and-locale-aware-search-pitfalls
description: "Use when text is sorted, compared, searched or measured for users of more than one language: lists ordered by code unit instead of the locale's collation, collation types and settings (strength, numeric ordering, punctuation handling), A-Z index headers, database versus application order and keyset pagination, accent- and case-insensitive search and matching, case mapping that changes length or depends on language (Turkish dotted i, German sharp s), Unicode normalisation of equal-looking text, and length or truncation by user-perceived character."
---

# collation-and-locale-aware-search-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the places where text meets an ordering or an equality test: a sorted
list, a search box, a unique constraint, a character counter. The two sections share one premise: **there is no
single order or equality of text, there is one per language and per purpose (display order, search match,
identity), and every bug here is a code-unit comparison standing in for the one the user expects**. Formatting
values (dates, numbers, money) is `locale-value-formatting-pitfalls`; names and addresses as stored data are
`international-input-pitfalls` §4; translated message text is `i18n-message-format-pitfalls`. The database-specific
behaviour of collations is in `mysql-pitfalls` §1.3, `mongodb-conventions` §2.2, `dotnet-conventions` (data access
portability) and `laravel-mysql-to-postgres-pitfalls`, and is linked, not repeated.

## When
- A list, table or autocomplete is sorted for users, or the order differs between two screens or between the
  application and the database.
- A search misses a word because of an accent, a capital, or the way it was typed, or matches where it should not.
- An uppercase, lowercase or title-case conversion changes the meaning or the length of a string.
- A username, email or code must be unique, and two values that look the same are accepted.
- A character limit, truncation or "N characters left" counter is applied to user text.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Sorting: locale collation, types, settings, numeric order, index headers, stored order and version, database order | a user-visible list is ordered, paged or indexed | [`01-sorting.md`](./references/01-sorting.md) |
| 2 | Matching: case folding and case mapping, accent-insensitive search, normalisation, uniqueness, grapheme length and truncation, word boundaries | text is compared, searched, cased, limited or cut | [`02-matching-case-and-length.md`](./references/02-matching-case-and-length.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a list with a word that starts with an accented letter, a word
starting with a capital and one with a lowercase letter, and a name with a digit sequence was sorted in at least
two locales whose rules differ, and the order was compared with an order written down beforehand from a
reference for that language (§1). A search was run with an accented and an unaccented spelling, with a decomposed
and a composed spelling of the same letter, and in a Turkish locale with the letter i; a string with an emoji
sequence and one with a sharp s was cased, counted and cut (§2). A configuration that was only read is not verified.

## Guardrails
- Never sort or compare user-visible text by code unit or byte; use the locale's collator, built once and
  reused (§1.1).
- Never pick the collation from the country or the server default; take the user's language and name the type
  when more than one exists (§1.2).
- Never persist a sorted structure (an index, a cached order) without recording the collation and its version, and
  rebuilding it when they change (§1.4).
- Never page by an order the database does not use; the sort key and the cursor come from one collation (§1.5).
- Never lower-case two strings and compare them for a language-sensitive match; use case folding or a collator at
  a stated strength, and pass the language to any display case change (§2.1, §2.2).
- Never strip accents by deleting combining marks for every language; where an accent changes the letter, choose
  the strength per language (§2.2).
- Never compare or store identifiers without one normalisation form (§2.3).
- Never measure or cut user text by code units; use user-perceived characters, and name the unit of each limit
  (§2.4).
- This block states facts of Unicode LDML collation (UTS #35 part 5, facts only) as of the date in
  [`references/origin.md`](./references/origin.md); everything marked "re-read before relying" is from our own
  knowledge of the algorithms and the ECMAScript Intl API and was not re-read. Nothing was run while writing it.

## Origin
Rewritten from Unicode LDML part 5 on collation (UTS #35, facts only, Unicode terms), the special-casing data, UAX #15 and the PostgreSQL collation page read 2026-10-20, plus our
own knowledge of Unicode text processing and the ECMAScript Intl API, marked where unchecked. 🟡: never run by
us; open points are in [`references/origin.md`](./references/origin.md).
