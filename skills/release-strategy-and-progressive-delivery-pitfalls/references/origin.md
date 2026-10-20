# release-strategy-and-progressive-delivery-pitfalls: origin and source stamps

> Provenance of `skills/release-strategy-and-progressive-delivery-pitfalls`. Read it when a rule has to be traced
> to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two documentation articles and own craft knowledge, never run on a
real release by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MicrosoftDocs/architecture-center (LICENSE file read: Attribution 4.0 International): the multitenant article on updates, and the article on blue-green deployment of a cluster | CC BY 4.0 | Rollback as a decision, update cadence and visibility of per-tenant versions, deployment stamps, deployment rings and their usual order, the staged blue-green sequence and its limited overlap period |

Credit as the licence requires: Microsoft, Azure Architecture Center, CC BY 4.0
(https://github.com/MicrosoftDocs/architecture-center). The text was rewritten, not reproduced; changes were made
(summarised and restated); no endorsement by the authors is implied.

## Removed
1. **Every product name, command and diagram.** They describe one vendor's stack, not the method.
2. **Every ring size, hold time or percentage.** None is in this block.

## Not verified
1. §1 and most of §2 and §3 are own guidance from general knowledge; nothing in them may be quoted as a source
   claim. Re-read before relying.
2. A trunk-based development reference site was not found as a repository and was not read.
3. Nothing was run, no pipeline or router touched, in writing this block.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line for single-environment sites, the stop-rule guardrail scoped, points added for a deploy job that cancels itself (§1.9), a live-address check after the publish (§2.10), client and CDN caches after a rollback (§3.9), a written rollback rule (§3.10) and the minimum for one environment (§3.11). The status stays 🟡.

## Related blocks
`skills/mobile-release`, `skills/feature-flag-lifecycle`, `skills/slo-design`, `skills/production-readiness-review`,
`skills/package-release`, `skills/backup-restore-drill-pitfalls`, `skills/api-change-classification-pitfalls`,
`skills/blameless-incident-review-pitfalls`, `skills/source-freshness`.
