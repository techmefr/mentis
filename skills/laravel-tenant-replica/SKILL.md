---
name: laravel-tenant-replica
description: Use in a database-per-tenant Laravel project (stancl/tenancy) whenever a record must be the same in several tenants — an account, a curated catalogue entry — and a tenant's own tables need a foreign key to it. Central stays the source of truth; each tenant carries a copy keyed from the central primary key, carrying no credential material, and a central change descends only to the tenants holding a copy. A per-client fact is not a replica — it has no central original at all.
---

# laravel-tenant-replica

The narrow case in `skills/laravel-tenant-context-by-default` §2: a record that exists on both
sides of the tenant boundary. Triggers on a foreign key to a central table from tenant
data, `SyncMaster`/`ResourceSyncing`, and "le même enregistrement dans plusieurs tenants".

## When
A tenant-side table needs to reference a central record (a user, a shared catalogue entry) by foreign
key, or a save on a central record needs to propagate to the tenants that reference it.

## Steps

### 1. Why a copy exists at all
1. **A foreign key cannot cross a database boundary.** A seat, a licence, an assignment on a tenant
   table must constrain against something inside that tenant's database, so the tenant carries a copy
   of the central row and its own tables point at it. Users are the headline case; any catalogue the
   business curates once and several clients reference works the same way.
2. Central stays the single source of truth; a change to the central row **descends** into the
   tenants currently holding a copy of it.

### 2. The copy keeps the central primary key
1. **This is the load-bearing decision.** Every central lookup (the authenticated user, a
   catalogue-id join) resolves against the central database. A copy written with a locally issued
   auto-increment id would point at whoever occupies that id in *that* tenant's numbering; writing the
   primary key explicitly from the central row makes the id mean the same record in every database.
2. Correlate the two sides on a global identifier on both rows (a UUID), writing the primary key
   alongside it, never deriving one independently.

### 3. The copy carries only what it needs — and never credentials
1. Only the declared synced attributes travel, and **no credential material of any kind** — no
   password hash, no two-factor secret, no passkey. Authentication already happened centrally;
   replicating credentials into every tenant database multiplies where a breach can read them, for no
   benefit. A tenant's copy of a user is a name, an email and the keys its own tables need, not a
   second account.

### 4. Creating a copy and propagating a change are two different jobs
1. **Creation belongs to whoever granted the access that needs it** (a person seated, a client given a
   shared catalogue entry), upserted by the global identifier, not invented later by the propagation
   listener.
2. **Propagation carries changes, and only changes**: bail out unless the synced attributes changed on
   that save, or a routine save (a login refreshing a token, an unrelated column touch) fans a write
   out across the estate for nothing.
3. **Don't lean on a package's built-in "sync on every save" helper without checking what it does.**
   Such a helper typically fires on every save with no changed-attribute check, and when it finds no
   copy it creates one from *every* attribute of the central row: for a user, a password hash and
   two-factor secrets written into a table that deliberately has no such columns. Write the propagation
   listener explicitly, gated on §4.2's changed-attribute check and scoped to the declared synced
   attributes only.

### 5. Traps specific to a copy, each worth naming
1. **A copy must never itself propagate.** Writes to copies typically suppress model events, so a
   synced model arriving from a tenant connection means a loop, not a change worth spreading: guard
   for it explicitly rather than assuming the event source is always central.
2. **Enter the tenant through the shared holder object (`skills/laravel-tenant-context-by-default`
   §3), never a bare run-in-tenant helper with no restore on the throwing path.** A refusal on the
   copy (a NOT NULL violation, say) is an ordinary throw, and a helper that restores the previous
   connection only *after* its callback returns leaves a multi-tenant walk pointed at the wrong client
   for the rest of the request.
3. **Read the loaded attributes, not a blanket "all attributes" accessor, when building the synced
   payload.** Such an accessor invents a null for any column the model never loaded: a row created
   without touching a column with a database default arrives at the copy as an explicit null and is
   refused by that column's NOT NULL constraint.
4. **Query copies including soft-deleted rows.** A soft-deleted copy is still the copy (a withdrawn
   catalogue entry, an account in its deletion grace period). The default scope wouldn't find it,
   would insert a duplicate, and the unique global-identifier constraint would refuse the insert.
5. **Writing the copy again is itself a re-admission**, not a no-op (granting access back, restoring
   an account). Leaving a soft-deleted copy marked deleted quietly re-admits someone every list in that
   tenant still hides.
6. **Remove a copy through the query builder, not by deleting the model instance**, when the record
   must disappear rather than be marked gone, and delete whatever inside the tenant referenced it
   first, or the tenant-side foreign key correctly refuses the delete.

### 6. What must not descend at all
1. **Ask: is this the same fact for everyone, or the same question answered separately per client?**
   Same fact → replica, per this skill. Answered per client → the tenant owns it outright, with no
   copy and no central original behind it.
2. Roles and grants inside a client are the canonical second case: who administers *this* client is
   decided per client, so each tenant carries its own permission catalogue, seeded by its own tenant
   migration, not a copy of a central role. The tell: one central role that answers everywhere, a
   single grant making someone administrator of every client. The fix is one row per client,
   reproduced *before* the central shortcut is removed, in the same migration (a deploy that only runs
   migrations has no other place for a step that must happen first).

## Output / checkpoint
Every tenant-side foreign key to a central concept points at a copy keyed from the central primary
key, with only the declared synced attributes and no credentials. Propagation runs on an
actual-change check and does not create missing copies from every column.

## Guardrails
- A locally issued primary key on a copy is disqualifying: foreign keys would mean a different record
  per database.
- A credential column on a copy is disqualifying.
- A replica to avoid walking every tenant for an estate-wide answer is the wrong direction: a copy
  exists so a foreign key resolves inside one tenant, not so a central query can answer across tenants.
- A central row behind something each client decides for itself isn't a replica candidate (§6).

## Origin
Mined from the org catalogue's `laravel` plugin, `tenant-replica` (commit shipping 2026-09-21, alongside `tenant-context-by-default`). Mechanism kept in full, including the five traps and the per-client-fact carve-out with its central-role tell. The source's stancl/tenancy helper class (`UpdateSyncedResource`) is kept generic ("a package's built-in sync-on-every-save helper"): the class name is one version's detail, the mechanism is what lasts. Its PHP listener example is described as mechanism (§4.3, §5.1), as in `skills/laravel-tenant-context-by-default`'s origin. Prose rewritten, none copied.