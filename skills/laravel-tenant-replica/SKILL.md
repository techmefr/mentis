---
name: laravel-tenant-replica
description: Use in a database-per-tenant Laravel project (stancl/tenancy) whenever a record must be the same in several tenants — an account, a curated catalogue entry — and a tenant's own tables need a foreign key to it. Central stays the source of truth; each tenant carries a copy keyed from the central primary key, carrying no credential material, and a central change descends only to the tenants holding a copy. A per-client fact is not a replica — it has no central original at all.
---

# laravel-tenant-replica

The narrow case inside `skills/laravel-tenant-context-by-default` §2: a record that legitimately
exists on both sides of the tenant boundary. Triggers on a foreign key to a central table from tenant
data, `SyncMaster`/`ResourceSyncing`, and "le même enregistrement dans plusieurs tenants".

## When
A tenant-side table needs to reference a central record (a user, a shared catalogue entry) by foreign
key, or a save on a central record needs to propagate to the tenants that reference it.

## Steps

### 1. Why a copy exists at all
1. **A foreign key cannot cross a database boundary.** A seat, a licence, an assignment on a tenant
   table has to constrain against something inside that same tenant's database, so the tenant carries
   a copy of the central row and its own tables point at that copy. Users are the headline case, not
   the only one — any catalogue the business curates once and several clients reference works the
   same way.
2. Central stays the single source of truth; a change to the central row **descends** into the
   tenants currently holding a copy of it.

### 2. The copy keeps the central primary key
1. **This is the load-bearing decision.** Every central lookup (the authenticated user, a
   catalogue-id join) resolves against the central database. A tenant-side copy written with a
   locally issued auto-increment id would point at whoever happens to occupy that id in *that*
   tenant's own numbering — writing the primary key explicitly from the central row is what makes the
   id mean the same record across every database in the estate.
2. Correlate the two sides on a global identifier carried on both rows (a UUID), and write the
   primary key alongside it rather than deriving one independently.

### 3. The copy carries only what it needs — and never credentials
1. Only the declared synced attributes travel, and **no credential material of any kind** — no
   password hash, no two-factor secret, no passkey. Authentication already happened centrally;
   replicating credentials into every tenant's database multiplies where a breach can read them for no
   benefit. A tenant's copy of a user is a name, an email and the keys the tenant's own tables need —
   not a second account.

### 4. Creating a copy and propagating a change are two different jobs
1. **Creation belongs to whoever granted the access that needs it** — the moment a person is seated,
   the moment a client gets access to a shared catalogue entry — upserted by the global identifier,
   not invented later by the propagation listener.
2. **Propagation carries changes, and only changes**: bail out unless the synced attributes actually
   changed on that save, or a routine save (a remembered login refreshing a token, an unrelated column
   touch) fans a write out across the whole estate for nothing.
3. **Don't lean on a package's built-in "sync on every save" helper without checking what it actually
   does.** A helper of that shape typically fires on every save with no changed-attribute check, and
   when it finds no existing copy it creates one from *every* attribute of the central row — for a user
   that means writing a password hash and two-factor secrets straight into a table that deliberately
   has no such columns. Write the propagation listener explicitly instead, gated on §4.2's changed-attribute
   check and scoped to the declared synced attributes only.

### 5. Traps specific to a copy, each worth naming
1. **A copy must never itself propagate.** Writes to copies typically suppress model events, so a
   synced model arriving from a tenant connection means a loop, not a real change worth spreading —
   guard for it explicitly rather than assuming the event source is always central.
2. **Enter the tenant through the shared holder object (`skills/laravel-tenant-context-by-default`
   §3), never a bare run-in-tenant helper with no restore on the throwing path** — a refusal on the
   copy (a NOT NULL violation, say) is an ordinary throw, and a helper that only restores the previous
   connection *after* its callback returns leaves a multi-tenant walk pointed at the wrong client for
   the rest of the request.
3. **Read the loaded attributes, not a blanket "all attributes" accessor, when building the synced
   payload.** An accessor that returns every attribute invents a null for any column the model never
   actually loaded — a row created without touching a column that has a database default then arrives
   at the copy as an explicit null and is refused by that column's own NOT NULL constraint.
4. **Query copies including soft-deleted rows.** A copy that soft-deletes is still the copy — a
   withdrawn catalogue entry, an account inside its deletion grace period. The default query scope
   wouldn't find the marked row, would insert a duplicate, and the copy's own unique global-identifier
   constraint would then refuse the insert.
5. **Writing the copy again is itself a re-admission**, not a no-op — granting access back, restoring
   an account. Leaving a previously soft-deleted copy marked as deleted quietly re-admits someone every
   list in that tenant still refuses to show.
6. **Remove a copy through the query builder, not by deleting the model instance**, when the intent is
   the record disappearing entirely rather than being marked gone — and delete whatever inside the
   tenant referenced it first, or the tenant-side foreign key correctly refuses the delete.

### 6. What must not descend at all
1. **Ask: is this the same fact for everyone, or the same question answered separately per client?**
   Same fact → replica, per this skill. Answered per client → the tenant owns it outright, with no
   copy and no central original behind it.
2. Roles and grants inside a client are the canonical second case: who administers *this* client is
   decided per client, so each tenant carries its own permission catalogue, seeded by its own tenant
   migration — not a copy of a central role. The tell that this went wrong is one central role that
   answers everywhere: a single grant making someone an administrator of every client. The fix is one
   row per client, reproduced *before* the central shortcut is removed, in the same migration —
   a deploy that only runs migrations has no other place to put a step that must happen first.

## Output / checkpoint
Every tenant-side foreign key to a central concept points at a copy keyed from the central primary
key, carrying only the declared synced attributes and no credentials. Propagation runs on an
actual-change check, not on every save, and does not create missing copies from every column.

## Guardrails
- A locally issued primary key on a copy is disqualifying — foreign keys would then mean a different
  person or record per database.
- Any credential column on a copy is disqualifying, full stop.
- Reaching for a replica to avoid walking every tenant for an estate-wide answer is the wrong
  direction — a copy exists so a foreign key resolves inside one tenant, not so a central query can
  answer a cross-tenant question.
- A central row behind something each client decides for itself isn't a replica candidate — see §6.

## Origin
Mined from the org catalogue's `laravel` plugin, `tenant-replica` (new file, commit shipping
2026-09-21, alongside `tenant-context-by-default`). Mechanism kept: the foreign-key-can't-cross-databases
justification, the central-primary-key decision and why, the no-credentials rule, the
create/propagate split with the changed-attributes-only gate, the five listed traps (self-propagation
loops, restore-on-throw via the holder, loaded-vs-invented-null attributes, soft-deleted rows, deletion
via the query builder), and the per-client-fact carve-out with its central-role tell. The source names
a specific stancl/tenancy helper class (`UpdateSyncedResource`) as the thing not to rely on; kept here
generically as "a package's built-in sync-on-every-save helper" since the specific class name is one
version's implementation detail rather than the durable part of the rule, and stating the mechanism
that's wrong with it (fires on every save, creates from every column) is what a reader actually needs
to avoid the same mistake against a different package or a future version. A full PHP listener example
from the source is described as a mechanism (§4.3, §5.1) rather than reproduced as code, consistent
with the same call made in `skills/laravel-tenant-context-by-default`'s origin note. `stancl/tenancy`
is kept by name — it's the public package already named in `skills/laravel-conventions`. Prose
rewritten throughout; no text copied from the source file.
