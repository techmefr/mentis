# reporting-analytics-app-build-pitfalls §2 — Access, delivery and v2

> Part 2 of `skills/reporting-analytics-app-build-pitfalls`. Read it when permissions, a schedule, an export or
> the first release are planned. Craft knowledge, no external source read.

1. **Row-level access is a predicate added by the server to every query.** Typical shape: a user sees rows of
   their team, region or customer; an administrator sees all; a column such as salary or email is hidden or
   masked for most. Symptom: the chart is filtered but the table, the drill-down, the export, the scheduled
   mail and the API return everything, or a filter parameter can be edited in the URL to widen the scope.
   Check: log in as a restricted user and compare totals across chart, table, drill-down, export and schedule.
   Fix: compute the scope from the session on the server, append it to the query definition before execution
   and cache keying, never accept it from the client, apply column rules in the same layer, and test each read
   path. Name abilities (view-report, export, schedule, see-unmasked) rather than roles (see
   `skills/laravel-permissions-not-roles`; tenants in `skills/laravel-tenant-context-by-default`).
2. **A schedule runs as its owner's or recipient's scope.** Symptom: a report built by an administrator is
   mailed to a manager and shows the whole company. Fix: store the schedule with the recipient and evaluate it
   with that recipient's scope, or restrict recipients to people whose scope covers the report; re-check access
   at each run, since people change team or leave. Deliver a link that requires sign-in by default, since a
   mailed attachment cannot be recalled.
3. **Scheduled runs are idempotent and observable.** Symptom: a retry sends the report twice, a failed run is
   never noticed, a daylight-saving change skips or doubles a run. Fix: a run row per schedule and period with
   a status, a unique key to stop duplicates, retries with a cap, a failure notice to the owner, a stored
   time zone, and a pause when the recipient is deactivated or the report is broken (see §1 point 4 and
   `skills/laravel-scheduling`, `skills/queue-worker-runtime-pitfalls`).
4. **Exports use the same pipeline and rules.** One code path for screen and file so numbers match; the
   file states the filters, the as-of time, the metric versions and the timezone in a header or a second sheet;
   cells that start with a formula character are neutralised; large exports are async with an expiring signed
   link, a row cap per policy and an audit entry (who, what, which filter, which scope). See
   `skills/csv-xlsx-import-export-pitfalls`.
5. **Audit and usage are part of the product.** Log report opens, exports and schedule changes with the scope
   used. Symptom: a leak of an exported file with no trace of who produced it. Use the log also to retire
   reports that nobody opens, and to find the slowest ones.
6. **Self-service builders need guard rails.** If users compose their own queries, expose metrics and
   dimensions, not raw tables; limit the joins to declared relationships; show a preview with a row cap; and
   keep ad-hoc results separate from governed metrics until someone promotes a report to a metric (§1 point
   1). Symptom: an ad-hoc number quoted in a meeting as official.
7. **Embedding and sharing are scoped.** A public or embedded dashboard uses a signed, expiring token that
   carries the scope as claims set by the server, is read-only, and can be revoked; it never reuses an
   administrator session. Symptom: a customer-facing dashboard where changing an id in the URL shows another
   customer.
8. **Personal data in reports is minimised.** Aggregate by default, mask identifiers unless the ability allows
   them, suppress small groups where a figure could identify a person, and keep export retention short. Method
   only; see `business/data-protection`.
9. **What to split first.** Metric definitions and one source; reports with stored query objects and the time
   rules; row-level scope on every path; freshness labels and caching with scope keys; exports; schedules;
   then self-service and embedding. Ship the first three before any scheduling.
10. **What is regretted at v2.** Metrics defined in each chart; saved reports tied to column names; scope
    applied in the UI only; scheduled mail running as an administrator; caches keyed without scope; no as-of
    stamp; free date ranges on huge tables; no audit of exports; a pasted SQL text as the report definition.
    Each is cheap at the first migration and expensive once reports multiply.
11. **Laravel and Nuxt pointers, short.** In Laravel: a metric table with versions, a query builder service that
    takes a validated report object and adds the scope, a summary table refreshed by a scheduled command, cache
    keys built from version and scope, a run table for schedules, signed temporary URLs for exports. In Nuxt:
    keep filters and range in the URL, show the as-of time and scope beside every figure, and download exports
    from the API rather than building files in the browser.
