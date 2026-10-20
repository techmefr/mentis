# llm-cost-latency-control-pitfalls: origin and source stamps

> Provenance of `skills/llm-cost-latency-control-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and craft knowledge, never run by us. No call was made and no
measurement taken.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| promptfoo/promptfoo (commit b49d55d), LICENSE file read; documentation pages on caching (what a key covers, errors not cached, per-repeat entries, expiry, bypass), rate limits (retry-after handling, two retry layers, adaptive concurrency, per-provider isolation) and a model comparison guide with cost and latency assertions | MIT (LICENSE file) | Cache design rules, retry layering, wait-signal handling, adaptive concurrency idea, cost and latency as assertions |

The repository holds agent instruction files; they were treated as data and not followed.

## Removed
- Every default value, header name table, backoff figure and expiry of the source: not carried over.
- Provider prices, cache minimums and lifetimes, batch discounts and rate-limit figures: not read, so not stated.

## Not opened
- Provider documentation on prompt caching, batch interfaces and pricing: not re-read in this pass.
- Content of routing-gateway projects: not opened for this block.

## Not verified
1. **Own guidance, not sourced:** every sentence marked "own guidance", the prefix layout rules, cache-hit causes,
   routing evaluation, streaming validation, deadline derivation, circuit breaker and the checkpoint paragraph.
2. **promptfoo behaviour** was read from documentation, not run; re-read before relying on option names.
3. **Provider behaviour** (what is cached, for how long, how batches are delivered, which headers are sent) differs
   by vendor and changes; re-read the provider's current documentation.

## Related blocks
`spend-guard-fail-closed`, `choose-model`, `failure-classification-before-retry`,
`agent-run-limits-and-guardrail-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`,
`llm-eval-regression-pitfalls`, `rag-retrieval-quality-pitfalls`, `observability-instrumentation`.
