---
name: i18n-message-format-pitfalls
description: "Use when translatable messages are written or reviewed in any framework: plural and select branches (CLDR categories, why `one {1 item}` is wrong, `other` required, plural on a formatted number, ordinals, offset and several plurals in one message), whole sentences with named placeholders and named tags, several strings of one widget kept together, translator comments and contexts for short ambiguous strings, and ICU syntax hygiene (escaping, invalid messages, vendor limits)."
---

# i18n-message-format-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the message text itself, whatever library renders it. The three
sections share one premise: **a translator receives one message at a time, out of order, with no screen
around it, so everything the message needs must be inside it or attached to it**. The rules that already exist
for Vue and Nuxt (plurals through the library, no concatenation, one key per meaning, sentence keys) are in
`vue-nuxt-vuetify-conventions` §6 and are not restated; this block extends them framework-neutrally. Catalog
extraction, IDs, fallback and pseudo-localisation are in `i18n-catalog-workflow-pitfalls`; locale choice and
the language switcher are in `locale-negotiation-and-switcher-pitfalls`. Right-to-left and bidirectional text
are not covered by any block yet.

## When
- Writing or reviewing a message that has a count, a gender or any other branch.
- A translator reports a message that cannot be translated as one sentence, or a plural that is wrong in
  Russian, Polish, Arabic or another language with more than two forms.
- A short string such as a button label is ambiguous, or a widget has several strings (value, placeholder,
  accessible name, title).
- Choosing or tightening lint rules for messages, or onboarding a translation vendor.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Plurals and selectors: categories, `other`, `#`, exact matches, formatted numbers, ordinals, offset, flattening, grammatical variation | a message branches on a number or another value | [`01-plurals-and-selectors.md`](./references/01-plurals-and-selectors.md) |
| 2 | Whole messages: fragments, placeholders, tags, several strings of one widget | a sentence is split, a placeholder is positional, markup sits in a message | [`02-whole-messages.md`](./references/02-whole-messages.md) |
| 3 | Context and syntax: comments, contexts, escaping, invalid ICU, whitespace, vendor limits | a string is short or ambiguous, or a message fails to parse | [`03-context-and-syntax.md`](./references/03-context-and-syntax.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: every plural was rendered for a language that has more
categories than the source language, with the numbers 1, 2, 5, 11 and 21 (§1), every sentence that carries a
link or a value was read as one message with the surrounding text removed from the screen (§2), and the
messages were run through the syntax and description lint the project uses (§3). A message read only in the
source language is not verified.

## Guardrails
- Never write a plural branch as a number or as `=1` where a category is meant, and never write `one {1 item}` (§1.1).
- Never ship a plural or select without its `other` branch (§1.1).
- Never put `offset` or two plurals in one message without having asked the translation vendor (§1.4).
- Never split a sentence around a value or a link (§2.1).
- Never use a positional placeholder or an indexed tag in a message a translator will read (§2.2, §2.3).
- Never leave a short or ambiguous string without a comment, or two meanings of one text without two contexts (§3.1).
- Keys in the examples are flat, following `vue-nuxt-vuetify-conventions` §6.1; the nested message objects that
  next-intl recommends are not adopted here.
- This block states library behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The formatjs documentation has no licence file and was used
  for facts only. Nothing was run while writing it.

## Origin
Rewritten from the Lingui guides on plurals, message format and translator-friendly messages (MIT), the Fluent
guide on selectors, terms and attributes (Apache-2.0), the next-intl message documentation (MIT), and the
formatjs lint rules and ICU syntax page (facts only), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
