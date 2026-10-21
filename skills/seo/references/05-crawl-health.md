# § 5 — Crawl and index health of a built site

> Section 5 of `skills/seo`. Read it before a launch, after a migration or a URL change, and whenever a
> built site is audited rather than a single diff reviewed. §1 to §4 describe what each page declares; this
> section checks what a crawler actually finds when it walks the site. The checks need a walk over the
> pages, so they run on a build or a staging copy, not on source files alone. The walker is a short
> script of the project's own (about sixty lines of standard library: fetch, record status and hops,
> parse links, canonical and robots directives, repeat), not a crawling product installed as a dependency
> (`CONVENTIONS.md`, rule B). Facts come from RFC 9110 (redirect statuses, section 15.4), RFC 9309 (robots.txt) and the
> search engine's published documentation, re-read on 2026-10-20 (`references/origin.md`); the sitemap protocol
> itself was not opened.

## What the walk records, per URL

Final status, number of redirect hops, final URL, `Content-Type`, canonical (tag and `Link` header), robots
directives (meta tag and `X-Robots-Tag`), outgoing internal links, and whether the URL was listed in the
sitemap. Everything below is a query over that table.

## Status and links

1. **Every internal link ends on a success.** A link to a missing page, an error page or a timeout is a bug
   in our content or routing; it is fixed or removed, and the check fails the pipeline. Images, scripts and
   stylesheets are links too, and a missing one is the same finding (`skills/webperf` §5.8).
2. **External links are checked, but on a schedule and without failing the build.** A third party's outage
   is not our regression. Report broken outbound links as a list for an owner; retry before reporting.
3. **A page that does not exist says so with the status.** The missing-page response is a real 404 (or 410
   for content removed on purpose), not a 200 with a "not found" message (Google treats 404 and 410 like other 4xx, drops indexed URLs
   that return them, and reports a 2xx error page as a soft 404); see `skills/html-document` for
   the page itself.
4. **A link must be followable.** `href=""`, `href="#"` and `javascript:` addresses are not crawlable and not
   navigable (`skills/accessibility` §6.17). A script-driven navigation that has no `href` is invisible to
   a crawler that does not run it (§2.2); Google finds links only in `<a>` elements with an `href` (JavaScript SEO
   basics).
5. **`mailto:` and `tel:` links are well formed.** The scheme is present, a telephone number is in
   international form and readable without spaces breaking the URI, and the visible text matches the
   target. They are excluded from the crawl as targets.

## Redirects

