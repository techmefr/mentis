# webperf-measurement-and-budget-pitfalls §1 — Evidence and thresholds

"The page is fast" is four different claims depending on where the number came from. Most wrong conclusions
here are a right number answering a different question.

## 1.1 Keep the evidence types apart
1. **Each instrument answers one question.** The Web Quality Skills measurement guide separates five. Field data
   from the Chrome UX Report is an aggregate of eligible real Chrome users over a rolling window, normally 28
   days, and answers whether users have a Core Web Vitals problem. First-party real-user monitoring is the site's
   own sessions, for segmenting and diagnosing current production. A DevTools trace is one observed session under
   stated conditions, for finding the cause. A Lighthouse lab run is a controlled synthetic navigation, for
   reproducing load problems and catching regressions. Reading source only yields hypotheses.
2. **A `PerformanceObserver` snippet in one tab is a single-session lab observation.** It becomes real-user
   data only when measurements from actual users are reported and aggregated.
3. **When nothing can run, label every finding a hypothesis** and name the measurement that would settle it
   (the same guide).
4. **Record the scope of a field number.** Prefer page-level data for the audited URL; origin-level data is
   context and not proof for that route. Keep phone and desktop apart: combining form factors cannot answer a
   question about one device.

## 1.2 Reading field data
1. **Decide at the 75th percentile and never on an average.** The guide's reporting advice for first-party
   monitoring is to assess each of the three Core Web Vitals at p75, together with the share of visits in the good,
   needs-improvement and poor buckets, the sample count and the time window.
2. **The combined pass needs all three.** All three p75 values must meet their "good" thresholds for a route or
   origin to pass the combined assessment (the same guide).
3. **Missing field data means unavailable, never passing.** Localhost, staging, new, private and low-traffic
   pages commonly have no record; then the lab run is for diagnosis, and real-user monitoring is the
   recommendation if production impact matters.
4. **Field data is delayed.** It is aggregated over a window, so it prioritises user outcomes but cannot confirm
   a change deployed minutes ago.
5. **Field and real-user monitoring can disagree legitimately.** They cover different users, browsers,
   routes, sampling rules and windows; the guide asks that those differences be written down before either
   source is called wrong. The `web-vitals` README adds one cause: its observers cannot see inside iframes, which
   the Chrome UX Report includes (§2.3).

## 1.3 Ratings
1. **The library publishes the edges.** In `web-vitals` 6.2.3, `CLSThresholds` is `[0.1, 0.25]`, `INPThresholds`
   is `[200, 500]` and `LCPThresholds` is `[2500, 4000]`. Values up to and including the first edge rate "good", values up to and including the
   second rate "needs improvement", and values above the second rate "poor".
2. **Use the `rating` the library puts on the metric.** The README says it is typically unnecessary, and not
   recommended, to recompute a rating from the thresholds by hand. A copy of the numbers in a dashboard
   rule is the kind of duplicate that goes stale (own guidance).

## 1.4 Lab runs and reconciling them with the field
1. **Record the conditions with the result**: final URL and page state; browser and tool version; viewport or
   form factor; CPU and network throttling; cold or warm cache; authentication, consent and experiment state
   (the measurement guide).
2. **For a decision based on a headline lab metric, run at least three equivalent navigations and report the
   median with the range.** Do not compare one local trace with a field p75 or expect the two to match. Use the
   metric values as evidence; the guide calls a Lighthouse score a diagnostic summary whose weighting can change
   between versions.
3. **Reconcile with a table, not an argument.**

   | Field | Lab | Reading |
   |---|---|---|
   | Poor | Poor | A reproducible user problem; trace and fix the dominant cause |
   | Poor | Good | The local run missed real conditions; segment real-user data or test other devices, routes and cache states |
   | Good | Poor | The synthetic cold throttled case is fragile; do not claim users are failing |
   | Unavailable | Any | Diagnose in the lab and recommend real-user monitoring |

4. **Start a report with an evidence table**: signal, scope and conditions, baseline, after, source (the guide's
   compact audit output). A row whose "after" is "pending the field window" is honest; a lab number in a
   field row is not.
