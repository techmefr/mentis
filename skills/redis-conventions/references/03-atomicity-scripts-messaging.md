# § 3 — Atomic updates, scripts, and messaging limits

> Section 3 of `skills/redis-conventions`. Read it when two clients can touch the same key, when a script
> is written, or when the server is used to pass messages.

1. **Read, change, write across two calls is a race.** Two clients that read the same value, both add one,
   and both write it back leave the value one short. Use the server's own atomic command (increment,
   append to a hash field, add to a set) wherever one exists; it is atomic by itself and is the cheapest
   form of the fix.
2. **When no single command expresses the update, use optimistic locking or a script, in that order of
   effort.** A transaction queues commands and runs them as one isolated unit; it does not read in the middle,
   so on its own it cannot express "read, compute, write". Pair it with watching the keys: if any watched key
   changes, including by expiry or eviction, the transaction is refused and the caller retries. From 8.4 the
   server also offers a single conditional set and a single conditional delete that compare the current
   string value, which replaces the watch loop for plain string keys; confirm the deployed version before
   relying on them.
3. **A transaction is not a database transaction.** If a queued command fails at execution time (a wrong
   type on one key), the others still run; there is no rollback. A command rejected at queue time causes the
   whole transaction to be refused. Validate the types and the preconditions before queueing, and do not
   treat a partly applied transaction as impossible.
4. **A script runs as one atomic unit and blocks the server while it runs.** That is its value (read,
   compute, write with no interleaving, close to the data) and its cost: a slow script stalls every client.
   Keep scripts short, with a bounded amount of work, and put no waiting and no network call in them.
5. **A script receives every key it touches as a declared key argument, and everything else as an ordinary
   argument.** The script must not build key names from its own logic or from data it reads: that breaks on a
   sharded deployment, where the declared keys are what the router uses to find the right node. Parameterise
   one generic script instead of generating a variant per call; generated variants fill the script cache and
   exhaust memory.
6. **Treat the script source as part of the client application.** A cached script can be missing after a
   restart or a failover, so the client loads it again on a missing-script error rather than assuming it is
   there. Version the script text in the repository next to the code that calls it, and never compose its body
   from untrusted input (§5.6).
7. **Publish-subscribe delivers at most once.** A message sent while a subscriber is disconnected is gone,
   and there is no acknowledgement. It is right for ephemeral notifications such as cache invalidation hints
   where a missed one is caught by a short expiry (§2.1). Where a message must be processed, use a stream
   with consumer groups, which persists entries and supports acknowledgement and re-delivery, and make the
   consumer idempotent (`skills/background-jobs-conventions`).
8. **A list used as a queue loses work on a consumer crash** unless the consumer moves the item to a
   processing list atomically and removes it only after success. The cheaper rule: do not build a reliable
   job queue from a list; use a stream, or the queue the framework already provides, and keep the server for
   what it is good at.
9. **A lock built on a key is a lease, not a guarantee.** Set it with a unique value and an expiry in one
   command, release it only if the value is still yours (a compare-and-delete, in one atomic step), and
   remember that a holder can pause past its expiry and keep acting after another has taken the lock. Work
   protected by such a lock must tolerate that: write with a fencing token or an idempotent operation, not
   with trust in the lock.

**Sources:** the vendor's documentation on transactions, Lua scripting (EVAL intro: declared keys, script
cache, atomic execution), pipelining versus scripting, and publish-subscribe delivery semantics, read
2026-10-02, and its distributed-locks page for the unique-value, expiry and compare-before-release shape
of point 9. Points 8 and the fencing clause of 9 are reasoning of ours, not a quotation of a page.
