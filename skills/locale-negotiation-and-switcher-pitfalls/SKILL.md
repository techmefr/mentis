---
name: locale-negotiation-and-switcher-pitfalls
description: "Use when the language of a page is chosen or switched in any framework: the order of resolution (URL prefix, stored preference, Accept-Language), best-fit versus lookup matching, redirecting only the root path, the stored-locale cookie and its attributes, a switcher that must also write the preference, hreflang and alternate links under each URL strategy, the language switcher markup and placement, a page transition during a switch, and time zone and dates between server and client."
---

# locale-negotiation-and-switcher-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for how a request becomes a locale, how the user changes it, and how
search engines are told about it. The three sections share one premise: **three sources compete to decide the
language (the URL, a stored choice, the browser header), and every bug here is two of them disagreeing without
a stated order**. Route strategy, time zone and the stored switch are stated as rules in
`vue-nuxt-vuetify-conventions` §6.18, `vue-nuxt-vuetify-conventions` §6.10 and `vue-nuxt-vuetify-conventions`
§6.22, and `hreflang` in `seo` §1.5; those are linked, not restated. Messages and catalogs are in
`i18n-message-format-pitfalls` and `i18n-catalog-workflow-pitfalls`. Right-to-left layout is not covered by any block yet.

## When
- Adding a second language, or changing the URL strategy (prefix always, prefix for non-default languages, never).
- A crawler or a shared link lands on a page in the wrong language, or a user's choice is forgotten after a navigation.
- Adding or reviewing a language switcher, or a page transition flashes the new language before it fades.
- A date shows another day or hour on the server and on the client, or a relative time disagrees between the two.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Negotiation and persistence: resolution order, matching algorithm, root-only redirect, the stored cookie, writing the preference, static export | the first-visit language is wrong or the choice does not stick | [`01-negotiation-and-persistence.md`](./references/01-negotiation-and-persistence.md) |
| 2 | URLs and alternate links: hreflang inputs, never-prefix, opting out of generated links, `x-default`, canonical, the matcher | the same page exists in several languages for crawlers | [`02-urls-and-alternate-links.md`](./references/02-urls-and-alternate-links.md) |
| 3 | Switcher and dates: native names, `lang`, landmark label, placement, data kept, page transition, time zone and `now` | a switcher is built, or dates differ between server and client | [`03-switcher-and-dates.md`](./references/03-switcher-and-dates.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a first visit was made with a stated header and no cookie, then
with a cookie, then on a prefixed URL, and the language each time was written down against the §1.1 order; a
crawler-style request for an inner page was seen not to be redirected (§1); the generated alternate links were
read from the response of a page that exists in one language only (§2); and a date was rendered once on the
server and once on the client with the time zone printed (§3). A configuration that was only read is not verified.

## Guardrails
- Never leave the order of resolution unwritten: URL, stored preference, header, default (§1.1).
- Never redirect an inner page by detected language; only the root (§1.3).
- Never build a switcher that changes the page language without writing the stored preference (§1.5).
- Never publish alternate links with bare language codes, a relative base URL, or under a URL strategy where
  the address does not differ per language (§2.1, §2.2).
- Never show an option in the current page's language alone: each option is in its own language and carries its `lang` (§3.1).
- Never format a date with the time zone left to the default of whichever runtime renders it (§3.3).
- Whether a locale cookie needs consent, or what lifetime is allowed, is a legal question and not answered
  here (see `references/origin.md`, Not verified).
- This block states framework behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The Nuxt module's options are version-bound to 10.6.
  Nothing was run while writing it.

## Origin
Rewritten from the next-intl routing, proxy, dates and configuration documentation (MIT), the Nuxt i18n module
documentation on browser detection, SEO and the language switcher (MIT), the GOV.UK Design System language
navigation component page (MIT) and Vercel's web interface guidelines (MIT), read 2026-10-15. 🟡: never run by
us; open points are in [`references/origin.md`](./references/origin.md).
