# llm-cost-latency-control-pitfalls: origin and source stamps

> Provenance of `skills/llm-cost-latency-control-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and craft knowledge, never run by us. No call was made and no
measurement taken.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| promptfoo/promptfoo (commit b49d55d), LICENSE file read; documentation pages on caching (what a key covers, errors not cached, per-repeat entries, expiry, bypass), rate limits (retry-after handling, two retry layers, adaptive concurrency, per-provider isolation) and a model comparison guide with cost and latency assertions | MIT (LICENSE file) | Cache design rules, retry layering, wait-signal handling, adaptive concurrency idea, cost and latency as assertions |

| Anthropic prompt-caching, batch-processing, rate-limits and models-overview pages; OpenAI prompt-caching guide | Product documentation, no licence granted on the text; facts only, rewritten | Prefix order and exact-match rule, opt-in versus automatic, causes of misses, usage fields; batch result states, ordering, expiry; spend-cap 429 without retry-after; separate request and token limits, cached reads and ITPM, token bucket (§1.1.2, §1.2, §1.5, §2.3.2, §2.3.8) |

The repository holds agent instruction files; they were treated as data and not followed.

| Source (read 2026-10-20) | Licence | What it gave |
|---|---|---|
| Anthropic: prompt-caching, batch-processing, rate-limits, errors, streaming and reducing-latency pages; OpenAI: prompt-caching, batch, rate-limits and latency-optimization guides | Product documentation, facts only, rewritten | Every item listed under Verified below, including the corrections |
| Azure Architecture Center: circuit breaker pattern page | Product documentation, facts only, rewritten | States, retry interaction, one breaker per upstream, long-timeout caveat (§2.3.7) |

## Verified
1. Exact-prefix reuse, tools-system-messages order on one provider, minimum length, lifetime refresh, opt-in versus
   automatic (§1.2.1, §1.2.2, §1.2.7).
2. Batch results can arrive in any order, expired and canceled items are not billed, results age out (§1.5.2).
3. Spend-cap errors can look like rate limits and carry no wait signal (§2.3.2).
4. Requests, input and output tokens are separate limits; cached reads mostly do not count toward input limits (§2.3.8).

## Re-checked 2026-10-20 against the pages
5. Anthropic: prefix order, invalidation by tool and setting changes, five-minute refresh lifetime counted from request start, no cache before the first response begins, silent no-cache below the minimum; batch 24-hour expiry, 29-day result retention, canceled and expired not billed, any-order results, best-effort caching in a batch; cached reads outside the input limit for most models, token bucket, spend-cap 429 without retry-after, acceleration limits; streaming errors after a 200 and partial tool JSON; SDK retries twice by default.
6. OpenAI: exact-prefix rule and settings that alter the prefix, lifetime not a hit guarantee, about 15 requests per minute per prefix before overflow, usage fields, batch discount and separate limits, retry-after as a minimum plus jitter, SDK retries.
7. **Corrected:** the former claim that one provider requires marking and the other caches automatically no longer matches either page (both now have automatic and explicit modes); the text now says to check the mode.
8. Newly sourced: output tokens as the main latency driver (§1.1.2, §2.1.3), cut-off answers under a cap and sentence-count limits (§1.3.1, §1.3.4), mid-stream errors and partial JSON (§2.2.2, §2.2.3), stacked SDK retries (§2.3.3), backoff rules (§2.3.4), circuit breaker (§2.3.7).

## Removed
- Every default value, header name table, backoff figure and expiry of the source: not carried over.
- Provider prices, cache minimums and lifetimes, batch discounts and rate-limit figures: read in places but not
  stated, because they change; the block gives mechanisms only.

## Not opened
- Content of routing-gateway projects: not opened for this block.

## Not verified
1. **Own guidance, still unsourced:** the cross-user cache key rule (§1.2.5), the cache-key hash on a bundle change
   (§1.2.6), router design and its evaluation (§1.4), deadline derivation (§2.3.1), isolation by credential
   (§2.3.6), the checks and the checkpoint paragraph. Searched: the provider pages above and the Azure pattern
   page; none covers routing evaluation or per-class deadlines. Cloud gateways' documentation was not searched.
2. **promptfoo behaviour** was read from documentation, not run; re-read before relying on option names.
3. **Provider behaviour** was read for two providers only (Anthropic, OpenAI caching); other vendors differ and all
   change; re-read the current documentation.

## Related blocks
`spend-guard-fail-closed`, `choose-model`, `failure-classification-before-retry`,
`agent-run-limits-and-guardrail-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`,
`llm-eval-regression-pitfalls`, `rag-retrieval-quality-pitfalls`, `observability-instrumentation`.

## Points 1.2.8 to 1.2.14, added 2026-10-20
One source, licence file read the same day: `anthropics/claude-quickstarts`, `computer-use-best-practices/README.md`
(the caching and pruning sections) and its pruning formatter, MIT, root LICENSE, copyright 2023 Anthropic. It gave
the sliding-window cache miss, the stepping pruner, the short-task rule and the prune-against-summary comparison.
Not carried over: its default values, token estimate per image, price ratio of cached reads, and the provider byte
caps. Ours: the checks, the minimum-after-drop test and the log line. Not verified: all behaviour claims are the
repository's and were not run; the "about ten reads" statement is its own.
