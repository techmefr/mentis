# sql-server-transactions-and-operations §2 — Dynamic SQL and procedure hygiene

`CREATE OR ALTER` needs SQL Server 2016 SP1 (the page's applies-to line); the rest holds for SQL Server 2017 and
later, the versions the pages read cover, and for Azure SQL.

## 2.1 Dynamic SQL
1. **Run dynamic statements through `sp_executesql` with parameters.** The documentation warns that
   runtime-compiled statements can expose an application to attack and says to parameterise. `@stmt` and
   `@params` must be Unicode constants or variables (`N` prefix, no concatenation inside the call), and every
   parameter in the statement needs an entry in `@params` and a value. Because the text stays constant while
   the values change, the optimizer is likely to reuse the plan.
2. **Pass values as parameters; quote only identifiers.** Names of tables, columns or schemas cannot be
   parameters. Wrap each in `QUOTENAME()`, which returns a valid delimited identifier. It accepts at most 128
   characters and returns `NULL` for longer input or an unsupported quote character, so a `NULL` result is
   a reason to stop, not to continue.
3. **Do not `EXEC` a concatenated string.** The `EXECUTE` page says to validate any character string before
   running it and never to execute a command built from unvalidated user input. The injection guide adds that
   data from parameters or read from a table should be wrapped in `QUOTENAME()` or `REPLACE()`, and that code
   calling `EXEC` or `sp_executesql` should be reviewed for exactly this.
4. **`LIKE` patterns need their wildcards handled too:** `[`, `%` and `_` in user input are escaped by the
   guide's example, otherwise the user controls the match.

```sql
DECLARE @sql nvarchar(max) =
    N'SELECT OrderId FROM ' + QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName) + N' WHERE CustomerId = @CustomerId';
EXEC sys.sp_executesql @sql, N'@CustomerId int', @CustomerId = @CustomerId;
```

## 2.2 Procedure hygiene
1. **Start procedures with `SET NOCOUNT ON`.** It stops the row-count message after each statement. The page
   says this reduces network traffic and can give a significant gain in procedures with several statements or
   loops, and `@@ROWCOUNT` is still updated. The `CREATE PROCEDURE` page (read 2026-10-20) says the gain is not
   measurable on current hardware and presents the setting as a way to keep output minimal, with the statement
   placed first in the body; treat it as output hygiene, not a tuning step. The same page recommends
   schema-qualified names and short explicit transactions, and its error handler tests `@@TRANCOUNT` before
   rolling back.
2. **End statements with a semicolon.** It is not required for most statements today but the syntax page says
   it will be required in a future version. It is already required before `THROW`, before a statement that
   starts with a `WITH` common table expression (the previous statement must end with one) and as the end of
   a `MERGE`, which raises error 10713 without it.
3. **`SELECT @variable = column` keeps the last row silently.** If the query returns several rows the variable
   gets the last value, with no error. Make the choice explicit with `TOP (1)` and an `ORDER BY`, or an
   aggregate. tsqllint's opposite preference for `SELECT` assignment is a style rule and is not carried over.
4. **Redeploy with `CREATE OR ALTER`.** It alters the procedure when it exists. `ALTER PROCEDURE` does not
   change permissions or dependent objects, though the current `QUOTED_IDENTIFIER` and `ANSI_NULLS` settings of
   the session are stored with the procedure, so run the deployment with the settings the code expects.
5. **Qualify objects with their schema inside procedures** (`sql-server-tsql-types-and-queries` §2.4).
