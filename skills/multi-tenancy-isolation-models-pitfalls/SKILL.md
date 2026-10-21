---
name: multi-tenancy-isolation-models-pitfalls
description: "Use when one deployment serves several customers (tenants) and the question is how their data and load are kept apart, in any stack: choosing row, schema, database or deployment isolation per customer tier, carrying the tenant through requests, jobs, caches, search indexes, files and logs, using database row-level security as a safety net, composite keys and unique constraints, noisy neighbours and per-tenant limits, per-tenant migrations, backup and restore, data residency, and tenant offboarding and deletion."
---

# multi-tenancy-isolation-models-pitfalls

A defensive block for the framework-independent half of multi-tenancy: **which isolation model, where the tenant
identifier travels, and what happens at the two ends of a tenant's life**. Premise: **a tenant leak is almost
never a database feature failing; it is one code path (a job, a cache key, an export, an admin query) that
forgot the tenant**. The Laravel database-per-tenant specifics are `skills/laravel-tenant-context-by-default`
and `skills/laravel-tenant-replica`; the decision about who may do what inside a tenant is
`skills/authorization-models-and-entitlements-pitfalls` and `skills/field-and-row-permission-ui-api-pitfalls`;
row-level security mechanics and grants are `skills/sql-conventions` §6 and
`skills/postgres-operations-and-exposed-api-pitfalls`; personal data duties in general are
`business/data-protection`; load testing a shared system is `skills/load-and-capacity-testing-pitfalls`. The
mirror question on the agent side, which tenant a connected drive, mailbox or CRM is signed into before it is
read, is `skills/agent-data-gap-honesty-pitfalls` §3 (not an app design question, so it was not added here).

## When
- A product moves from one customer to many, or a sales promise ("dedicated data", "EU only") must be honoured.
- A data leak between customers is reported, or a review asks "how do we know tenant A cannot read tenant B".
- A tenant is slow because of another, or one customer needs a restore, an export or deletion.
- A migration, a job or a report must run across all tenants.

## Steps

**Read only the section the task meets.** §1 is the entry point for a design; §2 for a leak report.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Isolation models and how to choose: row, schema, database, deployment, mixed tiers | a model is chosen, mixed or changed | [`01-isolation-models.md`](./references/01-isolation-models.md) |
| 2 | Keeping the tenant on every path: context, keys, constraints, row-level security as a net, jobs, caches, search, files, logs, tests | a feature touches tenant data, or a leak is suspected | [`02-enforcement-paths.md`](./references/02-enforcement-paths.md) |
| 3 | Life of a tenant: onboarding, noisy neighbours, migrations at scale, backup, residency, offboarding | tenants are created, throttled, moved, restored or deleted | [`03-tenant-lifecycle.md`](./references/03-tenant-lifecycle.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed design owes: the model per tier and the reason (§1), a table of every path that
reads or writes tenant data and how each gets the tenant (§2), a two-tenant test that tries to cross the boundary
(§2), per-tenant limits and the escalation when one is hit (§3), and the runbooks for restore, move and deletion
(§3).

## Guardrails
- Choose the model from the tenants' isolation, size and compliance needs. Never copy a competitor's model, and
  never let the first implementation silently decide it (§1).
- Resolve the tenant once at the edge from a trusted source and carry it as one value. Never read it from a
  field the caller can edit (§2).
- Make a query without a tenant fail instead of returning everything. Never rely on developers remembering a
  filter (§2).
- Treat database row-level security as the second lock. Never use it as the only control, and never run
  migrations or admin tools as a role that bypasses it without a reason on record (§2).
- Put the tenant in every cache key, index name, file path and log line. Never share a key space between
  tenants (§2).
- Give each tenant limits on the shared resources. Never let one tenant's batch job consume the pool (§3).
- Write the offboarding and deletion path before the first customer needs it (§3).
- This block is craft knowledge, with database facts marked "re-read before relying"; no source text was used
  and nothing was run (see [`references/origin.md`](./references/origin.md)).

## Origin
Written from general practice in multi-tenant software; no external source was read for this block. 🟡: never run
by us; open points are in [`references/origin.md`](./references/origin.md).
