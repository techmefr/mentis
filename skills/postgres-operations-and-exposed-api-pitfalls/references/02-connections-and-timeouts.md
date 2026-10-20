# postgres-operations-and-exposed-api-pitfalls §2 — Connections and timeouts

Sources: the `conn-limits`, `conn-pooling`, `conn-idle-timeout`, `conn-prepared-statements` and `lock-short-transactions` rules of the `supabase-postgres-best-practices` skill in supabase/agent-skills at c9be0e9, read 2026-10-20; pooling-mode facts also covered by `skills/sql-conventions` §4.8.

> Managed or proxied databases: some settings below are fixed or limited by the provider or its pooler (pool size, which timeouts may be changed, whether named prepared statements work). Read what the provider documents, set what the driver or the role may set, and write "not applicable: set by the provider" for the rest; do not claim a server setting you cannot read.

## 2.1 The connection budget
1. **Each connection is a server process with its own memory, so connections are a budget, not a free resource.** A connection opened per request turns a traffic peak into exhaustion; a client should hold a small pool built once (the same rule as `skills/redis-client-and-cluster-pitfalls` §2.1).
2. **Put a pooler between many clients and the server, and size its pool to what the server can run at once,** which is related to cores, not to the number of users. The source gives a pool-size formula; it is a starting point to measure, not a rule.
3. **Raising the connection limit is not the cure for exhaustion.** More connections multiply memory and context switching and usually make queries slower. Shrink demand first.
4. **Sort by state:** count sessions grouped by state in the activity view. Many idle sessions point at a missing pool, many active ones at slow queries, many idle-in-transaction at application code holding a transaction open (§2.3).
5. **Memory per sort or hash is multiplied by concurrent operations:** the per-operation memory setting times the number of connections times operations per query must stay well inside the machine's memory, or the server is killed under load.

## 2.2 Pool modes and prepared statements
1. **In transaction pooling, a client gets a different server connection per transaction,** so a named prepared statement made earlier may not exist on the next one and the error reads "prepared statement does not exist".
2. **Fix it where the driver is configured:** disable server-side prepared statements in the driver (the source names the options for the common Node and Java drivers), use unnamed statements, or use session pooling for the code that needs them. Re-check after a driver upgrade changes the default.
3. **Session pooling holds a connection for the whole session** and gives back the features that need it, at the cost of fewer clients per server connection.

## 2.3 Timeouts
1. **Set an idle-in-transaction timeout.** A session that opened a transaction and went quiet holds locks and blocks cleanup (§1); the timeout ends it. Set it on the application's role, not server-wide, so maintenance sessions are not killed.
2. **Set an idle-session timeout for clients that never close.** The pooler has its own idle timeouts; keep them coherent with the server's so one does not kill what the other still counts as alive.
3. **Set a statement timeout for the role that serves requests,** and a shorter transaction-local one for a known-short unit. Without it one runaway query holds a connection until a person notices. With a tiny pool (one connection per instance, typical of serverless) the effect is sharper: one runaway query or one idle-in-transaction session blocks every request that instance serves, so the two timeouts matter more there, not less. Where the role cannot be altered, pass them as connection options in the driver.
4. **Keep the transaction as short as the unit of work.** No network call between begin and commit: take the lock, write, commit, and make the slow call outside (`skills/sql-conventions` §4.7).
5. **Log lock waits and set the deadlock timeout,** so a lock problem leaves evidence; the deadlock statistics column shows whether it has happened.

## 2.4 Checks (own guidance)
0. **Static check, no server needed:** read the driver configuration and grep the repository for the statement timeout, the idle-in-transaction timeout, the pool maximum, the prepared-statement flag and the TLS mode. Report each as set, not set or set by the provider; a timeout that appears nowhere is a finding, not an assumption.
1. Report connections by state before and after any pool change.
2. Run the application's test suite once through the pooler production uses, with prepared statements as the driver defaults them.
3. Kill the client mid-transaction in a staging run: the session is gone within the timeout and the lock is released.
