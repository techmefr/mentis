# mysql-pitfalls §2 — Partitioning, replicas and timeouts

Rules hold for MySQL 8.4 with InnoDB. The variable names are those of the 8.4 manual; check defaults on your
version.

## 2.1 Partitioning
1. **Every column of the partitioning expression must be in every unique key, the primary key included.** The
   manual states this as the rule: every unique key must use every column of the partitioning expression, and a
   table whose key does not is rejected. Plan the primary key as `(id, partition_column)` or partition on an
   existing key column; the uniqueness of `id` alone is then no longer enforced by the database (own
   consequence of the rule, check it before choosing).
2. **A partitioned InnoDB table cannot have foreign keys, in either direction.** No user-partitioned InnoDB
   table may contain foreign key references, and no foreign key may reference one. Enforce the relationship in
   the application or choose another way to bound table size.
3. **Retire old data by dropping the partition, not by `DELETE`.** The manual says dropping the partitions that
   hold only expired data is the easy way to remove it. `ALTER TABLE ... DROP PARTITION` deletes the data in the
   partition with `ALGORITHM=INPLACE`; with `COPY` it rebuilds the table and tries to move the rows to another
   partition, deleting those that cannot move. It needs the `DROP` privilege. Name the algorithm.
4. **Keep a catch-all `MAXVALUE` partition on a `RANGE` table, or add partitions ahead of time.** A row with no
   matching partition makes the insert fail with an error; a catch-all partition avoids it, and later
   `ALTER TABLE` statements can add partitions for new ranges.

```sql
ALTER TABLE events DROP PARTITION p2024q1;
```

## 2.2 Replicas and read-your-writes
1. **Do not treat `Seconds_Behind_Source` as exact.** It compares the applier thread with the receiver
   thread. On a slow network the applier can keep up with a receiver that is itself late, so the value shows 0
   while the replica is behind the source, and clock changes such as NTP updates make it less reliable. Use it
   as an alarm, not as a guarantee.
2. **A read that must see a write goes to the source, or waits for the write's GTID.**
   `WAIT_FOR_EXECUTED_GTID_SET(gtid_set[, timeout])` returns when the server has applied all the transactions
   in the set. Its default timeout is 0, which means wait without limit, so always pass a timeout and fall back
   to the source when it expires.

## 2.3 Timeouts and locks
1. **`max_execution_time` limits `SELECT` statements only,** in milliseconds, default 0 (off). It applies to
   read-only `SELECT`s, and is ignored for `SELECT`s in stored programs. A write or a stored routine needs a
   different guard.
2. **`lock_wait_timeout` defaults to 31,536,000 seconds, one year,** and covers metadata locks: DML and DDL on
   tables, views and routines, and `LOCK TABLES`. A transaction holds the metadata locks of the tables it
   touched until it ends, and a DDL statement from another session blocks until then, so a migration behind one
   long transaction can wait for as long as the transaction lives. Set a short value in the session that runs
   DDL, and retry.
3. **`innodb_lock_wait_timeout` defaults to 50 seconds and covers row locks.** On timeout only the statement is
   rolled back, not the transaction, unless the server runs with `innodb-rollback-on-timeout`. The application
   must roll back or retry the whole transaction itself. The timeout does not apply to a detected deadlock:
   with detection on (default) one transaction is rolled back at once.
4. **`INSERT ... ON DUPLICATE KEY UPDATE` takes stronger locks than a plain `INSERT`.** On a duplicate it takes
   an exclusive index-record lock for a primary key and an exclusive next-key lock for a unique key, so
   concurrent upserts on neighbouring keys can deadlock. Keep the transaction short, touch rows in a
   consistent order, and index the columns used in `SELECT ... FOR UPDATE` and `UPDATE ... WHERE`.
