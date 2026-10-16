---
name: laravel-mysql-to-postgres-pitfalls
description: "Use when a Laravel application's database is moved from MySQL or MariaDB to PostgreSQL, or code starts behaving differently after the driver changes: the empty-database migration test, choosing between a loader tool and the query builder for the data move, searches that stop matching because Postgres compares case-sensitively (LIKE versus ILIKE, citext, lower-case indexes), booleans compared as integers in raw SQL, id sequences left behind after a bulk import, MySQL-only functions and quoting in raw SQL, stricter GROUP BY and no silent truncation, and keeping MySQL available until the cutover is proven."
---

# laravel-mysql-to-postgres-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the one-time move of a Laravel application from MySQL or MariaDB
to PostgreSQL. The two sections share one premise: **the data moves fine; what breaks is every place the
application leaned on MySQL being forgiving**, so the work is an audit of the application's assumptions, not a
copy of rows. The behaviours of MySQL itself (collation, JSON, partitions) are in `skills/mysql-pitfalls`;
the framework conventions around it are in `skills/laravel-conventions`.

## When
- A Laravel project plans, rehearses or executes a move from MySQL or MariaDB to PostgreSQL.
- After the driver changed, a search returns nothing, a raw query errors, or the first insert fails on a
  duplicate key.
- A review has to decide what to test before a database cutover.

## Steps

**Read the section the task meets; a cutover needs both.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Strategy: the empty-database test, moving the data, the sequence reset, keeping MySQL | a move is planned or rehearsed, or data is imported | [`01-strategy-and-data-move.md`](./references/01-strategy-and-data-move.md) |
| 2 | Behaviour that changes silently: case sensitivity, booleans, MySQL-only SQL, strict grouping, no truncation, and the checklist | application code or raw SQL is reviewed for the new driver | [`02-behaviour-differences-and-checklist.md`](./references/02-behaviour-differences-and-checklist.md) |

## Output / checkpoint
Each point was exercised, not read: the migrations ran from nothing on an empty PostgreSQL database (part 1,
point 1), every raw SQL call found by a search was reviewed and listed, one record was created in each
imported table after the import and no duplicate-key error appeared (part 1, point 4), the full test suite ran
against PostgreSQL, and the old MySQL database is still readable. A move where only the first of these was
done is not verified.

## Guardrails
- Never import data before the migrations have run clean on an empty PostgreSQL database (part 1, point 1).
- Never switch the application on after a bulk import without resetting every imported table's id sequence
  (part 1, point 4).
- Never delete the MySQL database on the day of the switch (part 1, point 2).
- Never leave a user-typed search on a plain `LIKE` and assume it still ignores case (part 2, point 1).
- Never leave a raw comparison of a boolean column to `1` or `0` (part 2, point 2).
- This block states one skill's rules, read 2026-10-16; the PostgreSQL behaviours it lists were not run by us
  and the source's own references (a cloud vendor's guide, a blog post, the loader tool's site) were not read.

## Origin
Rewritten from one agent skill (majdghithan/agent-skills, MIT), read 2026-10-16, with our own guidance marked.
🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
