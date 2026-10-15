---
name: webperf-measurement-and-budget-pitfalls
description: "Use when web performance is measured, reported or gated: which evidence answers which question (field data, first-party RUM, one trace, a lab run, source reading), p75 and the combined pass, missing field data, collecting vitals with the web-vitals library (callbacks that fire twice or never, delta and id, beacons, soft navigations, the payload), Lighthouse CI (runs, aggregation, assertions, presets, runner, static server, per-URL assertions, shallow clones, public storage) and a JavaScript size budget with size-limit."
---

# webperf-measurement-and-budget-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the numbers behind a performance claim. `webperf` says to measure
before touching anything and to re-measure the same way; it does not say which instrument answers which
question, how a field metric is collected without double counting, or how a budget fails a build without flaking.
The three sections share one premise: **a performance number is only as good as the instrument that produced
it, so a claim names the evidence type, the scope and the conditions**. The causes of a slow page and the phone
rules are in `webperf` and in `skills/webperf/references/01-responsive-touch-interface.md`; the Core Web Vitals
page rules are in `seo` §3. Diagnosing a single vital from a trace is not covered by any block yet.

## When
- Reporting a performance result, or deciding from one trace that a page is fast or slow.
- Adding real-user monitoring, or reading a field number that does not match a lab number.
- Adding Lighthouse CI or a bundle budget to a pipeline, or a performance check is red one run and green the next.
- Choosing a first limit for JavaScript size.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Evidence and thresholds: evidence types, p75, ratings, missing field data, repeatable lab runs, lab versus field | a number is about to be reported or compared | [`01-evidence-and-thresholds.md`](./references/01-evidence-and-thresholds.md) |
| 2 | Collecting vitals with `web-vitals`: lifecycle, delta and id, beacons, soft navigations, iframes, payload | real-user monitoring is added or reviewed | [`02-rum-with-web-vitals.md`](./references/02-rum-with-web-vitals.md) |
| 3 | Budgets in CI: Lighthouse CI configuration and noise, assertions, size-limit | a performance check is added to a pipeline or flakes | [`03-lighthouse-ci-and-size-budgets.md`](./references/03-lighthouse-ci-and-size-budgets.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a result was reported with its evidence type, scope and
conditions in a table (§1), a metric callback was logged across a tab switch and a back-forward restore and the
number of calls and ids was counted (§2), and a budget was made to fail on purpose by raising the measured
quantity and then seen to pass again after revert (§3). A configuration that was only read is not verified.

## Guardrails
- Never report a `PerformanceObserver` result from one tab as field data (§1.1).
- Never read missing field data as passing, and never decide from an average (§1.2).
- Never recompute a rating from thresholds when the library gives one (§1.3).
- Never call a vitals function repeatedly per page load, and never send only `value` when the backend sums (§2.1, §2.2).
- Never put a full URL with its query string, or user text, in a RUM payload (§2.4).
- Never gate on a score alone; assert on a fact such as the count and size of requests first (§3.2).
- Never use `temporary-public-storage` without reading what it publishes (§3.4).
- This block states tool behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). Flag names and versions are bound to web-vitals 6.2.3,
  Lighthouse CI at its last commit of June 2025, and size-limit 14.2.0. Nothing was run while writing it.

## Origin
Rewritten from the `web-vitals` README (Apache-2.0), the Lighthouse CI configuration and troubleshooting
pages (Apache-2.0), the size-limit README (MIT) and two measurement references of the Web Quality Skills
collection (MIT), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
