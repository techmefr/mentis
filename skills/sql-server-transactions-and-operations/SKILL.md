---
name: sql-server-transactions-and-operations
description: "Use when writing or reviewing SQL Server stored procedures, migrations or database operations: BEGIN TRAN nesting, TRY...CATCH with THROW and XACT_STATE, SET XACT_ABORT, isolation level choices, dynamic SQL with sp_executesql and QUOTENAME, SET NOCOUNT and statement terminators, CREATE OR ALTER redeploys, unindexed or untrusted foreign keys, heaps, identity range, recovery model and log backups, AUTO_SHRINK and PAGE_VERIFY, restore testing, and sqlcmd credentials."
---

# sql-server-transactions-and-operations

Step 6 of the pipeline (`WORKFLOW.md`), for the SQL Server code that changes state and the settings that keep
it recoverable. The premise: **T-SQL transactions do not nest, errors do not always abort, a backup that was
never restored is a hope, and a log in the full recovery model grows until someone backs it up**. Types,
literals and query shapes are the sibling block `sql-server-tsql-types-and-queries`.

## When
- A stored procedure, trigger or migration opens, commits or rolls back a transaction, or catches errors.
- A query is built as a string and executed.
- A procedure is redeployed, or a table, constraint or index is created or changed.
- A database setting, recovery model, backup job or command-line connection is written or reviewed.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Transactions and errors: nesting, XACT_ABORT, TRY...CATCH, THROW, XACT_STATE, isolation | code opens a transaction or handles an error | [`01-transactions-and-errors.md`](./references/01-transactions-and-errors.md) |
| 2 | Dynamic SQL and procedure hygiene: sp_executesql, QUOTENAME, NOCOUNT, terminators, variable assignment, CREATE OR ALTER | a query is built as a string, or a procedure is written or redeployed | [`02-dynamic-sql-and-procedures.md`](./references/02-dynamic-sql-and-procedures.md) |
| 3 | Schema health and operations: foreign keys, trusted constraints, heaps, identity range, recovery model, database options, restore tests, sqlcmd | a table or constraint is created or loaded, or a database or backup job is configured | [`03-schema-health-and-operations.md`](./references/03-schema-health-and-operations.md) |

## Output / checkpoint
Each rule was exercised: a forced error inside a transaction was caught and the session left with no open
transaction (§1.2), a dynamic statement was run with a hostile value and an identifier that needed quoting
(§2.1), and a backup was restored to a scratch database and checked (§3.4). A rule checked by reading code only
is not verified.

## Guardrails
- Never leave a transaction open on an error path: roll back when `XACT_STATE()` says it is uncommittable (§1.2).
- Never build a statement by concatenating values; pass values as parameters and quote identifiers (§2.1).
- Never use `READ UNCOMMITTED` or `NOLOCK` as a contention fix (§1.3).
- Never load constraints `WITH NOCHECK` and leave them untrusted (§3.1).
- Never pass a password with `sqlcmd -P` (§3.4).
- Versions: each rule names the SQL Server version it needs. Nothing was run while writing this block.
- General injection and secrets review belongs to `security-hardening`; migration review habits for ORMs are in
  `prisma-ops-and-test-hygiene` §1.4 and `devops-conventions`.

## Origin
Rewritten from the SQL Server documentation (CC-BY-4.0) and the Brent Ozar First Responder Kit check lists and
tsqllint rule documents (MIT), read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). Overlaps with `skills/sql-conventions` and `skills/devops-conventions` (2026-10-19); cross-referenced, not merged.
