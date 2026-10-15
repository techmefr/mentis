# mysql-pitfalls §3 — DDL that rebuilds, and gh-ost prerequisites

Online DDL rules hold for MySQL 8.4 (INSTANT is the default algorithm for adding and dropping a column there;
MySQL 8.0 has a narrower set). The gh-ost rules are those of its documentation at the commit read
(2026-10-06), which states it requires MySQL 5.7 or later.

## 3.1 Online DDL that copies or rebuilds
1. **Name the algorithm and the lock.** With no `ALGORITHM` clause MySQL tries `INSTANT`, then `INPLACE`, then
   falls back to `COPY`; a named algorithm must be used or the statement fails with an error. Write
   `ALGORITHM=INPLACE, LOCK=NONE` (or `INSTANT`) so that an operation that would copy the table fails instead.
2. **Widening a `VARCHAR` across the 255-byte boundary copies the table.** In-place widening is supported only
   while the number of length bytes stays the same: 1 byte for columns up to 255 bytes, 2 bytes from 256. Going
   from under 256 to 256 or more bytes needs `ALGORITHM=COPY`. The limit is in bytes, so with `utf8mb4` a
   `VARCHAR(64)` is already 256 bytes.
3. **Adding a stored generated column uses `ALGORITHM=COPY`,** because the server must evaluate the expression
   for every row; a virtual column can be added instantly. Adding an auto-increment column does not permit
   concurrent DML (at least `INPLACE` with a shared lock) and reorganises the data.
4. **An expression default on a new column rewrites the table.** strong_migrations documents that in MySQL and
   MariaDB adding a column with an expression default (for example `(now())`) rewrites the table and blocks
   writes; the same project reports the same for the `COPY` algorithm, a changed column type, and a stored
   generated column.
5. **Adding a foreign key is in place only with `foreign_key_checks` off,** otherwise only `COPY` is
   supported. Turning the check off for the session skips validation of existing rows; strong_migrations allows
   it only when every row is known to be valid and the migration runs on one connection without a connection
   pooler, because the setting is per session and a pooler can send the next statement elsewhere.
6. **Instant column changes have a budget.** Each instant add or drop creates a row version, up to 64 in 8.4
   (255 from 9.1.0); rebuilding the table resets the count. When the limit is reached the statement errors and
   asks for `COPY` or `INPLACE`.

```sql
ALTER TABLE orders ADD COLUMN note VARCHAR(100) NULL, ALGORITHM=INSTANT;
```

## 3.2 Shadow-table tools: gh-ost prerequisites
1. **A shared, non-null unique key is required.** The original and the ghost table must share a primary key
   or other unique key, and its columns must be `NOT NULL` or contain no `NULL`. By default gh-ost refuses to
   run when the only unique key includes nullable columns; `--allow-nullable-unique-key` overrides it, but the
   data must really hold no `NULL`. An `enum` column in that key degrades performance badly.
2. **No foreign keys and no triggers on the table.** Both are listed as unsupported.
3. **Row-based binary logs with the full row image.** One server must serve row-based logs and replicas are
   preferred. Switching the binlog format with `--switch-to-rbr` needs `SUPER` for the replication stop and
   start; when the format is already `ROW`, pass `--assume-rbr` to avoid that.
4. **Throttle on replica lag.** `--max-lag-millis` pauses the copy when any controlled replica lags more than the
   value, and the replicas it checks (`--throttle-control-replicas`) must really be in the table's replication
   chain: an unrelated host reports healthy lag while the real replicas go unwatched.
5. **Rehearse with `--test-on-replica`.** gh-ost does the whole migration on a replica, stops replication before
   the cut-over and leaves the original and ghost tables for comparison.
6. **Keep the default atomic cut-over.** The default swaps the tables with an atomic rename behind a lock; the
   alternative `--cut-over=two-step` renames in two steps, and between them the table does not exist and
   queries fail.
7. **Check the exclusions before choosing the tool:** a table that needs `ALTER ... RENAME`, an
   active-active master pair, a federated table, encrypted binary logs, and a case-only name clash with another
   table are unsupported.
