# delivery-metrics-definition-pitfalls: origin and source stamps

> Provenance of `skills/delivery-metrics-definition-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from own craft knowledge, with metric names and cautions checked against
the framework's own guide on 2026-10-20; never applied to a real delivery dashboard by us.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| dora.dev guide to the framework's software delivery metrics | official guide, licence not verified, facts only, rewritten, nothing copied, read 2026-10-20; credit: dora.dev | Metric names and the fifth metric, start and end of lead time, failure meaning, throughput and instability grouping, cautions on targets and comparison (§1.1, §1.4, §1.5, §1.11, §2.1-3) |
| dora-team/fourkeys | Apache-2.0 (`LICENSE` read 2026-10-20) | Not opened beyond the licence file |

## Removed
1. **Every benchmark, performance band and threshold.** None was read, so none is stated.
2. **Any definition attributed to a named framework.** The definitions here are the reader's to choose and write.

## Not verified
1. Metric names, lead-time boundaries, failure meaning, grouping and the cautions on targets and comparison are
   checked. The rest (batch size, clocks, definition versioning, cycle-time breakdown, toil, surveys, individuals) is
   own guidance; nothing there may be quoted as a source claim.
2. The guide's other pages (surveys, capabilities, bands) were not read. The framework's benchmark bands and
   research reports were not opened, and the block does not claim to describe them. If a team must report against
   the framework, re-read its current publication first.
3. The survey and toil points were not compared with any published method.
4. Nothing was run and no data was computed in writing this block.

Dogfood 2026-10-20: one static read on a real project, nothing run; the block was found not applicable there and nothing was wrong in it; fix: a skip-when exit when no delivery metric exists and a guardrail against inventing one. The status stays 🟡.

## Related blocks
`skills/saas-metric-definition-pitfalls`, `skills/semantic-layer-metric-pitfalls`,
`skills/metric-movement-diagnosis-pitfalls`, `skills/slo-design`, `skills/blameless-incident-review-pitfalls`,
`skills/release-strategy-and-progressive-delivery-pitfalls`, `skills/source-freshness`.
