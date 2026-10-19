# go-container-runtime §3 — Shutdown

Applies to any supported Go version. The `main` exit rule is `go-conventions` §4.6.

## 3.1 Catch the termination signal
1. **Handle `SIGTERM` and `SIGINT` yourself.** The `os/signal` documentation says that by default a
   `SIGHUP`, `SIGINT` or `SIGTERM` makes the program exit, so without a handler a stop request ends the
   process with requests still in flight.
2. **Use `signal.NotifyContext(parent, signals...)`** to get a context cancelled by the signal, and **call
   its `stop` function** as soon as the work is done: the documentation says it releases resources and
   restores default signal behaviour. If you use `signal.Notify` with a channel instead, the channel needs
   buffer space for the expected rate; a buffer of one is enough for a single notification.

## 3.2 Stop the server with a deadline
1. **Call `Server.Shutdown(ctx)` with a context that has a deadline.** It closes the listeners, then closes
   idle connections, then waits **indefinitely** for active ones to go idle; if the context expires first it
   returns the context's error. A context without a deadline therefore waits forever.
2. **Make `main` wait for `Shutdown` to return.** `ListenAndServe` and its siblings return `ErrServerClosed`
   immediately once `Shutdown` is called, and the documentation says to make sure the program does not
   exit and waits for `Shutdown` to return. Treat `ErrServerClosed` from `ListenAndServe` as the normal path,
   not as a failure.
3. **A server cannot be reused after `Shutdown`**; a later `Serve` returns `ErrServerClosed`.

## 3.3 Long-lived connections
`Shutdown` neither closes nor waits for hijacked connections such as WebSockets. The caller notifies those
connections separately and waits for them, and `Server.RegisterOnShutdown` is the documented hook for
starting that notification. `Server.Close`, which closes everything immediately, is the abrupt alternative
and also ignores hijacked connections.

## 3.4 The deadline against the orchestrator's grace period
**Make the shutdown deadline shorter than the time the orchestrator allows between the termination signal
and the forced kill,** so the process exits by its own path. Own guidance: no orchestrator document was read
for this block, so the grace period value and its name are left to the deployment, not stated here.

## 3.5 Shape of `main`
Put the signal context, the server start, the wait and the `Shutdown` call inside `run() error` and let
`main` call `os.Exit` once, as `go-conventions` §4.6 requires, so deferred cleanup still runs.
