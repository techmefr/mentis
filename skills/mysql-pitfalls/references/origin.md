# mysql-pitfalls: origin and source stamps

> Provenance of `skills/mysql-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 21 checked, 20 matched, 0 corrected, 1 unverified

**Status: 🟡.** Written from documentation and reading, never run by us. No MySQL server was used while
writing it. Overlaps with `skills/sql-conventions` §7 and `skills/devops-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MySQL 8.4 Reference Manual: The JSON data type, `CREATE INDEX` (prefixes, functional key parts, multi-valued indexes), InnoDB limits, `utf8mb4`, case sensitivity in string searches, generated columns | Licence of the manual not re-read in this pass: facts only, nothing copied | `->` and `->>`, JSON comparison limits and casts, indexing JSON, key length limits, 4 bytes per character, default collation, functional-index collation trap |
| MySQL 8.4 Reference Manual: partitioning keys and unique keys, partitioning limitations (foreign keys), RANGE partitioning, partition management, partitioning overview | Same: facts only | Unique-key rule, no foreign keys, `DROP PARTITION` semantics, `MAXVALUE`, retention by dropping |
| MySQL 8.4 Reference Manual: `SHOW REPLICA STATUS`, GTID functions, system variables (`max_execution_time`, `lock_wait_timeout`, `wait_timeout`), InnoDB parameters (`innodb_lock_wait_timeout`), InnoDB locks set, deadlocks, metadata locking | Same: facts only | Lag field limits, `WAIT_FOR_EXECUTED_GTID_SET` and its default timeout, timeout scopes and defaults, upsert locks, metadata lock duration |
| MySQL 8.4 Reference Manual: `ALTER TABLE` (algorithm selection), InnoDB online DDL operations | Same: facts only | Algorithm fallback and error rule, `VARCHAR` length-byte boundary, stored generated column and auto-increment cost, foreign key and `foreign_key_checks`, instant row-version budget |
| github/gh-ost documentation (`requirements-and-limitations`, `throttle`, `testing-on-replica`, `cut-over`), commit `dd44453` of 2026-10-06 (LICENSE re-read, MIT) | MIT, read 2026-10-08 | Prerequisites, throttling, rehearsal, cut-over options, exclusions |
| strong_migrations README, commit `23d8e1f` of 2026-09-26 (LICENSE.txt re-read, MIT) | MIT, read 2026-10-08 | Expression-default rewrite, stored generated column and type-change rewrites in MySQL, foreign key without validation behind a pooler |

Re-read 2026-10-20 (MySQL 8.4 manual pages, facts only, nothing copied, manual licence still not read): InnoDB row formats, `CREATE INDEX` (multi-valued, functional, prefixes), online DDL operations table, partitioning keys and storage-engine limits, the JSON type. Confirmed: default row format `DYNAMIC` and the 3,072 and 767 byte limits, the unique-key rule, no foreign keys with partitioning, the online DDL table, the `->` and `->>` and collation facts. Added: §1.1 points 7 to 9. The multi-valued index page gives no version, so none is claimed.

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
3. **Default row format:** confirmed `DYNAMIC` on 2026-10-20 (the page gives no introduction version); the reader still confirms the format of the table before applying the 3,072-byte limit.
4. **Multi-valued index and generated-column index behaviour in the optimiser** was not checked with `EXPLAIN`.
5. **gh-ost documentation** states a minimum of MySQL 5.7 and is not versioned against MySQL 8.4 specifics.
6. **MariaDB** is not covered.

## Related blocks
`devops-conventions`, `prisma-ops-and-test-hygiene` §1.4, `jpa-hibernate-pitfalls`, `security-hardening`.
