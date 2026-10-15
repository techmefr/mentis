# sql-server-tsql-types-and-queries §1 — Types, literals and dates

Rules carry the SQL Server version they hold for. The documentation read covers SQL Server 2017 and later
and Azure SQL; where a feature is newer, the rule says so.

## 1.1 Dates and times
1. **Use `datetime2` (or `datetimeoffset` when the offset matters) for new columns, not `datetime`.** The
   `datetime` page says to avoid it for new work; its values are rounded to increments of `.000`, `.003` or
   `.007` seconds and it is not ANSI or ISO 8601 compliant. `datetime2` takes a precision of 0 to 7 digits
   (default 7, 100 ns); `datetimeoffset` adds time zone support.
2. **Stamp rows with `SYSUTCDATETIME()`, not `GETDATE()`.** `GETDATE()` returns a `datetime` without the time
   zone offset; `SYSUTCDATETIME()` returns a `datetime2` in UTC with up to 7 fractional digits. Storing UTC and
   converting on display is own guidance.
3. **Cast explicitly when `datetime` and `datetime2` are compared.** From database compatibility level 130 the
   implicit `datetime` to `datetime2` conversion accounts for the fractional milliseconds, so mixed
   comparisons can give different results than before; the `datetime2` page says to cast explicitly in any
   mixed comparison.
4. **Write date literals in the ISO 8601 form with every element**, `yyyy-MM-ddTHH:mm:ss[.nnn]`: the `T`, the
   colons and the period are required, and this form is not affected by `SET DATEFORMAT` or `SET LANGUAGE`.

## 1.2 Character types and literals
1. **Always give a length.** When `n` is omitted in a declaration or variable the length is 1; when it is
   omitted in `CAST` or `CONVERT` the length is 30, and values that are too long are truncated without an
   error. tsqllint enforces the same rule on declarations.
2. **`n` counts bytes for `varchar` and byte-pairs for `nvarchar`, not characters.** With a UTF-8 collation
   (SQL Server 2019 and later) or supplementary characters in UTF-16, fewer characters fit than `n`. Size
   columns for the longest real value, then add headroom.
3. **Prefix Unicode literals with `N`.** Without it the string is converted to the database default code page,
   which can lose characters; an `N` literal longer than 4,000 characters becomes `nvarchar(max)`. tsqllint
   flags Unicode characters in a non-Unicode string.
4. **Do not use `text`, `ntext` or `image`.** The page says they will be removed in a future version; use
   `varchar(max)`, `nvarchar(max)` and `varbinary(max)`. Dropping an `ntext` column on a large table is slow
   because the cleanup runs as one serialised operation; the page advises setting the column to `NULL` first.
5. **Concatenation silently truncates past 8,000 bytes unless one operand is a large value type.** For
   `nvarchar`, 8,000 bytes is 4,000 characters (derived from the byte-pair sizing). Cast the first operand to
   `nvarchar(max)` when the result can be longer.
6. **`ISNULL` truncates, `COALESCE` does not.** `ISNULL` returns the type of its first argument and can
   truncate a longer replacement; `COALESCE` returns the type with the highest precedence. The two also differ
   in nullability (an `ISNULL` with a non-null replacement is non-nullable, which matters for computed columns
   used as keys) and `COALESCE` can evaluate a subquery argument twice, which under `READ COMMITTED` can give
   different results. Choose by which of those differences the code relies on.
7. **Use `sysname` for variables that hold object names.** It is `nvarchar(128)` and not nullable.

```sql
DECLARE @Note nvarchar(200) = N'text';
DECLARE @Joined nvarchar(max) = CAST(@Note AS nvarchar(max)) + REPLICATE(N'x', 5000);
```

## 1.3 Numbers and money
1. **Use `decimal` with a stated scale, not `money` or `smallmoney`, for amounts that are calculated.** The
   `money` page warns that rounding errors through truncation can occur when monetary values are stored as
   `money` and used in calculations, and advises `decimal` with at least four decimal places.
2. **Choose the integer width at creation.** `int` tops out at 2,147,483,647 and `bigint` is for values that
   might exceed it. Identity values are not reused after a failed or rolled-back insert, so the range is used
   up faster than the row count suggests (`sql-server-transactions-and-operations` §3.2 for the monitoring
   side). Starting on `bigint` is own guidance.
