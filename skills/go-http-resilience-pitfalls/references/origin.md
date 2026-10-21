# go-http-resilience-pitfalls: origin and source stamps

> Provenance of `skills/go-http-resilience-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 22 checked, 22 matched, 0 corrected, 0 unverified
**Status: 🟡.** Written from documentation and reading, never run by us. Overlaps with `skills/go-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| `net/http` package documentation and the `net/http` server and request source doc comments | BSD-3, read 2026-10-08 | Server timeout fields and fallbacks, header limit, `MaxBytesReader`, `DefaultClient`, `Client.Timeout` scope, client reuse, body EOF and close, `Shutdown` |
| Go 1.22 release notes | CC-BY-4.0 text, read 2026-10-08 | Method and wildcard mux patterns, `PathValue`, precedence, `httpmuxgo121` |
| Go 1.25, 1.26 and 1.27 release notes | CC-BY-4.0 text, read 2026-10-08 | `hostport` vet analyser, mux redirect 307, body auto-drain and `MaxHeaderValueCount` |
| `context` package documentation | BSD-3, read 2026-10-08 | Cancel obligation, vet check, `WithoutCancel` since 1.21 |
| The gosec rule list (G108, G112, G114, G119) | Apache-2.0, read 2026-10-08 | Which of these defaults a scanner flags |
| The Go diagnostics guide | CC-BY-4.0 text, read 2026-10-08 and again 2026-10-20 | Profile handlers on a custom mux and port; the package registers on the default mux |
| `net/http` package documentation (pkg.go.dev, Server fields, `MaxBytesReader`, `Client`, redirect header rule, `MaxHeaderValueCount` default 500), re-read | BSD-3 (Go licence), read 2026-10-20 | Confirmed timeout fallbacks, header limits, redirect rule (same domain or subdomain), 500 default |
| Go 1.22, 1.23 and 1.27 release notes, re-read | CC-BY-4.0 text, read 2026-10-20 | Mux patterns confirmed; timers of Go 1.23 collected when unreferenced (go.mod gated); 1.27 drain has no figure |
| `context` package documentation, re-read | BSD-3, read 2026-10-20 | Cancel obligation, `WithoutCancel` confirmed |
| gosec README and RULES.md (securego/gosec) | Apache-2.0 (README states it; the LICENSE file fetch by raw URL returned 404, so the file itself was not read) | One-line descriptions of G107, G108, G112, G114, G119 only |
| RFC 9110 HTTP Semantics, section 9.2.2 | IETF standard, read for facts only 2026-10-20 | Idempotent methods, automatic retry rule |
| cenkalti/backoff README and LICENSE | MIT (LICENSE read 2026-10-20) | Only that it exists; the README gives no behaviour detail, nothing taken |

## Removed in the verification pass (no page supporting them)
Circuit breaking of repeated failures (no page read), and "bound request body size" as a flat number. The
earlier review also listed "derive request context for downstream calls" and "always close response bodies"
as new rules; both are already `go-conventions` §3.2 and §4.1 and are cross-referenced, not repeated.

## Verification pass 2026-10-20
- **Sourced:** `MaxHeaderValueCount` default (500) and counting rule, the server closing request bodies, pprof on
  the default mux, the redirect-header rule (corrected from "not trusted" to "not the same domain or a
  subdomain"), the Go 1.23 timer note added to §3.3.3, retry safety (§3.3.1, RFC 9110), gosec rule meanings.
- **Corrected:** SKILL guardrail pointed at §3.2 for retries; now §3.3. redirect policy wording (part 2, redirects).
- **Deleted:** nothing.
- **Opened by mistake:** one vendor engineering article on retries was opened, its licence is not stated, and
  nothing was taken from it; it is not a source. Blog results from a search were not opened.
- **Still own guidance:** §3.3 points 2 to 5 (cap, jitter, wait on context, no retry of client errors, log once),
  timeout values, standard mux preference, 4xx status on oversize body, size-limited drain, internal profiling
  listener. No permissive source found, searched: Go documentation, gosec, cenkalti/backoff README.

## Not verified
1. **Own guidance, flagged as such in the text:** choosing timeout values per endpoint, using the standard
   mux before a router, the client-error status for an oversize body, the internal profiling listener, a
   deadline for work under `WithoutCancel`, the whole of §3.3 (retry safety, capped backoff with jitter,
   waiting on the context, no retry on client errors, logging once), and a size-limited drain before Go 1.27.
2. **The size limit of the Go 1.27 auto-drain** is described only as "conservative"; no figure was read.
3. **The redirect header rule** was read in the package documentation on 2026-10-20 (point resolved); the
   `Cookie` jar interplay was not read.

## Related blocks
`go-conventions` §3 and §4, `go-container-runtime` §3, `api-design`, `security-hardening`.
