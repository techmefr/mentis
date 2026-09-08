# § 2 — Document tables as a usage guide, not a schema dump

> Section 2 of `business/data-analytics`. Read it when writing down what a table is for, or when
> deciding whether an existing note is usable. Point 4 is the data-quality vocabulary the rest of the
> block and `agents/oracle` name findings by.

1. **A full column-by-column schema reference and a "which table for which need" usage guide are two
   different documents** — keep them separate. The schema reference answers "what does column X mean";
   the usage guide answers "which table, on which system, for this business question," with the table's
   role in one sentence, its handful of BI-relevant key columns (not the full column list), and its
   common joins. Most day-to-day querying only needs the second one. Merging them produces a document
   long enough that nobody reads either half, and the half that gets skipped is the one that would have
   prevented the wrong table being used.
2. **State the join, not just the foreign key name**, for anything non-obvious: which column on which
   side, and what real-world relationship it encodes. A join list that only names columns forces every
   reader to re-derive the relationship each time. The specific thing a column name cannot tell you is
   cardinality, and getting that wrong is how a join silently multiplies rows and doubles a sum.
3. **Write down known weaknesses of the landscape once**, and don't rediscover them every conversation:
   which source has poor data quality, which consolidation is fragile and needs manual upkeep on every
   new entity, where there's no data catalogue or lineage. A landscape's weaknesses are usually already
   known to the team that lives with it — ask, then keep the list somewhere queries can reference it.
   Rediscovering one costs a whole analysis and, worse, teaches the next person that the documentation
   is not worth reading.
4. **Name a data-quality problem by its actual dimension** rather than a vague "the data is bad" —
   accuracy (wrong value), completeness (missing value), consistency (the same fact disagrees across
   systems), timeliness (right value, stale), uniqueness (the same entity duplicated), validity (a value
   outside its allowed domain). A source flagged simply as "unreliable" gives a query-writer nothing to
   act on; "this source is complete but frequently inconsistent with the ERP on this field" tells them
   exactly which check to add.
5. **The dimension chooses the check, which is why the vocabulary is worth the discipline.** A
   uniqueness problem is found by counting distinct keys against rows; a completeness problem by
   counting nulls per column; a consistency problem only by comparing two systems, which is a different
   query against different credentials; a timeliness problem by reading a load timestamp rather than the
   data at all. Named vaguely, every one of these gets the same non-check — a glance at a sample — which
   finds none of them.
6. **A usage guide records what a table is *not* for.** The trap in a real landscape is a table that
   answers the question approximately: the one holding only open records, the archive that stops at a
   cut-off date, the extract rebuilt nightly from a subset. Each is correct for its own purpose and
   wrong for the neighbouring one, and the exclusion is the sentence that stops the substitution.
7. **Write down the grain of every table you document** — one row per what. It is the single fact that
   determines whether a join fans out and whether a sum double-counts, and it is not visible in a column
   list. A table whose grain nobody stated is a table whose totals get argued about later, with both
   sides right about a different grain.
8. **Say which column is the one to filter dates on, when there is more than one.** Created, updated,
   effective, closed and loaded dates coexist in real tables and answer different questions; a report
   built on the wrong one moves whenever a record is touched, which looks like activity and is
   bookkeeping.
9. **A note nobody can find is a note that does not exist.** The guide lives where the query-writer
   already looks, not in a document that has to be remembered — otherwise every rule in this section is
   satisfied and none of it is used. This is also what makes §4.3's traceability affordable: a number
   traced to a table whose role is written down is explainable, and a number traced to a table nobody
   documented has only moved the question.
10. **Documenting is not the same as trusting.** A usage guide written from the schema plus a reading of
    the queries around it is a hypothesis; a guide confirmed by the team that owns the landscape is a
    fact. Mark which one each entry is, because the difference decides whether a surprising result means
    the query is wrong or the note is.
