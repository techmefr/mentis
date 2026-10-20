---
name: translation-glossary-and-memory-pitfalls
description: "Use when translation of a product's text is done by people or a vendor and has to stay consistent over time: a per-locale glossary (term, definition, do-not-translate, status), a style guide per locale, the brief and context a translator needs, translation memory and fuzzy-match reuse, what an edit to the source does to the memory, exchange formats (TMX, XLIFF, TBX) and their loss, review and sampled quality checks, and who owns a term decision."
---

# translation-glossary-and-memory-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the people-and-process side of translation: the same product word
translated three ways, a vendor who never saw the screen, a memory full of stale matches. The two sections share
one premise: **a translation is only as consistent as the shared decisions behind it (terms, style, context), and
those decisions live in files the team owns, not in a translator's head or a vendor's tool**. The catalog, extraction,
IDs, pseudo-locale and the tool-side checks are `i18n-catalog-workflow-pitfalls` (§3.2 already names the
glossary and the blocking checks); the message text and its placeholders are `i18n-message-format-pitfalls`; locale
choice is `locale-negotiation-and-switcher-pitfalls`; sampled quality checks follow `sampled-evaluation`. This block
adds what those do not hold: the glossary as a record, the brief, the memory, and the review loop.

## When
- A second language is added, or translation moves to a vendor, a community, or a model plus human review.
- The same concept appears under different words across screens, emails and documents.
- A source sentence is edited, and nobody knows which translations are now stale.
- A translator asks what a string means, or a string was translated without seeing where it shows.
- A term decision (translate or keep, formal or informal address) is made in a chat and then lost.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Glossary and style guide: what a term record holds, do-not-translate, status and owner, locale style choices | terms, brand words or tone differ across a locale | [`01-glossary-and-style.md`](./references/01-glossary-and-style.md) |
| 2 | Context, memory and review: the brief, translation memory, fuzzy matches, source edits, exchange formats, review and quality sampling | a vendor is briefed, the memory is reused or migrated, or quality is checked | [`02-context-memory-and-review.md`](./references/02-context-memory-and-review.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a term was looked up in the glossary for two locales and found with
its status and owner (§1); one source sentence was edited and the memory was seen to offer the old translation as a
fuzzy match and to flag it for review (§2); an export to the exchange format was imported into a second tool and the
placeholders, notes and statuses were compared before and after (§2). A glossary or memory that was only read is not
verified.

## Guardrails
- Never leave a term decision in a chat or a translator's head; record it in the glossary with its owner (§1.1).
- Never translate a brand or product word that the glossary marks do-not-translate, and never mark it without a reason
  stated (§1.2).
- Never choose formal or informal address, or a regional variant, per string; decide once per locale in the style
  guide (§1.3).
- Never send strings to a translator without the context that says where each shows (§2.1).
- Never accept a fuzzy match as final; a changed source reopens the translation (§2.3).
- Never move a memory between tools without a round trip that compares placeholders, notes and statuses (§2.4).
- Never treat vendor delivery as the end; sample the result against the glossary and the style guide (§2.5).
- This block states process practice from our own knowledge of localisation work and the tools named in
  [`references/origin.md`](./references/origin.md); nothing was run, and all marked "re-read before relying" is
  unchecked.

## Origin
Written from our own knowledge of localisation practice, with one overlap point confirmed against
`i18n-catalog-workflow-pitfalls` (Pontoon documentation, BSD-style, read 2026-10-15). One specification page (XLIFF 2.1, facts only, partial) was read
for this block on 2026-10-20; the other candidate sources had licences that were not creditable or not verified. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
