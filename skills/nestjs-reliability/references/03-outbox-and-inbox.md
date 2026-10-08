# nestjs-reliability §3 — Transactional outbox and consumer inbox

Saving a row and announcing it are two writes to two systems, and no transaction spans both. The outbox
turns the announcement into a row written in the same transaction as the business change; a relay
publishes committed rows afterwards; the consumer remembers which message ids it already processed. The
principle holds for any Node service with a relational database; the Nest mapping is at the end.

## 3.1 The dual-write problem, in the three shapes it takes
1. **Save, then publish.** A crash or a broker outage between the two leaves the order saved and the event
   lost: no confirmation email, no stock reservation, analytics undercounts, and nothing logs an error
   because nothing failed at the time.
2. **Publish, then save.** The insert fails after the event is out: the customer is thanked for an order
   that does not exist.
3. **Retry the publish on error.** A timeout after a successful send looks like a failure, so the retry
   sends it again: two emails.

Anything that publishes from memory has this problem: a framework event emitter, an in-process event bus,
a message-client `emit()`. "After commit" dispatch narrows the window and does not remove it (what
`background-jobs-conventions` covers); only a durable row written with the data does.

## 3.2 The write side
1. **Insert the message in the same transaction as the business row.** Both commit or neither does.
   Anything that throws after the message was written, including a failure on the next line, rolls the
   order and its message back together, and the relay never sees them.
2. **Pass the transaction handle, never the database, the pool or an autocommit client.** Writing the
   message through the global handle commits it on its own, which is the dual write again, and a
   rolled-back order still sends its email. A correct implementation refuses a non-transaction handle with an
   error; a stand-in that applies the write immediately (an in-memory store) cannot join your transaction
   at all and should warn the first time it receives one. What a reader sees when this is wrong: an order
   that does not exist and a confirmation email that was sent.
3. **One message per destination.** A message goes to exactly one transport. The same fact for an in-process
   handler and for another service is two messages added in the same transaction, which lets each have its
   own key and retry state.
4. **The payload is a snapshot** serialised when the message is added; later changes to the object are not
   published. Version it (§3): a message added by the previous release can be delivered after a deploy.
5. **Wake the relay after commit** if the latency matters; otherwise the message goes out at the next
   poll, up to the poll interval later. Never publish inside the transaction.
6. **Keep the transaction short.** Adding keyed messages takes a per-key lock so that transactions adding
   the same key take turns; a long transaction holding it stalls every producer of that key. Check any
   interactive-transaction time limit of the ORM (a few seconds by default for some).

## 3.3 The relay
1. **Claim** a batch with a lease and a per-claim token, using `SELECT ... FOR UPDATE SKIP LOCKED` or an
   equivalent so two relays never take the same row. Publish the claimed messages; on success mark them
   published; on failure reschedule with backoff; after the attempts run out move them to a dead-letter
   table with the error of every attempt.
2. **Every later write for a message (published, rescheduled, dead-lettered) presents the claim token.**
   This is the fencing of §2.4 applied to a message: a relay that stalled past its lease cannot overwrite
   the work of the relay that took over. Without it, a slow relay un-publishes or double-schedules a
   message the second one already handled.
3. **Never start a publish with less than the publish timeout left on the lease**; release the rest of the
   batch instead. Keep the publish timeout well below the lease (a third is a reasonable ratio). A handler
   that outlives it counts as a failed attempt, and its abort signal fires; a handler that ignores the
   signal keeps running, and a retry reaching the same process should wait for it instead of running the
   handler twice.
4. **A relay that dies after publishing and before recording it publishes the message twice.** That is the
   at-least-once guarantee, and the inbox (§3.5) is what absorbs it. Nothing is lost with a dead instance,
   because nothing lives on it: the messages are rows.
5. **Relay topology is a deployment decision.** A producer-only instance runs with the relay off; a
   relay-only worker is an application context with no HTTP server whose poll timer keeps it alive until a
   shutdown hook stops it. The "wake now" signal only reaches the relay of the instance that added the
   message, so another relay picks the message up within one poll interval.
6. **Drain on SIGTERM**: stop claiming, let in-flight publishes finish (each bounded by the publish
   timeout), release the leases on claimed-but-not-started messages so another instance takes them at
   once. This needs the platform's shutdown hooks enabled, and the database pool closed after.
7. **Leases use the relay's clock** in this design, so keep hosts' clocks synchronised well inside the
   lease; where the store offers a clock, prefer it (§2.3).

## 3.4 Ordering
1. **Order exists only within a key**: messages sharing a key are published one at a time, in the order
   their transactions committed, whichever instance added them. Without a key, no order is promised.
