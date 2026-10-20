# dashboard-ui-pitfalls: origin and source stamps

> Provenance of `skills/dashboard-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No dashboard was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| None | n/a | No MIT, Apache-2.0 or CC BY source on dashboard design for business applications was found and read in this pass. The content is craft knowledge. |

The related blocks `chart-choice-pitfalls`, `saas-metric-definition-pitfalls`, `semantic-layer-metric-pitfalls` and `grafana-dashboard-pitfalls` were read inside this repository to avoid duplicating them.

## Own craft, not from a source
Metric definition and single-source rules, drill-down parity with the list, freshness and cache scope, per-widget isolation, role scoping and aggregate leakage, time zone and period comparison rules, accessibility, test and framework-pointer lists.

## Removed
Chart-type selection (in `chart-choice-pitfalls`), product metric formulas (in the metric blocks), infrastructure monitoring (in `grafana-dashboard-pitfalls`).

## Not verified
1. **Everything is own knowledge**: no external claim was checked against a source.
2. **Accessibility points** are recalled public practice (text alternatives, live regions, reduced motion), not re-read in this pass. Re-read before relying.
3. **Framework pointers** name features from memory; no version was checked.
4. **No threshold or number** (refresh interval, group size, widget count) is stated; none was measured.
