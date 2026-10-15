# seo-crawl-control-pitfalls §1 — Reading a robots.txt the way the matcher does

Every point here was read from the source of Google's open-source robots.txt parser and matcher (`robots.cc` and
`robots.h`, version-bound to the commit in `origin.md`), not run. It is the parser Google describes as its
production code, with internal headers removed; it implements the Robots Exclusion Protocol standard (RFC 9309,
named in the source and not read here) with Google-specific allowances. Other crawlers may behave differently.

## 1.1 Which rule wins
1. **The longest matching pattern wins, and the order of the lines does not matter.** Each matching rule gets a
   priority equal to the length of its pattern text, the best priority is kept for Allow and for Disallow, and the
   URL is disallowed only when the best Disallow is strictly longer than the best Allow. A tie therefore goes to
   Allow. The header comment of the matcher states the design decision: with `Allow: /` and `Disallow: /cgi-bin`,
   the expired internet draft's first-match reading would allow everything, and the longest-match reading blocks
   `/cgi-bin`, which is what webmasters mean.
2. **The length counted is the length of the written pattern, wildcards included.** Compare the patterns as text:
   a short pattern with `*` in it does not outrank a longer plain one because it matches more URLs.
3. **An empty `Disallow:` blocks nothing.** The code gives an empty pattern a priority of zero and a URL is
   disallowed only for a priority above zero.
4. **Rules before the first `User-agent` line are ignored.**

## 1.2 Which group applies
1. **A group that names the crawler replaces the `*` group for that crawler, entirely.** Once a `User-agent` line
   has matched the crawler, a URL that none of that group's rules matches is allowed and the `*` rules are never
   consulted, even if the specific group is empty. Repeat in it every rule from the `*` group that the crawler
   still needs.
2. **Rules from several groups naming the same crawler are merged.** The matcher keeps the best match across the
   whole file, not per group; the same holds for several `*` groups.
3. **Only an `Allow` or `Disallow` line closes the list of agents of a group.** Consecutive `User-agent` lines
   share the rules that follow them. Blank lines and comments do not start a new group, and neither do `Sitemap`
   lines or unknown lines, which the matcher does not act on.
4. **The crawler token is cut at the first character that is not a letter, a hyphen or an underscore, then
   compared without regard to case.** `Googlebot/2.1` becomes `Googlebot`, and a value with a space is cut at the
   space. A `*` followed by a space and more characters is still read as the global group.
5. **Fallbacks between crawler tokens are not in the library.** Its README gives the example of an image crawler
   following the rules written for the main crawler when it has no group of its own and says the library does
   not implement that. Read the crawler's own documentation for it; none was read here.

## 1.3 Patterns and URLs
1. **A pattern is anchored at the start of the path, `*` matches any run of characters, and `$` means the end
   only when it is the last character of the pattern.** Anywhere else `$` is an ordinary character. A pattern
   without the end anchor matches every path that begins with it.
2. **Paths are compared with case.** The comparison of path and pattern is exact, character by character, so
   `Disallow: /Private` does not cover `/private`; the crawler token and the directive names are the parts that
   ignore case. This was read in the matching function, not observed.
3. **The matcher sees the path, its parameters and its query.** The scheme, host and fragment are removed, so a
   rule can target a query string.
4. **Patterns are normalised, URLs are not.** Characters outside ASCII in a pattern are turned into percent-encoded
   octets and the hexadecimal digits of existing escapes are made upper case. The URL handed to the matcher must
   already be in escaped form (RFC 3986); the README says the library does not fully normalise it.
5. **`Allow` has an index-file shortcut, `Disallow` has none.** When an `Allow` pattern does not match the path
   and its last segment starts with `/index.htm`, the matcher retries with the directory part of the pattern
   followed by the end anchor. `Allow: /dir/index.html` therefore also allows `/dir/`.

## 1.4 What the parser forgives
1. **Directive names are matched by prefix and without regard to case.** The tolerated misspellings are
   `useragent` and `user agent` for the user agent line, five variants of `disallow` (`dissallow`, `dissalow`,
   `disalow`, `diasllow`, `disallaw`) and `site-map` for the sitemap line; there is none for `allow`.
2. **A missing colon is accepted** when the line has exactly two parts separated by white space. Text after `#` is a
   comment.
3. **A leading byte order mark is skipped, and a line longer than 2083 times 8 bytes, which is 16,664, is cut.**
   The line buffer keeps one byte less for its terminator, and the rest of a longer line is ignored. Line feed,
   carriage return and carriage return plus line feed are all handled as line endings.
4. **The matcher accepts any input and skips what does not look like a directive.** Its header says it does not
   follow the standard strictly, because many files do not conform, and that it errs on the side of disallowing
   when that seems intended.
5. **None of this is a contract.** Own guidance: write the file as the standard describes it, with the exact
   directive names, a colon, a file without a byte order mark and short lines, so that a stricter crawler reads
   the same thing as the lenient one.
