# reporting-analytics-app-build-pitfalls §1 — Minimal model and its pitfalls

> Part 1 of `skills/reporting-analytics-app-build-pitfalls`. Read it when a schema or a metric is designed.
> Craft knowledge; no fact in this part was matched to a source (`references/origin.md` lists what was read for part 2). Each point gives the symptom, the check and the fix.

1. **A metric is defined once, in a governed place.** Symptom: "active customers" is 1,204 on the home
   dashboard and 1,187 in the report, because each carries its own query and its own idea of active. Check:
   find every place a headline figure is computed. Fix: a metric record (name, one-sentence definition, source,
   expression, grain, time field, default filters, owner, version, status) referenced by charts, reports,
   exports and schedules; a change creates a new version and says what it does to history. Reports store the
   metric id and version, never a pasted expression.
2. **Minimal model.** Data source (a table, view or dataset with a schema and an owner), metric, dimension (a
   field you can group or filter by, with a type and allowed values), report (a saved query over metrics and
   dimensions with filters, grouping, sort and a time range), visualisation setting (separate from the query),
   dashboard (layout of reports), schedule, export job, access rule, user. Keep the query definition as data
   (an object that is validated), not as stored SQL text assembled from user input.
3. **Time is explicit: field, grain, zone, range.** Symptom: a daily chart whose days shift by one for users in
   another zone, or a "last month" report that changes meaning on the first of the month. Fix: each metric
   names its time field (created, paid, closed), reports store a relative range as a rule and resolve it at run
   time to an absolute range that is shown, the zone is a setting and displayed, week start is a setting, and a
   partial current period is labelled rather than compared to a full one.
4. **Saved reports survive schema change or fail loudly.** Symptom: a renamed column turns a saved report into
   an empty chart with no error, or a deleted dimension is dropped from the filter silently. Fix: store field
   references by stable id, not by column name; on a schema change keep a mapping from old to new; at run time
   an unresolved reference makes the report show an explicit broken state naming the missing field, and the
   owner is told. Test by renaming a field used by a saved report.
5. **Snapshots when history must not move.** Symptom: last quarter's revenue changes because a stage was
   renamed or a late record arrived. Fix: for figures that are reported externally, write a dated snapshot row
   (metric version, period, value, computed-at) and have the report read it; offer a recompute that creates a
   new snapshot and keeps the previous one, with the difference visible. Decide per metric which are live and
   which are snapshotted.
6. **Freshness is data shown to the reader.** Symptom: a cached or batch-loaded figure looks live, a decision
   is made on yesterday's number. Fix: every report carries an as-of timestamp from the data pipeline (when the
   source was last loaded) separate from the render time, a stale marker when it exceeds the metric's declared
   tolerance, and the active filters and scope in plain words next to the figure. A manual refresh states how
   long it takes and is rate-limited.
7. **Caching keys include scope, definition version and filters.** Symptom: a restricted user sees a figure
   cached by an administrator, or an old metric version keeps serving after a change. Fix: key on metric
   version, normalised filters, time range, the user's access scope (not the user id when scopes are shared),
   and the data source's load marker; invalidate on source load, not on a guessed time; cache the result, not
   a rendered chart. Pre-aggregate hot metrics in a summary table refreshed by a job instead of caching raw
   scans. See `skills/laravel-cache`.
8. **Queries are bounded.** Symptom: one wide report with a free date range locks the database for the
   product's other users. Fix: a statement timeout and a row cap for interactive reports, a requirement for a
   time filter on large sources, a cost estimate or a guard on cross joins and unbounded group-bys, a separate
   read replica or warehouse connection, a queue for heavy runs with progress and cancel, and a count of
   slow reports per owner. The limits are policy choices; none is stated here.
9. **Rates and averages carry numerator and denominator.** Symptom: an average of averages across groups, or a
   conversion rate that cannot be drilled into. Fix: store sums and counts, compute ratios at the last step,
   expose both parts, and let a figure drill down to the rows that produced it (subject to access).
10. **Null, deleted and test data are decided.** Symptom: cancelled orders or internal test accounts inflate a
    metric. Fix: the metric states how nulls, soft-deleted and flagged rows are treated, and the data source
    exposes flags for test and internal data instead of each report excluding them differently.
