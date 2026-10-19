# § 6 — Delivery: what the response itself carries

> Section 6 of `skills/webperf`. Read it when a page is slow before any resource arrives, when a hashed
> asset is re-downloaded on every visit, or when a build is about to ship. This block checks what the
> response carries; the server or CDN configuration that produces it belongs to
> `skills/devops-conventions`.

## Rules

1. **Time to first byte is its own number.** Measure it separately from everything after it: a high
   value points at the server, a redirect chain, a cold start or a database query, and no amount of
   front-end work moves it. Take several samples, since the first request often pays for a cold cache. A
   chain of redirects before the document is part of this number (`skills/seo` §5).
2. **Text responses are compressed.** HTML, CSS, JavaScript, JSON, SVG and fonts in formats that are not
   already compressed travel compressed; images and video, which already are, do not gain. The response
   states its encoding in `Content-Encoding`, and a `Vary: Accept-Encoding` keeps a shared cache honest.
   Check it on the production-like path, since a proxy in front can strip it.
3. **Caching follows the file name.** A file whose name contains a hash of its content never changes
   under that name, so it can be cached for as long as the policy allows and marked immutable. The HTML
   document that points at those names is revalidated, or cached very briefly, so a release reaches
   visitors at once (RFC 9111 and RFC 8246 for the directives). A long cache on a file whose name is
   stable is a bug that ships stale code to people for weeks; no cache at all on a hashed file wastes
   every repeat visit.
4. **The content type is exact.** A script served as plain text, or a stylesheet with the wrong type, is
   refused or ignored by the browser, and a missing `nosniff` lets it guess. The type comes from the
   file, and `X-Content-Type-Options: nosniff` is part of `skills/security-hardening`.
5. **Source maps are a decision.** A production build either serves them (useful for error monitoring,
   exposes readable source and comments) or does not (smaller attack surface, harder stack traces), or
   uploads them privately to the monitoring tool and ships none. State which, once, per project. Whatever
   is chosen, a secret inlined at build time is not made safe by hiding its map (`skills/security-hardening`
   §4.2).
6. **A hosting detail is not a code detail.** HTTP version, edge networks and image-resizing services
   change latency without changing code; they are recorded in the project's infrastructure notes and
   changed there.

## Mechanical checks

```
curl -sI -H 'Accept-Encoding: br,gzip' "$URL" | grep -i '^content-encoding'
curl -sI "$HASHED_ASSET_URL" | grep -iE '^(cache-control|content-type)'
curl -sI "$URL" | grep -iE '^(cache-control|content-type)'
curl -s -o /dev/null -w '%{time_starttransfer}\n' "$URL"
find dist -name '*.map'
grep -rlE 'sourceMappingURL' dist
```

- Run the time-to-first-byte request three times and read the spread, not one sample.
- The hashed asset is expected to carry a long, immutable policy; the document is expected not to.
- Source maps in `dist` are a finding only if the project's recorded decision says it ships none.
