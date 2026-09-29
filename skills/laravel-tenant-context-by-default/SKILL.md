---
name: laravel-tenant-context-by-default
description: Use when designing or writing code in a database-per-tenant Laravel project (stancl/tenancy) — a table, a query, a job, a console command, a tool call, an admin screen, a migration. Central answers only what must be answerable before any tenant is open; everything else descends into the tenant database. Never scope tenant data with a tenant_id column, and never let an HTTP middleware be the only door into a tenant — anything that isn't a request then runs central by default.
---

# laravel-tenant-context-by-default

Governs data residency and context-switching for database-per-tenant multi-tenancy. Triggers on
`tenancy()->initialize`, `Tenant::run`, a `tenant_id` column proposed on a central table, "central ou
tenant", and a permission check that seems to answer for the wrong client.

## When
Designing a table or feature in a project using `stancl/tenancy` in database-per-tenant mode, writing
a job/command/tool that needs to act inside a specific client's data, or debugging a permission or
data leak that looks like it's answering for the wrong tenant.

## Steps

### 1. The residency rule
1. **Central answers only what must be answerable before any tenant is open: who this person is, and
   which tenants they may enter.** Everything else descends into the tenant's own database. Central is
   not "the shared place" — it's the smallest surface that has no choice but to exist outside every
   tenant.
2. Decide each table with two questions, in order: **if this client disappeared tomorrow, should this
   row go with it?** (yes → tenant) and **who decides the value, the client or us?** (the client →
   tenant). A central schema growing faster than the tenant schema is a sign the design has already
   drifted the wrong way.
3. Central rows genuinely stay central: the account and the identity-to-tenant mapping (both must be
   readable before any tenant is known), estate-wide surfaces the business itself owns (staff,
   moderation, client lifecycle — read per client by walking the tenants, never from a shadow copy),
   and data the business curates once for every client (a shared catalogue, a price grid).

### 2. Two shapes look alike and aren't
1. **The same record needed in several tenants** (an account, a business-curated catalogue) —
   central owns the original, each tenant carries a copy its own foreign keys point at, and a central
   change descends to the tenants holding one. That's a replica; see `skills/laravel-tenant-replica`
   for its own rules (central primary key, no credentials, changes only).
2. **The same question answered separately per client** (who administers this client, which roles a
   person holds here) — nothing descends. Each tenant carries its own permission tables and its own
   grants, seeded by its own tenant migration. There's no `team_id`; the database is the separation.
   Central permissions exist only for the genuinely central surfaces from §1.3.
3. The account is the clearest case of the first: central holds the credential material (password,
   two-factor, passkeys) and sign-in happens there once; the tenant's copy is a name, an email and the
   keys, with no credential column at all.

### 3. The usual root cause: opening a tenant only from HTTP middleware
1. **Opening a tenant is almost always written as an HTTP middleware, undone in its `terminate()`.**
   That covers exactly one shape of work. A queued job, a console command, a tool call, a
   token-authenticated request, an admin screen reporting across clients — none of these have a door
   in, so they run on the central connection by default. Nobody decided that; it's what's left when
   the only door is a request.
2. **Move the opening into its own object, callable from anywhere**, and make the HTTP middleware one
   of its callers rather than its owner.
3. A tool, job or command entry point takes the tenant as a **declared, required argument** — it
   never guesses one, never remembers a previous one, and never opens the context itself. Putting the
   open/close call in a shared base class whose entry method is non-overridable keeps a concrete
   implementation from forgetting it.

### 4. Entering a tenant is more than switching the connection
1. **The permission cache is keyed globally by default.** A package like `spatie/laravel-permission`
   caches its whole catalogue under one key, which doesn't separate by database on its own — the
   first tenant to warm it answers permission checks for every tenant after it until the cache
   expires. Scope the cache key per tenant, and re-initialise anything that captured the old key at
   construction time; changing config alone doesn't reach an already-constructed singleton.
2. **Cached relations on the person survive the switch.** Eloquent keeps loaded relations (roles,
   permissions) on the instance, so a relation read under one tenant still answers for that tenant
   once another is open. Unset those relations on entry and on exit.
3. **The authenticated principal outside HTTP may not be the framework's own `User` model at all** —
   a guard written to only act "if it's a User" fails silently for a token-authenticated or
   system-triggered call.
