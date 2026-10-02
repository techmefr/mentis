# § 1 — Meta and indexing: the non-negotiable base

> Section 1 of `skills/seo`. Read it for any public page: titles, canonical, robots, social tags, languages.

1. Every page has a unique `<title>` and its own `<meta name="description">` (no copy-pasted duplicate
   between pages, no generic default value left in production).
2. A `canonical` tag as soon as the same page is reachable through several URLs (sort/filter
   parameters, trailing slash, http/https).
3. `robots.txt` and `meta robots`/`noindex` tags consistent with the real intent: a page deliberately
   excluded from the index says so explicitly, never through a forgotten `noindex` lingering on a page
   we want indexed.
4. Open Graph / Twitter Card filled in on shareable pages (title, description, image): otherwise social
   sharing shows an empty or generic preview.
5. **`hreflang` on every page that exists in more than one language**, including a `x-default` entry,
   listing every language version, the page's own included, each at that version's own URL: without it, a search engine can serve a
   French user the English URL of a page that has a French version, or index both as duplicates of each
   other. This is the direct SEO half of the i18n rules already in
   `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions` — those cover the string/label side, this
   covers the URL/indexing side.

