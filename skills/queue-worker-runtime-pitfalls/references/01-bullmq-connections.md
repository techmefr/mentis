# queue-worker-runtime-pitfalls §1 — BullMQ connections

Sources: the BullMQ documentation of taskforcesh/bullmq at 84e3424 (`guide/going-to-production.md`, `guide/connections.md`, `patterns/failing-fast-when-redis-is-down.md`, `guide/troubleshooting.md`), read 2026-10-16. The behaviour described is the package's at that commit; the pages say the separate scheduler class stopped being needed from BullMQ 2.0, so older answers on the web may not apply.

## 1.1 The code that adds jobs and the worker want opposite behaviour
1. **BullMQ reconnects to Redis by itself, and a job-adding call made while the connection is down does not fail: it waits until the connection returns.** That is the right default for a background process and the wrong one for a web request, which would sit on a hung call.
2. **For an adder in a request path, make it fail fast.** The page's example turns the client library's offline command queue off, so the call throws when Redis is unreachable, and the handler catches it and answers 503. The same connections page also offers a low per-request retry count instead (the default it states is 20; it suggests 1 when the user should get an error quickly). Either way the caller decides whether to retry or give up.
3. **For a worker, wait without limit.** The retry count per request must be null, so that errors raised by Redis on some commands do not break the worker, and the offline queue stays on. A worker created by BullMQ sets the null itself; passing in an existing client, or a different value, overrides it, and the library prints a warning. Treat that warning as a defect to fix.
4. **Adding a job from inside a worker's processor is background work,** and may share the worker's connection (the connections page's wording).
5. **The library's own reconnect policy for the connections it creates** is exponential back-off with a floor of one second and a ceiling of twenty seconds, retried forever. Override it through the client's options when another policy is needed.
6. **A limitation the failing-fast page states:** Redis must be reachable at the moment the queue object is created. Own guidance: test the startup order (service before Redis) as a separate case, because 2 and 3 above do not cover it.
7. **With another client through an adapter (node-redis or Bun in the documentation), the same split applies** and is configured on that client's own reconnect and timeout options. The page lists three cases to test before production: Redis down at startup, a short network drop while jobs run, and a graceful shutdown with active jobs.

## 1.2 No `keyPrefix` on the client
1. **Do not set the ioredis `keyPrefix` option on a connection given to BullMQ.** The connections page calls it incompatible and points to BullMQ's own `prefix` option on the queue and worker.
2. **Own guidance:** the repository holds a changelog entry (third major version) saying an exception is thrown when the option is used, so the failure may be loud or silent depending on the version in use; the rule is the same.

## 1.3 Undefined arguments reach the server as a Lua error
1. **A queue name or job argument that is undefined, an empty string, or an object where a string was expected ends in a Lua script error** that says its arguments must be strings or integers. The troubleshooting page traces it to environment variables passed straight through.
2. **Validate required variables at startup and throw with a clear message,** before the queue is created. A default is acceptable only when it is a value that is valid in production.

## 1.4 Errors must be heard
1. **Attach an `error` listener on every queue and every worker.** The page's reason: connection problems are reported through that event, and without a listener they surface as unhandled errors.
2. **Handle uncaught exceptions and unhandled rejections once, process-wide,** since Node ends the process on them by default. The page presents this as a general Node rule that matters more for workers.

## 1.5 Persistence and eviction
1. **Redis keeps nothing durable unless it is configured to.** The page recommends the append-only file with a one-second sync as enough for most applications, and tells the reader to benchmark the cost.
2. **`maxmemory-policy` must be `noeviction`.** It is the only setting the page says guarantees correct queues; an evicting policy removes keys arbitrarily and is one of the causes of the lost-lock error (2.5). The rest of the Redis side is in `nestjs-reliability`.

## 1.6 Checks (own guidance)
1. Stop Redis, call the adding endpoint, and confirm an error response within the request budget.
2. Keep the worker running through the same outage, restart Redis, and confirm a queued job is processed without restarting the worker.
3. Start the service with the queue name variable unset and confirm it fails at startup with a readable message.
