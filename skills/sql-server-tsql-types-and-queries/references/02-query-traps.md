# sql-server-tsql-types-and-queries §2 — Query traps

Each trap below turns a seek into a scan, fixes a row estimate at a guess, or caches a plan built for the
wrong value. Look at the actual execution plan before and after; the version each feature needs is stated.

## 2.1 Sargable predicates and implicit conversion
1. **Do not wrap a filtered or joined column in a function or expression.** tsqllint's non-sargable rule
   disallows functions in filter and join predicates, and the First Responder Kit's plan-cache check looks for
   intrinsic functions and expressions in predicates for the same reason. Move the work to the other side of
   the comparison and filter on a range.
2. **A leading-wildcard `LIKE` is in the same family.** The First Responder Kit check groups it with
   expressions on columns; plan an alternative (a narrower prefix filter, or full-text search) when the table
   is large.
3. **Make the parameter or literal type match the column type.** When an operator combines two types, the one
   with lower precedence is converted to the higher one, and `nvarchar` ranks above `varchar` in the
   precedence list, so an `nvarchar` parameter compared with a `varchar` column converts the column, not the
   parameter. The showplan warning for this case is `PlanAffectingConvert`, and the First Responder Kit reads
   its `ConvertIssue` value `Seek Plan` to report conversions that stop an index seek. For `datetime` and
   `datetime2` compare with an explicit cast (§1.1).
4. **Drivers and ORMs choose parameter types for you.** Check the generated type of a string parameter
   against the column (`varchar` or `nvarchar`) when a query on an indexed text column scans; for EF Core
   see `dotnet-aspnet-efcore-pitfalls` §3. This is own guidance built on the precedence rule.

```sql
SELECT OrderId FROM dbo.Orders WHERE CreatedAt >= @From AND CreatedAt < DATEADD(day, 1, @From);
```

## 2.2 Functions and table variables
1. **Scalar user-defined functions run once per row and block parallelism.** The documentation lists four
   causes: iterative invocation (one call per qualifying row), no costing of scalar operators, statement by
   statement interpreted execution, and no intra-query parallelism in queries that call them. The First
   Responder Kit flags a scalar function in a `WHERE` clause and a computed column or check constraint that
   calls one.
2. **From SQL Server 2019 (compatibility level 150) a qualifying scalar function is inlined** into the calling
   query. The conditions include a single `RETURN`, no time-dependent intrinsics such as `GETDATE()`, no
   table variables, no CTEs, and `EXECUTE AS CALLER`. Do not assume inlining: check the function against the
   list, and prefer an inline table-valued function when the logic is one query (own guidance).
3. **Multi-statement table-valued functions have no statistics.** The optimizer builds no statistics for
   them (statistics documentation) and the First Responder Kit notes their row estimates are inaccurate. Use an
   inline table-valued function, or write the result to a temporary table first.
4. **Table variables carry no distribution statistics and do not trigger recompiles.** The `table` page says
   the optimizer often plans as if the variable has no rows, advises caution above about 100 rows, and
   recommends `OPTION (RECOMPILE)` on statements that join one. From SQL Server 2019 (compatibility level 150)
   table variable deferred compilation uses the real row count at first execution. The First Responder Kit
   adds that modifications to them are single threaded.

## 2.3 Parameter sniffing
1. **One cached plan serves every value.** The engine sniffs parameter values when it compiles stored
   procedures, `sp_executesql` statements and prepared queries, and that plan is reused; with a skewed
   distribution it can be poor for other values. When the same statement is fast for one value and slow for
   another, test parameter sensitivity before anything else; the First Responder Kit's check looks for a wide
   variance in rows returned or duration between executions.
2. **Copying a parameter into a local variable defeats sniffing, not the problem.** The engine cannot sniff a
   local variable at compile time and falls back to the average density from statistics (or fixed guesses of
   10 percent for equality and 30 percent for ranges when no statistics exist), which is an estimate for the
   average value rather than for any real one.
3. **`OPTION (RECOMPILE)` makes parameters and local variables compile-time constants,** so the plan fits the
   current values, at the price of a compile per execution; keep it for the statements that vary.
4. **SQL Server 2022 (compatibility level 160) adds Parameter Sensitive Plan optimization,** which compiles a
   dispatcher plan that picks a query variant from the runtime value. Enabling the compatibility level is
   the switch; do not rely on it for older versions or for predicates it does not cover.

## 2.4 Names and metadata
1. **Qualify every object with its schema.** The `CREATE PROCEDURE` page says it takes the engine less time
   to resolve names that are qualified and avoids permission and access problems from a user's default
   schema; tsqllint enforces it.
2. **Prefer the `sys` catalog views over `INFORMATION_SCHEMA` for object metadata.** tsqllint's rule states
   this preference without a reason; treat it as a lint position, not as a documented behaviour.
