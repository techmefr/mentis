# nestjs-reliability §2 — Locks, leases, fencing tokens and scheduled jobs on several replicas

A scheduler inside the application process runs in **every** replica. Three replicas and a nightly
export means three exports; a five-minute reconciliation that takes longer than five minutes overlaps with
itself, then with a third copy. The fix is not a flag, it is a lock that can be trusted, which is harder
than it looks. The principle holds for any Node service; the Nest mapping is at the end.

## 2.1 What a scheduled job does on N replicas, and why the quick fixes fail
1. **Every replica fires every schedule.** The visible symptoms are downstream: the accounting system
   records every invoice three times, the warehouse is asked for three full counts, every user gets the
   reminder email three times. The job's own logs look healthy, which is why it is found late.
2. **"Only run jobs on the instance with `RUN_JOBS=true`"** holds until a rolling deploy briefly has two
   such instances, or the one instance dies and nothing runs the job at all. It trades a duplicate for a
   gap and fails exactly during deploys.
3. **A `SET key NX PX ttl` at the top of the job** holds until its holder pauses for longer than the
   TTL (a stop-the-world GC, swap, a VM migration, a blocked event loop, a network partition): another
   replica takes the key, then the first wakes up and finishes the run believing it still holds it. Two
   writers again, and neither knows.
4. **An in-process overlap guard** (a "running" boolean, a cron option that skips a tick while the previous
   one runs) excludes within one process only. It is still worth having, but it is not what stops three
   replicas.
5. **A session-bound database advisory lock** needs one connection checked out of the pool for the whole
   critical section, is lost silently when that connection drops, cannot be renewed, and offers neither an
   expiry for a paused holder nor a fencing token. A lock stored as a row has all of that, through any pool.
6. **Alternatives that are legitimate, with their cost.** A dedicated worker replica that runs the jobs and
   no other replica does: simple, but there is a handover gap at every deploy and the replica is a single
   point of failure. A scheduler that only enqueues a job under a deterministic job id, so duplicate
   enqueues collapse in the queue: the work then runs on queue workers, and the queue's own deduplication
   window is the guard (§1 applies to the worker). Pick one deliberately and write down why; do not
   discover it.

## 2.2 A lock is a lease, held in a store every replica shares
1. A lock is a row (or key) with an **owner** (a random id per acquisition), an **expiry** and a
   **fencing token** (§2.4). The holder keeps it alive with a **heartbeat**, renewing every third of the
   lease; a crashed holder stops renewing and the lease expires on its own after one lease duration.
2. **Three operations, each a single conditional statement, never a read followed by a write:**
   - `acquire(key, owner, ttl)`: one `INSERT ... ON CONFLICT (key) DO UPDATE ... WHERE owner IS NULL OR
     expires_at <= now RETURNING token`. Of any number of concurrent callers exactly one gets a row.
   - `renew(key, owner, ttl)`: `UPDATE ... SET expires_at = ... WHERE key = ? AND owner = ? AND
     expires_at > now`, success only when exactly one row changed.
   - `release(key, owner)`: the same compare-and-set, clearing the owner.
   Checked in a separate `SELECT` first, a takeover slips in between and two holders exist. What a reader
   sees: sporadic double runs that vanish under single-threaded testing and cannot be reproduced locally.
3. **A process-local store is only a single-instance stand-in.** It excludes callers in one process; three
   replicas would each have their own and all three take "the" lock. Production without a shared store
   must fail at startup, not run silently.

## 2.3 Whose clock
1. **Expiry is measured on the store's clock**, not on each replica's, so every replica agrees on when a
   lock expires whatever their own clocks say. On PostgreSQL that is `clock_timestamp()`; `now()` is the
   start time of the current transaction, which is exactly what an expiry must not depend on (a long
   transaction would renew into the past).
2. **A holder counts its own deadline from the moment it *sent* the last renewal the store confirmed**,
   which is earlier than when the store processed it. A holder that is running therefore gives up no
   later than the store's expiry, so its abort signal fires before any other replica can take the key.
