# sql-server-transactions-and-operations §1 — Transactions and errors

These rules hold for SQL Server 2017 and later (the versions the pages read cover) and for Azure SQL.

## 1.1 Transactions do not nest
1. **There is one real transaction: the outermost.** The Database Engine does not support independently
   manageable nested transactions. `COMMIT` of an inner transaction only decrements `@@TRANCOUNT`; the data is
   made permanent when the outermost one commits. A name passed to `COMMIT` is ignored.
2. **A `ROLLBACK` at any depth undoes everything.** Without a savepoint name it rolls back to the outermost
   `BEGIN TRANSACTION` and sets `@@TRANCOUNT` to 0, and the caller then finds no transaction. A procedure whose
   `@@TRANCOUNT` differs between start and end gets an informational message.
3. **Use a savepoint for a partial rollback.** `SAVE TRANSACTION` plus `ROLLBACK TRANSACTION <savepoint>` undoes
   only the work after it and does not change `@@TRANCOUNT`.
4. **Decide in one place who opens and who commits.** A reusable procedure that may be called inside a
   transaction checks `@@TRANCOUNT` before starting its own and uses a savepoint instead of a second
   transaction when one is open. Own guidance built on the rules above.

## 1.2 XACT_ABORT, TRY...CATCH and THROW
1. **Put `SET XACT_ABORT ON` at the top of every procedure that opens a transaction.** With `OFF`, the default
   outside triggers, a run-time error may roll back only the failing statement and the transaction carries on,
   committing a partial result; with `ON` the whole transaction is terminated and rolled back.
2. **`TRY...CATCH` catches errors above severity 10 that do not close the connection.** Warnings of severity 10
   or lower are not caught, and errors of severity 20 or higher that end the session are not caught.
3. **Check `XACT_STATE()` in the `CATCH` block before deciding.** `-1` means the transaction is uncommittable:
   it can only be rolled back, and a `COMMIT` or any write fails. `1` means it can still commit; `0` means
   there is none. Roll back when the value is `-1`, and in general roll back unless the block has a reason to
   commit. `@@TRANCOUNT` cannot tell you whether the transaction is uncommittable.
4. **Re-raise with `THROW;`, not `RAISERROR`.** The documentation says new applications should use `THROW`;
   it honours `SET XACT_ABORT`, `RAISERROR` does not. `THROW` without arguments is valid only inside `CATCH`
   and keeps the original error number and severity; the statement before any `THROW` must end with a
   semicolon.

```sql
SET XACT_ABORT ON;
BEGIN TRY
    BEGIN TRANSACTION;
    UPDATE dbo.Account SET Balance = Balance - @Amount WHERE AccountId = @From;
    UPDATE dbo.Account SET Balance = Balance + @Amount WHERE AccountId = @To;
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;
```

## 1.3 Isolation level
1. **Do not use `READ UNCOMMITTED` or `NOLOCK` to reduce blocking.** The isolation page says a transaction at
   that level takes no shared locks, is not blocked by exclusive locks, and can read uncommitted changes
   (dirty reads). It names the alternatives that cut contention while protecting against dirty reads: the
   `SNAPSHOT` isolation level, or `READ COMMITTED` with the `READ_COMMITTED_SNAPSHOT` database option on.
2. **The default is `READ COMMITTED`** (on SQL Server it uses shared locks; on Azure SQL Database and SQL database in Fabric the `READ_COMMITTED_SNAPSHOT` option is on by default, so it uses row versioning), which prevents dirty reads but allows nonrepeatable and phantom reads
   between statements. Raise the level for the block that needs it rather than the whole connection.
