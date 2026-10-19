# nestjs-integration-patterns §6 — Structured request logging

A request log is only useful if every line produced while serving a request carries the same identifier,
the lines are machine-readable, and nothing sensitive is in them. The principle: **one request context,
carried implicitly, configured once**. What to log and which metrics to keep is `observability-instrumentation`.

## 6.1 Set it up once
1. **Register the logger module once**, in the root module. Re-importing it in a feature module installs the
   request middleware a second time and every request is logged twice, with no error.
2. **Buffer logs until the logger exists**: create the app with log buffering on, then switch to the pino
   logger before initialising or listening, so startup lines use the same format.
3. **Needs a recent Nest and Node**: the version of the pino integration read here requires Nest 11.0.8 or
   12.0.2 and Node 22.12 or later.

## 6.2 Request context without request scope
1. **Carry the context in `AsyncLocalStorage`**, not with request-scoped providers: request scope re-creates
   providers per request and cascades to every consumer (see `nestjs-di-traps`).
2. **A child logger per request** carries the request id on every line. Use the integration's `assign()` to
   add fields (the user or tenant, once known) to later lines of the same request.
3. **Outside HTTP**, wrap the unit of work in the library's context runner: queue processors, scheduled
   tasks, CLI commands. Without it those lines have no request id. For microservices, enable the
   integration's microservice option (it uses the pre-request hook in `01-transports.md` §1.3).
4. **A per-class injected logger does not work inside a lazy module** (`03-module-composition.md` §3.3).

## 6.3 The request id
1. **Generate an id at the edge and return it** in a response header so a support report can quote it.
2. **Accept an incoming id only from a trusted edge** (the load balancer, an internal caller). A client-chosen
   id is untrusted input; unbounded or malicious values pollute logs. This rule is ours, not from the library.
3. **Propagate it on outbound calls** (HTTP and messages) so another service's lines join the same trace.
4. **On Fastify**, the id generator belongs to the adapter, not the logger options.

## 6.4 Do not log what you must not keep
1. **Do not include request or response bodies by default.** The integration leaves payload logging off
   because payloads carry personal data. Turn it on per route when needed.
2. **Redact** authorisation headers, cookies, tokens and known personal fields with the logger's `redact`
   paths, and test it with a real request.
3. **Do not log the error and rethrow at every layer**; log where it is handled (see `nestjs-node-conventions`).

## 6.5 Flushing on shutdown
Asynchronous destinations and transports may not flush when Nest's shutdown hooks re-raise the signal; the
last lines before a crash or deploy are the ones you need. From `@nestjs/core` 11.1.10, enabling shutdown
hooks with the process-exit option makes Nest exit explicitly after the hooks and gives the logger time to
flush; this changes the exit code, so check what the orchestrator expects. Verify by killing the process
with a signal and reading the last line.

## 6.6 Verification
- One request produces N lines, each with the same id; the id is in the response header.
- A line from a queue processor has an id too.
- A request with an authorisation header and a body shows neither in the log.
- Each request is logged exactly once.

## 6.7 Nest mapping
`nestjs-pino` (an MIT package) wraps pino-http and `AsyncLocalStorage` for Nest; the principles above
hold for any logger that offers context propagation.
