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
12. **A dimension that changes rapidly does not belong in the same row as one that barely changes.**
    Tracking every change to a fast-moving attribute (a status, a tier, a score) with the same
    row-per-change history as point 3's slowly changing dimension explodes the table and makes an
    otherwise simple join expensive — splitting the volatile attributes into their own smaller
    dimension, joined by its own key, keeps the stable dimension stable and the volatile one cheap to
    scan.
13. **A many-to-many relationship between a fact and a dimension needs a bridge, not a wider grain.**
    Forcing a fact table's grain to absorb a multivalued attribute (an order with several tags, an
    account with several holders) either duplicates the fact row per value or silently drops values —
    a bridge table carrying the relationship, constrained to one point in time when the dimension side
    is itself historised, is what keeps the fact table at its declared grain from point 2.
14. **Not every change needs history, and saying so explicitly is part of the design.** A column that
    should only ever show the current value (an overwrite, not a track), stated as such next to the
    column, is different from one nobody thought about — the silent case is the one that gets "fixed"
    into history months later, retroactively changing what old reports meant.
15. **A surrogate key is generated by the warehouse, not carried over from a natural key composed of
    several source columns.** A natural key built by concatenating fields is exactly as fragile as any
    one of them changing format, and it is usually wider and slower to join on than a single generated
    integer or hash — the surrogate key is what point 7's key-survives-source-changes rule is actually
    implemented with.
16. **A late-arriving dimension row is a known case, not an edge case.** A fact referencing a dimension
    member that has not been loaded yet needs an explicit placeholder row rather than a failed join or a
    silently dropped fact — and the placeholder gets reconciled once the real dimension row lands, rather
    than left as a permanent unknown.
17. **A conformed dimension is what makes two fact tables comparable, and it has one owner.** The same
    customer or product dimension reused, unchanged, across every mart that references it is what lets a
    revenue fact and a support-ticket fact be sliced by the same customer attributes — a dimension
    forked per mart to save a join produces two customer lists that quietly diverge.
18. **A fact table's grain determines what a `SUM` over it means, and stating the grain is not enough —
    every column has to be true at that grain.** A pre-aggregated column sitting in a table whose declared
    grain is the individual transaction produces the double-count in point 2 the moment it is summed
    alongside the transaction rows themselves, since the aggregate and its parts are no longer at the same
    level.
19. **A snapshot table exists to answer "what did this look like at time T", and it is not a substitute
    for point 3's historisation inside the dimension itself.** Periodically copying a whole table's current
    state captures history at the resolution of the snapshot interval, which misses every change between
    two snapshots — it is a coarser, cheaper mechanism for a different question, not a replacement for
    tracking the change itself when the analysis needs the exact moment it happened.
