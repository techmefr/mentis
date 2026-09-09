# laravel-conventions §3 — Data model and schema

> Section 3 of `skills/laravel-conventions`. Read it when a migration, a column, an enum, a soft delete. The other sections and the guardrails stay in `SKILL.md`.

1. **No DB-level ENUM column.** Use a string column, with a PHP enum as the single source of truth, cast on
   the model, and validated through the framework's enum rule. Five reasons, and the first is the one that
   bites: **every value change is an `ALTER TABLE`** — adding one status to a 50-million-row table is a long
   migration that may lock it. Then: the type is inconsistent across engines (native enum here, a created type
   with its own alter semantics there); the DB constraint and the PHP list are **two sources of truth that will
   drift**; renaming a value becomes a multi-step data-plus-schema-plus-code migration; and a value set that
   depends on the tenant or that an admin can extend is simply impossible.
2. **Don't tune the column length to the longest value**, and **don't skip the cast** — without it the column
   comes back as a raw string and the enum bought nothing. A `CHECK (status IN (...))` constraint is the same
   mistake wearing a lighter costume: same migration friction, same duplication.
3. **A set that changes at runtime isn't an enum at all.** An admin-configurable category, a per-plan status
   list, a feature parameter — those belong in a table, not in code. The test is who changes it: a developer
   with a deploy (enum) or a user at runtime (table). A boolean column beats a two-value enum outright.
4. **An enum with per-case data puts the value on the enum as a method**, not in a `match` scattered across
   callers. A `match` on an enum case returning a rate, a label or a threshold is behaviour that belongs to
   the enum — otherwise the day a case is added, the compiler helps you in one file and not in the other six.
5. **No cascade delete at the database level.** The DB deletes rows behind the ORM's back, so nothing fires
   on the children. What silently stops happening: no audit entry for the deleted child, the child stays in
   the search index, its cache is never invalidated, it stays in the CRM/billing/ERP because no
   `child.deleted` listener ran, the cancellation email is never sent, and denormalised counters on siblings
   stay wrong. None of that fails loudly.
6. **Keep the foreign key, drop only the cascade.** Removing the constraint to dodge the rule is worse — you
   trade silent-wrong-behaviour for silent-orphan-rows.
7. **Cascade through a listener class**, registered explicitly — not a closure in a model hook. A class is
   testable on its own, keeps the model thin, and can be queued when the cascade is heavy. Inside it, stream
   the children (a cursor, or chunk-by-id when you need to dispatch between chunks); reading the relation as a
   property loads every child row into memory first, which is exactly the case you were worried about.
8. **Never both.** A DB cascade *and* a listener means the listener deletes children the DB has already
   removed, and the same domain must not mix the two strategies per parent/child pair.
9. **Debugging tip worth its own line: when a lifecycle listener "isn't firing", check the parent's foreign
   key for a cascade first.** That's the most common root cause, and it looks like a broken listener.
10. **Where a DB cascade is genuinely fine**: a pure pivot table with no columns and no business meaning; a
    deliberate data-destruction purge at scale, where firing per-row notifications is the thing you don't
    want; and an append-only log table whose only consumer is its parent's lifecycle.
11. **Decide all of this at the ERD/plan stage, not at code review.** A plan sentence like "delete the user
    and cascade to orders and sessions" has already chosen the mechanism, and a verbal answer to "should
    deleting a company remove its invoices?" is the same decision made without noticing.
12. **Don't factorise two concepts into one table, model or abstraction** just because they look alike or
   share columns today. The shared table is cheap now and is the thing you can't unpick later, when one
   side grows a rule the other can't have. Factorisation is earned by **shared meaning and shared
   change** — the two play the same role in the domain and will evolve together — never by shared *shape*
   (similar columns right now) or shared *screen* (a designer drew them on one page). A mockup listing two
   kinds of thing in one table is a layout decision, and reading it as a schema decision is the most common
   way this one gets made.
13. Every model using soft deletes also carries a **pruning policy** with a retention window. Soft deletes
   without pruning is an unbounded table that silently becomes the biggest one in the database.
14. **Pruning is deleting, and a sweep fires the same per-row events as a delete.** A mass-prune trait,
   event suppression, a quiet delete, a table truncate and a hand-rolled `DELETE … WHERE created_at <`
   cron are the same bypass as point 5's database cascade arriving from the other direction: the rows
   leave and nothing downstream hears. "This data is never deleted, only pruned" is a contradiction — if a
   row can be purged after eighteen months then it is deletable, and the retention window only says when.
   A summary event carrying a class name and a count is not a substitute, because nothing can audit,
   archive, re-index or sync from a number: it says how many rows vanished, never which. Where the volume
   genuinely makes per-row events untenable, that is point 10's deliberate purge — an explicit decision
   with the lost listeners named, not a trait chosen to keep the log quiet.
15. Column defaults: prefer the application-side default, visible at the call site and testable without a
    database.
16. **A generated column (`virtualAs`/`storedAs`) is for a value that has to be filtered, sorted or
    indexed by the database, never for one only PHP ever reads.** An accessor already covers the second
    case, computed on read and free to change without a migration; the generated column exists specifically
    because an accessor's result cannot appear in a `WHERE`, an `ORDER BY` or an index, so reaching for one
    on a value nothing ever queries by adds a schema-migration cost point 1 already warns about, for a
    feature the code never uses.
