# § 1 — Idempotence and reproducibility: the non-negotiable base

> Section 1 of `skills/data-pipeline-conventions`. Read it on any pipeline run, and on any ad-hoc job
> against data somebody handed you. Points 4 and 5 were added 2026-09-07 and are cited by number from
> `references/origin.md`.

1. A pipeline replayed twice on the same source produces the same result (idempotent): never an
   `INSERT` that duplicates on every run with no deduplication or `UPSERT`. The reason this is the
   base and not an optimisation is that every pipeline gets replayed — a retry, a backfill, a crash
   halfway, a scheduler firing twice — so a non-idempotent one is not a pipeline with a caveat, it is
   one whose output is a function of how many times it happened to run.
2. Every run is traceable: source, version of the transformation code, timestamp: so you can trace
   back "which version of the pipeline produced this row". Without it, a wrong figure cannot be
   attributed: nobody can tell whether the source was wrong, the logic was wrong, or the row predates
   the fix, and all three have different remedies.
3. Transformations tested on a sample before a full run on production data, especially for a
   destructive transformation (full replacement of a table).

4. **A file someone handed you is never the working copy.** Read it, work on an in-memory or copied
   representation, and write the result somewhere else — the original stays byte-identical, because it is
   often the only copy and always the only evidence of what arrived. This is the ad-hoc counterpart of §3.1's
   raw layer: the same rule, at the scale of one file and one request rather than a scheduled run.
5. **A destructive transformation is confirmed before it is applied, not after.** Replacing values,
   dropping rows, merging accounts or normalising identifiers on someone's data is not reversible from
   their side. Say what the step will change and on how many rows, then apply it — one step at a time,
   rather than a single pass whose result has to be trusted wholesale.
6. **Idempotent means the whole run, not each statement.** A job that upserts correctly and then
   appends to a log table, increments a counter or fires a notification is not idempotent: the replay
   produces a duplicate somewhere nobody is looking, and it is usually the side effect rather than the
   data. Every write in the run is covered, or the run is not replayable.
7. **A partial run has to leave a state you can resume from or discard.** Failing halfway is the normal
   case, and the two safe shapes are all-or-nothing within a transaction and a run that records how far
   it got. Anything else leaves a table nobody can classify — and the usual response, re-running from
   the start, is exactly what point 1 has to survive.
8. **Never key a run on "now".** A pipeline whose window is derived from the wall clock produces a
   different result on every replay and cannot be backfilled, which turns a one-line fix into a manual
   reconstruction. The window is a parameter, and the run records the value it used.
9. **A late-arriving or corrected record is expected, not exceptional.** Source systems emit
   corrections, and a window that only ever moves forward will silently miss them — so the reprocessing
   policy is part of the design, and its absence shows up as a total that no longer matches the source
   with nothing having failed.
10. **The reproducible unit is the code plus its inputs plus its configuration.** A threshold in an
    environment variable, a mapping table edited by hand, a reference file replaced in place: each
    makes the same code produce a different answer, so each is versioned or recorded with the run. This
    is what makes point 2's attribution actually possible rather than nominal.
11. **A schema change in the destination is a migration, not an edit.** Renaming or retyping a column
    the analytics layer reads breaks every model and dashboard downstream, and the breakage arrives on
    their next run rather than yours — so the same expand-then-contract discipline applies as to any
    other published contract (`skills/api-design` §3).
12. **A test on a sample is not a test on the volume.** A sample proves the logic and says nothing
    about the cost, the timeout, the memory or the lock the full run will take. Point 3 is about
    correctness; the volume question belongs to §4, and treating a green sample as clearance for a
    destructive full run is the specific mistake that makes it worth saying twice.
13. **`unique_key` is the merge's real contract, and it has to be the model's actual grain, not "unique
    enough in the source today."** A merge keyed on a column that is only accidentally unique overwrites
    the wrong row the day two events share it, and the failure looks like a silently dropped record
    rather than an error — so the key gets its own uniqueness and not-null test, the same as any other
    published contract in point 11.
14. **A lookback window survives clock skew and late arrival better than a bare high-water mark.**
    Re-processing the last few periods on every incremental run costs a little recomputation and buys
    back the records point 9 says are expected: a source system's clock running a few minutes behind, or
    a correction landing just after the previous run's cutoff, both land inside the lookback instead of
    being silently missed forever.
15. **A schema change in the source is a decision, not a crash.** A pipeline has to state whether an
    unexpected new column is captured, ignored or fails the run — the alternative is finding out which
    one happens by accident, usually via a downstream query that started returning `NULL` for a column
    it used to fill.
16. **A scheduled full refresh is the self-healing companion to incremental processing, not a
    contradiction of it.** Incremental keeps the daily cost down; drift between the incremental history
    and the source still accumulates from edge cases nobody wrote a test for, and a periodic full rebuild
    (weekly, monthly) is what catches and corrects it before a customer does.
17. **Row-count trend, not just row-count-at-a-point, is what catches a broken filter.** A single run's
    count says nothing on its own; the same count against its trailing average is what turns "the join
    condition silently changed" into an alert instead of a number nobody looks at until the quarterly
    reconciliation.
18. **Idempotency has to be provable from outside the code, not asserted in a comment.** A test that runs
    the same pipeline twice against the same input and diffs the two outputs is the check that actually
    exercises point 1 — reading the code and reasoning "this looks idempotent" is exactly the kind of
    confidence a partial `UPSERT` or an unguarded side effect defeats silently.
19. **`on_schema_change` is a policy to set, not a default to inherit.** Left unset, a merge into a table
    whose source added a column either fails the whole run on the next build or silently drops the new
    column depending on the engine — stating whether new columns are appended, ignored or force a full
    rebuild turns point 15's "decision, not a crash" into something a reviewer can actually see in the
    model's own configuration rather than infer from an incident.
20. **A merge strategy still needs a deliberate answer for a row deleted at the source.** `MERGE` only
    ever inserts or updates matched keys; a row absent from the incoming batch is silently left in place
    forever unless the model explicitly checks for and marks it gone — which is the same absence-as-event
    rule §3.8 states for the modelling layer, arriving here at the mechanism that has to implement it.
