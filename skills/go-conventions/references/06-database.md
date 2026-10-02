# go-conventions §6 — database/sql and SQL access

> Section 6 of `skills/go-conventions`.

1. Parameters are placeholders. A query string built by concatenation or formatting with caller input is a
   defect whatever the source of the input.
2. Every call has a context: the `...Context` variant of query, exec and transaction begin, so a cancelled
   request releases its connection.
3. Rows are closed right after the query succeeds (`defer rows.Close()`), and the iteration error is read
   after the loop. A statement that returns no rows uses exec, not query, otherwise the connection stays
   checked out.
4. "No rows" is a normal outcome: test it with `errors.Is(err, sql.ErrNoRows)` and map it to a domain
   error. A nullable column is scanned into a pointer or a null-aware type.
5. Related writes share one transaction. A row read in order to be modified is locked in the read
   (`SELECT ... FOR UPDATE`) or protected by a version column. A serialization failure retries the whole
   transaction, not the failing statement.
6. The pool is configured explicitly (open connections, idle connections, connection lifetime, idle time);
   the defaults leave the open side unbounded.
7. Batch writes in bounded chunks: neither one round trip per row nor one statement of millions.
8. Migrations come from a migration tool run outside the application code. The agent writes the access
   code and does not design a schema or its indexes: that needs data volumes and access patterns it cannot
   see, so it proposes and a human decides.
9. Business rules stay in the Go code, not in triggers, views or stored procedures the code cannot see.
