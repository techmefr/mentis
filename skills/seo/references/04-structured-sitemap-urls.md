# § 4 — Structured data and discovery

> Section 4 of `skills/seo`. Read it when a page type could carry structured data, or sitemap, robots or URL shape changes.

1. JSON-LD (`schema.org`) placed on the content types that benefit from it (article, product, FAQ,
   breadcrumb) when the business need justifies it: not systematically out of reflex on every page
   type.
2. `sitemap.xml` generated (not maintained by hand) and referenced in `robots.txt`, updated on every
   deployment of new content.
3. Readable and stable URLs (slugs, no technical ID exposed without reason): a URL change breaks the
   indexing history, so a 301 redirect is mandatory if a public URL changes.

