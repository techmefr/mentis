# spreadsheet-data-cleaning-pitfalls §3 — Duplicates, keys and joins

Removing duplicates and looking things up are the two operations that change a table the most and are checked the
least. Both depend on a key, and most trouble is a key that is not what it was assumed to be.

## 3.1 Choose the key first
1. **Write what makes a row unique**: one column or a combination, and why. Symptom: "remove duplicates" on one
   column deletes two real customers who share a name, or keeps both rows of one customer who typed it twice.
2. **Test the key before using it**: count rows against distinct keys. If they differ, list the repeated keys and
   look at them.
3. **Exact duplicates and near-duplicates are two problems.** Exact ones can be removed by rule; near ones
   (spelling, spacing, case, a missing field) need a reviewed mapping (§3.3).
4. **Keep the removed rows** in a separate sheet or file with the reason, not only the survivors. Symptom: a
   count that no longer matches the source and no way to explain it.

## 3.2 Which row survives
1. **Decide the survivor by a rule** (most recent, most complete, the system of record), not by sort order. Sorting
   before removing decides which row stays, silently.
2. **Merge fields when two rows each hold something the other lacks**; do not drop the richer data by keeping the
   first row.
3. **Do not sort part of a table.** Sorting one column or a selection that excludes others detaches values from
   their rows. Check: sort with all columns selected, and keep a row number column that never changes.

## 3.3 Near-duplicates and mappings
1. **Build a mapping table** (variant, standard value) and apply it with a formula or a join, so the change is
   visible and reversible.
2. **Sort or filter by the normalised value** to find clusters, then decide each cluster; do not auto-merge on a
   similarity score without reading the cases.
3. **Blank is not a value.** Rows with an empty key match each other in some tools and match nothing in others.
   Check how blanks are treated and handle them before the join.

## 3.4 Lookups and joins
1. **Check the row count after a join.** More rows than before means the lookup table had repeated keys (rows
   multiplied); fewer, or errors, means keys that did not match. Both are findings.
2. **Test a row that should not match** and a row that should, and read the result. A lookup in approximate-match
   mode returns a plausible wrong value for a missing key.
3. **Match on the same type and form on both sides**: a text key against a number key, trailing spaces and case
   all produce silent misses (§1, §2.4).
4. **List the unmatched keys** on both sides, not only the matched count, and say what was done with each group.
5. **Do not enrich from a source you cannot cite.** Record where lookup data came from and when (§4.3).
