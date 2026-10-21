# dashboard-ui-pitfalls: origin and source stamps

> Provenance of `skills/dashboard-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No dashboard was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| W3C, Web Content Accessibility Guidelines 2.2 (Recommendation, 12 December 2024), <https://www.w3.org/TR/WCAG22/>, read 2026-10-20 (about the first 100,000 characters) | W3C Document License (copyright W3C); facts only, restated in own words, criteria credited by number | Success criteria 1.1.1, 1.3.1, 1.4.1, 1.4.11, 2.1.1, 2.2.2, 2.3.3 behind §2.5 points 2, 3, 4, 6, 8 |
| W3C, Understanding SC 4.1.3 Status Messages, <https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html>, read 2026-10-20 | W3C Document License; facts only, own words | status role, aria-atomic, assertive on unimportant content as a failure |
| Permissive dashboard-design source | n/a | No permissive source found, searched: design-system documentation known to the author; none opened because no licence was verified. The rest is craft knowledge. |

The related blocks `chart-choice-pitfalls`, `saas-metric-definition-pitfalls`, `semantic-layer-metric-pitfalls` and `grafana-dashboard-pitfalls` were read inside this repository to avoid duplicating them.

## Own craft, not from a source
Metric definition and single-source rules, drill-down parity with the list, freshness and cache scope, per-widget isolation, role scoping and aggregate leakage, time zone and period comparison rules, the non-accessibility presentation points, test and framework-pointer lists.

## Removed
Chart-type selection (in `chart-choice-pitfalls`), product metric formulas (in the metric blocks), infrastructure monitoring (in `grafana-dashboard-pitfalls`).

## Not verified
1. **Verified 2026-10-20 against WCAG 2.2:** accessibility points 2.5.2, 2.5.3, 2.5.4, 2.5.6 and the added 2.5.8. Point 2.5.1 (heading and text value) rests on SC 1.3.1 only in general terms.
2. **Verified 2026-10-20 (SC 4.1.3):** status role, aria-atomic and the assertive failure behind point 2.5.5. **Still unverified:** the polite-region wording is our reading, the page names no aria-live value. All other points (metrics, drill-down, freshness, roles, cost, tests) are own knowledge, no external claim checked.
3. **Framework pointers** name features from memory; no version was checked.
4. **No threshold or number** (refresh interval, group size, widget count) is stated; none was measured.
