# analysis-validation-pitfalls §2 — Calculation traps

The errors that produce a wrong number with a clean-looking query. Each has a way to catch it and a way to
prevent it; the catch is cheap and is done every time.

## 2.1 Join explosion and double counting
1. **A join to a one-to-many or many-to-many table multiplies rows**, and counts and sums inflate silently
   (anthropics, nimrodfisher).
2. **Catch it**: count rows before and after each join and compare with what the relationship should give.
   A template for the note:

   ```
   rows in the base table:    N
   rows after the join:       M
   expected relationship:     1:1 | 1:many (M should be ...)
   ```
3. **Prevent it**: count distinct entity keys when counting entities through joins; aggregate the many side
   before joining, or deduplicate on the grain key after (nimrodfisher).
4. **Check the join type too**: the anthropics checklist asks that join types are appropriate, inner against
   left, and that many-to-many joins have not inflated counts.

## 2.2 Partial periods and misaligned dates
1. **Never compare a partial period with a full one.** A month still running against the previous full month,
   or a Wednesday week-to-date against a whole prior week (anthropics).
2. **Filter to complete periods**, or compare the same number of days, or the same day of the month.
3. **Confirm year-over-year and month-over-month comparisons use the right base period.**
4. **Choose the baseline on purpose.** The same figure can look good against last week and poor against last
   year; show more than one baseline and say why the chosen one is the fair one (nimrodfisher).

## 2.3 Denominators
1. **Wrong denominator**: a conversion rate divided by events when it should be divided by unique visitors, or
   the reverse (nimrodfisher). Print the denominator and ask whether it is the population being measured.
2. **Denominator shifting**: the denominator changes between periods, for example a changed definition of
   "eligible" or "active", and the rates stop being comparable (anthropics).
3. **Prevent it**: define the denominator in the requirement before the query is written, keep definitions
   identical across compared periods, and note every definition change.
4. **Check the denominator is non-zero** (anthropics checklist). A division by zero needs a stated treatment,
   not a blank (own guidance).

## 2.4 Average of averages
1. **Averaging pre-computed averages gives a wrong answer when group sizes differ.**
2. **Worked case** (anthropics): group A has 100 users with an average of 50, group B has 10 users with an
   average of 200. The average of averages says 125; the weighted average is (100 x 50 + 10 x 200) / 110,
   about 63.64.
3. **Prevent it**: aggregate from the raw rows, or carry sums and counts, never averages of averages.

## 2.5 Timezones
1. **Different sources use different timezones**, which moves rows between days: UTC event timestamps against
   local-time dates, daily rollups with different cutoffs.
2. **Standardise every timestamp to one zone before grouping** and document which one; anthropics recommends
   UTC. Confirm the zone of every timestamp column (nimrodfisher).

## 2.6 Nulls
1. **Nulls change results silently**: a sum ignores them, an average excludes them from its denominator, a
   subtraction returns null if either side is null (nimrodfisher).
2. **Check null counts for every column used in a calculation** and decide the handling on purpose: exclude,
   impute or flag (anthropics).
3. **Do not fill a null with zero to make the number look complete.** nimrodfisher suggests a deliberate
   `COALESCE`; `business/data-analytics` §4 point 2 says never to assume a missing value because zero is a
   legitimate value. Reconciliation (own guidance): use the fill only where the business meaning of "missing"
   really is zero, and say so next to the number.
