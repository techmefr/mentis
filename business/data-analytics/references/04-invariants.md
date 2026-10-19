# § 4 — Data-handling invariants

> Section 4 of `business/data-analytics`. These hold regardless of which system is being queried; read
> them on any task that reads real data. Point 3 is the traceability rule the rest of the block and
> `agents/oracle` cite.

These hold regardless of which system is being queried:

1. **Never modify source data to answer a reporting question.** Reporting is read-only by construction;
   if a fix looks like it requires writing to a system of record, that's a different task with a
   different owner. The reason it needs stating is that the write always looks small — one corrected
   code, one backfilled null — and a write into an operational system has consequences the reporting
   task cannot see: triggers, downstream syncs, and an audit trail that now records a change nobody
   asked for.
2. **Never assume a missing value** — a null, an absent row, an unpopulated field. State that it's
   missing and what that means for the result, rather than substituting a default that makes the number
   look complete. Substituting zero is the common one and it is the worst, because zero is a legitimate
   value: the reader has no way to distinguish "none" from "not recorded", and the average computed over
   both is wrong in a direction nobody can estimate.
3. **Every result must be traceable to its source**: which system, which table, which logic produced
   it. A number nobody can explain a week later is a liability, not an insight — this is what makes the
   usage-guide documentation (§2) worth maintaining in the first place.
4. **A number without its filters is not traceable.** The date range, the entity scope, the excluded
   statuses and the deduplication rule are part of the answer, not context around it — two figures
   differing only by an unstated filter are the most common source of a disagreement that looks like a
   data-quality problem. State them next to the value, where they cannot be separated from it.
5. **Keep the query, not just the number.** The logic is the only complete record of what was asked, and
   a figure quoted in a message with the query left in a scratch buffer cannot be re-run when it is
   questioned. Re-deriving it from memory a week later reliably produces a slightly different number,
   which is worse than having none.
6. **Say the population, not only the count.** "1,200" answers nothing; "1,200 of the 4,000 records
   created in the period, excluding the two entities whose instance was unreachable" is a number that
   can be checked and that shows its own gaps. This is the same completeness statement §3.8 requires of
   a consolidation, applied to any figure.
7. **Never present a rate whose parts come from different sources without saying so.** A numerator from
   one system and a denominator from another is a comparison across two populations, two refresh
   cadences and two definitions, and the resulting percentage moves for reasons neither source explains.
   Where it cannot be avoided, the ratio is reported with both origins attached.
8. **A sample is not a result, and rounding is not precision.** A figure derived from a limited extract,
   a `TOP`/`LIMIT`ed query or a partially loaded table carries the extract's shape, not the
   population's; and a number presented to more digits than its source supports invites a comparison it
   cannot survive. Both are stated rather than smoothed over.
9. **Reporting inherits the data-protection rules of what it reads.** An extract is a copy: it leaves the
   access controls of its source behind and lands somewhere with different retention and a different
   audience, which is what makes personal data in a spreadsheet a different exposure from the same rows
   in the database. Take the columns the question needs and no more, and route any question about lawful
   basis, retention or access to the owner rather than answering it (`business/data-protection`).
10. **Never guess at a governance, retention or access-control policy.** These are decisions someone
    owns, they are not derivable from the schema, and a plausible answer is indistinguishable from the
    real one until it is wrong. Ask the team that owns the landscape, and record the answer where the
    next query will find it (§2.9).
11. **Count the outcome you want, and keep non-events out of the denominator.** A metric of attention
    (replies, clicks, opens, sign-ups) says people noticed; a metric of the outcome (interested replies,
    purchases, activated accounts) says they wanted it, and two campaigns can rank in opposite orders on
    the two. Pick the outcome as the numerator and say which classes of event count as it. Then decide
    what is not a real trial and remove it from the base: automatic replies and bounces are not people
    responding, and leaving them in lowers a rate for reasons unrelated to the thing measured. Write the
    inclusions and exclusions next to the figure (point 4), and give a rate on a small base as a count
    with a caveat rather than as a percentage that invites a winner to be declared.