2. **The order is the store's own numbering assigned at commit**, not the message ids (an id comes from its
   instance's clock, and clocks differ). That is why adding keyed messages serialises the producers' transactions.
3. **A retrying message holds back its key.** While `placed` is being retried, `cancelled` waits behind it,
   so consumers never see a cancellation before the order it cancels. Other keys keep flowing.
4. **A dead-lettered message unblocks its key**: later messages with that key are published without it. So
   size the retry budget to the outages you expect (§3.7); once it is spent, order is no longer guaranteed.
5. **Do not share a key across messages for different destinations.** The key is shared by every message
   that carries it, whatever the topic or transport; if the mail message used the order id as well, a mail
   outage would hold back that order's analytics events.
6. **The consumer has to preserve the order too**: handlers are asynchronous, two events for one order can
   run at once, and the cancellation can commit before the placement. Run one key's events one at a time
   in arrival order and different keys in parallel.

## 3.5 The inbox: consumer-side deduplication
1. **Each consumer keeps a table of processed message ids, keyed by (consumer name, message id).** Before
   running a handler it checks the table; after the handler succeeds it records the id. The primary key is the
   arbiter: two concurrent deliveries of one message meet there, the second waits for the first transaction
   and skips the handler if it committed.
2. **Message ids must be stable across redeliveries** (the id assigned when the message was written, not one
   minted per send), and **a requeue from the dead letters keeps the same id**, so consumers that already
   processed it skip it. That is how a requeued message reserves stock without sending a second
   confirmation email.
3. **The consumer name must stay stable.** Entries are keyed by it, so a renamed consumer treats every past
   message as new and replays the lot.
4. **The gap**: if the process dies after the side effect and before the id is recorded, the effect repeats on
   redelivery. Acceptable for an email; not for a stock reservation. Close it when the effect is in the same
   database as the inbox by **recording the id inside the handler's own transaction**: the record and the
   reservation commit together, a redelivery finds the record, and a failure rolls both back so the retry
   starts clean (the record call is awaited inside the transaction, so a missing `await` cannot let a
   duplicate through). This is exactly-once **for writes to that one database**. For an effect outside it
   (email, an external API), you have at-least-once, or you pass the downstream an idempotency key (§4.7).
5. **A handler can opt out of the inbox** and run on every delivery: that is at-least-once with all that
   implies; do it only for handlers that are naturally repeat-safe.
6. **A service that only consumes needs only the inbox**, in its own database, next to its own tables, with
   the relay off. It never reads the producer's tables.
7. **Prune the inbox.** Nothing does it for you. Run a scheduled prune with a window longer than any
   redelivery, requeues from the dead letters included (§2 for running it on one replica).

## 3.6 Delivery guarantees, in one table
| Situation | Outcome |
|---|---|
| The business transaction rolls back | The message never existed and is never published |
| The transaction commits | Published eventually, or dead-lettered with its error history |
| A relay dies after claiming | Another relay publishes it once the lease expires |
| A relay dies after publishing, before recording | Published twice; the inbox drops the duplicate |
| A publish or handler fails | Retried with backoff, then dead-lettered |
| A handler outlives the publish timeout | A failed attempt; the signal aborts; a handler ignoring it keeps running |
| A non-retryable error | Dead-lettered at once |
| A message is dead-lettered | Its key is unblocked; later messages overtake it |
| A fire-and-forget transport (raw TCP, core pub/sub) | "Published" only means the bytes left; a consumer crash afterwards loses the message |

The overall guarantee is **at least once, with inboxes absorbing the duplicates**. For events you cannot
lose, publish to a transport whose broker acknowledges receipt (a replicated log, a queue with publisher
confirms, a persistent stream).

## 3.7 Retries and dead letters
1. **Bound the retries and back off with jitter**; the default should fit the outages you actually have.
   Twenty attempts doubling up to five minutes cover roughly half an hour to an hour; ten attempts capped
   at a minute give up after a few minutes, and then the key's later messages overtake the dead one.
2. **Separate permanent from transient failures.** A handler throws a dedicated non-retryable error when
   retrying cannot help (no stock will appear); the message goes straight to the dead letters where a person
   decides. When several handlers fail, the message is rejected only if all of them threw the permanent kind;
   otherwise it is retried, the handlers that already succeeded are skipped by their inbox, and it is
   rejected once only permanent failures remain.
3. **A topic with no handler in this process is retried, not dead-lettered.** During a rolling deploy, an
   old instance's relay can see a topic only the new version handles.
4. **The dead-letter store has an owner.** List, inspect, requeue (fresh retry budget, same id) and purge
   behind real authorisation: the dead letters hold full payloads, customer data included. Requeue and
   purge refuse an empty filter; "all" is an explicit flag. Replaying or purging in a shared environment is
   a human decision (`background-jobs-conventions` Guardrails).
