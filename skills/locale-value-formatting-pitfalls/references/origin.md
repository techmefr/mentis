# locale-value-formatting-pitfalls: origin and source stamps

> Provenance of `skills/locale-value-formatting-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from a specification read plus our own knowledge of the ECMAScript Intl API, never run

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: duplicate formatters with different input units, UTC-day grouping and today limits, runtime-default locale search recipe, checkpoint scoped to changed screens, skip-when line.
by us. No formatter was called, no page rendered, no locale tested while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| unicode-org/cldr, `docs/ldml/tr35-numbers.md` (commit a70bfe9): numbering systems, number symbols, compact formats, currency formats, currency spacing, currency fraction digits and rounding including cash digits | **Unicode terms: facts only.** The LICENSE file says copies of the specification may be made for personal or internal business purposes and not for public distribution without permission, so nothing is reproduced; the sample patterns and counts are not carried | Symbols as locale data, numeric and algorithmic numbering systems, compact notation per locale, the default of two currency digits with ISO 4217 as basis and cash variants, currency spacing |
| unicode-org/cldr, `docs/ldml/tr35-dates.md` (commit a70bfe9): date, time and interval patterns, skeletons, calendar preference data, week data, time data (hour cycles), parsing guidance | same | Pattern per length with skeleton matching, interval patterns, calendars in preference order per territory, first day and minimal days per territory, preferred and allowed hour cycles per region, the lenient-parsing rules and the 03/07 ambiguity |

The licence statement was read from the repository LICENSE file on 2026-10-20: the specification text is under
Unicode's restricted copy terms, other content under the Unicode License. Only facts of the specification are
restated.

## Checked 2026-10-20 in ECMA-402 (tc39.es/ecma402, facts only)
Percent style multiplies by 100; compact notation scales to a locale-defined power of ten; list formatter types are conjunction, disjunction and unit; `ca`, `co`, `nu` are locale extension keys; sanctioned simple units are a fixed list from one CLDR release that may expand, compounds are two-part per-divisions. Corrected: the block said the unit list was fixed without qualification.

## Own knowledge, not re-read in this session (marked "re-read before relying" in the files)
The behaviour of the ECMAScript Intl formatters: the number, date-time, list, relative-time and duration
formatters and their options; the rule that a style option and field options cannot be combined; the percent
style multiplying by 100; the date-only versus date-time string parsing difference; the `-u-ca-` and `-u-nu-`
locale extensions; the fixed list of supported simple units; the "auto" numeric option; the support status of
the range and duration formatters. The MDN pages were not opened for this block: their text is share-alike
licensed, and no source with a creditable licence for the API was read.

## Not verified
1. **Nothing was run.** No formatter, locale or runtime was exercised.
2. **Intl option names and defaults** were written from memory of the language specification; confirm each in the
   specification or the runtime documentation before a rule is relied on.
3. **Runtime support** of the range formatter, the duration formatter and the plain-date types varies by runtime
   version and was not checked.
4. **Per-locale examples** (which locale groups how, which shows a symbol where) are not given on purpose: none
   was checked against the locale data. The German shapes quoted in §2.1 and §2.3 are illustrations of the
   mechanism, not verified output.
5. **Written by us, not sourced:** the three-things distinction for dates, the instant-versus-wall-time advice, the
   minor-unit round trip, the totals rounding order, the unit conversion rule, the stale relative time rule, the
   echo-back advice, and the checkpoint paragraph.
6. **Not covered, on purpose:** names and addresses, collation and sorting, case mapping, text expansion in
   layout, and any tax or legal rule for money.

## Related blocks
`i18n-message-format-pitfalls`, `i18n-catalog-workflow-pitfalls`, `locale-negotiation-and-switcher-pitfalls`,
`rtl-and-bidi-layout-pitfalls`, `nuxt-no-hydration-nondeterminism`.
