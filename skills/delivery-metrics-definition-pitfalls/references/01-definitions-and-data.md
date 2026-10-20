# delivery-metrics-definition-pitfalls §1 — Definitions and data

> Part 1 of `skills/delivery-metrics-definition-pitfalls`. Read it when a metric is defined or computed. Own
> guidance from general craft knowledge, except the points that cite the framework's metrics guide at dora.dev
> (read 2026-10-20 for facts only, licence not verified, rewritten). Re-read it before quoting it.

1. **Pin the start and end of every duration.** Symptom: "lead time" is quoted as three days and nobody can say
   from what. Check: name the start event (first commit, pull request opened, ticket moved to in progress; the framework's guide starts change lead time at the commit to version control and ends it at deployment to production) and
   the end event (merged, deployed, live to all users), each one queryable. Fix: choose, write both, and keep
   them for the life of the series; changing one starts a new series.
2. **Decide what a deployment is.** Symptom: frequency doubles after a pipeline change that only added a
   per-region step. Check: one deployment per release to production, per service, per region or per
   environment? Fix: count one event per change reaching production for one service, state the unit, and
   exclude redeploys of the same version, configuration-only pushes if you chose to, and non-production.
3. **Choose the unit of analysis.** Symptom: a company-wide number that describes no real pipeline. Fix: compute
   per service or per team that owns a pipeline, and aggregate only by summing counts, not by averaging rates.
4. **Define a failure and link it to a change.** Symptom: the failure rate is low because incidents are logged
   without a release reference. Check: the rule that marks a deployment as failed (a rollback, a hotfix within a
   window, an incident attributed to it) and who attributes it. Fix: one written rule, applied after the fact
   by the same people, and a field on the incident that points to the change. Own the blind spot: failures
   found weeks later by users are missed, so say what window the number covers. The framework's guide describes a
   failure as a deployment that needs immediate intervention afterwards, often a rollback or a hotfix.
5. **Define restore from the user's side** (the framework's guide now calls the metric failed-deployment recovery time, the time to recover from a deployment that fails and needs immediate intervention, so state which of the two meanings you compute). Symptom: time to restore ends when the fix was merged, not when
   users recovered. Fix: end the interval at the verified recovery of the affected users or the objective, start
   it at detection or at impact (pick one, write it), and take both from the incident record
   (`skills/blameless-incident-review-pitfalls`).
6. **A mean hides the tail.** Symptom: the average lead time improves while the worst changes wait longer.
   Check: plot the distribution. Fix: report the median and a high percentile, and the count of observations; a
   handful of values is not a series.
7. **Do not count what the pipeline cannot see.** Symptom: manual or out-of-band releases are absent and the
   number looks excellent. Fix: list the release paths that bypass the instrumented one and either instrument
   them or state that the metric excludes them.
8. **Batch size explains most movements.** Own guidance: a change that bundles many commits has a long lead time
   and a larger failure surface. Symptom: frequency falls after a release train is introduced. Fix: record the
   change size beside the duration so a shift is read as batching, not as a slower team.
9. **Time zones and clocks.** Symptom: negative or day-long gaps. Fix: store events in UTC from the system that
   emitted them, and reject a pair whose end precedes its start instead of silently averaging it.
10. **Version the definition.** Symptom: a chart shows a step on the day someone fixed the query. Fix: keep the
    definition in the repository beside the query, with a change note, and annotate the series on the day it
    changes.
11. **Use the names of the current publication, or say which edition you follow.** Symptom: a report lists four
    metrics while the framework's guide now lists five, or quotes "time to restore" where the guide says
    failed-deployment recovery time. Check: the framework's guide names change lead time, deployment frequency,
    failed-deployment recovery time, change fail rate and deployment rework rate, the last being the share of
    deployments that are unplanned and triggered by a production incident, grouped as three throughput measures
    and two instability measures. Fix: write which edition and which names the report follows, and do not mix
    names from two editions in one chart.
