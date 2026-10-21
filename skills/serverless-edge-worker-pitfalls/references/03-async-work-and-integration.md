# serverless-edge-worker-pitfalls §3 — Async work and integration

Sources: `references/runtime-patterns.md` (architecture section) and `references/platform-apis.md` of the `workers-best-practices` skill, and `references/rules.md` of the `durable-objects` skill, in cloudflare/skills at 86505e4, read 2026-10-20.

## 3.1 Queues and workflows
1. **Move slow, retriable or non-urgent work out of the request:** email, webhooks, multi-step processing. The handler accepts the work and answers with an accepted status.
2. **A queue decouples producer and consumer and delivers at least once** (Cloudflare Queues delivery guarantees page: duplicates are rare but possible; use a unique id as idempotency key). The same message can arrive twice, so the consumer must be safe to run twice: a natural idempotency key, a unique constraint, or a check of the effect before applying it (`skills/background-jobs-conventions`).
3. **A workflow persists each step's result and retries only the failed step,** and can run for a long time. Use it for multi-step durable processes; a queue in front of it buffers a high-throughput entry point.
4. **The result of a step must be serializable by the workflow's own contract;** check it in the platform documentation rather than assuming JSON.

## 3.2 Calling other functions
1. **Call another function of the same platform through a service binding,** not through its public URL. The binding stays inside the platform and supports typed calls; the public URL adds a network hop and an exposed endpoint.
2. **Handle a failing downstream explicitly:** timeout, a bounded retry for safe requests, and a response that says what failed. Own guidance: no retry of a write without an idempotency key.

## 3.3 Database connections
1. **Opening a database connection per invocation costs a handshake and an authentication every time,** and a burst of functions exhausts the database's connection limit (`skills/postgres-operations-and-exposed-api-pitfalls` §2).
2. **Route external-database traffic through the platform's connection pooling service,** and read its connection string from the binding. Create the client per request as the source directs and let the service hold the pool; do not cache a client in module scope (§2.1).
3. **The pooling service has its own supported databases and a Node-compatibility requirement:** re-read before choosing it.

## 3.4 Durable state
1. **Use one durable object per entity that needs coordinated state,** found by a deterministic name. In-memory state in it must be reconstructible from storage: the object can be evicted or restarted at any time.
2. **Prefer the SQL-backed storage for new classes and inspect the backend of an existing class before choosing an API.**
3. **For idle WebSocket servers use the hibernation form and plan how connection state is restored after waking.**
4. **A new class needs a migration entry, and its configured name must match the exported class.**
5. **Details of storage gates, alarms and migrations live in the vendor's documentation;** the source deliberately points there, and so does this block.

## 3.5 Serialization boundaries
1. **There is no single serialization rule across the platform's APIs.** A queue message follows its configured content type (JSON-compatible data, text, bytes or a structured-clone form); a durable-object key-value write accepts structured-clone values, so a map or set is allowed; SQL parameters accept only the SQL API's types; a WebSocket sends a string or binary, so objects are encoded first.
2. **Do not ban a value across the board on one API's rule, and do not assume one API accepts what another does.** Check the API at each boundary.

## 3.6 Other platforms (own guidance, not from the source)
1. **Initialise clients, load configuration and open connection pools outside the handler** so a warm container reuses them (Lambda developer guide: static initialisation is the usual place to open database connections, with a check that the connection still exists); keep per-request data inside it, since global variables hold their value across invocations.
2. **Set the function's timeout below the caller's timeout,** so the function fails first and cleanly, and size memory for the largest realistic payload, not the average.
3. **Treat the first request after idle as slower** and measure it separately before blaming code (Lambda guide: initialisation code runs only on a new environment and is the largest contributor to first-call latency; the environment is also recycled every few hours); nothing here quotes a number.

## 3.7 Checks (own guidance)
1. Deliver one queue message twice in a test: the effect happens once.
2. Run a burst of invocations against a staging database: connections stay under the limit.
3. Restart a durable object in a test: its behaviour is unchanged.
