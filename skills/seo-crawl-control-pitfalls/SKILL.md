---
name: seo-crawl-control-pitfalls
description: "Use when a robots.txt or a sitemap is written, changed or debugged: which rule wins (longest pattern, rule order irrelevant), a crawler-specific group replacing the star group, where groups start and end, crawler token matching, wildcards and the end anchor, case-sensitive paths, percent-encoding, the index file shortcut of Allow, tolerated typos, a byte order mark and long lines, testing a file against real URLs with Google's reference matcher, and sitemap size limits. Page-level meta, structured data and the audit of a built site are seo."
---

# seo-crawl-control-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the file that decides what a crawler may fetch. `seo` §1.3 says that
`robots.txt` must match the real intent; this block says how one such file is actually read, because the usual
errors are not typos but wrong beliefs about precedence. The two sections share one premise: **a robots.txt is
read by a matcher with fixed rules, and the only way to know what a file does is to ask that matcher about real
URLs**. The rules below were read from the source of Google's open-source matcher (`robots.cc` and `robots.h`),
so they describe that parser; another crawler can differ, and each statement says where it comes from. The sitemap at page level is `seo` §4 and the crawl health of a built site is `seo` §5; this block does not restate them.

## When
- Writing or editing a `robots.txt`, or a block in it for one crawler.
- A page that should be crawled is not, or the reverse, and the file looks right.
- Adding a sitemap, or a site grows past one sitemap file.
- Reviewing a `Disallow` that was written to protect something.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Reading the file: precedence, groups, crawler tokens, patterns, case, encoding, index shortcut, tolerance | a rule is written or a result is surprising | [`01-robots-matching.md`](./references/01-robots-matching.md) |
| 2 | Testing and sitemaps: the reference matcher, what it does not model, sitemap limits | a file is about to be shipped, or a sitemap is added | [`02-testing-and-sitemaps.md`](./references/02-testing-and-sitemaps.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the file was run through the reference matcher with a list of URLs
that must be allowed and a list that must be blocked, for each crawler named in it, including one URL with a
query string, one with different letter case and one directory index (§1, §2). A robots.txt that was only read
by eye is not verified, and a rule copied from this block was not verified until the matcher agreed with it.

## Guardrails
- Never assume the first matching rule or the order of the lines decides; the longest matching pattern does (§1.1).
- Never add a group for one crawler without repeating the rules of the star group that it still needs (§1.2).
- Never write a path in a different letter case from the URL it is meant to block (§1.3).
- Never rely on a tolerated typo, a byte order mark or an over-long line; other crawlers may not be as forgiving
  (§1.4).
- Never put a URL on a blocklist for security: a robots.txt asks crawlers to stay away and protects nothing
  (own guidance, §2.1).
- This block states the behaviour of the matcher at the commit named in
  [`references/origin.md`](./references/origin.md), read in source and not run. How `Disallow` and `noindex` tags
  interact was not verified and no rule about it is given here.

## Origin
Rewritten from reading `robots.cc`, `robots.h` and the README of google/robotstxt (Apache-2.0) and, for the
sitemap limits only, a short list of sitemap practices in the Web Quality Skills `seo` skill (MIT), read 2026-10-16. 🟡: never run by
us; open points are in [`references/origin.md`](./references/origin.md).
