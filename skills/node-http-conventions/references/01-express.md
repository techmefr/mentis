# § 1 — Express

> Section 1 of `skills/node-http-conventions`. Read it when an Express route, middleware, error handler or
> proxy-related setting is written. Read 2026-10-02 from the Express 5.x guides (error handling, behind
> proxies; security and performance best practice pages and the 5.x migration guide, added 2026-10-20) and the
> Helmet README. Express 4 differs on point 1.

1. **Write handlers as `async` functions and let them throw.** In 5.x a handler or middleware that returns a
   promise calls `next` with the rejection by itself, so an `async` function needs no wrapper. A promise chain
   must be returned from the handler for the same to hold; a chain that is not returned must end with
   `.catch(next)`, otherwise the rejection is unhandled and can crash the process.
2. **Errors from callback APIs and timers are passed to `next` by hand.** A callback receives its error as the
   first argument and must forward it; a timer or event callback has no promise to carry a throw, so wrap its
   body in `try`/`catch` and call `next(err)`. Anything that never reaches `next` skips the error handlers and
   may end the process.
3. **Keep the asynchronous part of a handler trivial and do the work after it.** Processing inside a callback
   runs outside the framework's catch; doing it in the next handler of the chain brings it back under
   synchronous error catching.
4. **Error handlers have four parameters and come last.** Register them after every route and other
   `app.use`; several may be chained (log, then translate to a response), each calling `next(err)` unless it
   ends the response itself. A handler that neither calls `next` nor ends the response leaves the request
   hanging.
5. **Delegate to the default handler once headers are sent.** An error after the response has started cannot
   be turned into a new response; check the headers-sent flag and call `next(err)` so the framework closes the
   connection. Calling `next(err)` more than once for the same request can trigger the default handler even
   when a custom one exists.
6. **Set `NODE_ENV` to `production` in production.** The default handler returns the status text only in
   production and the stack trace otherwise; the status comes from the error's status property when it is in
   the 4xx or 5xx range, and is forced to 500 outside it. A custom handler produces the agreed body
   (`skills/api-design` §5) and never echoes the stack.
7. **`trust proxy` is set to exactly what the proxy does, never to `true` by habit.** Behind a reverse proxy
   the client address and protocol come from forwarded headers, which a client can forge unless the last
   trusted proxy overwrites them. Prefer a list of the proxy addresses or subnets. A hop count is safe only if
   every path to the app has the same number of proxies; if the client can reach the app through a shorter
   path, it can supply the address. With `true`, the proxy must remove or overwrite the three forwarded
   headers (for, host, proto). Anything that uses the client address (rate limiting, audit logs) depends on this.
8. **Set the security headers with Helmet, then adjust the ones your pages need.** One call sets a default set
   of response headers (the README says 13), including a restrictive content security policy and strict
   transport security. Each header can be disabled or configured by name; the content security policy usually
   needs a directive tuned to the page's own scripts and styles. Every disabled header is a decision to
   write down. A directive you pass is merged into the default policy; turn the defaults off to replace them,
   and set a directive to null to drop it. The default policy also asks browsers to upgrade insecure requests and
   the transport-security header pins HTTPS, which breaks a plain `http://localhost` session in some browsers:
   disable both in development only. The old XSS filter header is sent as `0` on purpose, since the filter
   itself is buggy. Helmet validates little, so check the final policy with a policy evaluator.
9. **Do not use Express's `res.render` default error page for an API.** Return the agreed JSON error body
   from your handler, since the default handler answers with HTML.
10. **Express 5 renamed and removed route syntax; a ported route can silently stop matching.** A bare `*` is no
    longer valid and needs a name (`/*splat`, which does not match the root: use `/{*splat}` for that);
    the optional marker `?` becomes braces; regular-expression characters in a path are gone; wildcard values in
    `req.params` are arrays; `req.body` is `undefined` (not `{}`) until a body parser runs, so a handler that reads
    a field from it throws on a request with no parser; the default query parser is the simple one, and
    `req.query` is read-only. Symptom: 404 on a route that worked on 4, or a TypeError on a missing body. Check
    each after a major upgrade (Express 5.x migration guide).
11. **No synchronous API and no blocking log call on a request path.** A synchronous call blocks every request
    for its duration; the console writers are synchronous when they point at a terminal or a file. Use a real
    logger (the guide names Pino) and find stray synchronous calls in development with `node --trace-sync-io`,
    never in production.
12. **Do not keep the process alive with an `uncaughtException` listener.** The guide's position is to log, exit
    and let a supervisor restart; a process that carries on after an uncaught error runs in an unknown state.
    Send CPU-heavy work to a worker pool, not one worker per request (`skills/node-async-performance` §3).
13. **Session and cookie defaults.** The default session cookie name identifies the stack, so rename it; set the
    cookie secure and not readable by client script; the default in-memory session store is documented as not
    meant for production, so use a shared store (and with several instances keep session state out of process
    memory). A cookie-based session stores the whole session in the cookie, around 4 KB per domain at most.
14. **An open redirect is a missing allow-list.** Redirecting to a URL taken from the query lets an attacker send
    users anywhere; parse it and compare its host against the expected one before `res.redirect`. Also remove
    `X-Powered-By` if Helmet is not in use, and put the 404 handler and error handler last.
