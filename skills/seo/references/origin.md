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

§8 written on 2026-10-21 from the AI-visibility notes of the small-business plugin set in
anthropics/knowledge-work-plugins (Apache-2.0; the repository root LICENSE file was read, the plugin has no licence
file of its own), rewritten in our own words. Crawler-rule and structured-data facts were re-checked on
2026-10-20 (below). Not taken: its list of crawler tokens and operators
(they change; the section sends the reader to each operator's documentation), its example robots and summary
files, its sample answers with a named business, its catalog-refresh batching and its connector write paths. The
summary-file convention is kept as optional and unproven, consistent with §7.8. Never run on a real site.

## Re-verified 2026-10-20 (🟡, nothing run)

Every point below was checked against the page named, on that date, for facts only; the wording is ours.

| Source | Licence | Checked |
|---|---|---|
| Google Search Central: SEO starter guide, title links, duplicate URLs and canonicals, localized versions, qualify outbound links, redirects, URL structure, pagination, Googlebot crawler page (file size), HTTP status codes, JavaScript SEO basics, structured-data policies, Article, Product snippet, Review snippet, Breadcrumb, Organization, LocalBusiness, Video, publication dates, helpful content, spam policies, AI features, block indexing, sitemap build, robots.txt pages, and the changelog (FAQ rich result, llms.txt note) | CC BY 4.0 (page footers; code samples Apache-2.0) | §1.1 to §1.5, §2.1, §2.3, §2.4, §3 (figures below), §4.1, §4.3, §5.3, §5.4, §5.6 to §5.8, §5.9 to §5.13, §5.16, §5.17, §6.1 to §6.7, §7.1, §7.2, §7.5 to §7.8, §7.11, §7.12, §8 |
| web.dev: optimize LCP, optimize CLS, INP | CC BY 4.0 (page footers; code samples Apache-2.0) | LCP image rules and 2.5 s / 4.0 s, CLS dimensions and 0.1 / 0.25, INP 200 ms / 500 ms, all at the 75th percentile |
| RFC 9110 sections 15.4.2 and 15.4.9; RFC 9309 sections 1 and 3 | IETF documents, facts only | permanent and method-preserving redirects, robots.txt not access authorisation |
| Open Graph protocol (ogp.me) | Open Web Foundation Agreement 0.9 (page statement), facts only | four required properties, optional description, image alternative text |

**Corrected.** §2.1 said a single `h1` and an unbroken order were SEO rules: Google says number and order of headings
do not matter for Search, so they are now accessibility and readability rules. §4.1 and §6.4 listed FAQ among the
markups worth adding: Google stopped showing the FAQ rich result in May 2026 and removed its documentation in June.
§5.8 said crawlers handle `meta refresh` inconsistently: Google reads a 0-second refresh as permanent, so the point is
now about server-side redirects being preferred and script redirects failing when rendering fails. §5.11 left open
whether the engine reads previous and next hints: it does not. §6.4 listed the upload date as a video property and
equality with the visible trail for breadcrumbs as a Google requirement: neither is stated on the pages read, so they are marked.
§6.6 said engines discount a refreshed date: not found, reworded. §6.2 "once per entity on the home page" is replaced
by Google's placement rule. §8 had treated a summary file as unproven: Google now says it is not needed and has no
effect. §1.5 x-default is a fallback and not a requirement.

**Confirmed.** Unique titles and descriptions, canonical rules, reciprocal `hreflang` including self, `rel` values
for outbound links, status semantics, real links, pagination canonicals, URL case and hyphens, 2 MB crawl limit,
markup equal to visible content, JSON-LD preferred, author and date rules, helpful-content signals, doorway and
scaled-content definitions, keywords meta tag unused, `noindex` unseen under a `robots.txt` block, robots.txt not an
access control.

**Still unsourced (own guidance, kept marked or unmarked as before).** §5.1, §5.2, §5.5, §5.14, §5.15 (link
checks, orphans), the chain and error-target cases of §5.9 and most of §5.10, §5.18 (interstitials: no page read),
the platform card tag and preview-image rules of §6.7 to §6.9, `WebSite` markup, the contact page requirement and the
named reviewer of §7, source linking and policy pages (§7.3, §7.4), §7.10, §7.13, §7.14, the geographic meta tag,
and the audit method of §8 (from the plugin set credited above).