4. **Hand back the previously held tenant, not central, on the way out.** Always returning to central
   is correct for one request and wrong for a nested call — opening tenant B from inside tenant A must
   restore A, which is what lets a low-level helper wrap itself safely without knowing who called it.
   The restore must run on the throwing path too, or a failure leaves the rest of the request pointed
   at the wrong database.

### 5. Transactions never cross a database connection
1. **One transaction can't span two databases**, and the default connection is whichever database is
   currently open. Tenant rows open a transaction on the default connection only after asserting a
   tenant is actually initialised — with none, refuse with a named exception rather than silently
   writing a client's rows into central.
2. **Central rows, written from anywhere, name the central connection explicitly** rather than
   relying on whatever the default happens to be — a model pinned to central writes there regardless
   of context, so a transaction opened on the default connection holds none of those writes; each
   commits on its own and a later rollback undoes an empty transaction, not the central write.
3. Work that genuinely writes both databases in one operation has no single transactional helper for
   that and has to be split into two pieces with their own individual consistency guarantees.

### 6. Migrations, in a layered (OSDD) project
1. Central schema stays in the owning layer's ordinary `database/migrations/`. Tenant schema goes in
   a `database/migrations/tenant/` of the layer that owns the table — a single layer can carry both, a
   permission layer with central permission tables and a full tenant-side set.
2. **Declare the tenant migration paths by reading the layer buckets from configuration, never by
   listing them by hand.** A bucket left off a hand-written list yields zero tenant migrations for
   itself, which looks like a healthy repository while every tenant database silently misses that
   layer's tables — the failure only shows up at the first business query against them. A test
   asserting every `database/migrations/tenant` directory on disk is actually declared closes this
   gap mechanically.

## Output / checkpoint
Every table's residency decision is stated against the two questions in §1.2. Tenant context is
opened through one shared object, never only from HTTP middleware; that object scopes the permission
cache, drops stale cached relations, and restores the previously held tenant on both the return and
the throwing path. No `tenant_id`/`company_id`/team column scopes a central table.

## Guardrails
- A `tenant_id`, `company_id` or permission "team" column scoping a central table is single-database
  tenancy applied on top of a database-per-tenant project — the rows still share one table, isolation
  is back down to one missing `WHERE`, and it hands the central model a responsibility that belongs to
  the client.
- Never open a tenant with a bare `tenancy()->initialize()` (or the package's own `run()` helper) with
  no restore on the throwing path — that's the same silent cross-tenant bug as §4.4 states directly.
- No credential material (passwords, two-factor secrets, passkeys) in a tenant's copy of the account.
- Route-model binding on a tenant-owned model resolves against central if the framework's binding
  substitution runs before the tenancy middleware — bind by key instead and load the row inside the
  action.
- Reaching straight for the query builder on tenant data bypasses the model's own connection and
  scoping.
- Don't move an existing central table unprompted — that's a data migration with its own review; a
  *new* table follows this rule even when its neighbours are still central, stated in one line before
  proceeding.
- Existing single-database tenancy (one database, a `tenant_id` and a global scope) is a different,
  legitimate model this skill doesn't govern — see the stack's own scope-based conventions instead.

## Origin
Mined from the org catalogue's `laravel` plugin, `tenant-context-by-default` (new file, commit
shipping 2026-09-21). Mechanism kept in full: the two ordering questions for residency, the
replica/per-client-fact split (cross-referenced to its own skill rather than duplicated), the
HTTP-middleware root cause and the "its own object, called from anywhere" fix, the permission-cache
and cached-relation costs of entering a tenant, restoring the *previous* tenant rather than central,
transactions never crossing connections, and declaring tenant migration paths from configuration
rather than by hand. Left out/uncertain: the source includes a full PHP code sample for the tenant
holder (a `rescue()`-based wrapper explicitly written to avoid `try`/`catch`, per that catalogue's own
static-analysis rule banning it) and a second sample for a `Tool` base class with a `final handle()`.
Both are described here as a mechanism rather than reproduced as code, since mentis has no equivalent
blanket `try`/`catch` ban recorded for this project and asserting one would be inventing a constraint
this repo doesn't hold — a project that does forbid `try`/`catch` should still reach the same
"restore-on-throw, non-overridable entry point" shape, by whichever construct its own conventions
prefer. `stancl/tenancy` and `spatie/laravel-permission` are kept by name — both are public packages
already named in `skills/laravel-conventions`/`skills/laravel-permissions-not-roles`. Prose rewritten
throughout; no text copied from the source file.
