# § 2 — Fastify

> Section 2 of `skills/node-http-conventions`. Read it when a Fastify route, schema, hook, plugin, deployment
> setting or test is written. Read 2026-10-02 from the Fastify documentation (main branch): recommendations,
> validation and serialization, hooks, testing.

1. **Every route has a schema for what it accepts and what it returns.** The input schema validates; the output
   schema serializes through a compiled serializer, which is faster than generic JSON serialization and keeps
   fields not in the schema from leaving the process. It is the cheapest guard against leaking an internal
   field.
2. **Know what the default validator does to your data.** Its default configuration coerces types (including
   scalars to arrays), applies defaults and removes additional properties where the schema forbids them. A
   string `"5"` arriving for a number becomes `5`: say so in the schema when that is wanted, and switch coercion
   off for the request parts where it is not (it can be configured per part: body, query, params, headers).
   With coercion on, a union with a nullable primitive may coerce a value to null.
3. **Keep the validator's "all errors" mode off.** Enabling it makes validation do more work per request and
   makes denial of service easier on untrusted input. Turn it on only for a route that needs complete
   feedback, and never on a latency-sensitive one. Never compile schemas from user input: the compilers use
   code generation that is unsafe with user-provided schemas.
4. **No database access during validation.** The asynchronous validation feature may be used, but the
   documentation warns against it for initial validation since a lookup there is a denial-of-service lever;
   do asynchronous checks in a `preHandler` hook after validation.
5. **A custom validator returns an error object, it does not throw.** The contract is a value or an error
   value; a throw in a validator used with asynchronous pre-validation hooks becomes an unhandled rejection.
6. **Validation error text reaches the client by default.** The response includes the schema's message, which
   can expose internal field names. If that is not acceptable, format it with the schema error formatter or
   translate it in the error handler (`skills/api-design` §5 for the agreed shape). Per-route handling is
   available with the attach-validation option.
7. **Use hooks and plugins, not generic middleware,** on performance-sensitive paths; Fastify's middleware
   adapters work but native hooks are typically better. Hooks are scoped by encapsulation: a hook registered
   in a plugin applies to that plugin's routes, which is how a rule is limited to one area.
8. **A hook is either callback-style or `async`, never both.** In an `async` hook (or one returning a promise)
   the completion callback is not available; calling it anyway can invoke handlers twice. In the earliest
   request hook the body is not parsed yet, so authorization that needs the body belongs in a later one.
9. **Keep routes simple on hot paths.** Regular-expression routes are expensive and many parameters can hurt
   the router; version constraints cost router performance, and asynchronous custom constraints are a last
   resort.
10. **Put the app behind a reverse proxy,** which terminates TLS, redirects HTTP to HTTPS, serves multiple
    domains and static files and spreads load over instances; the project calls exposing the app directly an
    anti-pattern. Running several app instances in one process is fine (a metrics endpoint on a separate port
    is the documented case).
11. **Listen on an address the probe can reach.** The default is the loopback address, which a Kubernetes
    readiness probe addressed to the pod IP cannot reach: listen on all interfaces or give the probe a host.
12. **Size instances by measurement.** The guidance is a rule of thumb, not a standard: about 2 vCPU per
    instance for lowest latency (the second serves the garbage collector and thread pool), fewer for
    throughput; measure with a load tool on your own configuration before fixing a number.
13. **Test with injection.** `inject` sends a fake request through the whole lifecycle after plugins have booted,
    needs no open port, and returns the response to assert on. Build the app in a function that takes options
    so each test gets a fresh instance, and close it at the end of each test so connections to external
    services are released. Start a real listener only for what injection cannot cover.
