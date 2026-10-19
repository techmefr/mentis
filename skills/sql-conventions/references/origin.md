# sql-conventions: origin and source stamps

> Provenance of `skills/sql-conventions`. Read it when tracing a rule to its source or checking freshness
> (`skills/source-freshness`), never to apply a rule.

Written 2026-10-02 from primary sources read that day. Status: **new block, base to confront with a real
project**, no in-house production experience (🟡 in `CATALOG.md`).

| Source | Licence | Treatment |
|---|---|---|
| PostgreSQL manual ("current" pages: data types, constraints, CREATE INDEX, ALTER TABLE, transaction isolation, explicit locking, SELECT locking clauses, EXPLAIN, PREPARE, client connection settings, GRANT, CREATE FUNCTION, CREATE VIEW, row security, libpq parameter passing, UUID functions) | PostgreSQL licence (permissive) | Facts checked against it; wording ours |
| PostgreSQL community "Don't Do This" wiki page | wiki, licence not stated on the page | Idea only: each rule was re-checked against the manual where the manual states it, wording ours |
| MySQL 8.4 reference manual (isolation levels, online DDL and metadata locks, foreign keys, date and time types, character sets, SQL modes, EXPLAIN) | vendor documentation, all rights reserved | Idea only, facts checked, wording ours |
| SQLite documentation (foreign keys, write-ahead logging, strict tables, datatypes, transactions, pragmas, busy handler) | public domain | Facts checked, wording ours |
| PgBouncer features page (what survives in each pooling mode) | ISC-style permissive project | Facts checked, wording ours |
| Timescale's public PostgreSQL design skill (`pg-aiguide`) | Apache-2.0 | Rewrite with credit: table-design defaults (identity, text, numeric, timestamptz, partial and covering indexes, unique with nulls, upsert-friendly design) |
| Supabase's published agent skills (Postgres best practices and the security checklist) | MIT | Rewrite with credit: row-security, view, privileged-function and policy-performance traps; pooling-mode warning |
| PlanetScale's published MySQL skill and references | MIT | Rewrite with credit: InnoDB key design, gap locks, deadlock retry, non-sargable predicates, index maintenance queries |
| OWASP SQL Injection Prevention Cheat Sheet | CC-BY-SA 4.0 | **Idea only**: no sentence or example reused |

**Checked and corrected against the manual.** The vendor skills state some rules as flat prohibitions the
manuals qualify (bounded text types are a legitimate choice; the legacy auto-increment type is needed before
PostgreSQL 10). The block follows the manual's qualification. Figures the vendors give as thresholds (a row
count at which to partition, a pool size formula, batch sizes, a speed-up multiple for a policy rewrite) are
not standards and none is recited.

**Not taken.** Time-series, geospatial and vector-search extensions (a different subject, and vendor-specific);
partitioning thresholds (measure instead); replication and sharding operations; the vendors' hosting
recommendations; the Vitess/sharded-MySQL skills.

**Version stamps.** PostgreSQL manual "current" pages as of 2026-10-02 (the `ALTER TABLE` not-null validation
and virtual generated columns reflect a newer major than the oldest supported one: confirm on the deployed
major). MySQL 8.4 manual. SQLite strict tables need 3.37.0. Time-ordered UUID generation needs PostgreSQL 18;
unique-nulls-not-distinct needs 15; security-invoker views need 15.

**Reasoning of ours, not a source statement:** §2 points 1, 6, 9; §3 points 9, 11, 12; §4 points 2, 4, 7 (first
half), 10; §5 points 7, 9; §6 point 10; SQLite point 6.
