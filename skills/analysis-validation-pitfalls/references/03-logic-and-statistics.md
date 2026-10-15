# analysis-validation-pitfalls §3 — Logic and statistics traps

Errors where every number is computed correctly and the conclusion is still wrong. They are caught by asking
who is missing, what was chosen after the fact, and what would reverse the picture.

## 3.1 Who is in the data, and who chose them
1. **Survivorship bias**: only entities that still exist are analysed, so churned, deleted or failed ones are
   invisible. "Average tenure of active customers" leaves out the short tenures of those who left
   (nimrodfisher). Ask who is not in the dataset and whether including them would change the conclusion
   (anthropics, validate-data).
2. **Selection bias in segments**: a segment defined by the outcome measured gives circular logic. "Users who
   completed onboarding retain better" is true by construction. Define segments on characteristics that exist
   before the outcome (anthropics validate-data).
3. **Look-ahead bias**: using information that was not available at the time to explain what happened then.
4. **Cherry-picked time ranges** that favour one story, and cherry-picked significant results out of many
   tests (anthropics validate-data).

## 3.2 When the aggregate lies
1. **Simpson's paradox**: a trend in the aggregate reverses when segmented. Example (anthropics
   statistical-analysis): overall conversion rises while it falls in every segment, because the mix moved
   toward a higher-converting segment. Check key segments against the aggregate.
2. **Ecological fallacy**: a pattern across groups, for example countries, does not say the same holds for
   individuals (anthropics statistical-analysis).
3. **Correlation is not causation.** Before a causal claim ask whether the reverse holds, whether a third
   variable explains both, and whether it is coincidence among many variables. What can be said: "users of X
   retain 30 percent better". What needs more evidence: "X causes it" (anthropics). nimrodfisher's fix: add
   the caveat and recommend an experiment if a causal claim is required; see `experiment-design-pitfalls`.
4. **Many comparisons**: testing many hypotheses yields false positives by chance; correct for it or say how
   many tests were run (`experiment-design-pitfalls` §2.4).

## 3.3 Outliers, skew, precision
1. **Do not remove outliers automatically** (anthropics). Investigate first: a data error is fixed or
   removed, a genuine extreme is kept (consider robust statistics such as the median), a different
   population is segmented out.
2. **Report what was done**, with counts: records excluded, what share of the total, and why (anthropics'
   example states the count, the share and the reason).
3. **For skewed business metrics report the mean and the median together**; a large gap shows the skew and
   the mean alone misleads (anthropics).
4. **Statistical versus practical significance**: report effect size, confidence interval and business
   impact, not a p-value alone (anthropics).
5. **False precision**: "3.847362 percent" when the data supports "about 4 percent" (nimrodfisher). Prefer
   ranges and round to the precision the sample and the measurement warrant (anthropics).
6. **Small samples**: say so, and say what effects the sample cannot detect (anthropics). The "30 events"
   rule in that file is one author's number and is not carried.

## 3.4 Red flags and cross-checks
1. **A result that perfectly confirms the hypothesis** deserves suspicion; reality is usually messier
   (anthropics).
2. **Other red flags** from the same source:
   - a large unexplained change between periods;
   - exact round numbers in counts or sums, which suggest a filter or a default value;
   - rates of exactly 0 or 100 percent, which may mean incomplete data;
   - identical values across periods or segments, which suggest the query ignores a dimension.
3. **Cross-validate** (anthropics):
   - compute the same metric two ways and compare;
   - trace a few individual records by hand;
   - compare with a dashboard, a finance report or a prior analysis;
   - reverse engineer: per-user revenue times the user count should about equal the total;
   - check boundaries: a single day, user or category should give sensible micro-results.
4. **Order of magnitude**: user counts against known active-user figures, revenue against known annual
   revenue, rates between 0 and 100 percent (anthropics).
