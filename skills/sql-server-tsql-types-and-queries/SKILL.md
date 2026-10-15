---
name: sql-server-tsql-types-and-queries
description: "Use when writing or reviewing T-SQL for SQL Server: choosing column and variable types (datetime vs datetime2, varchar lengths, N-prefixed literals, text and ntext, money, ISNULL vs COALESCE, string concatenation past 8,000 bytes), or investigating a slow or wrong query (functions on filtered columns, implicit conversion from mismatched types, scalar functions, multi-statement table-valued functions, table variables, parameter sniffing, unqualified object names)."
---

# sql-server-tsql-types-and-queries

Step 6 of the pipeline (`WORKFLOW.md`), for T-SQL on SQL Server and Azure SQL: the type and literal defaults
that truncate or round without an error, and the query shapes that quietly turn an index seek into a scan.
The premise: **T-SQL's defaults were chosen for compatibility, so a declaration or predicate that works on
ten rows can truncate, round or scan on ten million**. Transactions, dynamic SQL and operations are the
sibling block `sql-server-transactions-and-operations`; the same ideas for EF Core are
`dotnet-aspnet-efcore-pitfalls` §3.

## When
- A column, variable or parameter is declared, or a literal is written.
- A string is built by concatenation, or `ISNULL` or `COALESCE` picks a default.
- A query is slow, a plan "flips", or the same statement is fast with one value and slow with another.
- A predicate wraps a column in a function, or a parameter type differs from its column.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Types, literals and dates: datetime2, lengths, N literals, deprecated types, money, ISNULL, concatenation | a type, a literal or a default value is chosen | [`01-types-literals-dates.md`](./references/01-types-literals-dates.md) |
| 2 | Query traps: sargability, implicit conversion, scalar and multi-statement functions, table variables, parameter sniffing, naming | a query is slow, flips, or a predicate touches a column with an expression | [`02-query-traps.md`](./references/02-query-traps.md) |

## Output / checkpoint
Each rule was checked against the engine: a declared length was probed with a value one character too long
(§1.2), a predicate rewrite was compared by its actual plan (seek or scan, rows read) before and after
(§2.1), and a parameter-sensitivity fix was tried with a skewed and a rare value (§2.3). A rule checked by
reading code only is not verified.

## Guardrails
- Never declare `varchar`, `nvarchar`, `char` or `nchar` without a length (§1.2).
- Never store timestamps in `datetime` or money in `money` for new columns (§1.1, §1.3).
- Never wrap a filtered or joined column in a function when a range on the other side expresses the same test (§2.1).
- Never "fix" parameter sniffing by copying the parameter into a local variable (§2.3).
- Versions: each rule names the SQL Server version it needs. Nothing was run while writing this block.
- Transactions, dynamic SQL, error handling and operations stay in `sql-server-transactions-and-operations`;
  injection review beyond those points belongs to `security-hardening`.

## Origin
Rewritten from the SQL Server documentation (CC-BY-4.0), the tsqllint rule documents and the Brent Ozar First
Responder Kit check lists and code (MIT), read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). The general SQL conventions block (`sql-conventions`) lives
only on the unmerged branch `feat/antislop-lot` (PR 118); this block is meant to be folded into the same-topic
sections of that block when PR 118 lands, and stands alone until then.
