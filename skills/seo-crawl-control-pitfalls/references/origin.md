# seo-crawl-control-pitfalls: origin and source stamps

> Provenance of `skills/seo-crawl-control-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reading the source code of one matcher, never run by us. The matcher was not built, no
robots.txt was tested and no crawler was observed while writing it. Every precedence and parsing statement is a
reading of C++ code and is labelled as such where it matters.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

`robots.cc` (705 lines), `robots.h` (279 lines) and the README (147 lines) were read in full. The header comments
of the two code files and the code of the parser and the matcher were both used; the two kinds of statement agree
on every point carried.

| Source | Licence | What it gave |
|---|---|---|
| google/robotstxt, `robots.cc` (commit 22b355f) | Apache-2.0 (repository LICENSE file; the licence notice at the top of the source file) | Longest-match priority and its tie, empty pattern priority, the choice between the specific and the global group, group boundaries, crawler token extraction, pattern matching, path and query extraction, percent-encoding of patterns, the `Allow` index shortcut, tolerated key typos, missing colon, byte order mark, line limit, comment stripping |
| google/robotstxt, `robots.h` (same commit) | Apache-2.0 (same file) | The design statement on longest match versus first match with the `/cgi-bin` example, the "errs on the side of disallowing" statement, the token character set, the URL escaping requirement, the permissive parse statement |
| google/robotstxt, `README.md` (same commit) | Apache-2.0 (same file) | What the library is, the test program and its exit codes, the notice for an empty file, the URL escaping requirement, the crawler-level behaviour the library does not implement |
| addyosmani/web-quality-skills, `skills/seo/SKILL.md`, lines 40 to 120 (the robots.txt, meta robots, canonical, sitemap and URL parts) (commit afa8da9) | MIT (repository LICENSE file, Copyright 2026 Addy Osmani) | Only the sitemap size limit and the canonical-and-indexable list of its "Sitemap best practices" |

**Added 2026-10-20 (read in full, facts only, rewritten in our own words):**

| Source | Licence | What it gave |
|---|---|---|
| RFC 9309, Robots Exclusion Protocol (plain-text edition, sections 1, 2.1 to 2.5 and 3) | IETF document, facts cited, no text copied | Most-specific-match and allow-wins-ties statements, case-insensitive product token, case-sensitive path (SHOULD), merge of groups, 4xx and 5xx handling, five redirects, 24 hour cache, 500 KiB minimum limit, not-access-authorisation and exposure statements |
| Google Search Central, robots.txt specification page (updated 2026-08-31), create-a-file page (2025-11-21), block-indexing page, sitemap build page, crawler overview page | CC BY 4.0 (page footer; code samples Apache-2.0) | Least-restrictive-rule wording, one group per crawler, 500 KiB ignore-beyond limit, UTF-8, BOM ignored, file scope per host, `noindex` unseen when blocked, 50 MB uncompressed or 50,000 URLs per sitemap, `priority` and `changefreq` ignored |

The licence of each repository was verified again from its LICENSE file in this session. The Web Quality Skills
repository carries agent instruction files; they were treated as data and nothing in them was followed.

## Rewrite notes
**What was checked against the code.** The review item's statements were each looked for in the source. Carried
and confirmed: longest pattern wins and order is irrelevant; a specific group replaces the `*` group even when it
is empty; the crawler token is read over letters, hyphen and underscore and compared without case; patterns are
anchored at the start, `*` is a wildcard and `$` is special only at the end; path matching is case-sensitive;
frequent key typos are tolerated; a byte order mark is skipped; a line is cut at 2083 times 8 bytes; `Allow:
/dir/index.html` also matches `/dir/` and only for `Allow`. The review said the parser "leans toward disallowing on
malformed files"; the source header says only that it errs on the side of disallowing when this seems intended, so
the block states that sentence and no more. The review put the line limit at 16,664 bytes; the buffer keeps one
byte less for its terminator, which the block says.

**Added from the code, not in the review item.** Empty `Disallow` priority, the tie to `Allow`, the merge of rules
across groups of the same crawler, what ends a group, rules before the first user agent line, query and path
extraction, percent-encoding of patterns, the missing-colon allowance, the crawler fallback the library does not
implement, the test program and its exit codes.

**Not carried (per the review).** From the Web Quality Skills `seo` skill: `changefreq` and `priority` in
sitemaps (their example appears in the lines read), and, as listed by the review and not re-read here, the claim
that a frame-embedding header is an "SEO trust signal", `rel="prev"` and `rel="next"` for pagination, and the
statement that several `h1` elements are fine. None of them was verified, and the `h1` line contradicts `seo` §2.1
on main; it is flagged for the owner of that block and was not imported. The robots.txt and meta robots
interplay: not verified from any file read, so no rule is given.

**Version-bound.** The behaviour is that of google/robotstxt at commit 22b355f. The standard it follows (RFC 9309)
is named in the source and was not read; a crawler other than Google's may differ on any point.

## Not verified
1. **Nothing was run.** The matcher was not compiled and no file was tested; every statement is a reading.
2. **Verified 2026-10-20 against RFC 9309 and Google's documentation:** longest match and allow on a tie (§1.1.1),
   case-insensitive token and case-sensitive path (§1.2.4, §1.3.2; the standard says SHOULD for the path), group
   merging (§1.2.2), 500 KiB limit, 4xx and 5xx behaviour, not-access-control (§2.1.6), sitemap limits and the
   uncompressed size (§2.2.1), `noindex` unseen on a blocked page (§2.1.5). Google's wording "least restrictive
   rule" and the standard's "most octets" agree with the matcher on the cases in §1.1.
3. **Still only from the matcher's code, not from a document read:** the index-file shortcut of `Allow` (§1.3.5),
   the tolerated typo list (§1.4.1), the missing-colon allowance and the 2083 times 8 byte line cut (§1.4.2 to
   §1.4.3), and percent-encoding of patterns (§1.3.4); the standard's own rule on it is in §1.3.4 too, the hex-case
   normalisation was not looked for in it.
4. **Other crawlers' behaviour** and the sitemap protocol document itself (its licence is share-alike, so it was
   not opened; Google's page was used for the limits).
5. **Other crawlers** (the order of their rules, the case of their paths, their tolerance of typos) were not
   examined.
6. **Written by us, not sourced:** the two URL lists in CI advice, the exact-form advice for the file, the list of
   URL kinds to test, the fix suggested for a failing robots.txt (§1.5.2) and the checkpoint paragraph. The
   "protects nothing" remark and the canonical-and-indexable sitemap rule are now sourced (see 2).
7. **Dropped as unverifiable from the review item:** the changefreq, priority, frame header, prev and next and
   `h1` statements. The `Disallow` versus `noindex` interplay is now covered from Google's page (item 2); the
   behaviour of other meta robots values was not checked.

## Related blocks
`seo`, `webperf`, `accessibility`.