3. The window that remains exists only for a holder that is **not running** (paused, stopped, its event
   loop blocked): from the store's expiry until it runs again, it still believes it holds the lock.
   That window is what fencing closes.
4. Keep replica clocks synchronised anyway: the scheduler fires on the replica's clock, and a holder counts
   its own deadline locally.

## 2.4 Lease expiry is not mutual exclusion: fence the writes
Take a reconciliation on replica A. It reads counts from the warehouse (item: 12), then stalls for longer
than the lease. B takes the job over, reads fresher counts (three sold, item: 9) and writes them. A wakes up
and finishes with what it read before the pause: item: 12 again, and the shop sells three it does not have.
Cancelling A's signal at its next renewal is too late for a write already on its way.
1. **Every acquisition of a key gets a token greater than every token the key ever had**: across releases,
   expiries and restarts. The resource being written keeps the highest token it has seen and **refuses a
   lower one in the same statement that writes**:
   `UPDATE products SET stock = :n, stock_token = :t WHERE id = :id AND stock_token <= :t`. A's token is
   lower than B's, so its late write updates nothing; log the count of refused rows.
2. **Draw the token after the row lock, in the same statement as the takeover.** On PostgreSQL that is
   `nextval()` inside the `DO UPDATE SET`, not in the `VALUES` (which runs before the lock, so a later
   holder may already have passed it). Use `greatest(nextval(seq), old_token + 1)` so the row's own token
   is the floor and a sequence that went back (a restore, a failover to a lagging replica) cannot hand a
   key an old token.
3. **Release by clearing the owner, never by deleting the row**: a delete lets an insert that drew its
   token early win the key after a later holder had released, and hand out a smaller one.
4. **The token only helps when the protected resource checks it.** A lock around an external system that
   cannot compare tokens (a third-party API, an email service) is a best-effort exclusion, not a
   guarantee; say so in the design and make the effect idempotent (§1, §4.7).
5. **Redis as the lock store**: acquire with one script (`SET NX PX`, then `INCR` a counter in the same
   script), renew and release compare the owner in a script. The counter must never go back and a lock
   must never be evicted, so give Redis persistence and `noeviction`. A failover to an asynchronous
   replica can lose the lock taken just before it *and* the counter's last increments, after which the next
   holder may draw a token the previous holder already has and tokens no longer tell them apart. Where
   fencing must hold across a failover, keep the locks in the database whose sequence is in the same
   write-ahead log as the rows, or replicate synchronously.
6. **Pass the lease's abort signal to everything the job calls** (HTTP client, database driver). It aborts
   when a renewal is refused or the local deadline passes. A job that ignores it keeps running, as in any
   process; nothing is killed. The signal stops cooperative work, the token stops the rest.
7. **Alert on a lost lock.** It means another replica may be in the same critical section right now.

## 2.5 Running a scheduled job on one replica
1. **Explicit key on every job that must never run twice.** A default derived from class and method name
   changes when someone renames either; during a rolling deploy the old and the new replicas each run the
   job once. Reject two jobs with the same key at startup, and reject a job whose key is another job's
   lease or an election's key: they would exclude each other silently.
2. **Sticky ownership beats a race per tick.** A tick is not an instant: clocks differ by tens of
   milliseconds, so a per-tick lock would have to outlive the run by the skew, and a fast job would need a
   "ran at" record to stop a lagging replica from running the tick again. A lease held *between* ticks has
   none of that, at the cost of one replica running all of a job's ticks, which a scheduled job rarely
   minds. The other replicas skip the tick (log it at debug); nothing is queued.
3. **On owner death, up to one lease duration of ticks is skipped, and missed ticks are not caught up.**
   Nothing records when a job last ran. Write jobs that do **everything that is due**, not "yesterday's
   work": an export that takes every order without an invoice catches up the next night; a reconciliation
   that writes current counts costs five minutes of staleness. A job whose ticks each do something
   distinct keeps that record in its own table.
