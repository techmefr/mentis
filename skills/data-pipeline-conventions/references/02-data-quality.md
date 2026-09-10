# § 2 — Data quality: verified, not assumed

> Section 2 of `skills/data-pipeline-conventions`. Read it when writing a pipeline's validations, or
> when deciding what to do about a source you do not control.

1. Explicit validation of the expected constraints (non-null on required fields, key uniqueness,
   plausible value ranges) at the pipeline's input and output: a validation failure blocks the
   pipeline, it doesn't pass silently while producing wrong data. Both ends matter for different
   reasons: the input check attributes the problem to the source, and the output check catches the
   transformation that produced something the source never contained.
2. The four quality dimensions verified explicitly where relevant: completeness (nothing missing),
   accuracy (correct value), consistency (same fact, same value across systems), timeliness (data up
   to date at the moment of use).
3. An external source (third-party API, partner file) is treated as unreliable by default: schema
   checked on every ingestion, not assumed stable over time. The change that hurts is not a removed
   column, which fails loudly: it is a column that starts arriving empty, a code whose meaning was
   redefined, or a date format that changed for one region.
4. **Failing loudly is the point, and it is a choice with a cost.** A pipeline that blocks stops the
   downstream numbers from moving, which is visible and gets attention; one that continues produces
   figures somebody will act on. Where blocking genuinely is not acceptable, the shape is a quarantine
   — the bad rows set aside, the run marked partial, the count published — never a silent skip. **A
   violation that is a property of the set makes the run the quarantine unit, not the row**: a duplicated
   key, a total that disagrees with its parts, an entity counted in two groups — none of these is
   attributable to one row, so setting rows aside is impossible and the honest granularity is the whole
   run, refused by default with a deliberate way to store it anyway. Found by dogfooding 2026-09-08.
5. **Say how many rows failed, not only that something did.** One row rejected and a third of the file
   rejected are different incidents with different responses, and a boolean result cannot distinguish
   them. The count, with an example, is what makes the alert actionable
   (`skills/observability-instrumentation` §4.3).
6. **A validation with no owner is a validation that gets disabled.** The first time a check blocks a
   run at an inconvenient hour, somebody will loosen it, and the loosening is permanent unless someone
   owns the rule. Name who decides, and record the reason next to the threshold.
7. **Count what came in against what went out, every run.** Row counts in, out, rejected and
   deduplicated are the cheapest possible check and the one that catches the largest class of silent
   failures: a join that dropped rows, a filter that matched more than intended, a file that was
   truncated in transit.
8. **Reconcile against the source, not only against yourself.** An internally consistent pipeline can
   be consistently wrong, and the only test that catches it is comparing a total to the system of
   record. That is the consistency dimension in point 2, and it needs a second connection and different
   credentials, which is why it gets skipped (`business/data-analytics` §1.6).
9. **A null is not a zero and an absent row is not a null.** Coercing either to make a total look
   complete produces a number nobody can question, because the gap has been erased rather than
   reported. Carry the distinction through the pipeline and let the reader see it
   (`business/data-analytics` §4.2).
10. **Duplicates are defined by a key you have to choose.** "The same record twice" is only meaningful
    against a stated business key, and the choice is a decision — two rows differing only in a
    timestamp may be one event or two. Deduplicating on the wrong key deletes real data, silently and
    irrecoverably.
11. **Never validate against what the pipeline itself produced.** A check that reads the transformed
    layer to decide whether the transformation was correct passes on any consistent error, which is the
    class this whole section exists to catch. The expectation comes from the source, the contract or a
    stated invariant.
12. **A quality check is code and needs a test.** A validation that never fires because its condition
    can never be true is worse than none: it reports green forever and the dashboard says the data is
    verified. Force it to fail once, the same way an alert is forced
    (`skills/observability-instrumentation` §4.2).
13. **Uniqueness is its own dimension, not a corollary of completeness.** A row can be fully populated,
    accurate and current and still be a duplicate, and a duplicate silently inflates every sum built on
    top of it — a count check that only looks at nulls and ranges never catches it, which is why it needs
    its own explicit assertion rather than riding along with point 2's four dimensions.
14. **A schema test and a unit test check different failures, and neither substitutes for the other.** A
    post-materialisation check (point 1) catches what the data actually is; a test against the
    transformation's logic on fixed input catches what the SQL or the code *would* produce before it runs
    against anything real — a logic bug that happens to produce plausible output on today's data passes
    the first and fails the second.
15. **A published contract on a table's schema is a promise checked before the data lands, not after.**
    Declaring the expected columns, types and nullability up front and failing the build when the model
    would violate it catches a breaking rename or a dropped column at merge time, before a consumer's
    dashboard breaks on the next refresh — which is strictly earlier than the input check in point 1 can
    fire.
16. **Validity is not accuracy, and conflating them hides the harder problem.** A value can be
    well-formed, in range and pass every schema check while still being wrong — a plausible but incorrect
    account number, a rounded amount that no longer matches its source. Point 2's four dimensions
    deliberately keep these separate because the cheap, mechanical check for one gives no signal at all
    about the other.
17. **An old data-quality framework choice is a freshness question in itself.** A validation library or a
    contract format adopted once and never revisited accumulates the gap between what it can express and
    what the pipeline actually needs — the check to make periodically is not only whether the rules still
    hold, but whether the tool enforcing them is still the currently maintained one.
18. **A quarantine needs a way back in, or it is just a second silent failure.** Point 4's quarantine
    stops bad rows from reaching the destination, but a quarantine nobody reviews and nothing ever
    reprocesses out of is equivalent to deleting the rows — the quarantine is a queue with an owner, not
    a place data goes to be forgotten.
19. **A unit test on a transformation runs before the model touches a warehouse, and that ordering is
    the value.** Feeding fixed rows straight into the SQL or the transformation function and asserting the
    output catches a logic error at the speed of a function call, whereas point 1's post-materialisation
    check only fires after a full build — the two are complementary, not redundant, precisely because one
    is cheap to run on every commit and the other needs real infrastructure.
20. **A data contract is a promise checked at the boundary between producer and consumer, not a shared
    understanding kept in someone's head.** Whichever format states it — a schema file, a YAML contract, a
    registry entry — the discipline is the same as the destination-side migration rule in §1.11: the
    producer cannot silently change what it emits, because a consumer is depending on the current shape
    without being asked each time.
