---
name: localisation-vendor-process-pitfalls
description: "Use when human translation is commissioned, run or reviewed with a translation vendor or in-house linguists: a brief with no audience or context, strings sent without screenshots, a glossary nobody maintains, a term translated three ways, a translation memory that spreads an old mistake, a review that is one person's taste, a quality score with no definition, a late change that restarts the job. Brief and kit, glossary and translation memory, review and error-based quality scoring, change handling and vendor feedback."
---

# localisation-vendor-process-pitfalls

Business layer (`business/README.md`), communication. Localisation fails less from bad translators than from a job
set up without what a translator needs: the audience, the context of each string, the approved terms. This block
is the check to run on a human-translation job, from the brief to the quality review. The code side of it is
elsewhere: message format and plurals `skills/i18n-message-format-pitfalls`, the catalogue workflow in the
repository `skills/i18n-catalog-workflow-pitfalls`, locale formats `skills/locale-value-formatting-pitfalls`,
right-to-left `skills/rtl-and-bidi-layout-pitfalls`. Choosing and scoring the vendor is `business/vendor-management`
and `skills/vendor-claims-and-scoring-pitfalls`; wording of the source is `business/ux-writing`.

It states method only. Quality-scoring frameworks and translation-industry standards were not read for this block;
any named error taxonomy or threshold is something to take from the version the parties agree on, and a contract
with a vendor is not legal advice here.

## When
- A job is scoped, briefed or sent to a vendor or a freelance linguist.
- A glossary or translation memory is created, merged or cleaned.
- A translation is reviewed, scored or disputed.
- The source changes mid-job, or a new language is added.

## Steps

**Read only the section the task meets.** §1 before sending; §2 when terms or memory are touched; §3 when a result
is reviewed or the source changes.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Brief and kit: audience, tone, context, screenshots, scope, source freeze, format | a job is prepared or sent | [`01-brief-and-kit.md`](./references/01-brief-and-kit.md) |
| 2 | Glossary and translation memory: terms, do-not-translate lists, ownership, memory hygiene, match reuse | a term or a memory is created or cleaned | [`02-glossary-and-translation-memory.md`](./references/02-glossary-and-translation-memory.md) |
| 3 | Review, scoring and change: reviewer role, error-based scoring, sampling, feedback loop, late changes | a result comes back, or the source moves | [`03-review-scoring-and-change.md`](./references/03-review-scoring-and-change.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a brief with the audience, context material and scope; a
glossary with a named owner and a do-not-translate list; and, at review, a score or a list of findings by
category with the sample it was taken on. A review is a sampled judgment, not proof that a file is correct; the
content owner and a native reviewer in the market decide acceptance.

## Guardrails
- Send the audience, the tone and the context with the strings. Never send a bare list of strings (§1).
- Freeze the source and say when it is frozen. Never send a moving source and call the job a fixed price (§1).
- Name a glossary owner and list what is never translated. Never let each linguist choose the term (§2).
- Clean the translation memory of known errors before reuse. Never let an old mistake propagate through matches
  (§2).
- Define the error categories and the pass mark with the vendor before the first review. Never score on a taste you
  cannot explain (§3).
- Review a sample chosen to be representative, and say how it was chosen. Never judge a language from its easiest
  strings (§3).
- Send findings back with the category and a correction. Never reject without feedback the vendor can act on (§3).
- Method written from general practice, no source taken; status and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Written from general localisation-management practice; no licensed source was read. 🟡: never run by us.
Details in [`references/origin.md`](./references/origin.md).
