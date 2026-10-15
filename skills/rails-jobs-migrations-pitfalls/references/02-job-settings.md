# rails-jobs-migrations-pitfalls §2 — Job settings

Sources: the GoodJob README (4.21.1) and the Solid Queue README (1.7.0), read 2026-10-08.

## 2.1 Timeouts
1. **Do not wrap a job's work in Ruby's `Timeout`.** The GoodJob README calls it dangerous and points to
   two articles on why. Set timeouts on the client that does the waiting (HTTP open and read timeouts, database
   statement timeouts) and tell Active Job what to do with the resulting exceptions: `discard_on` or `retry_on` for
   `Net::OpenTimeout` and `Net::ReadTimeout`, for example.
2. **If a Ruby `Timeout` cannot be avoided,** the same README puts it in an `around_perform` with its own error
   class, so the timeout is a named, handled failure and not a stray exception in the middle of the job.
3. **Process heartbeats do not detect a stuck job.** Solid Queue says a single stuck job can stay claimed while its
   worker process is alive, and that stronger detection needs an explicit timeout or watchdog on top.

## 2.2 Queues and priority
1. **Split queues by the latency a job can tolerate, not by what it does.** GoodJob's README argues that one slow
   job blocks every job behind it once it has started, and that priority cannot help then, since a started job
   cannot be preempted; the fix is a separate queue sized for short jobs, with its own workers. Heterogeneous jobs
   in one queue make waiting time unpredictable.
2. **In Solid Queue choose queue order or priority, not both.** The README recommends not mixing them, because a
   list of queues is polled in the order given and priority only orders jobs within a queue. With exact queue
   names and no paused queues polling is cheapest; wildcards are allowed only alone or at the end of a name.
   Smaller priority numbers run first.

## 2.3 Concurrency limits
1. **A concurrency limit is not a scheduling tool.** With Solid Queue's `limits_concurrency`, excess jobs are blocked
   or, with `on_conflict: :discard`, thrown away; blocked jobs are unblocked by priority and **queue order is
   ignored**, so jobs of one concurrency group in different queues do not follow a worker's queue order.
2. **`on_conflict: :discard` can lose work for the length of `duration`** if a running job fails to release the
   semaphore, and the default duration is three minutes. Set `duration` to a value longer than the job can take,
   because the guarantee holds only for that long.
3. **Do not combine concurrency limits with bulk enqueue** (`perform_all_later`): limited jobs must be enqueued one
   by one, so bulk enqueuing gives nothing, and discarded ones come back with `successfully_enqueued` false.

## 2.4 Database and shutdown
1. **On MySQL or MariaDB, run the queue database at `READ COMMITTED`.** Under the default `REPEATABLE READ` InnoDB
   takes gap locks on the indexes Solid Queue polls, which can deadlock enqueuing against claiming under heavy load;
   the README sets `transaction_isolation: READ-COMMITTED` in `database.yml`.
2. **A graceful stop is bounded.** Solid Queue sends `TERM`, waits `shutdown_timeout` (5 seconds by default) and
   then sends `QUIT`, and jobs still in flight on `QUIT` go back to the queue. GoodJob's own default is to wait
   forever (`-1`), so set a value below the platform's kill deadline (own guidance on the margin).
3. **Check for shutdown inside long loops.** GoodJob offers `GoodJob.current_thread_shutting_down?` for this; a README
   suggests calling it from inside a loop. Stopping early and re-enqueueing with the progress made, rather than
   being interrupted mid-record, is own guidance.
