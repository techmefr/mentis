# nestjs-reliability §1 — Idempotency keys

A client that loses the response cannot tell a lost request from a lost answer, so it sends the same
request again. An **idempotency key** lets the server run the operation once per key, store the outcome,
and answer every repeat with that outcome. The rules below hold for any HTTP or message handler in Node;
the Nest mapping is at the end.

## 1.1 Why a state check alone does not protect a write
Two repeats fail in two different ways, and a "is it still pending?" check in the service covers neither
completely.
1. **The repeat arrives after the first finished.** The check sees "already paid" and the client gets an
   error for a payment that went through. It sees a failure where it should see the original receipt.
2. **The repeat arrives while the first is still running.** Both pass the check before either writes, and
   the card is charged twice. This is the one that costs money, and it only shows under concurrency, so a
   test that sends the requests one after the other never finds it.

Keep the state check anyway, as a conditional update (`UPDATE ... WHERE status = 'pending'`). The key
deduplicates repeats of one attempt; two taps that mint two keys are two attempts, and only the state
check stops the second.

## 1.2 What the client has to do
The server can only deduplicate what the client sends consistently.
1. **Create the key when the user decides, not once per request.** Every retry of that decision sends the
   same key, including after the app is killed and restarted, so the key is saved with the pending action.
   A key regenerated on each retry deduplicates nothing and the symptom is a duplicate that "only happens
   on bad networks".
2. **Create a new key only for a new decision** (another card after a decline, an edited cart). Sending an
   old key with a different body is a client bug and must be refused (§1.4), not silently accepted.
3. **Read the outcome by code, not by status alone.** A 409 can mean "the first attempt is still
   running, wait and ask again" or "the order is already paid, final". Retry the first; stop on the second.
   Retry on no response, on 5xx and 429 (with the same key, after `Retry-After`), and never on a 4xx that
   is a deterministic answer: every repeat with that key gets the same answer.

## 1.3 What the server does with a request that carries a key
1. **Fingerprint the request**: a hash of the scope, the method, the URL and the body with object keys
   sorted. A client-chosen timestamp inside the body would make every repeat look different, so exclude
   fields that legitimately vary between repeats from the fingerprint, and nothing else.
2. **Claim the record atomically** under the record key `<scope>:<key>`. Of any number of simultaneous
   claims for a free key, exactly one wins; the rest read the winner's record (§1.5).
3. **Run the handler once**, renewing the claim while it runs so a slow handler does not lose it to a
   repeat, then turn the claim into a completed record that holds the status, the body and a short
   allowlist of headers that describe the body (location, content type, content language, ETag). Cookies,
   CORS and rate-limit headers belong to the first request and are never replayed.
4. **Answer repeats from the record**: in flight is `409` with `Retry-After`; completed replays the stored
   status and body and marks the response as a replay; same key with a different fingerprint is `422`.
   A missing key on an endpoint that requires one is `400` before any work is done. A payment without a key
   cannot be retried safely, so refuse it instead of charging unprotected.

## 1.4 Scope the key to the caller, and authenticate first
Without a scope, all clients share one namespace and a key one user picks can replay another user's
receipt. Scope by the authenticated principal (user or tenant id). The scope needs the caller identified,
so the key is claimed **after** authentication: an unauthenticated request must be rejected before it can
use up a key. Where one shared namespace is deliberate (a webhook keyed by the provider's event ids), say
so explicitly rather than leaving the scope out by accident.

## 1.5 The store: shared, durable, atomic
1. **A process-local store only excludes callers inside that process**, and loses its records on every
   restart. With two replicas, a repeat landing on the other one finds nothing; with one replica, a repeat
   after a deploy runs the payment again. In production the store is a database or a cache every instance
   reaches, even for a single instance.
2. **Acquire is one conditional write**, never read-then-write: `INSERT ... ON CONFLICT (key_hash) DO
   UPDATE ... WHERE expires_at <= now RETURNING` (or one Lua script on Redis). When no row comes back,
   someone else holds the key: read their record and report it. A read followed by an insert lets both
   callers in, which is exactly the double charge.
3. **Hash long record keys** (scope, client key, and for GraphQL the field path) before using them as a
   primary key, and store the response as plain `json`, not `jsonb`: `jsonb` rejects a NUL character that
   a response body can contain.
4. **On a cache store, disable eviction** (`maxmemory-policy noeviction`). Every record has a TTL, so the
   volatile eviction policies evict them too, and an early eviction is a double charge waiting to happen.
5. **Prune expired rows from a scheduled job**, with the expiry re-checked in the `DELETE` itself so a row
   a retry just took over stays. Expired rows are ignored in the meantime.
6. Expiry is measured on each instance's clock in this design, so keep clocks synchronised; prefer the
   store's clock where the store offers it (§2.3).
7. The store has to pass a **contract test with real concurrency**: many callers racing for each key on a
   connection pool, the owner checks, expiry. A store tested only sequentially, or on a one-connection
   embedded database, passes while being wrong.

## 1.6 An owner token on every attempt
Each attempt that claims a key gets a random **owner** id, and every later write on the record
(`extend`, `complete`, `release`) is conditional on that owner **in the same statement as the write**.
If a stalled attempt wakes after its claim expired and a retry took the key over, its late `complete`
changes nothing, instead of overwriting the retry's record. Checked in a separate read first, a takeover
slips in between and the stale attempt wins. This is the same fencing idea as §2.4, applied to a record.

## 1.7 Which outcomes are stored
1. **Anything below 500 is stored and replayed**: success, and deterministic client errors (validation,
   declined, not found, already paid), which would give the same answer again. A replayed error is
   rebuilt from status and body, so a filter that tests `instanceof` against a custom exception class sees
   the base class on a replay.
2. **A 5xx or an unknown error releases the key**, so a retry runs the handler again: most failures happen
   before the side effect.
3. **Streams and responses written directly to the socket cannot be replayed**: release the key and log a
   warning, do not store a half answer.
4. **The gap**: a 5xx that happens *after* the side effect (the provider charged the card, then the local
   write failed). The released key lets the retry charge again. Close it one of three ways, in order of
   preference: give the downstream provider its own idempotency key derived from the user id **and** the
   client's key (the client's key alone is not enough, two users can send the same one); or store the
   failure for that handler and make the client start a fresh attempt, throwing a dedicated error only for
   the post-effect failure; or write the effect and its message in one transaction (§3).

