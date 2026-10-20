# delivery-metrics-definition-pitfalls: origin and source stamps

> Provenance of `skills/delivery-metrics-definition-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from own craft knowledge, never applied to a real delivery dashboard by
us.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read for this block | not applicable | The terms (deployment frequency, lead time, change failure rate, time to restore) are common industry vocabulary used here as names for definitions the block asks the reader to write down |

No credit is owed: no text, structure or number was taken from a source. The research framework that popularised
the four terms was not opened, its licence was not confirmed as open, and the block does not claim to describe it.

## Removed
1. **Every benchmark, performance band and threshold.** None was read, so none is stated.
2. **Any definition attributed to a named framework.** The definitions here are the reader's to choose and write.

## Not verified
1. All of the content is own guidance from general knowledge; nothing may be quoted as a source claim.
2. Whether the framework's own definitions differ from the ones suggested here was not checked. If a team must
   report against that framework, re-read its current publication first.
3. The survey and toil points were not compared with any published method.
4. Nothing was run and no data was computed in writing this block.

Dogfood 2026-10-20: one static read on a real project, nothing run; the block was found not applicable there and nothing was wrong in it; fix: a skip-when exit when no delivery metric exists and a guardrail against inventing one. The status stays 🟡.

## Related blocks
`skills/saas-metric-definition-pitfalls`, `skills/semantic-layer-metric-pitfalls`,
`skills/metric-movement-diagnosis-pitfalls`, `skills/slo-design`, `skills/blameless-incident-review-pitfalls`,
`skills/release-strategy-and-progressive-delivery-pitfalls`, `skills/source-freshness`.
