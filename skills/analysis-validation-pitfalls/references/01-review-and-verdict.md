# analysis-validation-pitfalls §1 — Review and verdict

A number that survives only because nobody checked it is the expensive kind. This is the review done before
an analysis leaves the analyst, and the verdict that goes with it.

## 1.1 Review the frame before the arithmetic
1. **Question framing.** Is the analysis answering the question that was asked, or a related one? Could the
   question be read differently? (anthropics validate-data, nimrodfisher checklist.)
2. **Data selection and time range**: the right tables, an appropriate period, and scope boundaries respected
   with no silent out-of-scope data.
3. **Population**: is it defined correctly, and are there unintended exclusions?
4. **Metric definitions**: clear, consistent, and matching how the stakeholder understands the term
   ("active user", "revenue"). A deviation is noted, not buried.
5. **Baseline and comparison**: are periods, cohort sizes and contexts comparable?
6. **Source and freshness**: which tables were used, the "as of" date, known quality issues of the source and
   their effect (anthropics, nimrodfisher). Whether the data may be used for this purpose at all is a
   data-protection question (own guidance; nimrodfisher's checklist only asks that access was appropriate): `business/data-analytics` §4 point 9 and `business/data-protection`.

## 1.2 The checklist, in four groups
1. **Data quality**: source verified, freshness, no unexpected gaps in the series or missing segments, null
   rates checked on key columns, no double counting, filters correct.
2. **Calculation**: aggregation level matches the grain, denominators right and non-zero, same-length
   periods with partial ones excluded or noted, join types appropriate, metric definitions as stakeholders
   define them, subtotals sum to the whole or the gap is explained.
3. **Reasonableness**: magnitude plausible, no unexplained jump or drop in the series, key numbers match other
   known sources, boundaries behave (empty segments, zero-activity periods, new entities).
4. **Presentation**: bar charts start at zero, axes labelled, scales consistent across panels, titles state
   the insight and the date range, precision appropriate, caveats explicit, reproducible by someone else.

## 1.3 Spot-checks that catch most errors
1. **Recompute a few key numbers independently**, not by re-running the same query.
2. **Check subtotals sum to totals** and percentages sum to about 100 where they should.
3. **Check comparison base periods** for year-over-year and month-over-month figures.
4. **Check the same filters apply to every metric** in the analysis.
5. **Trace a few individual records** by hand (nimrodfisher asks for intermediate results to be spot-checked
   against source data on a few rows).

## 1.4 The verdict
1. **Three levels** (anthropics validate-data):
   - *Ready to share*: sound, verified, caveats noted, nothing blocking.
   - *Share with noted caveats*: largely correct, specific limits that must reach the reader; list the
     required caveats.
   - *Needs revision*: specific errors or missing analyses; list the required changes in priority order.
2. **Rate each issue** high, medium or low with its impact (same source).
3. **Fill the sign-off**: reviewer, issues found, resolution status, delivery decision (nimrodfisher's
   sign-off template). A line per field is enough:

   ```
   Verdict:           Ready | Share with caveats | Needs revision
   Issues:            severity | issue | impact | resolved?
   Spot-checks:       metric | verified or discrepancy
   Required caveats:  ...
   ```
4. **If issues were found, fix them and review again** (anthropics tip): a verdict applies to the version
   that was reviewed.
