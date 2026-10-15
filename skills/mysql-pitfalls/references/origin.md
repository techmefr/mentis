# mysql-pitfalls: origin and source stamps

> Provenance of `skills/mysql-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No MySQL server was used while
writing it. This block is meant to be folded into section 7 (engine notes) of `sql-conventions` and into the
safe-migrations reference of `devops-conventions`, both on the unmerged branch `feat/antislop-lot` (PR 118),
when PR 118 lands; until then it stands alone.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MySQL 8.4 Reference Manual: The JSON data type, `CREATE INDEX` (prefixes, functional key parts, multi-valued indexes), InnoDB limits, `utf8mb4`, case sensitivity in string searches, generated columns | Licence of the manual not re-read in this pass: facts only, nothing copied | `->` and `->>`, JSON comparison limits and casts, indexing JSON, key length limits, 4 bytes per character, default collation, functional-index collation trap |
| MySQL 8.4 Reference Manual: partitioning keys and unique keys, partitioning limitations (foreign keys), RANGE partitioning, partition management, partitioning overview | Same: facts only | Unique-key rule, no foreign keys, `DROP PARTITION` semantics, `MAXVALUE`, retention by dropping |
| MySQL 8.4 Reference Manual: `SHOW REPLICA STATUS`, GTID functions, system variables (`max_execution_time`, `lock_wait_timeout`, `wait_timeout`), InnoDB parameters (`innodb_lock_wait_timeout`), InnoDB locks set, deadlocks, metadata locking | Same: facts only | Lag field limits, `WAIT_FOR_EXECUTED_GTID_SET` and its default timeout, timeout scopes and defaults, upsert locks, metadata lock duration |
| MySQL 8.4 Reference Manual: `ALTER TABLE` (algorithm selection), InnoDB online DDL operations | Same: facts only | Algorithm fallback and error rule, `VARCHAR` length-byte boundary, stored generated column and auto-increment cost, foreign key and `foreign_key_checks`, instant row-version budget |
| github/gh-ost documentation (`requirements-and-limitations`, `throttle`, `testing-on-replica`, `cut-over`), commit `dd44453` of 2026-10-06 (LICENSE re-read, MIT) | MIT, read 2026-10-08 | Prerequisites, throttling, rehearsal, cut-over options, exclusions |
| strong_migrations README, commit `23d8e1f` of 2026-09-26 (LICENSE.txt re-read, MIT) | MIT, read 2026-10-08 | Expression-default rewrite, stored generated column and type-change rewrites in MySQL, foreign key without validation behind a pooler |

## Removed in the verification pass (no page supporting them)
"JSON documents over about 8 KB spill off-page" (no page). "`wait_timeout` does not close an idle open
transaction" (the page says only that it closes noninteractive connections after the idle period). "One huge
transaction creates a lag spike, so batch" and "deploys that restart all instances cause a connection storm"
(no page read). "Case and accent insensitive collations make unique constraints insensitive" (the page
confirms case-insensitive comparison by default but not the behaviour of unique indexes). "Multi-valued indexes
need 8.0.17" (the 8.4 page read gives no version). "Gap locks" for upsert deadlocks, corrected to the exclusive
next-key lock the page states. The PlanetScale database skills named in the earlier review were not read in
this pass and are not a source.

## Not verified
1. **Own guidance, flagged as such in the text:** a shorter column or helper column instead of a long key,
   restructuring the primary key as `(id, partition_column)` and its consequence for `id` uniqueness.
2. **MySQL 8.0 and 9.x differences:** only the 8.4 manual was read; the online DDL table is stated for 8.4, with
   the row-version limit change at 9.1.0 quoted from the same page.
3. **Default row format:** the manual page gives the key limits per row format but the page read does not state
   which format is the default; the reader confirms the format of the table before applying the 3,072-byte
   limit in `references/01-json-collation-keys.md`.
4. **Multi-valued index and generated-column index behaviour in the optimiser** was not checked with `EXPLAIN`.
5. **gh-ost documentation** states a minimum of MySQL 5.7 and is not versioned against MySQL 8.4 specifics.
6. **MariaDB** is not covered.

## Related blocks
`devops-conventions`, `prisma-ops-and-test-hygiene` §1.4, `jpa-hibernate-pitfalls`, `security-hardening`.
