---
name: seo
description: Use when writing or reviewing a frontend page/app meant to be indexed (Nuxt/React SSR or static), technical SEO checklist: meta tags, HTML semantics, structured data, Core Web Vitals performance, sitemap/robots. No dedicated SEO production experience at Xefi at this stage, sourced from established market guidelines (Google Search Central, web.dev).
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

### 2. HTML semantics: what a crawler and a screen reader read the same way
1. A single `<h1>` per page, an `h1 > h2 > h3` hierarchy with no arbitrary level skipping for a visual
   effect (the visual is handled in CSS, not by changing the tag).
2. Real text content in the HTML served (SSR/SSG), never only injected client-side after hydration for
   content that has to be indexed: a crawler that doesn't run JS sees nothing.
3. Internal links as real `<a href>` tags (navigable, crawlable), never a `<div onClick>` simulating a
   link.
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
(not just the diff in progress), see the `seo-auditor` agent.

## Guardrails
- Never applies to non-public pages (auth, back-office, internal dashboard): don't impose this
  checklist outside its scope.
- No JSON-LD over-engineering: only the content types that get a real benefit from it (product page,
  article), not a systematic addition.
- This block has no dedicated Xefi production experience yet: to be confronted with the first real SEO
  audit, not to be treated as proven doctrine.

## Origin
Sourced from established market guidelines: Google Search Central (indexing, structured data, Core Web
Vitals), web.dev (LCP/CLS/INP, HTML semantics, images). Mechanisms rewritten as an actionable
checklist, no copied text. Market research, no internal production feedback at this stage.
