# mongodb-conventions: origin and source stamps

> Provenance of `skills/mongodb-conventions`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No MongoDB server was used while
writing it. A new engine block with no same-topic block. Overlaps with `skills/sql-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MongoDB manual, rendered pages: ESR guideline, compound index and sort-with-indexes pages, query optimization (covered queries), collation | Licence of the rendered pages not re-read in this pass (the earlier review recorded the documentation repository as share-alike non-commercial, so nothing is taken from it beyond facts): facts only, nothing copied | ESR and ERS, `$in` under 201 elements, sort prefix and in-memory sort, covered-query conditions and `_id: 0`, collation match, collation-unsupported index types |
| MongoDB manual: limits and thresholds, avoid unbounded arrays, embedding versus references best practices, schema versioning | Same: facts only | 16 MiB document limit, GridFS pointer, embed and reference criteria, versioning pattern and its index cost |
| MongoDB manual: schema validation (level, action, JSON schema), `aggregate` command, aggregation pipeline optimization, `$lookup` | Same: facts only | Validation levels and actions with defaults, `constraint` level new in 9.0, 100 MB spill and `allowDiskUse`, `$project` placement and `$match` movement, `$lookup` index and `$expr` limits |
| mongodb/agent-skills, query optimizer skill, reference `core-indexing-principles` (LICENSE re-read, Apache-2.0), commit `18b014e` of 2026-10-02 | Apache-2.0 | Compound index first-key guideline (only this one statement is used) |

## Re-read 2026-10-20 (verification pass)
The MongoDB manual's documentation repository is recorded above as share-alike non-commercial; under the rule
for this pass such a source is not opened, so **no manual page was re-read** and every point that rests only on a
manual page keeps its 2026-10-08 reading, unverified by this pass: the 16 MiB limit, the embed and reference
criteria, the validation level and action definitions and defaults, `constraint` and `errorAndLog`, the
`$in` limit as the manual words it, the multikey sort stage, collation limits for text and 2d indexes, the
`$lookup` `$expr` limits, `$match` movement, the 100 MB and 6.0 `allowDiskUseByDefault` statements and the
usedDisk indicator.

What was done instead: the Apache-2.0 MongoDB agent skills repository (LICENSE file re-read, unmodified
licence text, no copyright holder filled in; files at the main branch on 2026-10-20: the indexing principles,
aggregation optimisation, schema validation, schema versioning, unnecessary indexes and excessive lookups
references, and the schema design skill) was read in full for those topics. It confirms: first key of a
compound index in the filter or sort; ESR, ERS and the 200-element `$in` rule; the exact-pattern need for
mixed-direction sorts (a point an earlier pass had removed as unsourced, now sourced and added at 2.2.1);
covered-query conditions and `_id: 0`; the four-step validation rollout (1.3.3, no longer own guidance);
schema versioning with lazy migration (1.4.1); unbounded arrays and the 16 MB hard limit with `$bsonSize`
monitoring; the `$lookup` foreign-field index; late `$project` and the memory limit of 100 MB per blocking stage.
Corrections: the agent skills' claim that an early `$project` can stop the optimizer from pruning fields is
not adopted (the earlier pass found the manual saying the opposite; the block keeps the weaker, agreed point
that an early `$project` to shrink documents does not help). The skills say `allowDiskUse` defaults to true; the
block keeps the manual's more precise 6.0 wording, unverified by this pass. Added: 1.2.3 monitoring, 2.2 mixed
directions, 2.3.3 and 2.3.4, 3.2.3 (limit after sort). Still unsourced: indexes across schema versions (1.4.2),
the validator-per-collection rule beyond the rollout, array bounds in code (own guidance), the multi-document
limits and everything the manual alone supports.
## Removed in the verification pass (no page supporting them)
"`$project` late defeats the optimizer" (the earlier review's claim): the pipeline optimization page says the
opposite, that an early `$project` is unlikely to help and `$project` should typically be last, so the rule was
reversed and reworded. "Mixed sort directions need an exact-match index" (not read on a manual page). "`allowDiskUse`
defaults to true from 6.0" reworded: the pages say stages over 100 MB write temporary files by default, with
`allowDiskUseByDefault` and per-command `allowDiskUse` as overrides. Other references of the MongoDB agent
skills (schema design patterns, anti-patterns, aggregation optimisation, update examples) were not read and are
not used.

## Not verified
1. **Own guidance, flagged as such in the text:** state array bounds in code and test past them (the
   warn-then-error rollout and the index-only-for-queries-that-run rule are now sourced to the Apache-2.0
   agent skills, 2026-10-20).
2. **The first key of an index should appear in the filter or sort:** from the agent skills only (now re-read
   in full); no manual page was checked, by rule.
3. **Server versions:** the manual pages are the current ones; only the 6.0 spill default and the 9.0
   `constraint` level are stated with versions, and behaviour on older servers was not checked.
4. **Multikey covered queries, sharding, transactions and time-series collections** are not covered.

## Related blocks
`sql-server-tsql-types-and-queries`, `mysql-pitfalls`, `jpa-hibernate-pitfalls`, `prisma-ops-and-test-hygiene`, `security-hardening`.