5. **Alert on**: the age of the longest-waiting message (lag), the dead-letter count, dead-letter events,
   and lease-lost events (another relay took a message over mid-publish, so it may reach consumers twice).

## 3.8 The tables belong to the store
1. **The outbox, the dead letters and the inboxes live in the same database as your business rows**,
   because they must commit with them, on a database server that outlives any instance. Never keep them in
   memory, in a file database on the instance's disk, or on a container filesystem: when the task is
   replaced, every unpublished message goes with it.
2. **They are not part of your ORM's schema** and your migrations do not create them: the store owns its own
   schema (or a table-name prefix where the engine has no schemas), so your migration tool does not drift or
   drop them. A column named in your tool's diff for those tables is a sign they were mixed in.
3. **Apply the store's migrations before the new version starts**, as a deploy step, not at application boot
   in production: booting instances changing a schema in the middle of a rolling deploy locks busy tables and a
   least-privilege database user cannot do it anyway. Check migration status in CI. The store's migrations only
   add tables, columns and indexes, so the previous version keeps running on the migrated schema; there are no down
   migrations.
4. **Isolation level**: the store's own transactions (claims, dead-letter moves, requeues) rely on READ
   COMMITTED. Your transactions may run at any level; under REPEATABLE READ or SERIALIZABLE, two deliveries
   racing on one message can fail the second with a serialisation error instead of skipping it, and the
   retry then finds the record. Check the database's default level at startup.
5. **On MySQL-family engines** a deadlock rolls your whole transaction back and the store cannot run your
   work again: the error reaches your code, and the transaction has to be run again by you.
6. **Size the connection pool for requests and the relay**: each claim holds a connection for one short
   transaction.

## 3.9 Verification
1. **Rollback test**: let the message be written, then fail the transaction on the next line. The row and the
   message disappear together; the relay claims nothing; no email is sent.
2. **Publish-after-commit test**: the downstream handler has not run before the relay is driven, and has run
   once after.
3. **Duplicate test**: deliver the same message twice (once sequentially, once concurrently on two instances
   against a real database with a pool): the effect happens once.
4. **Crash test**: kill a relay holding a lease; another publishes after the lease expires; the consumer
   skips the repeat.
5. **Ordering test**: make the first message of a key fail, add a second; the second is not published
   before the first is retried or dead-lettered.
6. **Downstream outage test**: stop the consumer, add messages, watch the lag grow and the retries log,
   restart it, watch them go out in order.
7. Run the store's contract tests against the real engine and major version on a pool. An embedded
   single-connection database runs the races one at a time and cannot show a lost one.

## 3.10 Nest mapping
Documented in the Nest 12 docs as the `@nestjs/outbox` package.
- `Outbox.add(tx, message | messages)` takes the transaction handle first (with the ORM-specific
  transaction: the callback argument of the ORM's transaction helper, an entity manager from a transaction,
  an interactive-transaction client) and refuses the database itself; `Outbox.notify()` wakes the relay.
- `@OnOutboxMessage(topic, { consumer })` registers an in-process handler; it must be on a **singleton**
  provider, and `consumer` is required and must stay stable. `inbox: false` opts out.
  The handler context carries the message, an abort `signal` and a `processInTransaction(tx, work)` that
  records the inbox id in your transaction (exactly-once for the same database).
- Outside Nest handlers, `OutboxInbox.process()` and `processInTransaction()` do the same for any consumer,
  including a separate microservice that receives the message through a transport client.
- Routing sends each message to exactly one named transport; the built-in local one runs the handlers.
- The relay has its own options (poll interval, batch size, lease, concurrency, publish timeout) and the
  retry has attempts, backoff with jitter and a `retryIf` hook; a dedicated error class marks a permanent
  failure.
- `OutboxDeadLetters` lists, requeues and purges; the package mounts no HTTP route, so expose it behind your
  own guard.
- The store is **registered by you**: a Postgres and a MySQL store are provided, taking an executor for each
  of several ORMs. Production without a store fails at startup unless in-memory is allowed. A command-line
  tool applies and checks the store's migrations.
- Run with the relay switched off in API-only replicas by an environment variable and call
  `app.enableShutdownHooks()`.

## 3.11 Related smaller rules
- **Payload versioning**: add fields, never rename or remove, for at least one deploy (`background-jobs-conventions` §4).
- **A search index kept by the application in a separate write after the database write is a dual write**:
  drive it from an event, the outbox, or change data capture, and do not mock the search engine in end-to-end
  tests.
- **A queue enqueue after commit** has the same lost-message window as any publish; where the job matters,
  the outbox row is the durable record and the enqueue is its relay.
