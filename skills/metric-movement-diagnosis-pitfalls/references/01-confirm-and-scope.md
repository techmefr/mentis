# metric-movement-diagnosis-pitfalls §1 — Confirm the signal and scope the movement

The most expensive mistake in a metric investigation is explaining something that did not happen. Two checks
come before any story: is the movement real, and how big, when and where is it.

## 1.1 Confirm the signal
1. **Is the pipeline fresh?** Check for delays in the data load before reading a drop as a business event
   (nimrodfisher rca_framework).
2. **Is the definition consistent?** Has a query, a schema or a filter changed (same source)?
3. **Does it show in more than one independent source**, or in a single dashboard or report only?
4. **Is it outside normal variation?** nimrodfisher's SKILL compares the change with the usual spread or a
   rolling average and closes the case as "within normal range" if it is not beyond it; its threshold
   (a number of standard deviations) is not carried. Compare the same weekday across weeks: if a Tuesday is
   always lower, a low Tuesday is not news (hypothesis_testing_guide).
5. **A false alarm wastes the team's time**, so this step is done first even when the movement looks obvious
   (rca_framework).

## 1.2 Scope the movement
1. **When did it start, how large is it, which populations are affected** (rca_framework). Plot the metric
   far enough back to see ordinary variation; the source says 12 weeks or more and a start date to within a
   day or two.
2. **Step or drift.** A sudden step suggests a specific event; a gradual drift suggests a structural shift
   (nimrodfisher SKILL).
3. **All users or a slice**: check whether the movement affects everyone or one segment.
4. **Correlate with the event log**: deployments and releases, campaigns and pricing changes, seasonal
   patterns compared with the same period last year, external events. An event that lines up with the onset is
   a strong candidate, not a conclusion (rca_framework).
5. **Keep the log at hand**: the SKILL's inputs are a change or incident log for the same period and the
   business decision that depends on the metric.

## 1.3 When not to investigate
1. **A movement explained by a known cause** (a holiday, a planned outage, a product launch) does not need
   a full investigation (rca_framework).
2. **What counts as material depends on context.** The source gives example percentage thresholds by metric
   type; they are not carried here. Agree the materiality with the owner of the metric before the work starts
   (own guidance).
3. **Decide how deep to go from the decision at stake**, and say what depth was chosen in the write-up
   (own guidance).

A header for the write-up (shape from nimrodfisher's template, wording ours):

```
Metric / movement:       name | direction and size | comparison period
Detected on:             date | owner | status (open, cause identified, resolved)
Signal confirmed:        yes | no | sources checked | pipeline fresh?
Onset:                   date, plus or minus days
Scope:                   affected | not affected (platform, region, segment, product area)
```
