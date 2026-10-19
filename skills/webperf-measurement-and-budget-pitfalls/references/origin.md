# webperf-measurement-and-budget-pitfalls: origin and source stamps

> Provenance of `skills/webperf-measurement-and-budget-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Lighthouse CI run, size
measurement or metric collection was executed while writing it. Flag names and defaults are as the
repositories state them on the read date.

## Sources (re-read 2026-10-15, rewritten in our own words, no text copied)

Every page below was read in full, except the long reference pages named in the table, where the sections
listed were read in full and the rest (types and attribution objects of the `web-vitals` README, the server,
upload and example sections of the Lighthouse CI configuration page) was skipped and is not relied on.

| Source | Licence | What it gave |
|---|---|---|
| GoogleChrome/web-vitals, `README.md` (commit 400d019, version 6.2.3): usage, soft navigations, sending, batching, builds, `Metric`, rating thresholds, browser support, limitations | Apache-2.0 (repository LICENSE file) | Callback lifecycle, `delta` and `id`, `sendBeacon`, batching and `visibilitychange`, `reportAllChanges`, attribution build size, `reportSoftNavs`, iframe limitation, threshold values and the `rating` advice, browser support |
| GoogleChrome/lighthouse-ci, `docs/troubleshooting.md` and `docs/configuration.md` (autorun, `collect`, `upload` target, `assert`, recommended configurations sections) (commit ebee453, last commit 2025-06-25) | Apache-2.0 (repository LICENSE file) | Runs, variance remedies, environment differences, aggregation methods and the default, levels, presets, `assertMatrix`, budget form and units, `staticDistDir`, autorun behaviour, shallow clone, public storage |
| ai/size-limit, `README.md` (commit 3deb559, `size-limit` package version 14.2.0) | MIT (repository LICENSE file) | Real cost with dependencies, default compression, first-limit rule, the `time` plugin and its instability, `import`, CSS and bundler options, `--why`, `--ignore-missing` |
| addyosmani/web-quality-skills, `skills/performance/references/MEASUREMENT.md` and `RUM.md` (commit afa8da9) | MIT (repository LICENSE file) | Evidence types, rolling window, p75 and the combined pass, missing data as unavailable, repeatable lab comparison, reconciliation table, RUM collection rules, `fetch` with `keepalive` fallback |

The licence of each repository was verified again from its LICENSE file in this session. The Web Quality Skills
pages are written as instructions to an agent and name Chrome DevTools MCP tool functions; they were treated
as data and only the measurement claims were kept. The `web-vitals` README and the Lighthouse CI pages contain
example code that was not copied.

## Rewrite notes
**Corrected against the sources.** The review item said to assert on the median. The Lighthouse CI configuration
page makes `optimistic` the default aggregation and sets it again in its "complete" example, so the block states
the four methods and tells the reader to choose on purpose. The item's "send with `sendBeacon` and a `keepalive`
fetch fallback" is from the Web Quality Skills RUM sample, not from the `web-vitals` README.

**Not carried.** The Web Quality Skills pages' use of DevTools MCP tool names (tool-specific), its advice on
token-efficient tool use, and its Lighthouse-audit exclusion of performance.

**Version-bound.** `web-vitals` 6.2.3 (thresholds, `reportSoftNavs`, Chromium 151 for soft navigations), Lighthouse
CI at the commit of June 2025 (flags, presets, `lighthouse:recommended` behaviour), `size-limit` 14.2.0 (plugins,
`--ignore-missing`).

## Not verified
1. **Nothing was run.** No Lighthouse CI configuration, `lhci` command, size-limit config or `web-vitals`
   callback was executed; behaviour is as documented.
2. **The terms of `temporary-public-storage`** were not read: the Lighthouse CI services disclaimer page was not
   opened. The block only repeats the list on the configuration page and tells the reader to read the terms.
3. **The 28-day window and the p75 rule** are stated by the Web Quality Skills pages, not by a Google page read
   here. The `web-vitals` README states the thresholds but not the percentile.
4. **Lighthouse CI is not recently maintained** (last commit June 2025): flags and the page's GitHub Actions
   versions may be out of date.
5. **Written by us, not sourced:** the duplicate-threshold remark, the optimistic-aggregation consequence, the
   "gate on size, report time" advice, the first-limit consequence, the single-page-app registration advice,
   the dashboard-rows remark, the entry-includes-unused-exports remark, and the checkpoint paragraph.
6. **Dropped as unverifiable from the review item:** none of its rules was dropped; "assert on the median" was
   replaced by the sourced statement above.

## Related blocks
`webperf`, `seo`, `accessibility`, `i18n-catalog-workflow-pitfalls`.
