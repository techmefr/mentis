# translation-glossary-and-memory-pitfalls: origin and source stamps

> Provenance of `skills/translation-glossary-and-memory-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of localisation practice, never run by us. No glossary was built,
no memory imported, no vendor briefed while writing it.

## Sources (read 2026-10-20)

None read for this block. The overlap check was against blocks already in the repository.

| Candidate | Status |
|---|---|
| OASIS TMX, XLIFF and TBX specifications | Not opened. Licence not verified; the formats are named only, with no clause or version detail |
| Weblate, Crowdin, Lokalise documentation | Not opened. The Weblate repository is GPL-licensed (not creditable for text); the others were not checked |
| Mozilla and Microsoft style guides | Not opened. Licences vary and none was verified |
| Mozilla Pontoon documentation (BSD-style, read 2026-10-15 for `i18n-catalog-workflow-pitfalls`) | Not re-read here; the overlap with its glossary point is cross-linked rather than restated |

## Rewrite notes
**Overlap.** `i18n-catalog-workflow-pitfalls` §3.2 already holds the translator-tool checks and a glossary point;
this block adds the record, the brief, the memory and the review loop and links back.

## Not verified
1. **Nothing was run.** No tool, format or workflow was exercised.
2. **Every rule is own knowledge.** Tool behaviour (fuzzy-match handling, state flags, format support and
   what each exchange format preserves) differs by tool and version and must be confirmed in the tool in use.
3. **Quality frameworks** (error types and severities) are described generically; no published framework was read.
4. **Thresholds** are deliberately not given; where one is used, the team records it and its check.
5. **Locale style examples** (variants of Portuguese, Spanish and Chinese, address forms) are illustrations
   from our own knowledge; a native reviewer for each locale must confirm any locale rule before it is written
   in a style guide.
6. **Not covered, on purpose:** legal translation and certified translation, pricing and vendor contracts, and
   machine-translation model selection (`choose-model`).

## Related blocks
`i18n-catalog-workflow-pitfalls`, `i18n-message-format-pitfalls`, `locale-negotiation-and-switcher-pitfalls`,
`locale-value-formatting-pitfalls`, `international-input-pitfalls`, `sampled-evaluation`.
