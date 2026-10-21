# sql-server-transactions-and-operations §3 — Schema health and operations

Rules hold for SQL Server 2017 and later and for Azure SQL unless a version is named. The settings are
properties of the engine; check the documentation page for your version before changing a production server.

## 3.1 Constraints and indexes
1. **Index foreign key columns that are joined or whose parent rows are deleted.** Creating a foreign key does
   not create an index, unlike a primary key. The documentation says an index on the foreign key is often
   useful because those columns are common in join conditions and because changes to the parent key are
   checked against the child table. The First Responder Kit reports unindexed foreign keys. Index by the real
   access pattern, not by reflex.
2. **Load constraints `WITH CHECK`, and never leave one untrusted.** `WITH NOCHECK` adds a foreign key or
   check constraint without validating existing rows; the `ALTER TABLE` page says this is generally never
   recommended and that the query optimizer ignores such constraints until they are re-enabled with
   `ALTER TABLE ... WITH CHECK CHECK CONSTRAINT ALL`. Find them with `is_not_trusted` in `sys.foreign_keys` and
   `sys.check_constraints`.
3. **Give every table a clustered index unless it is a deliberate staging heap.** The heap page advises
   against heaps for data that is read sorted, grouped or by range, for large tables with no nonclustered
   index, and for data that is updated often: an update that no longer fits moves the row and leaves a
   forwarding pointer that every scan must follow. The First Responder Kit reports heaps with forwarded
   fetches and heaps with deletes.

## 3.2 Identity range
1. **An identity column can run out sooner than the row count suggests.** Values consumed by a failed or
   rolled-back insert are lost and never reused, and values cached around a restart can leave gaps. `int` ends
   at 2,147,483,647.
2. **Create new identity keys as `bigint` when growth is unbounded, and monitor the rest.** The First
   Responder Kit raises a finding for an identity column near the end of its range. The `bigint` default is own
   guidance; the data type of an identity column can be changed only to a compatible type and the property
   cannot be removed once set, so this is a design-time choice.

## 3.3 Recovery model and database options
1. **The full and bulk-logged recovery models require log backups, and the log grows until one is taken.** If
   point-in-time restore is not needed, the simple model does not support log backups. The log backup page
   suggests every 15 to 30 minutes as often enough, more often to cut work-loss exposure; a frequent backup
   also truncates the log more often, so the file stays smaller.
2. **Keep `AUTO_SHRINK` off.** The page says not to turn it on without a specific requirement. It shrinks
   files that have more than 25 percent unused space on a schedule the application does not control.
3. **Keep `AUTO_CLOSE` off on a database that serves requests.** With it on, the first use after the last user
   leaves must reopen the database, which the page says can take time and cause application timeouts.
4. **Use `PAGE_VERIFY CHECKSUM`.** It is the default for new databases; a database upgraded from an old version
   keeps `NONE` or `TORN_PAGE_DETECTION`, and the page recommends changing it, including for `tempdb`. It can be
   set without taking the database offline.

## 3.4 Backups, restores and credentials
1. **A backup is proven by restoring it.** The backup and restore guide says there is no restore strategy
   until backups are tested: restore a copy on a test system, for each backup type in use, and run
   `DBCC CHECKDB` on the result.
2. **`RESTORE VERIFYONLY` is not a restore test.** It checks that the backup set is complete and readable, with
   extra checking on the data, but does not verify the structure of the data in the backup.
3. **Do not pass a password with `sqlcmd -P`.** The page marks it insecure. Use the `SQLCMDPASSWORD`
   environment variable, or omit `-P` so that the utility prompts and hides the input; for a non-interactive
   job, prefer integrated authentication where it is available (the page recommends integrated security
   where possible; combining it with a user name or password is an error). In a script, also set the
   exit-code options (`-b`, and `-V 16` as the page suggests for automation) and check the exit code, or a
   failed deployment script exits zero; the page also recommends `-X` for unattended runs, which stops
   environment variables and the startup script from being read.
