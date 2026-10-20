# collation-and-locale-aware-search-pitfalls: origin and source stamps

> Provenance of `skills/collation-and-locale-aware-search-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one specification part plus our own knowledge of Unicode text processing and the
ECMAScript Intl API, never run by us. No collator was built, no database queried, no text sorted while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| unicode-org/cldr, `docs/ldml/tr35-collation.md` (main branch, read 2026-10-20): collation overview, types and type fallback, version, settings table and common combinations, normalisation and variable-top notes, collation indexes and index characters | **Unicode terms: facts only.** The repository LICENSE file says the specification may be copied for personal or internal business purposes and not distributed publicly without permission, so nothing is reproduced; sample tables and the data examples are not carried | Collation varies by language and use, several types per locale and the fallback chain to root, version setting, strength levels and the common "ignore accents / ignore case / ignore punctuation" combinations, numeric ordering, case settings, variable handling and its default difference from the base algorithm, reordering of scripts, search type, match boundaries, index characters and buckets |

## Own knowledge, not re-read in this session (marked "re-read before relying" in the files)
The behaviour of the ECMAScript collator (options, sensitivity, building cost), `toLocaleLowerCase` and
`toLocaleUpperCase`, the segmenter (grapheme and word granularity), the Turkish and Azerbaijani i pairs, the
sharp s expansion, context-dependent final sigma, Unicode normalisation forms and their use for identifiers,
the behaviour of databases when a collation library changes version, and the count units of columns. The MDN pages
were not opened: their text is share-alike licensed. The Unicode Collation Algorithm report (UTS #10) itself was
not opened; only the part of it that UTS #35 restates is relied on.

## Not verified
1. **Nothing was run.** No collator, segmenter, normaliser or database was exercised.
2. **Intl option names and defaults** were written from memory of the language specification; confirm in the
   specification or the runtime documentation before relying.
3. **Per-language examples** (Swedish Ö after Z, Czech CH, German and Turkish letters) are illustrations of
   the mechanism from our own knowledge; none was checked against locale data.
4. **Database behaviour** on a collation library upgrade differs by engine and was not read here.
5. **The spec statements** quoted as defaults (strength, handling of spaces and punctuation, case settings) are
   as of the CLDR main branch on the read date; the data and defaults change between releases.
6. **Written by us, not sourced:** the tie-breaker advice, the build-once advice, the order-in-one-place advice,
   the per-column uniqueness decision, the unit-per-limit advice and the checkpoint paragraph.
7. **Not covered, on purpose:** confusable-identifier policy, locale-specific sort exceptions for names, and
   full-text search engine tuning beyond the links.

## Related blocks
`locale-value-formatting-pitfalls`, `international-input-pitfalls`, `i18n-message-format-pitfalls`,
`rtl-and-bidi-layout-pitfalls`, `mysql-pitfalls`, `mongodb-conventions`, `search-engine-index-settings-pitfalls`.
