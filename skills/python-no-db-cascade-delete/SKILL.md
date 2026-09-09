---
name: python-no-db-cascade-delete
description: "Use when adding or reviewing a foreign key relationship in an ORM model: never a DB-side cascade delete (ondelete=CASCADE) — cascade in the ORM layer, where the hooks live."
---

# python-no-db-cascade-delete

Narrow trigger extracted from `skills/python-conventions` §7.1, so a foreign-key relationship routes
here directly instead of only through the whole Python block.

## When
Defining or reviewing a foreign key or relationship in an ORM model, or looking at why deleting a
parent row removed its children with no registered listener having run.

## Steps
1. **No DB-side cascade delete** (`ondelete="CASCADE"`). The database bypasses the ORM, so delete
   events and registered listeners never fire on child rows.
2. **Cascade in the ORM layer, where the hooks live.** The rows still get removed, but through the
   path that also fires the ORM's own lifecycle events.
3. **The consequence is not only a missed event.** Search indexes, audit trails, file cleanup and
   outbound notifications all hang off those hooks — with a DB cascade, the rows vanish and everything
   derived from them silently does not.

## Output / checkpoint
No foreign key in the diff declares a database-level cascade; deletion of dependent rows goes through
the ORM's own relationship/cascade configuration or an explicit handler.

## Guardrails
- The same failure shape as `laravel-no-cascade-delete` — a different framework, the same reason:
  a database-level cascade is invisible to whatever layer expects to react to a delete.
- The full ORM/migrations section, including Python-side vs server-side defaults and async lazy
  loading, lives in `skills/python-conventions` §7 — read it for the neighbouring rules this one sits
  beside.

## Origin
No external source: this is `skills/python-conventions` §7.1 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