## 1.8 Lifetimes
1. **TTL** (how long a completed result replays) must exceed the longest time any client keeps retrying.
   If the client queues offline payments for a day, 24 hours is too short: after the TTL the key is
   forgotten and a repeat runs again, which should end in a "already paid" conflict by the state check
   rather than a second charge, but the customer loses the receipt.
2. **Lock TTL** (how long an in-flight claim survives once renewals stop) only has to cover a crash: the
   claim is renewed every third of it while the handler runs, so a long charge keeps it and a crashed
   instance blocks the key for at most that long. A renewal that cannot reach the store must be logged, and
   alerted on: the attempt's outcome is then not in the store and a retry may run the handler again.
3. **`Retry-After`** on the 409 is a few seconds, not one: the typical duration of the slow call.

## 1.9 What a replay skips, and what it must not leak
1. A replay returns the stored body exactly: it skips serialisers and any interceptor that runs inside the
   idempotency layer. Anything that strips fields on the way out (an "exclude" decorator) would have been
   applied before storing, but one placed *outside* the layer sees a plain object on a replay and can
   send what it was meant to hide. Keep the idempotency layer outermost.
2. **Store the minimum.** The whole response is stored and there is usually no size limit, so keep
   idempotent responses small.
3. **Encrypt the records at rest when the response holds personal or payment data**: authenticated
   encryption with a random IV per record, the record key included as authenticated data so a record
   copied under another user's key fails to open, plain-text records rejected once encryption is on, keys
   at least 32 random bytes. Turn it on before the first record is stored. Rotate in three deploys: add the
   new key as second, then make it first, then drop the old one only after the TTL has passed. A replay
   whose key was removed too early must **fail closed** (a 500 that names the record as unreadable), never
   re-run the handler: the record proves the effect already happened.
4. Browsers need the header allowed and the replay marker and `Retry-After` exposed in the CORS
   configuration, or the client code never sees them.

## 1.10 Message handlers
A broker delivers at least once, so the same rule applies to event handlers.
1. **Derive the key from the data, not from the send.** A key generated on each publish is different on
   every redelivery and deduplicates nothing. `order-paid:<order id>` is the same for every delivery of
   that fact.
2. **Records belong to the handler**, not just the key: two handlers reacting to the same event each keep
   their own record, so each still handles every event exactly once.
3. **The TTL is long** (days): a message can return from a dead-letter queue long after the first
   delivery.
4. **A duplicate that arrives while the first delivery is running is rejected as "in use". With a broker
   that acknowledges messages, do not acknowledge that delivery**: let the broker redeliver later, when it
   will be skipped as completed.
5. Event ids are unique across the system, so no scope is needed; one record store is still shared per
   service, and when several services share one Redis each gets its own key prefix, because handler names
   are only unique inside a service.

## 1.11 Verification
1. Send the same request twice **sequentially**: one side effect, the second answer identical to the first
   and marked as a replay, the downstream provider called once.
2. Send it twice **concurrently** against a deliberately slow downstream: one `2xx`, one `409` with
   `Retry-After`, one downstream call.
3. Reuse the key with a different body: `422`. Omit the key on a required endpoint: `400`.
4. Kill the process mid-handler (or stop renewals) and confirm the key becomes usable again after the lock
   TTL, and the late attempt's completion changes nothing.
5. Restart the service between the two requests: the replay still works. (A process-local store fails here.)

## 1.12 Nest mapping
Documented in the Nest 12 docs as the `@nestjs/idempotency` package; its decorator is `@Idempotent()` and
it works on HTTP routes, GraphQL mutations and microservice handlers, following the IETF
`Idempotency-Key` header draft.
- Register the module once, in the root module, with a scope function that reads the authenticated user:
  guards run before interceptors, so the user is known when the scope is computed.
- The store is **not shipped**: implement the `IdempotencyStore` contract (`acquire`, `complete`,
  `release`, `extend`, each taking the record key and the owner first, durations in whole milliseconds) in
  a provider that registers itself with the registry in its constructor. Registration is single and locks
  at module init; with `NODE_ENV=production` and no store, startup fails unless in-memory is allowed
  explicitly.
- The package ships a contract test suite for a store, with a concurrency option. Run it against the real
  database on a pool.
- `required`, `ttl`, `lockTtl`, `retryAfter`, `keyFrom`, `fingerprint` and `storeIf` can be set per
  handler. `keyFrom` takes a payload field for events.
- The module is an app-wide interceptor, so import it **before** other modules that register global
  interceptors (the first registered runs outermost) and keep response-shaping interceptors out of the
  global list; the module refuses to start with the class-serialising interceptor in front of it.
- Events for replays, rejections and lost locks are exposed as a stream and on diagnostics channels;
  alert on lost locks.
