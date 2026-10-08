# nestjs-integration-patterns §5 — Queue retention, limiter failure, index dual write

Three small decisions that are normally left to defaults, and whose defaults fail slowly: finished jobs
that accumulate, a rate limiter whose store goes down, and a search index updated beside the database.
Job behaviour once a job runs (idempotency, overlap, payload compatibility) is `background-jobs-conventions`.

## 5.1 Queue job retention
1. **The default keeps every finished job.** In BullMQ, completed and failed jobs stay in their sets until you
   say otherwise, and each carries its data and result in Redis. A busy queue grows without bound.
2. **Set retention on both outcomes**: `removeOnComplete` and `removeOnFail` accept `true`, a number (keep
   the last N) or an object with an age in seconds and a count. Keep failures longer than successes, since
   they are what you debug; keep neither longer than your incident window needs.
3. **Removal is lazy**: it happens when new jobs finish, so an idle queue does not shrink.
4. **Retention and de-duplication interact.** A job id prevents re-adding the same job while it exists; once
   a finished job is removed, the id is free again. If dedup by id must outlive the job, it needs its own
   record.
5. **Job data must be serialisable and small**: store an identifier, not a large payload (Redis memory) and
   not a secret (it sits in plaintext, and in the failed set).
6. **Set `attempts`.** The default is one: no retry. With more, choose a backoff: fixed (the delay) or
   exponential (doubling per attempt from the delay), or a custom strategy. See `background-jobs-conventions`
   for what a retried job must tolerate.

## 5.2 Stalled jobs
1. **A stalled job is one whose worker stopped renewing its lock**, usually because a long synchronous task
   blocked the event loop. BullMQ checks every 30 seconds by default and, after the allowed stall count
   (default one), fails it with a message that it stalled more than allowed.
2. **Fix the cause, not the interval**: split CPU-heavy work, yield to the event loop, or use a separate
   processor process (see `node-async-performance` §2). Sandboxed processors help but lose dependency
   injection.
3. **Alert on stalled and failed counts** and on queue wait time, which is a different signal from execution
   time; both going quiet is also an alert.
4. **Prefer the BullMQ package**: the older queue package is in maintenance mode. Recurring work is
   registered as a scheduler, and a worker's job name is read in `process()`; see
   `nestjs-reliability` §2 for running schedules across replicas.

## 5.3 Rate limiter: decide fail-open or fail-closed
The Nest throttler documentation does not say what happens when its storage fails, and we did not run it.
The decision is ours; make it explicit.
1. **In-memory storage is per instance.** With several replicas the effective limit is multiplied by the
   replica count and resets on deploy. A shared store is required for a real limit.
2. **Behind a proxy, set the trust-proxy option and override the tracker** so the limit keys on the client
   and not on the proxy's address. IPv6 clients share a subnet prefix (64 by default in the documentation).
3. **Ttl is in milliseconds** in current versions; a value carried over from an older config is a thousand
   times too long.
4. **When the shared store is unreachable, choose per route.** *Fail open* (let requests through, log and
   alert) for general API traffic, because a cache outage should not become an outage of the service.
   *Fail closed* (refuse) for abuse-sensitive routes such as login, password reset and one-time codes,
   where unlimited attempts are the harm. Implement it by wrapping the storage in a class that catches
   errors and applies the chosen policy, and test it with the store stopped.
5. **Count what you can alert on**: limiter errors and limited requests as metrics.

## 5.4 Search index: do not write twice
A database write followed by an index write is a dual write; the core rule and its alternatives are in
`nestjs-reliability` §3. Practical points in addition:
1. **The index is derived data.** Write the database, emit through the outbox, and let a worker index with
   retries; or capture changes from the database log. A failure between the two then leaves a lag, not a
   permanent difference.
2. **Make indexing idempotent** (index by the entity's id, overwrite) and rebuildable from the database.
3. **Test against a real engine.** Do not mock the search engine in the end-to-end tests that matter: mapping
   and analyser behaviour are the risk. Run a container for it.
4. **Do not use the search engine for structured lookups** that the database answers exactly (by id, by
   unique key, by foreign key); it is eventually consistent and approximate.
5. **Expect and monitor lag**: record the age of the oldest unindexed change.

## 5.5 Verification
- After a day of traffic or a load test, the finished-job count in Redis is bounded.
- A job was made to block the loop beyond the stall interval and the alert fired.
- The limiter store was stopped and the login route refused while a read route still answered.
- The index worker was killed mid-batch and the index converged after restart.

## 5.6 Nest mapping
`@nestjs/bullmq` for queues (options passed per job or as queue defaults), `@nestjs/throttler` for the
limiter (the guard bound with `APP_GUARD`, a storage class for the shared store), and the outbox package
documented in `nestjs-reliability` §3 for the index feed.
