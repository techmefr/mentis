# queue-worker-runtime-pitfalls §3 — Graphile Worker

Sources: the Graphile Worker documentation of graphile/worker at 4cda192 (`website/docs/error-handling.md`, `job-key.md`, `tasks.md`, `scaling.md`, `index.md`), read 2026-10-16. The files do not name the library version they describe, except that one note mentions a behaviour from 0.16 on; treat numbers as version-bound.

## 3.1 What a task must do
1. **A task that throws, or whose promise rejects, fails the job, and the job is retried with exponential back-off.** The introduction gives the default as 25 attempts over about three days.
2. **Await every asynchronous step before returning.** The page warns that a task which leaves a promise running is judged a success as soon as it returns, so a failure afterwards is lost. No untethered promises.
3. **The library does not open a database transaction for the task's queries.** The helper that borrows a client and the query helper both leave transactions to the caller; the page adds that long transactions cut throughput by holding clients from the pool.
4. **Split a large job into several small ones,** which the page recommends both for parallelism and for tasks that are not idempotent, with sending mail as its example: a retry of a large job repeats every side effect that already happened. Idempotency itself is in `background-jobs-conventions`.
5. **A task with an array payload may return an array of promises of the same length.** Entries that reject are re-queued as a job whose payload holds only those entries, so a batch does not redo its successes.

## 3.2 Shutdown, hard kills and stale locks
1. **A termination signal starts a graceful shutdown:** the worker stops taking jobs, lets the running ones finish, and exits. If a second signal arrives after five seconds, the shutdown becomes forceful: running jobs are failed, so they retry on another worker after their back-off, and the process exits. Restart workers through the graceful path.
2. **A kill the worker cannot handle** (an immediate process exit, a crash, `SIGKILL`, a lost machine) leaves its jobs locked for at least four hours. Workers sweep for locks older than four hours every eight to ten minutes, and with many workers the release lands near the four-hour mark.
3. **To release such jobs earlier, clear the lock columns on the relevant job rows.** The page allows it; own guidance: do it by hand, only after confirming the worker that held them is really gone, because a job released while still running runs twice.
4. **Own guidance:** a platform that kills containers without a grace period turns every deploy into this case; set the grace period (BullMQ's version of this is in `02-bullmq-jobs-and-shutdown.md`, part 2).
5. **A new library version that brings a database migration sends a notification, and running workers on 0.16 or later shut down when they receive it.** Own guidance: the process supervisor must restart them, or a deploy ends with no worker running.

## 3.3 Job keys
1. **A job key identifies a pending job so it can be replaced, rescheduled or removed.** Adding again with the same key updates the job instead of queueing another, which gives debounce, throttle and one-at-a-time scheduling.
2. **The key is unique across the whole table while the job is pending or failed,** so a reused key can replace a job of a different task and payload. The page suggests building the key from the task identifier.
3. **Three modes decide what happens on a match:**

| Mode | Effect | Suited to |
|---|---|---|
| replace (default) | overwrites the unlocked job, run time included | debounce: each event pushes the run later |
| preserve run time | overwrites everything except when it runs | throttle: at most once per period |
| unsafe dedupe | returns the existing job untouched, even if it is running or has failed for good | nothing the page recommends |

4. **The unsafe mode can drop the event that triggered the add.** The job that was found may be finished or dead, and nothing runs for the new event. The page strongly advises against it unless the caller is certain.
5. **A job that is running when the same key is added is not replaced:** a second job is scheduled and both run, while the running job loses its key and cannot run again after a failure. Removing a running job by key likewise only stops its retries.
6. **Array payloads are concatenated, but only when both the old and the new payload are arrays.** If either is an object, the old payload is lost. Combined with the preserve-run-time mode this makes a fixed batching window; with the default mode each event pushes the window out.
7. **Completed jobs are deleted,** so removing a completed key does nothing, and there is no permanent log of keys.
8. **Under very high contention on one key an add can return null.** Check for it and retry, throw or otherwise handle it; the page links an open issue.

## 3.4 Perma-failed jobs
1. **The jobs table must stay small for the queue to stay fast,** which is why finished jobs are deleted. A job that fails for good is left in place for debugging, and a pile of them slows the queue; so does a large number of jobs scheduled far ahead.
2. **A job should not end in perma-failure.** The page's advice: the task detects its own repeated failure, records it in the proper place, and returns successfully so the library deletes the job. A long-term failure log does not belong in the jobs table.
3. **Clear perma-failed jobs on a schedule, by a person.** Find why they failed and fix the task, then lower the attempts count so they retry, or delete them. The page's delete statement targets a private table whose layout may change in a patch release, and says it should be run by a human after inspecting the jobs; do not put it in a cron entry.
4. **The table churns heavily,** so vacuum it in a quiet period. The page leaves the exact options undecided (it says so itself), so choose them from the database's own advice.

## 3.5 Checks (own guidance)
1. Start a worker on a task that sleeps, send it one termination signal, and confirm the job finishes; then repeat with two signals more than five seconds apart and confirm the job is failed and retried.
2. Add the same key twice with an object payload and then with array payloads and confirm the first replaces and the second concatenates.
3. Count the perma-failed rows after a load test; a non-zero count is a task to fix, not a table to empty.
