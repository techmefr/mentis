# experiment-design-pitfalls §2 — Running and reading the test

The readout is where a sound design is usually lost: a look at day three, a result read before the split was
checked, a segment found afterwards.

## 2.1 Analyse once
1. **A well-designed test is analysed once** (nimrodfisher). Checking results repeatedly and stopping early
   invalidates the p-value. The RefoundAI summary lists "decisions on real-time p-values" among the common
   mistakes, for the same reason.
2. **Sources differ on a positive trend that is not significant.** phuryn's table says to extend the test.
   nimrodfisher's design guide says do not ship, revisit the hypothesis or the MDE, and its guide opens with
   the analyse-once rule. **This block follows nimrodfisher**: extending after seeing a positive but
   non-significant result is a look at the data that changes the stopping rule.
3. **An extension is allowed only if it was written in the design** (own guidance, resolving the two
   sources): a rule fixed before launch that says when more data will be added. Otherwise run a new,
   pre-registered test. nimrodfisher's own SKILL lists "extend" among its possible recommendations, but gives
   no rule for when, so the design card is where that rule has to live.
4. **Early stopping is for the harm case only**: monitoring and rollback criteria from §1.1 may end a test
   that is damaging users; that is a safety stop, not a result (own guidance, built on the monitoring item).

## 2.2 Sample ratio mismatch (SRM), checked first
1. **Check the split before any metric** (nimrodfisher's process puts the SRM check before the per-variant
   metrics): chi-squared test on the actual allocation against the intended one. nimrodfisher flags a
   p-value below 0.01; that threshold is the source's choice.
2. **SRM is an instrumentation signal, not a treatment effect**, and it invalidates the test. If it is
   detected, do not interpret the results; investigate the assignment mechanism before re-running.
3. **Usual causes** (nimrodfisher's list):
   - bots filtered on one side only;
   - stickiness failure: users re-assigned when they return;
   - a triggered experiment where only a subset qualifies after assignment;
   - a cache or CDN serving a stale experience to some users.
4. **Report the check in the readout** next to the sample sizes, so a reader can see it was done.

## 2.3 Reading the primary result
1. **Per variant**: the rate or mean with a 95 percent confidence interval, and the absolute and relative
   difference (nimrodfisher). Report intervals, not only p-values (product-on-purpose).
2. **Test choice** (nimrodfisher): two-proportion z-test for rates, Welch's t-test for means. anthropics adds
   Mann-Whitney U for skewed data. The nimrodfisher reference on test choice is missing from the clone, so
   nothing else is carried.
3. **Statistical significance is not practical significance.** A tiny difference can be significant with a
   large sample (anthropics, phuryn). Report effect size, interval and what it means in business terms.
4. **Run the same test on every guardrail.** A significant degradation on any guardrail blocks the ship
   (nimrodfisher).
5. **Decision table** (nimrodfisher):

   | Result | Decision |
   |---|---|
   | Significant positive, guardrails pass | ship |
   | Significant positive, a guardrail fails | do not ship, investigate the regression |
   | Not significant | do not ship, revisit hypothesis or MDE |
   | Significant negative | do not ship, understand the harm first |
   | SRM detected | re-run, do not interpret |

## 2.4 Segments and many comparisons
1. **Look at segments for differing effects**, and check that the result holds across devices or regions or
   explain why not (nimrodfisher). product-on-purpose: an overall result can hide a segment effect.
2. **Count the looks.** anthropics: testing 20 metrics at 0.05 gives about one false positive; if many
   segments were examined before one stood out, say so.
3. **Correct or disclose**: Bonferroni (alpha divided by the number of tests) or a statement of how many
   tests were run (anthropics). product-on-purpose's results template has a line for the correction used.
4. **A segment found after the readout is a new hypothesis**, to be tested in its own pre-registered
   experiment (own guidance).
5. **Aggregates can mislead when the mix shifts**; `analysis-validation-pitfalls` §3 covers Simpson's paradox.
