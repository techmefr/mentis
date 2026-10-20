---
name: locale-value-formatting-pitfalls
description: "Use when a product shows dates, times, numbers, money, units, percentages, lists or relative times to users in more than one locale, or in one locale that is not the developer's: values stored in a canonical form and formatted only at display, the locale-aware formatter instead of hand-built strings, money as integer minor units plus a currency code (never inferred from the locale), units converted by your code and only named by the formatter, calendars and numbering systems as locale extensions, and reading what a user typed back into a value."
---

# locale-value-formatting-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the values that sit inside a sentence or a table cell: a date, a
price, a distance, a count, a list of names. The three sections share one premise: **a value has a canonical
form that the program owns (an instant, an integer of minor units, a number in SI units) and a display form
that the locale owns, and every bug here is the two being the same string**. Plural branches, catalogs,
pseudo-locales, locale negotiation and right-to-left text are in `i18n-message-format-pitfalls`,
`i18n-catalog-workflow-pitfalls`, `locale-negotiation-and-switcher-pitfalls` and `rtl-and-bidi-layout-pitfalls`;
the time-zone choice between server and client is `locale-negotiation-and-switcher-pitfalls` §3.3 and is not
repeated. Isolating a formatted value inside right-to-left text is `rtl-and-bidi-layout-pitfalls` §2.

## When
- A date, price, number or unit is built with string concatenation, a template, or a hand-written pattern.
- A value reads differently from what a user in another country expects: `1.234` meaning one thousand or one
  point two, `03/04` meaning March or April, a currency symbol on the wrong side, a 12-hour clock where a
  24-hour one is the norm.
- Money, quantities or measurements are being stored or exchanged between services.
- A form must accept a number or a date typed by the user.
- A list of items is joined with a comma in code, or a relative time ("3 days ago") is written by hand.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Dates, times, calendars, week and hour conventions | a date or time is shown, picked or stored | [`01-dates-and-times.md`](./references/01-dates-and-times.md) |
| 2 | Numbers, percentages, currency, units, compact notation, numbering systems | any quantity is shown or stored | [`02-numbers-money-units.md`](./references/02-numbers-money-units.md) |
| 3 | Lists, relative time, durations, and reading user input back | a list is joined, a relative time is written, or a typed value is parsed | [`03-lists-relative-parsing.md`](./references/03-lists-relative-parsing.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: every formatted value on the changed screens was rendered in at
least three locales that differ in separators, order and clock (for example English (United States), German,
and one with non-Latin digits or a non-Gregorian default), with a value that exposes the common bugs (a day
above 12, a number above one thousand with a fraction, a price in a currency that differs from the locale's,
a zero-decimal currency). A screen checked in one locale is not verified.

## Guardrails
- Never build a date, number or price by concatenation or a hand-written pattern; call the locale-aware
  formatter with options (§1, §2).
- Never store a formatted string as data; store the canonical value and format at display (§1, §2).
- Never infer the currency from the locale, and never hold money as a binary floating-point number (§2).
- Never assume the formatter converts units; convert in code, then name the unit (§2).
- Never set the hour cycle, first weekday or calendar from a country list of your own when the locale data
  says it (§1).
- Never parse a typed number or date with the global parser of your language; read it with the user's locale
  separators or ask for a structured input (§3).
- This block states specification facts and runtime behaviour as of the sources read on the date in
  [`references/origin.md`](./references/origin.md). Runtime behaviour listed as "re-read before relying" was
  written from knowledge of the language specification and was not re-read. Nothing was run while writing it.

## Origin
Rewritten from the date, number, currency, calendar-preference, week and hour-cycle parts of Unicode LDML
(UTS #35, facts only, Unicode terms) read 2026-10-20, plus our own knowledge of the ECMAScript Intl API, marked
where unchecked. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
