# dashboard-ui-pitfalls §1 — Metrics, drill-down and freshness

Sources: own craft; no source text was used.

## 1.1 One definition per metric
1. **Write each metric as a sentence plus a query**: what is counted, the unit, the population, the time field, the inclusions and exclusions ("open invoices: status Open or Overdue, excluding drafts, by due date, in the company currency").
2. **Keep the definition in one place** (a server function or a metric catalogue) used by the card, its trend, the drill-down list, the export and any email. Symptom: the card says 120 and the list behind it shows 114. Cause: two code paths with slightly different filters.
3. **Show the definition on demand** (a "how is this calculated" popover reachable by keyboard); a number users cannot interpret is argued about, not used.
4. **Name things once.** Two cards called "Revenue" with different bases (invoiced against paid) are a defect; the label carries the basis ("Invoiced revenue").
5. **Say which entities are in scope**: archived, test, deleted, internal accounts. Excluding test data is a rule written in the definition, not an accident of a join.
6. **Count a thing once.** Joins through one-to-many relations multiply rows; count distinct ids or aggregate before joining.
7. **Money and units**: one currency or an explicit conversion date; do not sum amounts in different currencies; format with the user's locale, calculate with exact numbers (`money-arithmetic-and-rounding-pitfalls`).
8. **Ratios show numerator and denominator** on demand; a conversion rate with a denominator of 3 is noise, so show the count or mark small samples.
9. **Averages hide shape**: when a distribution matters (delays, amounts), show the median or a percentile with the count, and say which.
10. **Compute aggregates in the database** and return a few rows, not the table to the browser (`laravel-aggregate-in-database`).

## 1.2 Time ranges and zones
1. **One range control for the page** unless a widget has a stated reason for its own; show the active range as text on every widget ("1 Sep to 30 Sep 2026").
2. **Define the day boundary in a named time zone**, the user's or the business one, and use it in the card, the drill-down and the export. A card computed in the server zone and a list in the browser zone disagree near midnight and at month end.
3. **Compare like with like**: "this month so far" against the same elapsed days of the last month, or label it as a partial period; a half-finished month compared with a full one reads as a collapse.
4. **Name the comparison** ("vs previous 30 days", "vs same period last year") and what happens when the previous period has no data (no percentage, not infinity).
5. **Fixed against rolling ranges** are different promises; "last 30 days" moves each day, so a saved or shared link must say which one it holds (`filters-search-and-saved-views-pitfalls` §1.2).
6. **Late data and backfills change old numbers.** Say whether history is restated, and let reports state their cut-off; a past month that changes silently destroys trust.

## 1.3 Trends and comparisons
1. **A trend card needs the period count and an axis starting from a defensible baseline**; a truncated axis turns noise into a cliff (`chart-choice-pitfalls`).
2. **Delta direction is not good or bad by itself** (a rise in refunds is bad); colour follows the business meaning and is never the only cue.
3. **Sparklines are decoration unless readable**: give a text value and the range; they carry no axis, so do not use them for exact reading.
4. **Missing periods are zero or unknown on purpose**: a gap in data drawn as zero reports an outage as a business result.

## 1.4 Drill-down contract
1. **Every number is a link to the set that was counted**, with the same filter model, range and zone applied to the target list (`filters-search-and-saved-views-pitfalls` §1.1).
2. **The target says it came from a card** ("Filtered from Overdue invoices") with a chip to clear.
3. **The counts must match.** Check: card number equals list total under the same filter and same permissions; where a difference is legitimate (list is paged, card is cached), the card says "as of" (§1.5).
4. **Drill-down for derived metrics** (rates, averages) lands on the underlying rows, with the numerator filter and a note for the denominator.
5. **A chart point drills down to its bucket**, with keyboard activation, not only mouse; a chart with no link stays a read-only picture and says nothing misleading.
6. **Permission mismatch**: a viewer who may see a card but not the list behind it gets a clear message, not an empty list or an error.
7. **Back returns to the dashboard with its range and scroll restored** (state in the URL).

## 1.5 Freshness
1. **Each widget shows an "as of" time** (relative with an exact time on hover or focus), derived from the data pipeline, not from the page load time. Symptom: "updated 10:02" next to data that stopped arriving at 06:00.
2. **State the expected lag per source** (live, a few minutes, daily batch) so users know what to expect; mark a widget stale when its age passes its own threshold.
3. **Caching is a freshness decision.** Cache keys include the filter, range, zone and the viewer's permission scope; a shared cache without the scope leaks one role's numbers to another.
4. **Refresh only what changed and what is visible**: polling every widget every few seconds loads the database for nothing; refresh on focus or on a slow timer, pause when the tab is hidden, back off on errors.
5. **Manual refresh exists** and shows when it ran; it does not reset the range, the scroll or the open popover.
6. **Real-time is a cost**: use it only where a decision depends on seconds; elsewhere a labelled interval is calmer and cheaper.
7. **Numbers that move under the pointer** (live counters) must not shift layout; reserve width and announce changes politely, rarely.

## Checks
- For three cards: compare the number with the list count under the same filter, range and user.
- Change the user time zone and the server zone; do card, list and export still agree?
- Stop the data feed: does the card turn stale with its age, or keep saying "live"?
- Open the dashboard as two roles with a shared cache warm: does either see the other's numbers?
