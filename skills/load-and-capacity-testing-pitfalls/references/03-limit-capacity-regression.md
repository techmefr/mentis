# load-and-capacity-testing-pitfalls §3 — Limit, capacity statement and regression check

> Part 3 of `skills/load-and-capacity-testing-pitfalls`. Read it when a result becomes a decision or a
> pipeline step.
> Sources, read 2026-10-20: mercari/production-readiness-checklist, "Capacity Planning" (MIT); Azure
> Architecture Center, "Continuous validation..." (CC BY 4.0). Sentences marked "own guidance" are ours.

1. **Say what capacity planning is for.** The capacity notes define it as measuring performance and working out
   the limits of operation, then estimating whether the service can handle expected traffic. They list the uses:
   predicting whether it will serve the customers, planning and justifying performance work, planning
   autoscaling, configuring monitoring and alerting, and understanding the failure conditions. Check: each
   number you produce feeds one of those, or it was not worth measuring.
2. **Find the first bottleneck and name it.** Own guidance: at the limit one resource saturates first (CPU, a
   pool, a lock, the database, a downstream call, the network, the generator). Fix that, rerun, and find the
   next; the report names each one in order. Symptom: "it tops out at N" with no cause.
3. **Write the capacity statement with its conditions.** Own guidance: "on this instance size, with this data
   volume, this traffic mix and these dependencies, the service holds a given rate at the owner's latency target
   with a stated margin; the first limit is X". A bare number travels without its conditions and becomes wrong.
4. **Keep headroom explicit.** Own guidance: plan to run below the knee by a margin the owner chooses, so a
   spike, a deploy and a failed node fit; state the margin as a decision, not a feeling.
5. **Convert load into resources with a model you can check.** Own guidance: per-request cost (CPU time, memory,
   queries) times the expected rate gives a first estimate of instances, connections and database load. Verify
   it against the measured result; where they disagree, the model is missing something shared.
6. **Account for the dependency you cannot scale.** Own guidance: the database, a licence limit, a third-party
   rate limit or a single-writer queue caps the whole path whatever the web tier does; raise it in the report
   as the real ceiling.
7. **Set autoscaling and alert thresholds from the measurement.** The capacity notes name autoscaling and
   alerting as outputs of the work. Own guidance: scale on the signal that leads the bend (queue depth, request
   concurrency) with enough time for new capacity to start, and alert on saturation signals before the knee
   (`skills/slo-design` §3).
8. **Re-measure after a change that matters.** The capacity notes say the real-world test should be updated
   periodically since traffic numbers change. Own guidance: a new feature on the hot path, a framework or
   instance upgrade, a data growth step or a pricing campaign each invalidate the old statement; date it.
9. **Put a small test in the pipeline and a large one on a schedule.** The Azure guide recommends integrating
   load tests into the CI/CD pipeline early in feature work and running manual tests regularly to see how the
   system reacts to unexpected peaks. Own guidance: a short smoke-level run asserting the thresholds on every
   merge (scenario count and duration chosen by the owner), and the full ramp and soak before a launch or on a
   cadence.
10. **Compare against the previous run, not only the threshold.** Own guidance: a slow drift that never crosses
    the limit still halves your headroom in a year. Store the key figures per run and look at the trend.
11. **Keep the result reproducible.** Own guidance: record the code version, configuration, data set, generator
    version and settings, environment differences and the date with the figures. A result nobody can rerun is
    not evidence.
12. **Report what you did not test.** Own guidance: untested paths (a rare endpoint, a bulk import, a failover
    during load), untested durations and the stubbed dependencies belong in the report so no one reads silence
    as safety.
13. **Hand the findings to the right place.** Own guidance: a code hot spot goes to the language block's
    profiling method; a missing index or plan change goes to the database blocks (`skills/sql-conventions`); a
    limit that is too low goes to the platform config; the capacity statement goes to the readiness review
    (`skills/production-readiness-review` §2).
