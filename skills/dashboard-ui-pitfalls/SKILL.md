---
name: dashboard-ui-pitfalls
description: "Use when a dashboard or summary page of a business application is designed, written or reviewed, whatever the framework: metric definitions that differ between cards, drill-down that does not match the number clicked, data freshness and 'as of' times, loading, empty, error and partial states per widget, role-based views and permission-scoped numbers, time ranges and time zones, refresh and polling cost, accessibility of cards and charts, and the tests that catch them."
---

# dashboard-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the page people use to decide what to look at next. The premise: **a
dashboard number is a claim, and the user will compare it with the list behind it, with last week's screenshot and
with a colleague's screen**; each defect below is a number that cannot be reproduced. Which chart to draw is in
`chart-choice-pitfalls`; how a metric is defined in a product (churn, MRR) is in `saas-metric-definition-pitfalls`
and `semantic-layer-metric-pitfalls`; infrastructure dashboards as code are in `grafana-dashboard-pitfalls`. The
tables and filters that a drill-down lands on are in `data-table-ui-pitfalls` and
`filters-search-and-saved-views-pitfalls`.

## When
- A home page, an overview, a KPI row or a report page is designed or reviewed.
- A user reports "the number does not match the list", "it is stale", "my colleague sees different numbers", "one card never loads".
- A widget is added that counts, sums or trends business data, or a role gets its own view.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Metric definition, one source of truth, time ranges and zones, drill-down contract, freshness | a metric card, a trend or a drill-down is written | [`01-metrics-drill-down-freshness.md`](./references/01-metrics-drill-down-freshness.md) |
| 2 | Per-widget states, loading order, role-based views, refresh cost, accessibility, tests, framework pointers | a dashboard page is assembled, scoped by role, or tested | [`02-states-roles-access-tests.md`](./references/02-states-roles-access-tests.md) |

## Output / checkpoint
A dashboard is done when: every metric has a written definition shown on demand; every number drills down to a
list that has the same count under the same filter; every widget shows its "as of" time; each widget fails and
loads on its own; role views are scoped on the server; and the tests in §2.7 exist. No checkpoint: a craft block,
🟡, nothing here was run in an application.

## Guardrails
- Define each metric once, in one place used by the card, the drill-down and the export (§1.1). Never recompute it in the component.
- Make a click land on the same set that was counted (§1.4). Never link to an unfiltered list.
- Show when the data is from (§1.5). Never present cached or lagging numbers as live.
- Isolate widgets: one failure marks one card (§2.1). Never block the whole page on its slowest query.
- Scope numbers by permission on the server (§2.3). Never hide a card in the interface and compute the number anyway.
- Accessibility points cite WCAG 2.2 success criteria (§2.5); everything else is craft and marked so in `references/origin.md`.

## Origin
Own craft knowledge, except the accessibility points (§2.5), checked against WCAG 2.2 and WAI-ARIA 1.2 (W3C, facts only, credited), and the page-visibility and time-element facts of §1.5 (HTML Standard, CC BY 4.0). No permissively licensed source for dashboard design was found and read. Details in
[`references/origin.md`](./references/origin.md).
