# localisation-vendor-process-pitfalls §2 — Glossary and translation memory

> Part 2 of `business/localisation-vendor-process-pitfalls`. Read it when a term or a memory is created or
> cleaned.

A glossary decides how a term is translated; a translation memory remembers how a sentence was. Both save money
and both spread errors at the same speed.

## 2.1 Glossary
1. **List the terms that carry the product**: feature names, plan names, domain words, the things the interface
   names. Symptom: "workspace" is "espace", "zone" and "projet" in three screens. Check: search the translated
   catalogue for each term's variants. Fix: one approved translation per term and per market.
2. **Keep a do-not-translate list.** Brand and product names, command names, legal entity names, code. Each entry
   says why it stays, and whether it takes a local article or ending in that language.
3. **Give each entry a definition and an example sentence.** A term with no definition is translated by guess.
   Add part of speech where it matters: the verb and the noun of the same word differ in many languages.
   Crowdin's glossary documentation lists the same fields: a definition, a subject, a translatable toggle (the
   do-not-translate switch), a note, and per term its part of speech, type (acronym, abbreviation, phrase),
   gender and status.
4. **Record forbidden translations**, such as a word with an unfortunate local meaning or a competitor's term.
   Crowdin's term status offers preferred, admitted and not recommended; that three-level idea is what we mean.
5. **Name an owner and a change rule.** Symptom: three people add terms and nobody removes any. Fix: one owner
   per market approves additions, and a change sends a note to every current linguist.
6. **Have a native in-market reviewer approve the first version.** An unreviewed glossary teaches the mistakes of
   whoever wrote it.

## 2.2 Translation memory
1. **A memory is a record of past choices, correct or not.** Symptom: the same wrong term appears in every new
   job, at a "100% match" nobody rechecks. Fix: correct the segment in the memory, not only in the file.
2. **Clean before reuse.** Remove segments from a retired product, a brand that was renamed, a superseded legal
   text and any known mistake. Check: sort by age and by project and review the oldest and the largest. Crowdin's
   TM documentation shows each unit's creation and modification dates and original contributor, and lets
   units be edited or deleted, so age is a usable filter there; another tool may differ.
3. **Do not trust a match without its context.** The same English words can need different translations in two
   places; a repeated or perfect match from another context needs a look, particularly for short strings.
4. **Separate memories by client, product or domain** where terminology differs; mixed memories suggest the wrong
   term with full confidence. Crowdin lets several memories be created and assigned per project, ranks competing
   suggestions by match first and by assigned memory priority after, and lets a penalty lower the match of an
   adjusted suggestion.
5. **Do not pay twice for the same segment, and do not skip checking it either.** What a vendor charges for a
   repeated segment is a contract term; the quality check for it is yours and does not shrink with the price.
6. **Machine translation output is a draft, and a draft of unknown quality.** If a vendor uses it, ask whether and
   how, how it is post-edited, and whether your text trains anything. Never allow your confidential text to be
   sent to a service you did not agree to; data handling is `business/data-protection`.
7. **Keep the memory in an exchange format you can export**, and export it after each job. A memory held only in
   the vendor's tool leaves with the vendor. Crowdin's page names TMX, XLSX and CSV for upload and TMX for
   download; the TMX specification itself was not read.
