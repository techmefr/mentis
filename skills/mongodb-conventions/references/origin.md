# mongodb-conventions: origin and source stamps

> Provenance of `skills/mongodb-conventions`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No MongoDB server was used while
writing it. This is a new engine block with no same-topic block on main; it is meant to sit beside the general
SQL conventions block (`sql-conventions`, on the unmerged branch `feat/antislop-lot`, PR 118) and be linked
from it when PR 118 lands.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MongoDB manual, rendered pages: ESR guideline, compound index and sort-with-indexes pages, query optimization (covered queries), collation | Licence of the rendered pages not re-read in this pass (the earlier review recorded the documentation repository as share-alike non-commercial, so nothing is taken from it beyond facts): facts only, nothing copied | ESR and ERS, `$in` under 201 elements, sort prefix and in-memory sort, covered-query conditions and `_id: 0`, collation match, collation-unsupported index types |
| MongoDB manual: limits and thresholds, avoid unbounded arrays, embedding versus references best practices, schema versioning | Same: facts only | 16 MiB document limit, GridFS pointer, embed and reference criteria, versioning pattern and its index cost |
| MongoDB manual: schema validation (level, action, JSON schema), `aggregate` command, aggregation pipeline optimization, `$lookup` | Same: facts only | Validation levels and actions with defaults, `constraint` level new in 9.0, 100 MB spill and `allowDiskUse`, `$project` placement and `$match` movement, `$lookup` index and `$expr` limits |
| mongodb/agent-skills, query optimizer skill, reference `core-indexing-principles` (LICENSE re-read, Apache-2.0), commit `18b014e` of 2026-10-02 | Apache-2.0 | Compound index first-key guideline (only this one statement is used) |

## Removed in the verification pass (no page supporting them)
"`$project` late defeats the optimizer" (the earlier review's claim): the pipeline optimization page says the
opposite, that an early `$project` is unlikely to help and `$project` should typically be last, so the rule was
reversed and reworded. "Mixed sort directions need an exact-match index" (not read on a manual page). "`allowDiskUse`
defaults to true from 6.0" reworded: the pages say stages over 100 MB write temporary files by default, with
`allowDiskUseByDefault` and per-command `allowDiskUse` as overrides. Other references of the MongoDB agent
skills (schema design patterns, anti-patterns, aggregation optimisation, update examples) were not read and are
not used.

## Not verified
1. **Own guidance, flagged as such in the text:** introduce a validator as `warn` with `moderate` then move to
   `error`, state array bounds in code and test past them, index only for queries that run.
2. **The first key of an index should appear in the filter or sort:** from the agent skills only, not checked on
   a manual page.
3. **Server versions:** the manual pages are the current ones; only the 6.0 spill default and the 9.0
   `constraint` level are stated with versions, and behaviour on older servers was not checked.
4. **Multikey covered queries, sharding, transactions and time-series collections** are not covered.

## Related blocks
`sql-server-tsql-types-and-queries`, `mysql-pitfalls`, `jpa-hibernate-pitfalls`, `prisma-ops-and-test-hygiene`, `security-hardening`.
