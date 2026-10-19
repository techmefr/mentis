# § 1 — Express

> Section 1 of `skills/node-http-conventions`. Read it when an Express route, middleware, error handler or
> proxy-related setting is written. Read 2026-10-02 from the Express 5.x guides (error handling, behind
> proxies) and the Helmet README. Express 4 differs on point 1.

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
   write down.
9. **Do not use Express's `res.render` default error page for an API.** Return the agreed JSON error body
   from your handler, since the default handler answers with HTML.
