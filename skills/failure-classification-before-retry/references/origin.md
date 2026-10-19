# failure-classification-before-retry: origin and source stamps

> Provenance of `skills/failure-classification-before-retry`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published sources, never run against a real dependency by us.

## Sources (all read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Google SRE book, "Handling Overload", https://sre.google/sre-book/handling-overload/ | Published online by Google; reused here as idea only | Scope decides retry versus bubble up, per-request and per-client retry budgets, retry at one layer, "overloaded, do not retry" signal |
| Google SRE book, "Addressing Cascading Failures", https://sre.google/sre-book/addressing-cascading-failures/ | same | Randomised exponential backoff, retry limits, layered retries multiplying, retriable versus non-retriable errors, fail fast, retries as symptom |
| RFC 6585 section 4, https://www.rfc-editor.org/rfc/rfc6585#section-4 | IETF Trust, freely redistributable text | Meaning of the "too many requests" status, optional wait hint, counting left to the server |
| An AI vendor's API error reference, https://platform.claude.com/docs/en/api/errors | Vendor documentation, idea only | Error classes (invalid request, authentication, billing, permission, rate limit, spend cap without a hint, internal, timeout, overloaded), backoff for internal errors, mid-stream errors after a success status |
| OmniRoute resilience and empty-turn documents (MIT, commit 9ec0bf15; docs only, no code) | MIT | Own-guidance points flagged in the text: account versus provider scope, busy-not-broken refusals, stalls not cooling the credential, terminal states not overwritten, lazy recovery, concurrent-failure double counting, valid empty turn |

## Removed
1. **Every number**: breaker thresholds, cool-down durations, backoff bases, retry limits and ratios from the
   SRE examples and from the gateway guide.
2. **Product mechanics**: provider names, strategy lists, headers of one vendor's subscription tiers, and the
   multi-account rotation that the gateway is built around (account-limit evasion is not taught here).

## Not verified
1. The gateway's docs are one maintainer's: none of the own-guidance points was checked in its code.
2. RFC 9110 the Retry-After section (semantics) could not be read in this session (the fetch tool returned
   only part of the document); the wait-hint point rests on RFC 6585 and the vendor page.
3. The SRE chapters were read through a fetch tool's summary, not page by page.
4. The vendor's table is dated and changes; re-read it for the dependency in use.

## Related blocks
`skills/go-http-resilience-pitfalls`, `skills/polly-resilience-pitfalls`, `skills/jvm-resilience-observability`,
`skills/dotnet-conventions` §8, `skills/spend-guard-fail-closed`, `skills/observability-instrumentation`.
