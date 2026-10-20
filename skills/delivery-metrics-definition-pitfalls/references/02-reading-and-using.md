# delivery-metrics-definition-pitfalls §2 — Reading and using the numbers

> Part 2 of `skills/delivery-metrics-definition-pitfalls`. Read it when a number is compared, targeted or acted
> on. Own guidance from general craft knowledge, except the points that cite the framework's metrics guide at
> dora.dev (read 2026-10-20 for facts only, licence not verified, rewritten); no benchmark is given.

1. **Compare a service with itself.** The framework's guide says the same: the metrics are meant for one application or service at a time, not for comparing very different applications, and not as a contest between teams or organisations. Symptom: a table ranks teams, the lowest one owns the oldest, most
   regulated system. Fix: read the trend of one service over time against its own earlier definition; compare
   across services only to ask why, never to rank.
2. **Speed and stability move together or the metric is wrong** (the framework's guide warns against relying on one metric and recommends several that pull against each other, grouped as throughput and instability). Symptom: frequency rises and failures rise too,
   reported as a win on the first. Fix: always show a throughput metric next to a stability metric, and read
   them as a pair.
3. **A target invites gaming** (the framework's guide says not to set the metrics as goals, citing the law that a measure used as a target stops measuring). Symptom: deployments split into empty releases, failures reclassified as
   "not related", tickets closed early. Fix: use the number to locate a constraint in a retrospective; where a
   target is unavoidable, pair it with a counter-metric that the gaming would worsen, and review the definition
   for loopholes first.
4. **Break the cycle time into waits.** Symptom: "we are slow" with no direction. Check: time in review before
   the first response, review rounds, queue for a build or environment, wait for an approval, time from merge
   to production. Fix: pick the largest wait and change that, then re-measure; coding time is rarely the
   biggest part.
5. **Measure the queue, not only the work.** Own guidance: items waiting are invisible in a duration that
   starts at pickup. Fix: include the wait before work starts, or count the age of what is still open.
6. **Toil is a measured category, not a feeling.** Symptom: a team says it drowns in manual work and cannot show
   it. Fix: sample a fortnight of time into planned work, interrupts and repeated manual tasks, list the
   top few repeated tasks with their frequency and cost, and rank candidates for automation by hours saved.
   Do not read a single sample as a trend.
7. **A survey needs a definition too.** Symptom: a satisfaction score falls and nobody knows why. Fix: ask about
   named parts of the work (build time, review, local setup, on-call) with a free-text field, keep the
   wording stable across rounds, report the response rate, and act on one or two items and say so before the
   next round. A score with no follow-up teaches people not to answer.
8. **Pair numbers with a story.** Symptom: a metric changed and the explanation is invented afterwards. Fix:
   when a number moves, read the underlying changes and incidents of that period before concluding
   (`skills/metric-movement-diagnosis-pitfalls`).
9. **Do not import outside bands.** Own guidance (the bands were not read): published performance bands are a snapshot of a surveyed
   population, redefined between editions. Symptom: a slide says "we are in the top group" from a number built
   on a different definition. Fix: if a band is needed, re-read the current publication, quote it with its year,
   and check that your definitions match its own before comparing.
10. **Protect the people in the data.** Symptom: per-person commit or review counts appear in a dashboard.
    Fix: aggregate to the team, never rank individuals, and say what the data will not be used for before
    collecting it.
