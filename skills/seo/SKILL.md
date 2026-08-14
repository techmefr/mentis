---
name: seo
description: Use when writing or reviewing a frontend page or app meant to be indexed, technical SEO checklist: meta tags, HTML semantics, structured data, Core Web Vitals, sitemap and robots.
---

# seo

Step 6 of the pipeline (`WORKFLOW.md`), complementing
`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`: applies only to pages meant to be indexed
by a search engine (not to back-offices, authenticated internal apps, or dashboards).

## When
As soon as a frontend page is public and has to be findable through search: during `code` (6) or at
review time (`review`, 8) if the diff touches public pages.

## Steps

### 1. Meta and indexing: the non-negotiable base
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
   pointing at the other language's own URL (never at itself): without it, a search engine can serve a
   French user the English URL of a page that has a French version, or index both as duplicates of each
   other. This is the direct SEO half of the i18n rules already in
   `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions` — those cover the string/label side, this
   covers the URL/indexing side.

### 2. HTML semantics: what a crawler and a screen reader read the same way
1. A single `<h1>` per page, an `h1 > h2 > h3` hierarchy with no arbitrary level skipping for a visual
   effect (the visual is handled in CSS, not by changing the tag).
2. Real text content in the HTML served (SSR/SSG), never only injected client-side after hydration for
   content that has to be indexed: a crawler that doesn't run JS sees nothing.
3. Internal links as real `<a href>` tags (navigable, crawlable), never a `<div onClick>` simulating a
   link, with anchor text that describes the destination rather than "click here"/"read more" repeated
   across a page. An outbound link to content we don't vouch for (user-generated content, a comment, an
   unmoderated submission) carries `rel="nofollow ugc"` — otherwise the page passes its own trust to
   whatever the untrusted content links to.
4. A descriptive `alt` attribute on meaningful images, empty (`alt=""`) on purely decorative ones: never
   absent.

### 3. Performance: Core Web Vitals
1. LCP (Largest Contentful Paint): the main above-the-fold image/block doesn't wait on a heavy JS load
   or an avoidable client-side fetch; `loading="eager"`/`fetchpriority="high"` on the LCP image, `lazy`
   on the rest.
2. CLS (Cumulative Layout Shift): explicit dimensions (`width`/`height` or `aspect-ratio`) on
   images/videos/embeds to reserve the space before loading: never content that pushes the layout
   around afterwards.
3. INP (Interaction to Next Paint): no long blocking JS task on the main interactions (click, typing):
   see the perf conventions already set in
   `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`.

### 4. Structured data and discovery
1. JSON-LD (`schema.org`) placed on the content types that benefit from it (article, product, FAQ,
   breadcrumb) when the business need justifies it: not systematically out of reflex on every page
   type.
2. `sitemap.xml` generated (not maintained by hand) and referenced in `robots.txt`, updated on every
   deployment of new content.
3. Readable and stable URLs (slugs, no technical ID exposed without reason): a URL change breaks the
   indexing history, so a 301 redirect is mandatory if a public URL changes.

## Output / checkpoint
The four sections reviewed on the diff touched; for a broader audit of a site already in production
(not just the diff in progress), see the `keymaker` agent.

## Guardrails
- Never applies to non-public pages (auth, back-office, internal dashboard): don't impose this
  checklist outside its scope.
- No JSON-LD over-engineering: only the content types that get a real benefit from it (product page,
  article), not a systematic addition.
- This block has no dedicated in-house production experience yet: to be confronted with the first real SEO
  audit, not to be treated as proven doctrine.

## Origin
Sourced from established market guidelines: Google Search Central (indexing, structured data, Core Web
Vitals), web.dev (LCP/CLS/INP, HTML semantics, images). Mechanisms rewritten as an actionable
checklist, no copied text. Market research, no internal production feedback at this stage.

Re-checked directly against Google's current SEO starter guide
(developers.google.com/search/docs/fundamentals/seo-starter-guide) on 2026-08-10, item by item: two real
gaps closed — `hreflang` for multi-language pages (§1.5, genuinely relevant since the frontend conventions
this block complements already carry an i18n section) and `nofollow`/descriptive anchor text on links to
content we don't vouch for (§2.3). Everything else the guide lists (canonical, sitemap, structured data,
Core Web Vitals, robots control, image alt text) was already covered here under a different heading; the
guide's own "not required" list (keywords meta tag, content-length targets, heading count/order,
PageRank) confirms nothing was missing there either.
