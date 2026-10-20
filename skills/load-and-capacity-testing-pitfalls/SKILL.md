---
name: load-and-capacity-testing-pitfalls
description: "Use when a service is about to be load-tested, soak-tested or sized for expected traffic, or when a load-test result is being read: model realistic traffic, drive it without hiding slow responses, read percentiles not averages, find the limit and the first bottleneck, and turn the result into a capacity statement and a regression check."
---

# load-and-capacity-testing-pitfalls

A method for answering "will it hold, and how much room is left" with a measurement that can be trusted. The
usual failures: a test that sends traffic nobody sends, a generator that slows down when the server does and
reports a flattering tail, an average that hides the slow few, a run on an environment unlike production, and a
result nobody can reproduce or act on. The block owns no load tool and no result dashboard, and names none. It
sits beside the per-language performance blocks (`skills/go-performance`, `skills/node-async-performance`), which
find the cost inside one process, and `skills/webperf-measurement-and-budget-pitfalls`, which covers the browser
side. Related: `skills/slo-design` §1 (the indicator a test should assert), `skills/chaos-experiment` (a fault
during load), `skills/kubernetes-workload-pitfalls` (the limits that become the ceiling).

## When
- A launch, a campaign or a migration will raise traffic and nobody knows the headroom.
- A change to a hot path, a query, a cache or a pool needs a regression check under load.
- A load-test result is presented and has to be judged before anyone relies on it.
- Autoscaling or alert thresholds are about to be set from a guess.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The question, the workload model, the environment and the data | a test is designed | [`01-design-the-workload.md`](./references/01-design-the-workload.md) |
| 2 | Driving the load honestly, ramp, warm-up, and reading percentiles and errors | a test is run or a result is read | [`02-driving-and-reading.md`](./references/02-driving-and-reading.md) |
| 3 | Finding the limit and the bottleneck, the capacity statement, and a recurring check | the result becomes a decision or a pipeline step | [`03-limit-capacity-regression.md`](./references/03-limit-capacity-regression.md) |

## Output / checkpoint
No pipeline checkpoint. A written test plan before the run (question, target figures from the owner, traffic mix,
environment and how it differs from production, data, stop conditions) and a report after (what was driven, the
percentiles and errors per scenario, the first thing that saturated, the capacity statement with its conditions,
what was not tested).

## Guardrails
- Write the question and the pass criteria before the first run. Never tune the criteria after seeing the
  result.
- Send only to an environment the owner approved, with a stop condition and a person who can stop it. Never aim a
  generator at production, a shared system or a third party without written agreement.
- Report percentiles and the error rate together, per scenario. Never report one average for a mixed workload.
- State how the environment differs from production next to every number. Never present a figure from a small
  environment as a production capacity.
- Keep the plan, the scripts and the raw results so the run can be repeated. Never keep only the chart.

## Origin
A hosted-platform architecture guide on continuous load validation (CC BY 4.0) and a production-readiness
repository's capacity-planning notes (MIT), plus the wrk2 (Apache-2.0) and HdrHistogram (public domain) READMEs, all read 2026-10-20 and restated, plus own guidance flagged in the
references. Provenance, what was removed and not verified: [`references/origin.md`](./references/origin.md).
🟡: never dogfooded.
