# prisma-ops-and-test-hygiene §4 — Postgres row-level security behind Prisma

> Section 4 of `skills/prisma-ops-and-test-hygiene`. Read it when tenant isolation is enforced by Postgres
> row-level security (RLS) policies and the data access goes through Prisma. The isolation model itself
> (shared schema, schema per tenant, database per tenant) is chosen in
> `skills/multi-tenancy-isolation-models-pitfalls`; this section is how RLS holds once chosen.

RLS fails open in a way no query review shows: the policies are correct, and the application connects as a
role they do not apply to. Every rule below closes one of those doors, and the last one proves it.

## 4.1 Roles
1. **The application role is neither superuser nor `BYPASSRLS`, and does not own the tables.** Superusers
   and roles with `BYPASSRLS` skip every policy; the table owner skips them too unless the table is
   `FORCE ROW LEVEL SECURITY`. Create a dedicated login role (`NOSUPERUSER NOBYPASSRLS`), grant it the
   table privileges it needs, and set `FORCE ROW LEVEL SECURITY` on every tenant table as a second lock.
2. **Migrations run as another role, from another URL.** The owner role creates and alters tables; the
   application role only reads and writes rows. Prisma takes the runtime URL for the client and a separate
   URL for migrations (a `directUrl` in the datasource up to the version that moved datasource configuration
   out of the schema, the migration URL of the configuration file after it; check the version the project
   is on). One shared URL means the application runs as the owner, and the policies never apply.
3. **Check it in the database, not in the environment file:**
   `SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user;` run through the
   application's own client returns `f`, `f`.

## 4.2 Tenant context
4. **The tenant is set per transaction, with `set_config(..., true)`.** The policies read a setting
   (`current_setting('app.tenant_id', true)`); the application sets it with
   `SELECT set_config('app.tenant_id', $1, true)` as the first statement of an interactive transaction,
   and runs the queries in that same transaction. The `true` makes it local to the transaction. A plain
   `SET` or a session-level `set_config` survives on the pooled connection and the next request, for another
   tenant, inherits it.
5. **Behind a transaction-mode pooler, nothing session-level is safe.** Only the transaction-local form of
   rule 4 holds. A Prisma client extension that wraps each operation in a transaction with the setting is
   the usual shape; a query that escapes the wrapper (a raw query on the base client) runs without tenant.
6. **No tenant means no rows.** The policy compares against the setting read with `missing_ok = true`, so an
   unset context yields `NULL` and matches nothing. A policy that falls back to "all tenants" when the
   setting is empty is a finding.

## 4.3 The proving test
7. **One integration test proves isolation through the application's own client and role**, against a real
   Postgres (not a mock, not the owner role):
   1. seed two tenants with one row each, as the migration role;
   2. through the runtime client with tenant A set, read and assert only A's row comes back;
   3. with tenant A set, update and delete by B's identifier and assert zero rows affected;
   4. with no tenant set, assert zero rows;
   5. assert the role check of rule 3.
   Seen failing once: run it with the owner URL and watch steps 2 to 4 fail. A test that passes under both
   roles proves nothing.

## Mechanical checks
```
grep -rnE "BYPASSRLS|SUPERUSER|FORCE ROW LEVEL SECURITY|ENABLE ROW LEVEL SECURITY" prisma migrations
grep -rnE "set_config|SET (LOCAL )?app\." src
grep -rnE "directUrl|DIRECT_URL|MIGRATION_URL|migrate.*url" prisma src *.ts
grep -rnE "\\$queryRaw|\\$executeRaw" src
```
- A tenant table with `ENABLE` but no `FORCE` relies on the role never owning it (rule 1).
- A `set_config(..., false)` or a `SET` without `LOCAL` is a leak across pooled requests (rule 4).
- One URL for runtime and migrations is a finding (rule 2).
- Each raw query is checked to run inside the tenant transaction (rule 5).

## Not verified
Written from the Postgres documentation on row security and role attributes and the Prisma documentation on
datasources, interactive transactions and client extensions. Nothing was run while writing this section.
