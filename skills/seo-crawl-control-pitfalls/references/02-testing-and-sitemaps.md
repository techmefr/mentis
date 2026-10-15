# seo-crawl-control-pitfalls §2 — Testing the file, and sitemaps

Reading a robots.txt, even with §1 open, is how the wrong belief survives. The matcher that §1 describes is
available as a small program, and it is the cheaper way to know what a file does.

## 2.1 Test against real URLs
1. **Ask the reference matcher, do not reason about the file.** The library ships a small program that takes a
   robots.txt, a crawler name and a URL, and prints whether the URL is allowed or disallowed; its exit code is 0
   for allowed and 1 for disallowed. The README builds it with Bazel or with CMake and a C++14 compiler. The
   library is described as slightly modified production code of Google's crawler, so it answers for that crawler.
2. **Keep two URL lists next to the file.** Own guidance: one list that must stay allowed and one that must stay
   blocked, run for every crawler the file names, so that a later edit that flips a result fails a check, and the
   exit code of the program is enough for that. Include a URL with a query string, one in different letter case,
   one directory with its index file and one with a non-ASCII character in its path.
3. **Hand the matcher escaped URLs.** The README says the URL must follow RFC 3986 because the library does not
   fully normalise it; a URL written with raw non-ASCII characters is not tested as the crawler will see it.
4. **An empty file allows everything**, and the program prints a notice saying so.
5. **What the matcher does not model.** Anything a crawler does around parsing and matching, such as one crawler
   following another's group, is outside it (README). It also answers only whether a URL may be fetched; how a
   `Disallow` and a `noindex` tag interact was not verified here (`seo` §1.3 asks for consistency and gives no
   mechanics).
6. **A robots.txt protects nothing.** Own guidance: it is a request that well-behaved crawlers honour, and it is
   itself public, so a `Disallow` that lists a private path also advertises it. Access control belongs to the
   server.

## 2.2 Sitemaps
1. **Size limits.** The Web Quality Skills `seo` skill states a maximum of 50,000 URLs or 50 MB per sitemap file and
   a sitemap index for larger sites. It does not say whether the size is counted compressed or not, and the
   sitemap protocol was not read here, so check the limit at the source before building a splitter around it.
2. **Only canonical, indexable URLs.** The same list says to include only canonical, indexable URLs, which is the
   sitemap side of the canonical rule of `seo` §1.2.
3. **A `Sitemap` line in a robots.txt is read and does nothing to access.** The parser recognises the directive
   (and the misspelling `site-map`), and the matcher takes no action on it: it never changes whether a URL is
   allowed, and it does not end a group (§1.2).