4. **Overlap is a second lock**, named after the same key, held for the whole run, renewed while it
   runs, released at the end. A tick that finds it held is skipped, on this or any replica; a crashed run's
   lock expires after the lease and the next tick runs. It works with or without sticky ownership
   ("any replica, one run at a time").
5. **A manual trigger (an admin endpoint that runs the job now) takes the same lock**, with a bounded
   wait, and answers `409` when it cannot get it. Contention is not the caller's mistake, so the lock
   layer carries no HTTP status; the handler decides. While the manual run holds the lock, scheduled ticks
   on every replica skip.
6. **A leader election is the same lease, held on purpose** for as long as the leader lives: one replica
   holds a single-subscriber connection (a feed that allows one connection per shop), the others retry
   each third of the lease. Run connect code on "acquired", disconnect on "lost" or step-down, tie the
   connection to the lease's abort signal, and carry the token on anything the leader writes. A paused
   leader still receives what the feed sends until its next renewal fails: the same blind spot, the same
   answer.
7. **Pick the lease duration** well above the store's round trip and the longest event-loop stall you
   accept, short enough that a crash does not skip too many ticks. About 30 seconds fits most jobs. A long
   run's lock is renewed at the same pace, so the lease does not need to cover the run.

## 2.6 Shutdown, observability, tests
1. **Hand leases back on SIGTERM.** Enable the platform's shutdown hooks so a deploy releases leases at
   once; otherwise each lease waits out its expiry and the job pauses for up to one lease at every deploy.
   Release locks before closing the store's connection pool, and close the pool in the last shutdown phase.
2. **A scheduled method that throws is logged and the schedule goes on** (the Nest scheduler wraps every
   `@Cron`, `@Interval` and `@Timeout` method in a try/catch). A job that silently *stops being
   scheduled* (process crashed, container descheduled, a typo in the expression shipped) is the failure
   nobody hears about until the report is missing. Report success per job and alert on **silence**: "job
   X has not succeeded in the last N hours". A rule that fires only for jobs that have reported at least
   once avoids paging for something not yet integrated.
3. **Test on several instances in one process on one shared store**: start N copies of the application on
   the same database, fire the same tick on each, assert one run. Then a paused one: use a manual clock
   for one instance so it stops renewing, let the database's clock expire its locks, let another take over,
   resume the first and assert its stale write is refused and its signal aborted. Then the overlap: hold a
   run open, fire three more ticks across two replicas, assert they were skipped.
4. **Run the store's contract tests against the real engine on a connection pool**, with many callers racing
   for each key. A single-connection embedded database serialises the statements and passes while the real
   thing would not.
5. Do not test the lock logic by calling the job method once: that passes with no lock at all.

## 2.7 Nest mapping
`@nestjs/schedule` fires every `@Cron()`, `@Interval()` and `@Timeout()` in every process; `ScheduleModule.forRoot()` must be imported **once**
(each additional import registers every handler again, so three imports run each job three times).
`waitForCompletion: true` on `@Cron()` stops overlap on one instance only.

The Nest 12 docs describe a `@nestjs/locks` package:
- `@OnOneInstance({ key })` next to the schedule decorator: sticky ownership through a `<key>:owner` lease;
  `@WithoutOverlapping()`: the run lock named after the same key; the two share the key.
- `Locks.withLock(key, fn, { wait })` and `acquire()` for manual runs; errors for contention carry no HTTP
  status.
- `LocksContext` carries `fencingToken` and `signal` through async local storage into every service the job
  calls (the scheduler calls the method with no arguments).
- `@LeaderElection(key)` on a singleton provider with acquired/lost callbacks.
- The store is **not shipped**: implement `LockStore` (`acquire`, `renew`, `release`, each taking the key
  and owner first, durations in whole milliseconds) in a provider that registers itself with the registry;
  production without a store fails at startup unless in-memory is allowed explicitly. A contract test suite
  with a concurrency option is exported.
- The default lease is 30 seconds, renewals every third of it; call `app.enableShutdownHooks()`.
- Lost locks, leadership gained and lost are exposed as events and on diagnostics channels.
