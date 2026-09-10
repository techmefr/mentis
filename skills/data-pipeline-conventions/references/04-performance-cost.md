# § 4 — Performance and cost

> Section 4 of `skills/data-pipeline-conventions`. Read it before a full reprocessing, and when
> choosing how a table is laid out.

1. Incremental processing (only the new/modified data) rather than a full reprocessing by default,
   unless the volume genuinely allows it at no significant cost. The "unless" is doing real work: a
   full reload is simpler, easier to reason about and idempotent for free, so it is the right answer
   for a small table — and the wrong one at the volume where it starts to time out, which arrives
   without anyone changing the code.
2. Table partitioning/clustering aligned with the real query patterns (the most frequent filter), not
   chosen arbitrarily. Aligned with the wrong column it costs the same and buys nothing, since every
   query still reads everything — and the layout is expensive to change afterwards because it means
   rewriting the table.
3. **Incremental is only correct if you can say what "new" means.** A high-water mark on a column the
   source updates in place, a timestamp that is set at insert but not at correction, a clock that
   differs between systems: each produces a pipeline that runs cheaply and quietly stops picking things
   up (§1.9). Say which column defines the window and why it is safe.
4. **Cost is a number to look at, not a feeling.** How much data a run scans, how long it takes and
   what it costs are all measurable, and a pipeline nobody has measured is one whose expensive step is
   unknown — usually not the one anybody would guess. Measure before optimising, and record the figure
   so the next change can be compared against it.
5. **A full reprocessing has a blast radius beyond its cost.** It rewrites tables other jobs and
   dashboards are reading, holds locks, and where it replaces rather than merges it makes the
   destination briefly empty or inconsistent. Say when it will run and what reads the target, which is
   the same confirmation §1.5 requires for a destructive step.
6. **The expensive part is usually the shape of the query, not the volume.** A join whose keys are of
   different types, a filter applied after an aggregation, a function wrapped around the partition
   column, a row-by-row transformation where a set operation exists: each defeats the layout chosen in
   point 2 and each is invisible in the result.
7. **Never process row by row what the engine can do in one statement**, and never pull a whole table
   into the pipeline's memory to filter it there. Both work on the sample and both fail at volume, and
   the failure mode of the second is an out-of-memory kill halfway through — which is exactly the
   partial run §1.7 has to be able to classify.
8. **A pipeline that grows with its data needs a bound, or it becomes an incident on a schedule.** Run
   time creeping towards the interval between runs, two runs overlapping, a retry queue that never
   drains: each is predictable from a trend nobody is watching. Alert on the duration, not only on the
   failure (`skills/observability-instrumentation` §4).
9. **Storage is part of the cost, and so is what is never deleted.** A raw layer that keeps everything
   is deliberate (§3.1); a transformed layer that keeps every historical rebuild is not, and neither is
   a table nobody queries. Retention is decided per layer, with the personal-data question routed to
   its owner (`business/data-protection`).
10. **Optimising before the pipeline is correct is wasted work.** Incremental logic, partitioning and
    a rewritten query all make the code harder to reason about, and doing that to a pipeline whose
    output is not yet verified means debugging two things at once. Correct, measured, then faster — and
    the measurement is what says whether the last step is needed at all.
11. **Clustering and partitioning solve different problems and a table often needs both.** Partitioning
    on a coarse, frequently-filtered column (a date) lets the engine skip whole physical segments before
    it even starts scanning; clustering orders the data within what is left so a second, finer filter (an
    id, a status) still prunes rather than reading every row in the partition — choosing one without the
    other leaves the query pruning on only one axis of its actual filter.
12. **A clustering or partition key chosen for today's query is stale the day the dominant query
    changes.** The layout is expensive to rewrite, so the choice is revisited against the query patterns
    that actually run — measured, per point 4 — rather than assumed still correct because nobody
    complained.
13. **A function wrapped around the partition or clustering column defeats pruning even when the filter
    value would have matched.** `WHERE DATE(created_at) = ...` on a column partitioned by `created_at`
    forces a full scan the same way an unindexed predicate would in a transactional database — the
    filter has to be written on the raw column for the engine to prune on it.
14. **Compute is usually the majority of the bill, and it hides in what a warehouse's autoscaling
    quietly grants.** A warehouse or cluster left to scale up during a spike and never scale back down
    accumulates cost nobody attributes to a specific pipeline; the fix is measuring per-job cost, not
    only per-day cost, so the expensive job is the one that gets optimised rather than whichever ran
    most recently before the bill arrived.
15. **A join between differently-typed keys is invisible in the query's result and expensive in its
    plan.** An implicit cast on one side of a join defeats both the index and the clustering key on that
    column, and the query still returns the right rows — which is exactly why point 6 calls this class of
    mistake invisible: nothing about the output signals that the engine scanned far more than it needed
    to.
16. **A materialised, pre-aggregated table is a cache, and a cache has a staleness budget.** Refreshing
    it on the same schedule as the tables it summarises is not automatic — the moment its refresh lags,
    it silently answers yesterday's question with today's confidence, and nothing about querying it
    signals that the number is stale.
17. **Autoscaling compute up is cheap to trigger and easy to forget to scale back down.** A cluster or
    warehouse resized for a one-off backfill and left at that size runs every routine job afterwards at
    the inflated cost, and because nothing failed, nothing draws attention to it — the fix is a scheduled
    check on the running size against the workload actually queued, not a one-time resize decision assumed
    to still be correct.
18. **A cost regression is a diff worth reviewing like a correctness one.** A query rewritten for a new
    feature that adds an unfiltered join or a wider scan passes every test in point 10's "correct first"
    ordering while quietly changing what the run costs — the measurement recorded in point 4 is what turns
    that into a reviewable number instead of a surprise on next month's invoice.
