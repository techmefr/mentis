---
name: international-input-pitfalls
description: "Use when a form asks for a person's name, phone number, postal address, email address or a date and has to work for people outside one country: single or split name fields and their labels, titles and name changes, phone formats and validation, address lookup versus manual entry, postcode tolerance, email length and typo warnings, memorable versus approximate dates and calendar controls, and example values that teach the right format."
---

# international-input-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the fields where a form most often rejects a real person. The three
sections share one premise: **a format check written for the developer's own country is a rule that refuses
everyone else, so every check either accepts what a real value can look like or offers a way around itself**.
Labels, error association, autocomplete metadata and input types are already in `accessibility` §4 (points 6
and 7) and the phone keyboard rules are in `webperf`; this block adds what each kind of value needs and does
not restate them. Translating the labels themselves is in `i18n-message-format-pitfalls`.

## When
- Adding or reviewing a name, phone, address, email or date field in a sign-up, checkout or profile form.
- A user reports that their name, phone number or address is refused, reformatted or cut.
- A form built for one country is opened to others, or a postcode lookup is added.
- Choosing example values for hint text.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Names and phone numbers: one field or several, labels, titles, name changes; formats, validation, masking, `tel:` links | a form asks for a person's name or a way to call them | [`01-names-and-phone-numbers.md`](./references/01-names-and-phone-numbers.md) |
| 2 | Addresses: lookup, several inputs, a textarea, postcode tolerance | a form asks for a postal address or adds a lookup | [`02-addresses.md`](./references/02-addresses.md) |
| 3 | Email addresses and dates: length, typo warnings, date kinds, calendars, example dates | a form asks for an email address or a date | [`03-email-and-dates.md`](./references/03-email-and-dates.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a name with a single word, a name with a digit and an apostrophe,
a phone number typed with spaces, brackets and a country code, an address that a lookup does not list, a
postcode typed in lower case with stray spaces and an email address of more than 100 characters were entered in
the real form and none was refused, cut or silently reformatted (§1, §2, §3). A form that was only read is not verified.

## Guardrails
- Never validate a name against a character set or a length taken from one language (§1.1).
- Never use a select for a title; never require one (§1.1).
- Never reject a phone number for its punctuation, and never rewrite what the user typed (§1.2).
- Never offer an address lookup without a manual way out (§2.1).
- Never reject a postcode for case, spacing or punctuation (§2.1).
- Never block an email address because of a suspected typo (§3.1).
- Never offer a calendar as the only way to enter a date (§3.2).
- This block states guidance of the GOV.UK Design System pages read on the date in
  [`references/origin.md`](./references/origin.md). Country-specific rules in those pages (postal identifiers,
  a regulator's number ranges, a county rule, the national writing style) were left out. Nothing was run while
  writing it.

## Origin
Rewritten from the GOV.UK Design System pages on names, phone numbers, addresses, email addresses, dates and the
date input component (MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
