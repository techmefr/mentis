# feature-flag-lifecycle: origin and source stamps

> Provenance of `skills/feature-flag-lifecycle`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published sources, never run on a real flag by us.

## Sources (read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Martin Fowler, "Feature Toggles (aka Feature Flags)", https://martinfowler.com/articles/feature-toggles.html | Published article, idea only | Four categories with longevity and dynamism, toggle point versus router, inventory with a carrying cost and a possible ceiling, expiry metadata and "time bomb" checks, removal task at creation, test the expected configuration plus its fallback plus all-on, in-memory reconfiguration for tests only, kill switch as a manual circuit breaker, consistent cohort for experiments |
| alirezarezvani/claude-skills, skill `feature-flags-architect` (SKILL.md and its lifecycle and taxonomy references, read in full; commit 19392f7a08264ed00486a251f5b2098321771f94; LICENSE file re-read: MIT, Alireza Rezvani 2025) | MIT | Own-guidance points flagged in the text: record written before the code, deploy off and exercise the kill switch before the ramp, abort criterion per stage, quiet period then removal of the dead branch, owner at creation, reassignment on departure, audit of stale flags |

## Removed
1. **Every number**: ramp percentages, hold times, the quiet-period length, lifetime ceilings, age and usage
   thresholds, the source's service-level targets for flag age and the count of stale flags.
2. **The provider chooser** (named products, pricing models): perishable and out of scope.
3. **The three Python scripts and the slash command**: a runtime, not a method; nothing here depends on them.

## Not verified
1. The article is read through a fetch tool's summary, not page by page; section-level claims (the test
   subsets, time bombs) should be re-read before being quoted.
2. The article does not name "toggle debt"; that term is ours, built on its carrying-cost argument.
3. No claim here was checked against a flag product's documentation or an OpenFeature specification.
4. The quiet-period idea rests on one collection's workflow, not on a primary source.

## Related blocks
`skills/deprecation-migration`, `skills/observability-instrumentation`, `skills/slo-design`,
`skills/spend-guard-fail-closed`, `skills/source-freshness`.
