# metric-movement-diagnosis-pitfalls §2 — Decompose, hypothesise, test

Once the movement is real and scoped, split it into parts before naming a cause, then treat each candidate
cause as a claim that has to survive a test.

## 2.1 Decompose before drilling
1. **Break the metric into its parts** (nimrodfisher SKILL): for example revenue as volume times price times
   mix. Find which part drives the change before cutting by dimension.
2. **Volume, rate and mix effects** (rca_framework): the segment had more or fewer users, the metric per user
   changed, or the segment's share of the total changed. A mix shift can move a total with no segment changing.
3. **Contribution**: for a metric that is a sum across segments, a segment's contribution is its change divided
   by the total change. A segment with a large absolute change and a large share is the primary driver.
4. **Drill by dimension** (platform, region, plan, cohort, channel, product area), ordered by absolute
   contribution, to see whether the movement is concentrated in a slice.
5. **Compare the denominator, not only the numerator.** A different mix of users entering a funnel changes a
   rate with no change in the product (hypothesis_testing_guide). Compare cohorts by acquisition cohort when
   newer users may behave differently.
6. **Report the share each part explains.** The SKILL's report names the primary driver with its quantified
   share of the impact, so a movement with several contributors stays honest about it.

## 2.2 Write hypotheses that can fail
1. **A testable hypothesis has three parts** (hypothesis_testing_guide): a specific cause, the effect it
   predicts, and the test that confirms or refutes it. "Something broke" cannot be tested.
2. **Record for each**: evidence for, evidence against, and the test (rca_framework).
3. **Rank by likelihood times ease of testing** and test the likely and cheap ones first (rca_framework).
4. **Run tests in parallel** when they need independent data pulls; **in sequence** when one confirmed cause
   would explain everything or when one test needs the outcome of another (hypothesis_testing_guide).
5. **Check confounders on observational work**: day of week, cohort, user mix (same guide).

## 2.3 How much to trust the evidence
1. **A hierarchy, strongest first** (hypothesis_testing_guide):
   - a controlled experiment;
   - a natural experiment, where an event reached only a subset and affected and unaffected are compared;
   - a before and after comparison with no simultaneous changes;
   - segment analysis where the pattern sits in the segments the hypothesis predicts;
   - correlation in a time series, the weakest, which needs corroboration.
2. **Say which level the evidence is at** next to the verdict, with a confidence (high, medium, low) as in the
   source's outcome table.
3. **Ruling out counts as much as confirming.** A hypothesis is out when the predicted pattern is absent, when
   the timing does not fit (the metric moved before the cause), or when the population does not fit (desktop
   only moved, the cause was a mobile release).
4. **Record ruled-out hypotheses** with the reason, so the same dead end is not investigated twice. The final
   report lists every hypothesis tested, not only the confirmed one.

## 2.4 When a cause is established
1. **The hypothesis explains timing, magnitude and population** (rca_framework).
2. **Reversing the cause stops the movement**, where that can be tested.
3. **No alternative explains the data as well.**
4. **Close the loop**: the confirmed cause, the impact quantified (users, revenue, duration), a corrective
   action with an owner and a date, and a preventive measure that would catch it earlier next time
   (rca_framework and the report template).
5. **Say "cause not established" when it is not.** An open verdict with the remaining candidates is a result;
   a story that fits the timeline only is not (own guidance, from the evidence hierarchy in point 1 of §2.3).

A hypothesis record (fields from the source, layout ours):

```
Hypothesis:        one sentence, specific
Predicted signal:  the pattern that would confirm it
Evidence found:    what the data shows
Verdict:           confirmed | refuted | inconclusive
Reason if refuted: timing | population | pattern absent
Confidence:        high | medium | low
```
