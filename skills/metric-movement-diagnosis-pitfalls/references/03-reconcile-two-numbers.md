# metric-movement-diagnosis-pitfalls §3 — Reconcile two numbers

Two sources show different values for the same metric. Most of the time the data is fine and the two
questions are not the same question. Work through the places they diverge in a fixed order.

## 3.1 Define before comparing
1. **Pin down the metric**: numerator, denominator, filters, timezone and the exact period. Mismatched
   definitions are the most common cause (nimrodfisher metric-reconciliation).
2. **Pull both values for the same period from authoritative sources**, not from cached dashboards, and record
   the absolute values, the row counts and the query or path behind each.
3. **Compute the gap** in absolute and percentage terms.
4. **Accepting a gap needs a documented agreement** with the owner of the metric. The source gives a
   tolerance table by metric type; it is not carried, because the figures are arbitrary (own guidance on what
   replaces it: an agreement written down, not a number from a table).

## 3.2 Why two numbers differ
1. **Filters**: the most common cause. Different status filters, date truncation (a greater-or-equal bound
   against a between), null handling, exclusion of deleted records.
2. **Join types**: a left join keeps unmatched rows that an inner join drops, so a revenue figure joined to a
   customer table differs.
3. **Grain**: one query at order level, another at order-line level; duplicate rows in one inflate the total.
4. **Timezone**: UTC against local time puts rows in different periods.
5. **Definition drift**: the business definition changed ("active user" now needs two sessions) and not
   every pipeline was updated.
6. **Refresh lag**: one source is yesterday's snapshot, the other nearly real time, so an intra-day
   comparison shows a spurious gap.

## 3.3 The order of the investigation
1. **Confirm the numbers** from the authoritative sources.
2. **Check the grain**: what does one row mean in each source?
3. **Align the period**: same start, same end, same timezone.
4. **Put the filters side by side**: every condition of both queries in two columns.
5. **Trace every join** and its type.
6. **Check at sample level**: take a sample of rows that are in A and not in B, and the reverse (the source
   says 20 of each). One concrete row explains more than a total.
7. **Name the divergence point** with the query excerpt that shows it.

A note for the write-up (fields from the source, layout ours):

```
Metric / period:       name | dates | timezone
Source A / Source B:   value | row count | query or path
Gap:                   absolute | percent
Divergence point:      filter | join | grain | timezone | definition | refresh
Resolution:            fix | designate a source of truth | accepted gap with owner
```

## 3.4 After the cause is found
1. **State the root cause in one sentence.**
2. **Designate which source is the single source of truth** from now on.
3. **Decide whether the fix is in the pipeline or in the definition**: a calculation bug is fixed; a
   definition difference is documented and chosen.
4. **Record the dates** the discrepancy was observed and resolved.
5. **Say whether downstream consumers need recalculation.**
6. **The cause classification of the source is not carried**: nimrodfisher's SKILL points to a
   `metric_discrepancy_guide.md` for it, and that file is missing from the clone. The causes in §3.2 come
   from `reconciliation_patterns.md` only.
