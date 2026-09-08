# § 1 — Map the landscape before querying it

> Section 1 of `business/data-analytics`. Read it before the first query of any task that touches
> reporting, a dashboard, a KPI, an extraction or a consolidation.

1. **Name every system of record involved** and how they relate: is there one authoritative database
   per business entity/tenant (common after an acquisition-heavy growth strategy, a franchise model, or
   any multi-subsidiary structure), one shared operational database (a CRM, an ERP) common to everyone,
   or both? Each shape has different failure modes — don't assume the "one big warehouse" model without
   checking. The cost of skipping this is not a failed query, it is a query that succeeds: it returns
   the subset of reality the one system it reached happens to hold, and nothing in the result says which
   subset that was.
2. **Never assume an identifier is universal** across independent instances of the same schema. When
   the same database schema is deployed once per entity/tenant (same table names, same column names,
   *different* underlying data), the same code or ID in two instances can mean two different real-world
   things. Trace which instance a value came from before joining or comparing it across instances — the
   schema being identical is exactly what makes this trap easy to fall into. What the reader sees when
   this goes wrong is a plausible total: the join matched, the rows came back, and two unrelated
   entities were summed under one name.
3. **Look for a central crosswalk/reference table** before hand-rolling entity matching across systems.
   A landscape with several systems of record for the same business entities usually has (or needs) one
   pivot table mapping each entity to its identifier in every system — the CRM's ID, the per-tenant
   database's name, the reporting layer's key. That table, not a fuzzy name match, is the source of
   truth for "which record in system A corresponds to which record in system B."
4. **Distinguish the systems of record from the restitution/reporting layer.** A layer built purely of
   views over other systems (no data stored locally) is a convenience, not a mandatory hop — dashboards
   and queries can usually reach the underlying systems directly when the reporting layer's shape
   doesn't fit the need. Don't treat "go through the reporting layer" as a hard rule unless the company
   says it is.
5. **A name match is not an identity match, and it fails in the direction nobody checks.** Matching
   entities by label produces both false positives (two real entities sharing a name) and false
   negatives (one entity spelled two ways, or renamed since), and only the second is visible as a
   missing row. The first arrives as a merged total that looks like good news. Where no crosswalk exists,
   say that the matching is heuristic and quantify it — how many rows matched, how many did not — rather
   than shipping the number alone.
6. **Ask which system wins when two disagree, and record the answer.** In a landscape with more than one
   system of record for the same fact, the same field will disagree; that is not a defect to be fixed in
   the query, it is a governance question with an owner. Answering it silently — picking whichever source
   was easier to reach — produces a number that contradicts somebody's existing report, and the
   discussion that follows is about whose number is right rather than about the decision the number was
   for.
7. **Establish which population each source actually contains** before comparing counts. An operational
   system usually holds only active records, a per-entity database holds that entity's history, and a
   reporting layer often holds a filtered view of both. Two sources counted without that check produce a
   difference that reads as data loss and is really two different questions being answered.
8. **Find out how fresh each source is, and state it with the result.** A landscape assembled from
   several systems has several refresh cadences, so "today's figure" is a mix of ages, and any comparison
   across sources is a comparison across moments. The visible failure is a rate whose numerator and
   denominator come from different days, which moves for reasons nobody can trace.
9. **Know what your access lets you see, because a permission filter is invisible in a result set.** A
   query run under an account scoped to a subset of rows returns a smaller, entirely valid-looking
   answer with no marker distinguishing it from the whole. Confirm whether the credentials used are
   scoped, and say so alongside the figure — this is the one landscape fact that cannot be discovered by
   reading the schema.
10. **Read-only access is the default and the request.** Reporting work needs no write path, and asking
    for one is asking to be trusted with a risk the task does not require (§4.1). Where the only
    credentials available are privileged, say so as a finding rather than treating it as convenience.
