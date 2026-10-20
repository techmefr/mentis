# load-and-capacity-testing-pitfalls §2 — Driving the load and reading the result

> Part 2 of `skills/load-and-capacity-testing-pitfalls`. Read it when a test is run or a result is read.
> Sources, read 2026-10-20: Azure Architecture Center, "Continuous validation with Azure Load Testing and Azure
> Chaos Studio" (CC BY 4.0), for the baseline and failed-run points; the wrk2 README (Apache-2.0) and the
> HdrHistogram README (public domain or BSD 2-Clause) for the delayed-request and histogram points. The rest is own
> guidance from the craft, marked so, and rests on no source read.

1. **Warm up, then measure.** Own guidance: the first minutes include cold caches, a JIT, a connection pool still
   filling and an autoscaler not yet reacting. Discard or separately report the warm-up; a result that averages
   it in is a result about the warm-up. (The wrk2 README gives a 10-second calibration period and warns that runs shorter than 10 to 20 seconds may not be useful.)
2. **Ramp in steps and hold each step.** Own guidance: raise the offered load in stages and hold each long
   enough to see a steady state; a single sharp spike tells you only that a spike hurts. The step where the
   curve bends is the finding.
3. **Do not let a slow response hide the requests it delayed.** Own guidance: when a generator waits for a slow
   reply before sending the next scheduled request, the requests that should have been sent during the stall are
   never recorded, and the tail looks better than users would have felt it (the effect is usually called
   coordinated omission). Symptom: the max latency is a few seconds yet a stall of twenty seconds is visible in
   the server's own logs. Fix: send on a schedule independent of replies, or correct the recorded times for the
   intended send time, and check the tool's documentation for which one it does. Confirmed (wrk2 and HdrHistogram READMEs, read 2026-10-20): a generator that waits for each reply before sending the next measures from the actual send time and underrepresents slow periods; wrk2 sends at a fixed rate and measures from the scheduled send time, keeping an uncorrected histogram for comparison (in its example, a 1.4-second stall gives a corrected 99th percentile near 1.27 seconds against about 6 milliseconds uncorrected); the histogram library adds synthetic samples at the expected interval for each value that exceeds it. Which other tools correct, and how, was not checked.
4. **Read percentiles, not the mean.** Own guidance: the average of a skewed distribution describes nobody;
   report at least the median and a high percentile per scenario, plus the maximum, and the count of requests
   behind each. A percentile from a handful of samples is noise.
5. **Never average percentiles across runs, instances or time slices.** Own guidance: percentiles do not combine
   that way. Merge the underlying histograms or the raw samples, then compute (HdrHistogram README: histograms are additive, and the recommended practice is to merge them across threads or time and compute percentiles on the combined data; why averaging fails is own guidance).
6. **Count errors as part of latency.** Own guidance: a fast failure is not a fast success. Report the error
   rate and its kinds (timeouts, 5xx, rejected by a limiter) next to the percentiles, and decide up front
   whether a rejection counts as a failure for the test's purpose (`skills/failure-classification-before-retry`
   §1).
7. **Assert on thresholds, and treat a failed run as information.** The Azure guide runs tests with explicit
   criteria so a run that misses them is a failed run, and says a failed run means the baseline needs adjusting
   or something unexpected broke. Own guidance: decide which, and write it down; a baseline moved without
   reasons is a regression you approved by accident.
8. **Look at the server while it runs.** Own guidance: record CPU, memory, garbage collection or pause time,
   connection and thread pool usage, queue depth, database connections and slow queries, disk and network. A
   latency curve without the resource curves cannot say why it bent
   (`skills/observability-instrumentation` §3).
9. **Look for the knee, not only the failure.** Own guidance: throughput usually rises with load, flattens, then
   falls while latency climbs; capacity is the load just before the knee at the latency the owner accepts, not
   the load at which it falls over.
10. **Check retries and timeouts as a source of load.** Own guidance: under stress clients retry, and retries add
    load exactly when the system is weakest. Read the request count at the server against the count sent; a gap
    is retry amplification (`skills/go-http-resilience-pitfalls`, `skills/polly-resilience-pitfalls`).
11. **Run a soak for leaks and drift.** Own guidance: a short test cannot show a slow memory leak, a handle that
    never closes, a log or temp directory filling, a certificate or token expiring, or a job that gets slower as
    a table grows. Hold a moderate load for hours and watch the slopes, not the levels.
12. **Repeat the run.** Own guidance: one run is an anecdote. Repeat it, compare the spread, and quote the
    range; a difference smaller than run-to-run noise is not a regression.
13. **Test the autoscaler and the limits you configured.** Own guidance: confirm that scale-out triggers on the
    signal you chose, how long it takes, and that requests are not lost while it happens; the pod limit, pool
    size or rate limit you set may be the real ceiling.
14. **Expect a different baseline when a fault is injected.** The Azure guide notes that running chaos during a
    load test raises latency and error rates until a scale-out or failover completes, so such runs get their own
    baseline. Keep separate thresholds (`skills/chaos-experiment` §1).
