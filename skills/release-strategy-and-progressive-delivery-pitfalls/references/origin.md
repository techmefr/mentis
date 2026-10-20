# release-strategy-and-progressive-delivery-pitfalls: origin and source stamps

> Provenance of `skills/release-strategy-and-progressive-delivery-pitfalls`. Read it when a rule has to be traced
> to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation articles and own craft knowledge, with the concurrency and
canary points checked on 2026-10-20; never run on a real release by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MicrosoftDocs/architecture-center (LICENSE file read: Attribution 4.0 International): the multitenant article on updates, and the article on blue-green deployment of a cluster | CC BY 4.0 | Rollback as a decision, update cadence and visibility of per-tenant versions, deployment stamps, deployment rings and their usual order, the staged blue-green sequence and its limited overlap period |
| github/docs, "Control the concurrency of workflows and jobs" (LICENSE read 2026-10-20) | CC BY 4.0; credit: GitHub docs contributors; restated | Run groups, cancel-in-progress, one pending run replaced by a newer one, ordered queue option (§1.9, §1.10) |
| argoproj/argo-rollouts documentation, canary and concepts pages (LICENSE read 2026-10-20) | Apache-2.0 | Pause without duration, analysis abort, pod-count weight granularity, blue-green at a glance (§2.3-2.5) |
| kubernetes/website, Deployments page (LICENSE read 2026-10-20: CC BY 4.0) | CC BY 4.0 | Fetched, but the summary returned did not say it came from the page's own text, so nothing is taken |

Credit as the licences require: Microsoft, Azure Architecture Center, CC BY 4.0
(https://github.com/MicrosoftDocs/architecture-center); GitHub docs, CC BY 4.0 (https://github.com/github/docs);
Argo Rollouts, Apache-2.0 (https://github.com/argoproj/argo-rollouts). The text was rewritten, not reproduced;
changes were made (summarised and restated); no endorsement by the authors is implied.

## Removed
1. **Every product name, command and diagram.** They describe one vendor's stack, not the method.
2. **Every ring size, hold time or percentage.** None is in this block.

## Not verified
1. Still own guidance: §1.1-1.8, the exposure-unit and like-for-like points, health versus validation, long tail,
   all of §3 except the source's rollback question. Nothing in them may be quoted as a source claim. Now checked:
   deploy-job cancellation and replacement (§1.9, §1.10), pause and abort behaviour and weight granularity
   (§2.3, §2.4), blue-green at a glance (§2.5). The trunk-based development reference was not read again.
2. A trunk-based development reference site was not found as a repository and was not read.
3. Nothing was run, no pipeline or router touched, in writing this block.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line for single-environment sites, the stop-rule guardrail scoped, points added for a deploy job that cancels itself (§1.9), a live-address check after the publish (§2.10), client and CDN caches after a rollback (§3.9), a written rollback rule (§3.10) and the minimum for one environment (§3.11). The status stays 🟡.

## Related blocks
`skills/mobile-release`, `skills/feature-flag-lifecycle`, `skills/slo-design`, `skills/production-readiness-review`,
`skills/package-release`, `skills/backup-restore-drill-pitfalls`, `skills/api-change-classification-pitfalls`,
`skills/blameless-incident-review-pitfalls`, `skills/source-freshness`.