6. **At most one hop from any URL we link to.** Variants of the same address (protocol, host prefix,
   trailing slash, case) are normalised in a single redirect to the final form, not in a chain; chains
   cost time and crawl budget, and a loop is an outage (own guidance: the pages read give no figure for chains;
   Google's status-code page says it follows up to 10 hops). Internal links and the sitemap point at the final
   URL, never at a redirect.
7. **The status says what it means.** A permanent move uses a permanent redirect status and a temporary
   one uses a temporary status (RFC 9110 sections 15.4.2 and 15.4.9: 301 and 308 are permanent, and 308 and 307 keep the
   method while a user agent may turn a 301 `POST` into a `GET`); Google treats 301 and 308 as a strong and 302 and
   307 as a weak signal about the canonical. The method-preserving variants matter when the request is a
   `POST`. A permanent redirect is kept in place for as long as the old URL is referenced anywhere.
8. **Redirect on the server.** Google ranks server-side redirects as the most reliably understood. A `meta refresh`
   is accepted where the platform offers nothing else (0 seconds read as permanent, a delay as temporary), and a
   script redirect only as a last resort, because rendering can fail and the redirect then goes unseen (Google's
   redirects page). Both also fail timing criteria for readers (`skills/accessibility` §6.14); a client-side route
   change is not a redirect.

## Canonical and indexing directives

9. **A canonical points at a page that deserves it.** The target returns a success, is itself indexable,
   and canonicalises to itself: no chain (A to B to C), no canonical to a redirect, to an error or to a
   page that carries `noindex`. It is an absolute URL, declared once, in the head. When both the tag and a
   `Link` header exist, they agree. Sourced from Google's duplicate-URL page: absolute URL, one preferred canonical,
   `head` only, self-referencing, internal links to the canonical; it recommends the tag or the header, not both.
   Own guidance: the chain, redirect and error-target cases, which that page does not address.
10. **Directives never contradict one another.** The recurring conflicts, each a finding: `noindex`
    on a page that `robots.txt` disallows (the crawler never fetches the page, so it never sees the
    `noindex`, Google's block-indexing page); a `noindex` page listed in the sitemap; `noindex` with a canonical to another page;
    structured data on a `noindex` page; a header directive that disagrees with the meta tag; a snippet
    restriction left over from an experiment. A page excluded on purpose says so in one place and nowhere
    contradicts it (§1.3). Only the first conflict is documented in a page read; the others are own guidance.
11. **Pagination keeps every page reachable.** Each page of a series is a real link, self-canonical, and
    indexable; pointing all of them at the first page hides the items on the rest. Google's pagination page says the engine no longer
    uses previous and next hints (other engines may), that the first page is not the canonical of the series, that
    each page is reached by a real link, and that a fragment is not a page number.
12. **Sponsored and user-supplied links are labelled.** Paid or affiliate links carry `rel="sponsored"`,
    user-supplied ones `rel="ugc"` (§2.3); internal links are not `nofollow` without a recorded reason. The
    disclosure the law asks for next to an affiliate link is `business/legal-documents`.

## Sitemap

13. **The sitemap is valid and exact.** It parses as the sitemap protocol requires, its URLs are absolute,
    on the same host and protocol as the site's canonical form, and within the path scope the sitemap's own
    location allows. It lists the canonical, indexable, successful URLs and nothing else: no redirect, no
    error, no `noindex`, no non-canonical variant. The size and count limits are read from the source and
    answered with a sitemap index, never from a remembered figure (Google's figures are in
    `seo-crawl-control-pitfalls` §2.2). `lastmod` is the real date
    of the last substantive change or it is omitted.
14. **Sitemap and crawl agree in both directions.** Indexable pages the walk found that are missing from the
    sitemap, and sitemap URLs the walk could not reach by links, are both listed; the second set is also
    the list of orphans.

## Link graph and URL shape

15. **No page is an island, and none is a dead end.** From the walk's link table: pages with no inbound
    internal link (orphans), pages reached by one weak link, and pages with no outbound link. A page worth
    indexing is linked from where a visitor would look for it, with descriptive anchor text (§2.3).
16. **URLs are lowercase, hyphenated and stable.** Paths are case-sensitive, so two cases are two pages;
    words are separated by hyphens; the characters are the unreserved set of RFC 3986 and anything else is
    percent-encoded; no session identifier or tracking parameter in an indexable URL; query parameters on
    indexable pages are few and canonicalised (§1.2); one trailing-slash convention is enforced by
    redirect. A URL that is read aloud or copied is short enough to survive a messaging app. Google's URL-structure page
    confirms that case matters, that hyphens are preferred to underscores, that session identifiers are best kept out of
    URLs and that non-ASCII characters in links are percent-encoded; it says nothing on trailing slashes or length,
    which are own guidance.
17. **A large inline state is not content.** The HTML a crawler downloads has a size limit per engine,
    published in its documentation. Google's crawler page (read 2026-10-20) says it
    reads the first 2 MB of a supported file, measured uncompressed, with each referenced resource bound by its own
    limit; what lies beyond is not considered. Content-bearing markup comes early, and a serialised application
    state or a base64 asset the size of the page is not inlined into it (`skills/webperf` §4).
18. **Full-page overlays do not block the content.** An interstitial that covers the page on arrival hides
    the content from visitors and is judged by the engine's guidance on intrusive interstitials; a
    legally required notice (consent, age check) is sized so the content stays readable and the notice
    never traps focus (`skills/accessibility` §1.6). Own guidance: no page on intrusive interstitials was read.

## Mechanical checks

```
curl -sIL -o /dev/null -w '%{num_redirects} %{url_effective}\n' "$URL"
xmllint --noout sitemap.xml
grep -oE '<loc>[^<]+</loc>' sitemap.xml
grep -rniE 'noindex' src public
grep -rnP 'href="(#|javascript:[^"]*|)"' src
grep -rnP 'target="_blank"[^>]*href="https?://' src
```

- Redirect hops greater than one fail; each `<loc>` is requested and a non-success fails; each page's
  canonical is requested and compared with the `Link` header.
- `noindex` hits are crossed with the `Disallow` lines of `robots.txt` and with the sitemap.
- The walker's table answers points 1, 6, 9, 10, 14, 15 and 16 as set differences and counts; its output is
  a list for a person to read, since a legitimate exception exists for most of them.
- URL shape is a regular expression over every crawled URL: uppercase, underscore, characters outside the
  allowed set, length, parameter count.
