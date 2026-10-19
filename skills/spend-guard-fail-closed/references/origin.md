# spend-guard-fail-closed: origin and source stamps

> Provenance of `skills/spend-guard-fail-closed`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published sources, never run against a real budget by us.

## Sources (all read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| A cloud provider's budgets guide, https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html | Vendor documentation, idea only | Budget figures refresh a few times a day; alert may arrive after the threshold is passed; notification targets; optional automatic actions at a threshold |
| An AI vendor's API error reference, https://platform.claude.com/docs/en/api/errors | Vendor documentation, idea only | Org and workspace spend limits present as an invalid-request error; tier spend cap shown as the rate-limit status with no wait hint |
| OmniRoute strict zero-cost routing document and cost-tracking guide (MIT, commit 9ec0bf15; docs only, no code) | MIT | Own-guidance points flagged in the text: new or unclassified options excluded, free as a catalogue fact not headroom, hard-stop claim from the provider's own terms, per-credential verification, cache invalidation on failure, distinct exclusion reasons, a stated known gap, cost shown as an estimate and not a bill |

## Removed
1. **Every number**: freshness intervals, safety margins, thresholds, defaults.
2. **Product mechanics**: provider and plan names, free-tier catalogue entries (they go stale), flag and route
   names.
3. **The multiplexing of many accounts behind one key to stretch free tiers** that the gateway is built
   around: account-limit evasion is not taught here.

## Not verified
1. The gateway's docs are one maintainer's: none of the own-guidance points was checked in its code.
2. The cloud provider's page covers one product; its refresh delay is not a claim about any other provider.
3. The vendor's rate-limits page (the spend-cap recognition rules) was not read, only the errors page that
   links to it.
4. Free-tier terms of any named provider: deliberately not stated, to be read and dated by whoever relies on one.

## Related blocks
`skills/failure-classification-before-retry`, `skills/choose-model`, `skills/source-freshness`,
`skills/observability-instrumentation`.
