# multi-tenancy-isolation-models-pitfalls §2 — Keeping the tenant on every path

All points are own guidance from craft knowledge unless stated. Database behaviour marked "re-read before relying" was not looked up while writing this; read the manual for your engine and version.

## 2.1 One source for the tenant
1. **Resolve the tenant at the edge from something the caller cannot forge:** the authenticated identity's membership, a verified domain, or a signed token claim. Symptom: the tenant read from a body field, a header or a query string the user can change, so changing one value opens another customer's data. Check: change that value in a test and expect a refusal.
2. **Carry it as one typed value** through the request, not as a loose string or as several copies. Symptom: a function that takes `tenantId` in some places and `accountId` in others for the same thing.
3. **The tenant a user acts in is a choice among memberships.** A person in several tenants must pick one explicitly per request or session, and the choice is checked against membership every time (`skills/auth-session-conventions`).
4. **Never infer the tenant from the resource alone on a write.** The resource's tenant must equal the caller's tenant; otherwise a guessed identifier writes into someone else's data (`skills/security-hardening` §3.2).

## 2.2 Queries and constraints
1. **A query with no tenant must fail, not return all.** In row isolation, a default scope or a query layer that refuses to run without the tenant. Symptom of relying on discipline: one report endpoint written in a hurry without the filter. Check: grep for raw queries and for the places that bypass the layer, and list them with a reason.
2. **Composite keys and unique constraints include the tenant.** A unique email or slug is unique per tenant, so the constraint is on (tenant, email). Symptom: a signup "email already used" caused by another customer, which also leaks that the email exists elsewhere.
3. **Foreign keys include the tenant,** so a child row cannot point to a parent of another tenant (a composite foreign key on (tenant, id)). Symptom: an order referencing another tenant's customer, which no single-column key forbids.
4. **Database row-level security is the second lock.** It checks the tenant in the database whatever the application did (`skills/sql-conventions` §6). Points to re-read in the manual of your engine before relying: roles that own the table or are marked to bypass the policy are not restricted unless forced; a tenant value set per session is leaked to the next user of a pooled connection unless it is set per transaction or reset; a policy that calls a function on every row can slow scans.
5. **Migrations and admin tools often run as a role that bypasses the policy.** Record which roles bypass it and why, and keep application roles away from them.
6. **Indexes lead with the tenant** in row isolation, since nearly every query filters on it (check with the plan, `skills/sql-conventions` §3).

## 2.3 Everything that is not a request
1. **Background jobs carry the tenant in the payload and set the context before running.** Symptom: a job that works in the web process and writes to a default tenant in the worker. Check: run the job with two tenants queued back to back and see which data changes (`skills/queue-worker-runtime-pitfalls`).
2. **Scheduled and console tasks iterate tenants explicitly** and restore the context after each, including after an exception (`skills/laravel-tenant-context-by-default` §3 for the failure shape).
3. **Caches:** the tenant is in every key. Symptom: a cached dashboard shown to the wrong customer. Include the tenant in the key builder itself, not in each call site.
4. **Search indexes:** per-tenant indexes, or a tenant field that every query filters on and that the index client adds for you (`skills/search-index-sync-pitfalls`). Check that a query cannot be sent without it.
5. **Files and object storage:** a tenant prefix, with access rules per prefix, and signed URLs that expire. Symptom: a guessable path serving a file across tenants.
6. **Exports, emails, notifications and webhooks:** each takes the tenant from the data they send, and tests assert the recipient belongs to it.
7. **Logs, metrics and traces carry the tenant identifier** so support can filter and so a leak can be scoped (`skills/observability-instrumentation`); log content must not mix one tenant's data into another's view.
8. **Support and admin tools** that look into a tenant do so by an explicit, audited switch, not by removing the filter.

## 2.4 Tests
1. **Two-tenant tests for every endpoint and job:** create the same data in tenants A and B, act as A, and assert that B's records never appear in lists, counts, search, exports or errors.
2. **A deliberately unfiltered query in a test must fail** (own guidance: remove the filter once and confirm the suite turns red).
3. **Penetration-style checks:** take an identifier from tenant B and call every route as tenant A.

## 2.5 Checks
1. The path table: HTTP, jobs, schedule, console, cache, search, files, mail, logs, admin; one line each with how it gets the tenant.
