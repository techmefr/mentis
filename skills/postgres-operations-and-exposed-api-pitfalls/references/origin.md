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

| PostgreSQL manual (current), re-read 2026-10-20: autovacuum settings, resource consumption (work_mem), row security, CREATE POLICY, CREATE FUNCTION | PostgreSQL licence (permissive), facts only | Autovacuum defaults and per-table override, per-operation memory rule, default deny, check defaulting to the filter, per-command policy table, public execute default, search path of privileged functions |
| Vendor product documentation (row-level security, securing the API, storage access control guides), read 2026-10-20 | product documentation, facts only, rewritten, no text copied | Exposed-schema rule, default grants and the exposure setting, anonymous users on the signed-in role, editable and server-controlled metadata, stale claims, view invoker option, upsert policy trio, public execute default and its removal |

The PostgreSQL manual facts already stamped in `skills/sql-conventions` were reused by pointer, not re-read for
this block.

## Removed (stated in the sources, not carried)
- Everything already in `sql-conventions` (types, keys, index kinds, covering and partial indexes, upsert, keyset pagination, bulk insert, skip-locked queues, advisory locks, deadlock ordering): pointed to, not repeated.
- Full-text search, JSONB indexing and the extension-specific skill content (vectors, queues, scheduled jobs): other subjects.
- Every percentage or multiple the files give as a benefit, the pool-size formula, the connection-memory estimate and the partitioning size threshold: not recited.
- The Supabase command-line, MCP and documentation-access sections: tooling of one vendor.
- All SQL code samples (rewritten as prose).

## Not verified
1. **Defaults.** Timeout defaults confirmed (all disabled). Autovacuum defaults and the per-operation memory rule now confirmed against the manual (2026-10-20). The per-connection memory size of a server process was not checked.
2. **Platform-specific behaviour.** Confirmed on the vendor's product pages 2026-10-20 (not tested): the exposure setting and default grants, anonymous users on the signed-in role, editable metadata unsafe, stale claims, the view invoker option, the upsert policy trio. Still only the agent-skills statement: the in-expression role test deprecation, token validity after user deletion, and the speed-up from wrapping the identity function (page says only that the result is cached per statement).
3. **Confirmed against the manual 2026-10-20 (one refinement: plain vacuum can truncate trailing empty pages):** plain vacuum not shrinking the file and the partition key in unique constraints (§1).
4. **Corrected 2026-10-20:** the earlier claim that an update policy with only a filter lets a user reassign a row is wrong, the manual reuses the filter as the check; the select-policy rule was refined to the cases where the statement reads columns.
5. **Own guidance, labelled in the text:** the oldest-open-transaction-first order (§1), one change per plan (§1), coherence of pooler and server timeouts (§2), and every "Checks" section.

## Related blocks
`sql-conventions` (types, locking, DDL that locks, row-level security basics), `devops-conventions` (safe
migrations), `laravel-mysql-to-postgres-pitfalls`, `queue-worker-runtime-pitfalls`, `source-freshness`.
