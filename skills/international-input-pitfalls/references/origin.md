# international-input-pitfalls: origin and source stamps

> Provenance of `skills/international-input-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from design-system documentation and reading, never run by us. No form was built, no
phone library was called and no real user was asked while writing it. The guidance is the GOV.UK Design System's
as it stands on the read date, reduced to what holds outside one country.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

Every page below was read in full, except the date input component page, where the first 70 lines (the
"how it works" part up to the autocomplete section) were read in full and the error message wording was skipped
and is not relied on.

| Source | Licence | What it gave |
|---|---|---|
| alphagov/govuk-design-system, `src/patterns/names/index.md` (commit d10a01d) | MIT (repository LICENSE file, Crown Copyright, Government Digital Service) | One field or several, labels, field length, characters, autocomplete values, spellcheck, optional middle names, titles, name changes |
| alphagov/govuk-design-system, `src/patterns/phone-numbers/index.md` (same commit) | MIT (same file) | Formats, library validation, type of number in the label, masking, reformatting, `tel:` links, reserved example numbers (idea only), open questions |
| alphagov/govuk-design-system, `src/patterns/addresses/index.md` (same commit) | MIT (same file) | Lookup, manual path, postcode tolerance, several inputs, textarea, autocomplete values |
| alphagov/govuk-design-system, `src/patterns/email-addresses/index.md` (same commit) | MIT (same file) | Reason for asking, 254 characters, helping the user, visible width, typo warning, repeat entry, confirmation loop |
| alphagov/govuk-design-system, `src/patterns/dates/index.md` (same commit) | MIT (same file) | The kinds of date, documents and cards, approximate and relative dates, calendar conditions, example date |
| alphagov/govuk-design-system, `src/components/date-input/index.md`, first 70 lines (same commit) | MIT (same file) | Separate day, month and year inputs in a fieldset, month names, no automatic tabbing, birth date autocomplete values |

### Added 2026-10-20 for §4

| Source | Licence | What it gave |
|---|---|---|
| google/libphonenumber, `FAQ.md` and `README.md` (master, read 2026-10-20) | Apache-2.0 (LICENSE file read the same day) | Valid is not reachable, region-checked validation rarely right, formatting by country not language, short numbers apart, native-digit formatting gap, large-number precision loss in JavaScript, metadata ageing |
| google/libaddressinput, `README.md` only (master, read 2026-10-20) | Apache-2.0 code, CC BY 4.0 data (README statement; LICENSE file read, data licence not independently checked) | That per-country metadata can drive the fields and validation of an address form |

Not opened on purpose: the W3C internationalization article on personal names (licence not verified, so no
reader was available), and the libaddressinput wiki and data files. The name and address points of §4 are own
knowledge and say so.

The licence was verified again from the repository's LICENSE file in this session (MIT text, copyright line
"Crown Copyright (Government Digital Service)"). A search of the five pattern pages for the Open Government
Licence found no mention in them; the review noted the licence on a few other pages of the site (footer and
news pages), which this block does not use. Every sentence is rephrased regardless.

## Rewrite notes
**Removed (UK-specific, per the review).** The UPRN section of the addresses page and the single-API advice that
sits inside it, the postal operator's county rule as a reason (the optional-and-removable stance is kept and the
reason dropped), the national phone number ranges, the national phone-number and date writing style links, the
UK-formatted example phone numbers in the error wording, the "UK address" wording of the lookup (turned into
"the countries the data covers"). The "outside the UK" label rule is carried as a
principle without a country list.

**Decisions where the source is silent.** The page recommends a phone library; whether to prefer it over a
regular expression is own guidance, labelled as such. The order of day, month and year in an example date is the
page's order; the block states the principle and defers the order to the page locale, labelled own guidance.

**Version-bound.** None of the guidance names a version; the repository is a design system under active change
(the language navigation component, for example, is marked as a trial), so recheck against the source before
quoting a rule as current.

## Not verified
1. **No claim was run.** No form, validator or library was exercised.
2. **The 254-character limit:** checked 2026-10-20 against RFC 5321 section 4.5.3.1.3 (standards text, facts only): a path is at most 256 octets including punctuation, and the two angle brackets leave 254 for the address. The erratum itself was not read.
3. **libphonenumber's coverage** ("most countries") is the page's statement; the library was not read.
4. **WCAG 2.2 success criterion 1.3.5** checked 2026-10-20 on the W3C Understanding page (facts only): Identify Input Purpose, level AA; the autocomplete attribute is the technique for fields about the user.
5. **The research behind each recommendation** (Notify observations, the Baymard and W3C articles the names page
   lists) was not read; only the page's own statement of the guidance is relied on.
6. **Written by us, not sourced:** the "if nothing reads a part, use one field" advice, the regular-expression
   remark, the reserved-range lookup advice, the postcode order of checks, the region-input decision per country,
   the "typo warning is a message" remark, the date-order-from-locale advice and the checkpoint paragraph.
7. **Dropped as unverifiable from the review item:** none of its rules was dropped; the date item's "three fields"
   is sourced from the date input page, which the review had not listed.

8. **§4 not run.** No library was called. Name rules, per-country address shape, local-script label practice and
   the libphonenumber FAQ statements (including its description of native-digit formatting) are as of the read
   date and marked "re-read before relying" where they vary by country or version.

## Related blocks
`accessibility`, `webperf`, `i18n-message-format-pitfalls`, `vue-nuxt-vuetify-conventions`,
`collation-and-locale-aware-search-pitfalls`.
