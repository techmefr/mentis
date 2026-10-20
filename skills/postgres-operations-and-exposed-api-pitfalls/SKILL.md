---
name: postgres-operations-and-exposed-api-pitfalls
description: "Use when running or diagnosing a PostgreSQL database in production, or exposing one through an auto-generated API: stale statistics, autovacuum and bloat, finding the costly queries, connection and memory budget, idle and statement timeouts, partitioning to drop old data, and access control through grants, row-level security and JWT claims on a Supabase-style data API."
---

# postgres-operations-and-exposed-api-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for what happens to a PostgreSQL database after the schema is right. The
premise: **the database keeps accepting statements while it degrades**: plans worsen as statistics age, dead rows
pile up behind an open transaction, connections eat memory, and an API generated from the schema serves every
table the roles can reach. Types, keys, indexes, locking, DDL that locks and the basics of row-level security are
in `sql-conventions`; migration tooling is in `devops-conventions`; this block starts where those end.

## When
- A query got slow without a code change, or a table grew far beyond its live data.
- A connection limit, an out-of-memory event or an idle-in-transaction session is reported.
- A table is exposed through an auto-generated REST or GraphQL layer, or authorization reads token claims.
- A team asks whether to partition a table.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Statistics, autovacuum and bloat, finding costly queries, partitioning | performance drifted, tables bloat, a table is called too big | [`01-maintenance-and-diagnosis.md`](./references/01-maintenance-and-diagnosis.md) |
| 2 | Connection and memory budget, pooler role, timeouts | connections run out, sessions hang, the server runs out of memory | [`02-connections-and-timeouts.md`](./references/02-connections-and-timeouts.md) |
| 3 | Grants against row-level security, claims, anonymous users, storage policies | a table is reachable through a generated API, or a policy reads a token | [`03-exposed-data-api.md`](./references/03-exposed-data-api.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: the diagnosis names the number that
proves it (dead rows, estimated against actual rows, connections by state), no setting was changed before that
number, and every table in an exposed schema has row-level security and a policy that names an owner.

## Guardrails
- Diagnose with the statistics views and the plan before changing a setting (§1.1, §1.3). Never tune from a guess.
- Never raise the connection limit to cure exhaustion; shrink demand with a pooler first (§2.1).
- Never use a claim the user can edit to authorize (§3.4).
- Never add a privileged function to get past a permission error (`skills/sql-conventions` §6.6).
- Vendor figures (percentages, sizes, thresholds) are not recited; measure instead (🟡, nothing here was run on a server).

## Origin
Rewritten from Supabase's `agent-skills` repository (MIT, commit c9be0e9), read 2026-10-20, checked against the
PostgreSQL manual where the manual states the fact. Version-bound facts and own guidance are listed in
[`references/origin.md`](./references/origin.md).
