---
name: offline-first-sync-and-conflict-pitfalls
description: "Use when an application must keep working without a connection or feel instant on writes: choosing between online writes, optimistic state, persisted queued mutations and a local database synced both ways, deciding who wins when two edits collide (last write, field-level merge, convergent data types, server arbitration), scoping what is synced to a device, protecting a public sync endpoint, handling long offline periods, schema changes on local data, and testing offline and reconnect."
---

# offline-first-sync-and-conflict-pitfalls

A defensive block for the moment "works offline" or "feels instant" is added to an application with a server
database. Premise: **the hard part is never reading while offline; it is what a write means when the server may
refuse it later, when someone else changed the same thing, or when the device sat unused for a month**. List
screen states are `skills/flutter-four-async-states` and `skills/data-fetching-state-conventions`; the Android
repository layout for offline-first reads is `skills/kotlin-android-data-flow-and-api-pitfalls`; real-time editing
of shared text is `skills/rich-text-editor-pitfalls`; ordering and concurrent moves on a board are
`skills/kanban-board-ui-pitfalls`; a retry-safe write is `skills/nestjs-reliability` (idempotency keys) and
`skills/laravel-idempotent-jobs`.

## When
- A mobile or web client must read and write with no network, or must not wait on the network for each write.
- Two people or two devices can edit the same record, and nobody has decided who wins.
- A local database, a persisted queue or a sync service is added, or a sync bug is reported ("my change came
  back", "the item reappeared", "the app is empty after a week away").
- A sync endpoint is exposed to clients.

## Steps

**Read only the section the task meets.** §1 is the entry point: most apps need less than they think.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Choosing the write path: four patterns from online writes to a synced local database, rollback, separation of synced and local state | the first design, or "do we need offline writes at all" | [`01-write-path-choice.md`](./references/01-write-path-choice.md) |
| 2 | Conflicts and convergence: last write wins, field-level merge, convergent types, deletes, identifiers, ordering, clocks | two writers can touch the same data | [`02-conflicts-and-convergence.md`](./references/02-conflicts-and-convergence.md) |
| 3 | Scope, security, transport and lifecycle: subsets, a public sync endpoint, proxies, long offline, local schema changes, logout, tests | a sync service is exposed, data is scoped to a device, or an offline test is written | [`03-scope-security-lifecycle.md`](./references/03-scope-security-lifecycle.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed design owes: the write pattern chosen per entity with the reason (§1), for each
entity the conflict rule and what the user sees when it fires (§2), the subset each device may hold and how that
is authorised (§3), the longest offline period supported and what happens past it (§3), and an offline and
reconnect test list (§3).

## Guardrails
- Start with the simplest write path that meets the product need. Never build a local-first stack for screens that
  only need cached reads (§1).
- Keep synced server state and unsent local changes apart, and combine them when reading. Never overwrite the
  synced copy with an unconfirmed edit (§1).
- Give every queued mutation a stable identifier the server can de-duplicate. Never replay a queue with
  non-idempotent writes (§2).
- Pick the conflict rule per field or entity and show the loser what happened. Never leave "last write wins" as
  an accident of the transport (§2).
- Authorise sync requests on the server, per shape or subset. Never expose a sync endpoint that serves anything
  its database user can read (§3).
- State the offline limit, and what is lost or re-fetched beyond it. Never let a long-offline device push stale
  state silently (§3).
- This block restates the Electric sync documentation at idea level plus marked own guidance; nothing was run.
  Convergent-type internals were not read in a source (see [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten at idea level from the Electric documentation (Apache-2.0), read 2026-10-20, with own guidance marked in
the references. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
