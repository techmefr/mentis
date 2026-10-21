# multi-tenancy-isolation-models-pitfalls §3 — Life of a tenant

All points are own guidance from craft knowledge; nothing was read from a source for this file. Legal topics (retention duties, deletion rights, transfer rules) are method only and not legal advice: see `business/data-protection`.

## 3.1 Onboarding
1. **Creating a tenant is a repeatable, idempotent procedure,** run as code: record, schema or database, default roles, seed data, keys, quotas. Symptom of a manual checklist: tenants with different settings nobody can explain. Check: create a tenant twice in a test; the second run changes nothing.
2. **Failure halfway leaves a visible state** (provisioning, failed) with a way to resume or clean up. Symptom: a half-created tenant that blocks the name.
3. **Seed per-tenant defaults from versioned data,** and record which version a tenant was created from, so later changes to defaults do not rewrite existing tenants.

## 3.2 Noisy neighbours
1. **Symptom: one customer's import slows everyone.** Cause: a shared pool, queue or database with no per-tenant limits. Check: look at per-tenant usage in metrics during the incident (needs the tenant on metrics, §2.3.7).
2. **Per-tenant limits on the shared resources:** request rate, concurrent jobs, queue share, rows per export, storage, connections. Return a clear refusal with a retry hint, not a timeout.
3. **Fair queues for jobs:** a tenant's backlog must not starve others, which usually means per-tenant queues or a fair dispatcher (`skills/queue-worker-runtime-pitfalls`).
4. **Isolate the heavy tenants by moving them up a tier** (§1.1.5), rather than slowing the rest.
5. **Load test with an unbalanced mix,** one tenant at ten times the median, not a uniform one (`skills/load-and-capacity-testing-pitfalls`).

## 3.3 Migrations across tenants
1. **A migration across thousands of tenants is a rollout,** not one command: order, batch size, concurrency, a stop on first failure rate, a list of tenants done and failed, and the ability to resume.
2. **Both versions of the code must run during the rollout** since tenants will be at different schema versions for a while (expand-contract, `skills/devops-conventions` §6).
3. **Record the schema version per tenant** and make the application refuse or adapt when a tenant is behind.
4. **Rehearse on the largest and the oldest tenant first,** which find the slow and the legacy cases.

## 3.4 Backup, restore and moving a tenant
1. **Decide the unit of restore.** With shared tables, restoring one tenant means extracting its rows from a backup into a staging copy and merging, which needs a written procedure. With a database per tenant it is a restore of that database. Symptom of finding out during an incident: a promise to restore one customer, with only whole-system backups.
2. **Test the single-tenant restore** and measure its time, as for any restore (`skills/backup-restore-drill-pitfalls`).
3. **A tenant move (to another region, tier or cluster) is a copy, a catch-up of changes, a short freeze and a switch,** rehearsed with a rollback (`skills/devops-conventions` §6).

## 3.5 Residency and keys
1. **Residency is part of the model choice,** since "data stays in a region" needs a deployment, database or storage per region for that tenant, not a flag. Check that logs, backups, search indexes and support exports stay in the region as well.
2. **Per-tenant encryption keys** allow cryptographic deletion and separate access, at the cost of key management and recovery rules; decide it with the customer's requirements (own guidance on trade-off).

## 3.6 Offboarding and deletion
1. **Separate suspend, export and delete.** Suspend blocks access and keeps data for a grace period; export hands the customer their data in a documented format; delete removes it everywhere.
2. **List every store holding tenant data** before promising deletion: primary database, replicas, caches, search indexes, object storage, backups, logs, analytics copies, support tickets, email provider, error tracker. Symptom: a "deleted" tenant still findable in search or in an exported report.
3. **Backups age out on their own schedule;** say so in the customer terms and record the deletion in a log that survives a restore, so a restored backup is re-purged (own guidance, check the law that applies).
4. **Delete in an order that fails safe:** revoke access first, then data, then the tenant record last, with a state that shows progress and can be resumed.
5. **Verify after deletion:** a script searches every store for the tenant's identifier and reports what remains.
6. **Keep what the law requires** (invoices, audit records) in a form that is separated from the product data and says why it is kept (`business/data-protection`).

## 3.7 Checks
1. Runbooks exist and were rehearsed for: create, throttle, migrate, restore one tenant, move, export, delete and verify.
