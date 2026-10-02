# seo — origin and source stamps

> Provenance of `skills/seo`. Read it when a rule has to be traced back to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

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

Correction on 2026-10-02: §1.5 said an `hreflang` set points at the other language's URL "never at itself".
The search engine's multilingual documentation says each version lists itself as well as the others;
§1.5 now says so.

§5 to §7 written on 2026-10-02 after reading the public `Front-End-Checklist` repository (README and
package metadata declare MIT; no licence file is present, so only the list of topics was used and no
sentence was reused). The facts come from primary documents: RFC 9110 (redirection statuses), RFC 9309
(robots exclusion), RFC 3986 (URI characters), the sitemap protocol, the Open Graph protocol, schema.org,
and the search engine's published documentation on canonicalisation, redirects, sitemaps, structured data,
helpful content and spam policies, all read as the engine's own current statements. The editorial and local
material (§7) was first classed out of scope in the coverage matrix and then reinstated as
harness-independent knowledge a developer or product owner needs; the ranking-myth items (keyword density,
word count, reading level, geographic meta tag, keywords meta tag, machine-oriented summary file) are kept
out on purpose and listed in §7.6 to §7.8 so nobody re-adds them. Not taken: crawling products and
validators as dependencies (rule B), any size or count limit recited from memory, and a list of which rich
results are currently displayed (it moves).
