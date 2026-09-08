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
