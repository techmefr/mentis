# § 3 — Analytical schema modelling

> Section 3 of `skills/data-pipeline-conventions`. Read it when shaping tables meant for analysis.
> Point 1 is the raw-layer rule §1.4 cites at file scale.

1. Clear separation between the raw layer (data as received, never modified) and the transformed layer
   (cleaned/aggregated data): never a transformation that overwrites the original raw data without
   keeping it. The raw layer is what makes every later mistake recoverable: a logic error found six
   months on is a re-run rather than a request to the source system for data it may no longer hold.
2. Consistent and documented column/table naming (explicit table grain: one row = what exactly); a
   table with no defined grain invites wrong joins. The concrete failure is a sum that double-counts
   after a join fanned out, and it produces a number that is plausible, stable and wrong
   (`business/data-analytics` §2.7).
3. Explicit historisation (SCD - slowly changing dimension) when a value changes over time and the
   history matters for the analysis, rather than a plain `UPDATE` that loses the previous state. The
   test is whether any question is asked about the past: an order's total has to be computed with the
   price that applied then, and an `UPDATE`-in-place makes last year's revenue change every time a
   price does.
4. **A transformation belongs in one tier, and the tiers are what keep a source change cheap.**
   Cleaning and renaming per source table, joins and business logic above it, the final tables an
   analyst queries at the top: a rule duplicated across two of those, or a top-level table reading a
   raw source directly, is a boundary being skipped rather than modelling being too heavy
   (`business/data-analytics` §3.3).
5. **Never let a business rule live in two models.** The same filter or derivation written twice
   diverges at the first change, and the divergence surfaces as two dashboards disagreeing — at which
   point both are defensible from their own code, which is the argument
   `business/data-analytics` §5.3 describes.
6. **A model's name is read by people who did not build it.** A table named after its source system,
   its job or an internal abbreviation cannot be found by someone holding a business question, and the
   analyst's fallback is to pick whichever table looked closest. Name by what it holds and at what
   grain.
7. **A dimension needs a key that survives the source's own changes.** Reusing the source's primary key
   as your own means a source that renumbers, merges or recreates a record silently rewrites your
   history, and the join that used to be right is now pointing at somebody else.
8. **Deletion in the source is an event, not an absence.** A row that disappears upstream has to be
   recorded as deleted rather than vanishing from the model, or a historical count changes retroactively
   with no trace — and the reason nobody can find is that the evidence was the row.
9. **Say what a column means in the same place it is defined.** A code column with no stated
   vocabulary, an amount with no currency, a timestamp with no timezone: each gets interpreted by the
   first analyst to use it, and their interpretation propagates into every report built afterwards.
10. **Never model for a question nobody has asked.** An extra dimension, an extra grain or a
    pre-aggregation built in advance is a table that has to be maintained, tested and kept consistent
    with the ones people actually query — and the one that goes stale is always the unused one, which
    is then found and trusted (`skills/design-patterns` §1).
11. **A model has to be readable as a whole, not only run.** Someone will have to answer "where does
    this number come from" under pressure, and a chain of views referencing views with logic scattered
    through it cannot be answered from — which is what makes the tiering in point 4 a legibility rule
    as much as a maintenance one.
