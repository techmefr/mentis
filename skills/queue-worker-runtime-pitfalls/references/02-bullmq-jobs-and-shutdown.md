# queue-worker-runtime-pitfalls §2 — BullMQ jobs, shutdown and lost locks

Sources: the BullMQ documentation of taskforcesh/bullmq at 84e3424 (`guide/retrying-failing-jobs.md`, `patterns/stop-retrying-jobs.md`, `guide/jobs/job-ids.md`, `guide/going-to-production.md`, `guide/workers/graceful-shutdown.md`, `guide/jobs/stalled.md`, `guide/troubleshooting.md`), read 2026-10-16. Defaults quoted here are the pages' and are version-bound.

## 2.1 Throw Error objects
1. **A processor must throw `Error` instances.** The retry page says BullMQ does not work correctly with other thrown values, and points to the lint rule that forbids throwing literals. Turn that rule on in the worker code.

## 2.2 Say when a failure must not be retried
1. **Throw the library's unrecoverable error class for a failure no retry can fix** (a payload that fails validation, a record that no longer exists). The job moves to the failed set at once, and this overrides the `attempts` given when the job was added.
2. **Rate limiting is the exception to the attempts count.** A job that is rate limited and re-queued through the rate-limit error is not counted as a failure, so the attempts check is skipped. To cap it, compare `attemptsStarted` with the job's `attempts` option inside the processor and throw the unrecoverable error when it is reached.
3. **The two counters differ:** `attemptsMade` goes up on any error except the rate-limit, delayed and waiting-for-children signals; `attemptsStarted` goes up every time the job moves to active.
4. **Own guidance:** send a terminal error to the failed set deliberately and read it there; the retry limits, back-off and dead-letter rules themselves are in `background-jobs-conventions`.

## 2.3 Job ids and payloads
1. **A custom job id is how a job is deduplicated:** adding a job whose id already exists in the same queue is ignored, not queued twice. Ids are unique per queue, and automatic ids are counters per queue.
2. **The duplicate check ends when the job is removed.** A job taken out by hand or by `removeOnComplete` or `removeOnFail` no longer counts, so the same id can be added again. If an id must stay unique for a day, retention has to cover that day (own guidance), or the uniqueness belongs somewhere durable.
3. **No colon in a custom id.** The separator is also Redis key syntax, and the id would be split in two; use a dash or an underscore.
4. **An id of only digits is rejected,** because it collides with the automatic counter ids, and the call throws. Prefix a numeric business id (`job-123` in the page).
5. **The payload is stored in clear text.** Keep sensitive data out of it (pass an identifier and read the record in the processor); if that is impossible, encrypt the sensitive part before adding the job. The page treats this as a serious concern, not a nicety.

## 2.4 Shutdown
1. **Handle both `SIGINT` and `SIGTERM`, and close the worker in the handler.** `SIGINT` is the interactive interrupt; `SIGTERM` is what orchestrators and process managers send to stop a service.
2. **`close()` stops the worker taking new jobs and waits for the active ones to finish or fail, and it has no timeout of its own.** The page tells the reader to make sure jobs end in a timely way.
3. **A job that outlives the grace period before the hard kill is left active, and stalls** (2.5): it is picked up by another worker later, after a wait the page puts at about 30 seconds by default. The page says explicitly that closing the worker does not guarantee no stalled jobs.
4. **Own guidance:** set the platform's termination grace period above the longest normal job, or keep jobs short enough that it is true; exit the process after the close promise resolves, as the page's handler does.

## 2.5 Stalled jobs and the lost-lock error
1. **A worker renews a lock on the job it is running.** If it cannot, because it crashed or its event loop is blocked, the job returns to waiting and the queue emits a stalled event. There is no stalled state, only the event.
2. **A job that stalls more than the allowed count fails for good** with a message saying it stalled more than allowed. The default allowance is one, on the page's reasoning that stalls should be rare.
3. **Avoid stalls by not blocking the event loop longer than the lock window** (30 seconds by default), or by running the processor in a separate process, which the page calls a sandboxed processor.
4. **'Missing lock for job' means the lock vanished and the worker only found out when it tried to finish the job.** The page's causes: the worker was too busy to renew the lock, it lost its Redis connection, the job or the queue was removed by an API call, or Redis evicted keys because the memory policy is not `noeviction`.
5. **Own guidance:** when the error shows up, check the four causes in that order against the worker's CPU graph, its reconnect logs, recent job removals and the Redis memory policy, before raising any timeout.

## 2.6 Checks (own guidance)
1. Add a job with an id containing a colon and one made of digits and confirm both are refused or fixed in the producer.
2. Throw the unrecoverable error in a processor with several attempts and confirm one run only.
3. Send SIGTERM to a worker with a job running longer than the grace period and confirm the job is seen to stall and is picked up by another worker.
