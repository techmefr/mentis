# § 3 — Consolidation across independent instances

> Section 3 of `business/data-analytics`. Read it when a figure has to span several independent
> per-entity or per-tenant databases, or when a consolidated layer is being shaped.

1. **A `UNION ALL` view across N independent per-entity databases is a real technique, and a fragile
   one**: it needs manual maintenance every time a new entity is added (a new acquisition, a new
   tenant), and its performance degrades as N grows, because every query touches every instance. Treat
   it as a stopgap whose maintenance cost is visible, not as a permanent architecture, and say so when
   proposing it as the answer to "consolidate this across all entities." The failure mode is the one
   nobody notices: a new entity that was never added to the view is simply absent from every report
   built on it, and the total stays plausible.
2. **A real analytical need (repeated queries, growing entity count, real-time-adjacent latency
   requirements) is the signal to raise a proper consolidated/warehouse layer**, not to add yet another
   hand-maintained view. Recommending the fragile pattern as a one-off is fine; recommending it as the
   long-term answer without naming the tradeoff is not.
3. **When that proper layer gets built, model it in tiers rather than one flat pile of views/tables.**
   The shape that keeps a growing analytics codebase workable: a **staging** tier that cleans and
   renames each source table one-for-one (no joins, no business logic — every mart pulls through this
   tier, never straight from a raw source), an **intermediate** tier where joins, filters and business
   logic actually happen (organised by business domain, not by source system), and a **mart** tier of
   the final fact/dimension tables a dashboard or an analyst actually queries. A business rule
   duplicated across several marts, or a mart joining straight to a raw source table, are both signs a
   tier boundary is being skipped rather than that the modeling is "too heavy" for the need.
4. **The tiers exist so that a source change costs one file.** A renamed column in a source system is
   absorbed by its staging model and invisible above it; the same rename reaching marts directly is a
   search-and-replace across every mart that referenced it, and the ones that are missed keep working
   until the next run. That is the whole argument for the layering, and it is the argument to make when
   the layering is called overhead.
5. **A consolidation has to carry which instance each row came from.** Dropping the source column
   because the union made the schemas identical destroys the one fact that makes a wrong figure
   diagnosable, and it is exactly the fact §1.2 says an identifier does not carry on its own. Keep it
   as a real column, not as a comment.
6. **A union across instances requires the same field to mean the same thing in each.** Identical
   schemas do not guarantee identical conventions: a status code, a currency, a unit or a category can
   be populated differently per instance because each was configured by different people. Check the
   distinct values per instance before uniting on a field, or the consolidated total is a sum of
   different questions.
7. **Say what the consolidation costs to keep, in the same sentence as the recommendation.** The
   maintenance is not abstract: one edit per new entity, in a place nobody is reminded of, by whoever
   remembers. Naming the owner and the trigger is what turns a stopgap into a stopgap someone can
   actually maintain; leaving both unnamed is what turns it into permanent architecture by default.
8. **A consolidated figure needs a completeness statement, not just a value.** How many instances were
   reached, how many were expected, and what happened to the ones that failed. A union where one
   instance was unreachable can return successfully with that entity's rows silently missing, and
   without the count there is nothing in the output that differs from a genuine drop in the business.
9. **A consolidation is not a place for business logic.** Filters and derivations applied inside the
   union get applied N times, drift between branches as they are edited, and cannot be tested in one
   place — which is the same argument as the tier boundary in point 3, arriving one layer earlier. The
   union's job is to stack rows and label their origin.
10. **Never propose a consolidation without saying what it replaces.** A new consolidated layer beside
    the existing hand-maintained views is two answers to the same question, which is §5.3's problem
    rather than a migration. Either the old path is retired on a stated date or the new one is
    explicitly a parallel run with an end.
