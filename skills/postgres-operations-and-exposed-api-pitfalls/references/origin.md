# postgres-operations-and-exposed-api-pitfalls: origin and source stamps

> Provenance of `skills/postgres-operations-and-exposed-api-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us against a PostgreSQL server or a
Supabase project. No statement, setting or policy was executed while writing it.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: step to decide from a repository whether a data API is exposed (§3.0), applicability gate for managed or proxied databases, timeouts with a tiny pool, static timeout check.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| supabase/agent-skills at commit c9be0e9 (2026-10-02): `skills/supabase-postgres-best-practices/SKILL.md` and its `references/` rules `monitor-*`, `conn-*`, `lock-short-transactions`, `schema-partitioning`, `security-*` | MIT, Copyright (c) 2026 Supabase (`LICENSE` read 2026-10-20; frontmatter `license: MIT`) | Vacuum and statistics, statements view, plan reading, pool and timeout rules, partitioning, policy and privilege rules |
| supabase/agent-skills at c9be0e9: `skills/supabase/SKILL.md` (security checklist section) | MIT (same file) | Exposure of tables, policy shape, privileged functions, user-editable claims, token lifetime, storage upsert |
| PostgreSQL manual pages: routine vacuuming, table partitioning, pg_stat_statements, client connection defaults | product documentation, facts only, rewritten, read 2026-10-20 | Vacuum space reuse, partition key in unique constraints, no-partition insert error, extension loading and reset, timeout defaults |

The PostgreSQL manual facts already stamped in `skills/sql-conventions` were reused by pointer, not re-read for
this block.

## Removed (stated in the sources, not carried)
- Everything already in `sql-conventions` (types, keys, index kinds, covering and partial indexes, upsert, keyset pagination, bulk insert, skip-locked queues, advisory locks, deadlock ordering): pointed to, not repeated.
- Full-text search, JSONB indexing and the extension-specific skill content (vectors, queues, scheduled jobs): other subjects.
- Every percentage or multiple the files give as a benefit, the pool-size formula, the connection-memory estimate and the partitioning size threshold: not recited.
- The Supabase command-line, MCP and documentation-access sections: tooling of one vendor.
- All SQL code samples (rewritten as prose).

## Not verified
1. **Defaults.** Timeout defaults confirmed (all disabled). The autovacuum scale-factor values were not stated on the page read and the per-connection memory was not checked.
2. **Platform-specific behaviour.** The new-table exposure setting, the in-expression role test deprecation, anonymous users carrying the signed-in role, editable metadata appearing in the token, token validity after user deletion and the storage upsert policy requirement are the vendor's statements at the commit; none was tested.
3. **Confirmed against the manual 2026-10-20 (one refinement: plain vacuum can truncate trailing empty pages):** plain vacuum not shrinking the file and the partition key in unique constraints (§1).
4. **Own guidance, labelled in the text:** the oldest-open-transaction-first order (§1), one change per plan (§1), coherence of pooler and server timeouts (§2), and every "Checks" section.

## Related blocks
`sql-conventions` (types, locking, DDL that locks, row-level security basics), `devops-conventions` (safe
migrations), `laravel-mysql-to-postgres-pitfalls`, `queue-worker-runtime-pitfalls`, `source-freshness`.
