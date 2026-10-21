# § 1 — Meta and indexing: the non-negotiable base

> Section 1 of `skills/seo`. Read it for any public page: titles, canonical, robots, social tags, languages.

1. Every page has a unique `<title>` and its own `<meta name="description">` (no copy-pasted duplicate
   between pages, no generic default value left in production). Google's title-link page asks for a unique,
   descriptive title per page, warns that repeated or boilerplate titles make pages hard to tell apart, and says the
   engine may show another title when the element does not describe the page; its starter guide adds that the meta
   description is used only occasionally as the snippet, so it is a summary offered, not a lever.
2. A `canonical` tag as soon as the same page is reachable through several URLs (sort/filter
   parameters, trailing slash, http/https). Google's page on duplicate URLs: absolute URL, one preferred canonical
   per page (do not give different ones by different techniques), a self-referencing canonical on the canonical page,
   accepted only in the `head`; a script that edits it is a risk, so write it in the served HTML. Do not use
   `robots.txt` or `noindex` to choose a canonical.
3. `robots.txt` and `meta robots`/`noindex` tags consistent with the real intent: a page deliberately
   excluded from the index says so explicitly, never through a forgotten `noindex` lingering on a page
   we want indexed. A page that carries `noindex` must stay fetchable: if `robots.txt` blocks it, the tag is never
   seen (Google's block-indexing page; mechanics in `seo-crawl-control-pitfalls` §2.1).
4. Open Graph / Twitter Card filled in on shareable pages (title, description, image): otherwise social
   sharing shows an empty or generic preview. The Open Graph protocol requires four properties (`og:title`,
   `og:type`, `og:image`, `og:url`) and lists `og:description` as optional (ogp.me); the platform-specific card tag is
   not covered by that page and is unverified here.
5. **`hreflang` on every page that exists in more than one language**, with an `x-default` entry
   as the fallback for users matching no version (Google: typically a language selector or auto-redirecting page),
   listing every language version, the page's own included, each at that version's own URL: without it, a search engine can serve a
   French user the English URL of a page that has a French version, or index both as duplicates of each
   other. Google's localized-versions page adds that the annotations must be
   reciprocal (a version that does not link back is ignored), that URLs are fully qualified with their protocol, that
   the language code comes first, optionally followed by a region (a country code alone is invalid), and that it does
   not use `hreflang` or the `lang` attribute to detect a page's language. This is the direct SEO half of the i18n rules already in
   `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions` — those cover the string/label side, this
   covers the URL/indexing side.

