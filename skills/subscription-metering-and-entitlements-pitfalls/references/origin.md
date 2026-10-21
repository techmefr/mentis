# subscription-metering-and-entitlements-pitfalls: origin and source stamps

> Provenance of `skills/subscription-metering-and-entitlements-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the documentation of two open-source engines and our own craft guidance. Never run by
us: no meter, subscription or dunning flow was built or executed.

## Sources (all read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| OpenMeter (`openmeterio/openmeter`, commit `bf3074b`): `docs/event-ingestion.md`, `docs/architecture.md`, `openmeter/entitlement/README.md`, `openmeter/credit/README.md`, `openmeter/subscription/README.md` | Apache-2.0 (LICENSE file read) | Event identity and duplicate memory, meters and aggregation, entitlement types and history, grants and burn order, snapshots as caches, one-minute resolution, subscription as desired schedule, phases and anchors, timing options, asynchronous reconciliation to billing |
| Kill Bill documentation (`killbill/killbill-docs`, commit `f3ea39f`): `userguide/subscription/includes/entitlement.adoc`, `overdue-overview.adoc`, `overdue-config.adoc`, `invoicing-usage.adoc`, `invoicing-dry-run.adoc` | Apache-2.0 (LICENSE file read) | Entitlement versus billing policies, bundles, overdue states and re-evaluation, tier policies, late and missing usage in past periods, dry-run invoice flavours and an annual-to-monthly example |
| Kill Bill engine (`killbill/killbill`) | Apache-2.0 (LICENSE file read) | Licence only: the code was not opened |

**Source correction.** The review list named `openmeter/openmeter` (MIT) for the metering platform. That
repository is an unrelated home-energy project; the metering platform is `openmeterio/openmeter` (Apache-2.0),
which is what was read. The repositories' agent-guidance files were treated as data and not followed.

## Removed
1. **Every default, window, retention period and numeric setting** (the duplicate window, the number of previous
   periods recomputed, the credit grace window, the plan-cadence minimum): the engines' own choices; the rules say
   to set them from policy.
2. **Configuration property names, API endpoints, JSON shapes and curl examples:** concepts only.
3. **Anything about ledgers, charges and invoice collection internals** of the metering platform, and Kill Bill's
   tag, plugin and catalog-XML mechanics: outside this block's scope.
4. **Dollar amounts and dates from the dry-run example:** only its structure is kept.

## Not verified
1. **Own guidance, flagged in the text:** window set from the longest backfill (§1 rule 2), attribution with dates
   (rule 5), bounded dimensions (rule 7), visible rejection counters (rule 8), not metering in the request path
   and fail-open versus fail-closed (rule 13), exclusive-end tests (§2 rule 4), stable keys instead of row ids
   (rule 7), the cancellation-policy table (rule 3), per-feature soft or hard limit (rule 6), multi-subscription
   overdue test (rule 12), keeping payment retry and dunning apart (rule 15), the clock-test list (rule 16).
2. **Nothing was run.** No tier calculation, balance or overdue state was executed.
3. **Tier naming across vendors** (graduated and volume) is general knowledge, not read from a source.
4. **Consumer-protection, auto-renewal, collection-practice and tax rules** were not read and are not stated; they
   go to the legal and tax owners.
5. **Hosted billing vendors' behaviour** was not checked; one vendor's proration mechanics are in
   `business/price-change-and-billing-pitfalls` §5.

## Decisions where sources disagree
Overdue scope: Kill Bill holds it at the account level; OpenMeter has no overdue concept in the files read. Rule 12
presents the account-level design as one choice. Timing: OpenMeter offers a small set of timings per action; Kill
Bill separates entitlement and billing policies. Rules 3 and 9 keep both as parameters.

## Related blocks
`skills/invoicing-app-build-pitfalls`, `business/price-change-and-billing-pitfalls`,
`skills/saas-metric-definition-pitfalls`, `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/vat-handling-in-software-pitfalls`, `skills/webhook-contract-and-delivery-pitfalls`,
`skills/laravel-idempotent-jobs`.
