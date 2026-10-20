# load-and-capacity-testing-pitfalls: origin and source stamps

> Provenance of `skills/load-and-capacity-testing-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two published sources and own craft knowledge, with the generator
points checked on 2026-10-20 against two permissive repositories; never run on a real load test by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MicrosoftDocs/architecture-center, page "Continuous validation with Azure Load Testing and Azure Chaos Studio" (docs/guide/testing/mission-critical-deployment-testing.md; LICENSE file read: Creative Commons Attribution 4.0 International; repository pushed 2026-10-20) | CC BY 4.0 | Define tests from key scenarios and measurable thresholds; production-like environment and sustained synthetic traffic; failed run means adjust the baseline or an unexpected error; separate baseline for chaos runs; integrate tests in the pipeline; regular manual peak tests |
| mercari/production-readiness-checklist, docs/concepts/capacity-planning.md (LICENSE file read: MIT, Copyright 2020 Mercari, Inc.; repository last pushed 2021-11-22) | MIT | What capacity planning is and what it feeds; isolation, then a real-world mix, then randomised input; refreshing the test as traffic changes; bad input can degrade a cache-backed service |
| giltene/wrk2 README (LICENSE read 2026-10-20) | Apache-2.0 | Delayed-request effect, scheduled-send measurement, uncorrected comparison, 10-second calibration (§2.1, §2.3) |
| HdrHistogram README (LICENSE.txt read 2026-10-20) | public domain (CC0) with an optional BSD 2-Clause grant | Expected-interval correction, additive histograms merged before percentiles (§2.3, §2.5) |
| Gatling documentation, injection page | official product documentation, licence not verified, facts only, rewritten | Open and closed model definitions (§1.6) |

Credit as the licences require: Microsoft Azure Architecture Center, CC BY 4.0 (https://github.com/MicrosoftDocs/architecture-center); Mercari production readiness checklist, MIT, Copyright 2020 Mercari, Inc. (https://github.com/mercari/production-readiness-checklist); wrk2, Apache-2.0, Gil Tene (https://github.com/giltene/wrk2); HdrHistogram, public domain / BSD 2-Clause (https://github.com/HdrHistogram/HdrHistogram). The text was rewritten, not reproduced; no endorsement by any author is implied.

## Removed
1. **Every number**: thresholds, durations, user counts, percentiles to report and pass criteria. They belong
   to a service and its owner.
2. **All named tools and the managed-service steps** from the Azure page: runtime detail, not method.
3. **The load-testing tool whose licence is AGPL-3.0, and its documentation, were not opened.** Nothing here
   reflects its text or its option names.

## Not verified
1. Most of §1 and §3 and the rest of §2 are own guidance from the craft: the knee of the curve, soak signals, why
   open traffic fits the web, retries as load, headroom, capacity statements. Check each against the documentation
   of the tool in use before relying on it. Now sourced: open and closed definitions, delayed-request effect,
   histogram merging, warm-up length of one tool.
2. Which tools beyond the one read correct for the delayed-request effect was not checked. The AGPL tool and its
   documentation were not opened.
3. The sources are one company's cloud guide and one company's checklist; their fit for other stacks is our
   judgement.
4. No load was generated, and no tool run, in writing this block.

## Related blocks
`skills/slo-design`, `skills/chaos-experiment`, `skills/go-performance`, `skills/node-async-performance`,
`skills/webperf-measurement-and-budget-pitfalls`, `skills/kubernetes-workload-pitfalls`,
`skills/observability-instrumentation`, `skills/production-readiness-review`, `skills/source-freshness`.
