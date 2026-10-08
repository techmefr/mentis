# go-http-resilience-pitfalls: origin and source stamps

> Provenance of `skills/go-http-resilience-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. This block is meant to be folded
into `go-conventions` when the extended version of that block (the branch that takes it to nine sections)
lands; until then it stands alone so nothing cites a section that is not on the main branch.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| `net/http` package documentation and the `net/http` server and request source doc comments | BSD-3, read 2026-10-08 | Server timeout fields and fallbacks, header limit, `MaxBytesReader`, `DefaultClient`, `Client.Timeout` scope, client reuse, body EOF and close, `Shutdown` |
| Go 1.22 release notes | CC-BY-4.0 text, read 2026-10-08 | Method and wildcard mux patterns, `PathValue`, precedence, `httpmuxgo121` |
| Go 1.25, 1.26 and 1.27 release notes | CC-BY-4.0 text, read 2026-10-08 | `hostport` vet analyser, mux redirect 307, body auto-drain and `MaxHeaderValueCount` |
| `context` package documentation | BSD-3, read 2026-10-08 | Cancel obligation, vet check, `WithoutCancel` since 1.21 |
| The gosec rule list (G108, G112, G114, G119) | Apache-2.0, read 2026-10-08 | Which of these defaults a scanner flags |
| The Go diagnostics guide | CC-BY-4.0 text, read 2026-10-08 | Profile handlers on a custom mux and port |

## Removed in the verification pass (no page supporting them)
Circuit breaking of repeated failures (no page read), and "bound request body size" as a flat number. The
earlier review also listed "derive request context for downstream calls" and "always close response bodies"
as new rules; both are already `go-conventions` §3.2 and §4.1 and are cross-referenced, not repeated.

## Not verified
1. **Own guidance, flagged as such in the text:** choosing timeout values per endpoint, using the standard
   mux before a router, the client-error status for an oversize body, the internal profiling listener, a
   deadline for work under `WithoutCancel`, the whole of §3.3 (retry safety, capped backoff with jitter,
   waiting on the context, no retry on client errors, logging once), and a size-limited drain before Go 1.27.
2. **The size limit of the Go 1.27 auto-drain** is described only as "conservative"; no figure was read.
3. **How the default client treats sensitive headers on redirect** is quoted from a summary of the `Client`
   documentation, not from the exact paragraph.

## Related blocks
`go-conventions` §3 and §4, `go-container-runtime` §3, `api-design`, `security-hardening`.
