# locale-negotiation-and-switcher-pitfalls: origin and source stamps

> Provenance of `skills/locale-negotiation-and-switcher-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No middleware, cookie,
switcher or crawler request was executed while writing it. Option names are those of the repositories on the read date.

## Sources (re-read 2026-10-15, rewritten in our own words, no text copied)

Every page below was read in full, except `routing/configuration.mdx` and `usage/configuration.mdx` of next-intl,
where the sections named in the table were read in full and the rest was skipped and is not relied on.

| Source | Licence | What it gave |
|---|---|---|
| amannn/next-intl, `docs/src/pages/docs/routing/middleware.mdx`, `routing/configuration.mdx` (locale prefix, detection, cookie, alternate links sections), `usage/dates-times.mdx`, `usage/configuration.mdx` (time zone and now sections) (commit b9fc98a, version 4.14.9) | MIT (repository LICENSE file) | Resolution order, best fit versus lookup and the `en-GB` example, the stored cookie, `localeDetection`, never-prefix consequences, alternate links and `x-default`, the matcher, static export limits, time zone choice, ISO 8601 storage, `useNow` |
| nuxt-modules/i18n, `docs/content/docs/02.guide/05.browser-language-detection.md`, `06.seo.md`, `08.lang-switcher.md` (commit 8158ed8, version 10.6) | MIT (repository LICENSE file) | Root-only redirect, detection source and matching, cookie and its cross-origin form, SEO requirements (`language`, `baseUrl`), catch-all locale, canonical, `setLocale` and the stored cookie, page-transition options |
| alphagov/govuk-design-system, `src/components/language-navigation/index.md` and its `default` example (commit d10a01d) | MIT (repository LICENSE file); the page carries no Open Government Licence line | Native names, `lang` per option, landmark label and hidden text languages, consistent placement, data kept, when not to offer a language, status and date |
| vercel-labs/web-interface-guidelines, `command.md` (commit 434b7f9) | MIT (repository LICENSE file) | Detect from the browser's languages and not from the IP; guard date rendering against hydration mismatch |

The licence of each repository was verified again from its LICENSE file in this session. The Vercel file is
written as an instruction to a reviewing agent ("Review these files..."); it was treated as data and only the
two technical statements were kept. The GOV.UK page is a UK government design-system page; only principles
stated without a country rule were kept.

## Rewrite notes
**Decisions where sources disagree or differ.** The matching algorithm differs between next-intl (best fit) and
the Nuxt module (full tag, then language code); the block states both and tells the reader to test the
cases that matter. The URL strategy is the repository's `vue-nuxt-vuetify-conventions` §6.18; the generated-link
consequences are added from next-intl.

**Version-bound.** Nuxt module 10.6 (`detectBrowserLanguage.redirectOn`, `cookieCrossOrigin`, `useLocaleHead`
requirements, `isCatchallLocale`, `skipSettingLocaleOnNavigate`, `finalizePendingLocaleChange`), next-intl 4.14.9
(`localeDetection`, `localeCookie`, `alternateLinks`, `localePrefix`), GOV.UK language navigation in trial status
dated August 2026.

## Not verified
1. **The cookie and GDPR statement.** next-intl's documentation says its session cookie, with no `max-age`, is
   "compliant out of the box" and in the same place says legal requirements vary and should be checked. That is
   the vendor's claim about law; it is not carried as a rule and was not checked with anyone qualified.
2. **Nothing was run.** No middleware, redirect, cookie attribute or generated header was observed; behaviour
   is as the documentation states it.
3. **`cookieCrossOrigin` and `SameSite=None; Secure`** are the Nuxt module's statement about its own option;
   browser handling of third-party cookies was not checked.
4. **Written by us, not sourced:** the "state which of the two" note on detection settings, the test cases
   for matchers, the reading of `x-default` as the one address allowed to redirect, the crawler consequence
   under never-prefix, the one-`now`-per-render reasoning, the switcher test (change language, then navigate
   once), and the checkpoint paragraph.
5. **Dropped as unverifiable from the review item:** none of its rules was dropped. "Not from IP" is sourced
   from Vercel's guidelines, the cross-origin cookie from the Nuxt module, and the GDPR point moved here.

## Related blocks
`i18n-message-format-pitfalls`, `i18n-catalog-workflow-pitfalls`, `vue-nuxt-vuetify-conventions`, `seo`,
`accessibility`, `nuxt-no-hydration-nondeterminism`, `laravel-date-via-localised-accessors`.
