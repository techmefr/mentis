# nestjs-integration-patterns §1 — Microservice transports, WebSockets, Server-Sent Events

A handler that is not an HTTP route does not run in the HTTP pipeline's world. It has another exception
type the caller can read, another meaning for "response", and a lifecycle tied to a connection. The
principle: **find the channel's own error and completion model before writing the handler**.

## 1.1 Errors on a message channel
1. **Throw the transport's exception.** In a microservice handler throw `RpcException`; the caller receives
   `{status: 'error', message}`. An `HttpException` thrown there reaches the client as a generic internal
   error. Passing an object to `RpcException` returns that object as is.
2. **Pipes and guards follow the same rule.** Make `ValidationPipe` produce `RpcException` through its
   exception factory. A guard that returns false makes Nest throw an `RpcException` with a forbidden message.
3. **A custom filter's `catch()` returns an Observable**, usually `throwError(() => exception.getError())`.
4. **An event handler has no response stream.** An error a filter rethrows for an event pattern never
   reaches the producer; the filter must do the handling (log, dead-letter, metric). Do not design a producer
   that expects to learn the failure of an event.

## 1.2 Request-response versus event
1. **A message pattern is request-response.** It opens two logical channels and costs more; use it when the
   caller needs the answer. An event pattern is fire-and-forget; use it for notification.
2. **Both are valid only in controllers.**
3. **Several handlers for one event pattern all run, in parallel.** Do not rely on order between them.
4. **`send()` on a client is a cold observable, `emit()` is hot.** A `send()` nobody subscribes to sends
   nothing; an `emit()` goes out regardless.
5. **Always bound the wait**: pipe the observable through `timeout(ms)` and handle the timeout error. An
   unanswered request otherwise waits for the transport. After a timeout the outcome is unknown, see
   `nestjs-reliability` §4.7.
6. **The client is lazy**: connect it in `onApplicationBootstrap` so a broker problem fails at startup, not
   at the first call. Prefer an injected client over the `@Client()` decorator.
7. **Client listeners persist.** From Nest v12.1.1 an `on()` listener on a client stays until `close()` and
   is not deduplicated; registering inside a per-call path accumulates handlers.

## 1.3 Hybrid applications
1. **Global enhancers do not carry over.** Pipes, guards, interceptors and filters registered globally on
   the HTTP app (`useGlobal*()` or the `APP_*` providers) do not apply to a connected microservice unless
   `inheritAppConfig: true` is passed in the second argument of `connectMicroservice()`. Call the
   `useGlobal*()` methods before `connectMicroservice()`.
2. **Start order matters.** `startAllMicroservices()` before `listen()` lets handlers receive messages before
   `onModuleInit` and `onApplicationBootstrap` finished. Call `listen()` (or `init()`) first when handlers
   depend on initialised modules.
3. **Pre-request hooks** run before guards, interceptors and pipes on every handler call of a microservice; a
   hook must call `next()` or the handler never runs. They are global, apply only to microservices (not
   gateways), and are the place to start an `AsyncLocalStorage` context. Register them before initialisation.
4. **TCP transport has limits** (`maxBufferSize`, `incompleteMessageTimeout`, `maxSendBufferSize`); size them
   to the largest message you intend to send. Use `tlsOptions` when the network is not private.

## 1.4 WebSocket gateways
1. **A gateway is a provider**; it does not exist until it is listed in a module's providers. By default it
   shares the HTTP server's port.
2. **Use the decorators, not the raw-socket signature.** `@MessageBody()`, `@ConnectedSocket()` and `@Ack()`
   keep handlers testable; the two-argument raw form needs the socket mocked.
3. **Write to the client through the handler's return value.** Calling `client.emit` directly bypasses
   interceptors. Any return that is not `null` or `undefined` is sent, including `false` and `0`.
4. **Errors**: only a `WsException` reaches the client with its message; any other exception, including the
   validation pipe's default, is reported as an internal error. Make pipes throw `WsException`. The client
   receives an `exception` event with `status`, `message` and the `cause` pattern and data.
5. **Global filters do not apply to gateways**; guards and pipes, including global ones, do. A guard that
   returns false yields a forbidden `WsException`. Bind filters on the gateway or handler.
6. **Validate per parameter** (`@MessageBody(new ParseIntPipe())`): a pipe bound at method or gateway level
   runs for every parameter, the socket included.
7. **Rate limiting needs a custom guard** that overrides the throttler's `handleRequest`; do not register it
   globally, and expect an `exception` event when the limit is hit.
8. **Several instances need two things**, not one: an adapter over a shared store (the Redis adapter for
   socket.io) *and* either websocket-only transport or sticky sessions at the balancer. The adapter alone is
   not enough. Register it with `app.useWebSocketAdapter`. The plain `ws` adapter has no namespaces and
   throws if one is set; use a path.
9. **Request-scoped gateways exist** (a gateway instance per socket) at a performance cost; prefer
   singletons and read per-connection data from the socket. See `nestjs-di-traps` for the scope cascade.
10. **Lifecycle hooks** `OnGatewayInit`, `OnGatewayConnection`, `OnGatewayDisconnect` are where per-connection
    setup and cleanup go; clean up per-socket subscriptions in the disconnect hook.

## 1.5 Server-Sent Events
1. **A route with `@Sse()` returns an Observable of message events** (or a Promise of one). Nest subscribes,
   and unsubscribes when the client disconnects; put teardown in `finalize`.
2. **The async setup trap.** If the client disconnects while the handler's promise is still resolving, the
   Observable is never subscribed, so its teardown never runs and whatever the setup opened leaks. Take the
   abort signal parameter (`@SseSignal()`): it aborts on client disconnect, completion or error; check it
   during setup, make cleanup idempotent, and note it is undefined on a non-SSE route.
3. **If no `id` is set**, Nest assigns an incrementing one. Set your own when the client resumes from a last
   event id, since a counter restarts with the process.
4. **An event stream holds a connection open**: count it in the capacity plan and in the load balancer's idle
   timeout (send a periodic comment or event to keep it alive).

## 1.6 Verification
- Throw on each channel (handler, pipe, guard) and read what the caller actually receives.
- Disconnect a client in the middle of async SSE setup and confirm the resource is released.
- Run two replicas behind a balancer and send between sockets connected to different ones.
- With `inheritAppConfig` off, confirm which global enhancers are missing from the microservice.

## 1.7 Nest mapping
All of the above is Nest-specific; the transferable principles are 1.1.4 (events have no reply), 1.2.5
(bound every remote wait) and 1.5.2 (an async setup must be cancellable).
