# ofetch-client-pitfalls §2 — Retry, timeout and shared defaults

> Part 2 of `skills/ofetch-client-pitfalls`. Read it when a client is configured for reliability or shared by
> several call sites. Sourced from the README of unjs/ofetch (commit `1dbc37f`, the README of its second major
> version in alpha), read 2026-10-16. Sentences marked "own guidance" are ours.

## 2.1 Retry
1. **A failed call is retried if its status is in `retryStatusCodes`.** The default list is 408, 409, 425,
   429, 500, 502, 503 and 504. `retry` sets the number of retries and `retryDelay` the pause in milliseconds
   between them; the default delay is 0.
2. **The default is one retry, but not for POST, PUT, PATCH or DELETE.** The README says ofetch does not retry
   those by default, to avoid side effects.
3. **A custom `retry` value overrides that and retries all requests, writes included.** The README says so in
   one sentence. Own illustration: `retry: 3` on a client shared with a POST makes a POST that got a 502 after the
   server had done the work run up to three more times.
4. **Own guidance:** retry a write only when the server can recognise a repeat (an idempotency key it stores,
   or an operation that is naturally repeatable), and set `retry` per call for those calls, not on a shared
   instance.
5. **Own guidance:** a zero delay turns a retry against an overloaded server (503, 429) into an immediate second
   hit. Set `retryDelay` and keep the number small; the README gives no backoff option, so a growing delay
   needs your own wrapper.
6. **The list includes 409 and 429**, which are not always transient. Narrow `retryStatusCodes` to the
   statuses your server uses to mean "try again".
7. **Verify** with a stub server that returns 503 once and then 200: count the requests for a GET, for a POST
   with default options and for a POST with `retry` set.

## 2.2 Timeout
1. **The timeout is off by default.** `timeout` takes milliseconds and aborts the request after that long.
2. **Set one on every client.** Own guidance: pick a number per kind of call (a health check and a file
   download do not share a value), and decide whether retries share the deadline or get a fresh one; the
   README does not say whether each attempt has its own timeout, so test it.
3. **Verify** by pointing the client at a server that accepts the connection and never answers, and checking
   that the call ends with the timeout error near the configured time.

## 2.3 Interceptors
1. **There are four hooks:** `onRequest` (as soon as ofetch is called, may change `options`), `onRequestError`
   (the fetch itself failed), `onResponse` (after the call and after the body is parsed) and `onResponseError`
   (like `onResponse`, but only when the response is not ok). Each receives the request, the options and, where
   relevant, the response or the error.
2. **A hook may be an array of functions**, called one after another.
3. **Put shared hooks on an instance** made with `ofetch.create`, not on each call.
4. **Own guidance:** a logging hook must not print the whole `options` or the request headers, because they
   hold tokens; log the method, the path without its query, the status and the duration. The README's logging
   examples print the full request, and they are examples, not a policy.
5. **Own guidance:** a hook that adds a header or a query value runs on every retry, so make it idempotent (set
   the header, do not append to it).

## 2.4 Shared defaults with `ofetch.create`
1. **`ofetch.create({ baseURL: '/api' })` returns a client with those defaults**, so `apiFetch('/test')` is the
   same as `ofetch('/test', { baseURL: '/api' })`.
2. **Defaults are cloned one level deep and inherited.** The README warns to be careful with nested options such
   as `headers`. Own guidance: do not assume a call-site `headers` object is merged with the instance's;
   write a test that sends one call with its own header and prints what the server received, and build one
   instance per audience (public, authenticated) instead of overriding headers per call.
3. **Extra headers go in `headers`**, and are added to the request defaults.

## 2.5 Extra options with types
1. **Augment the `FetchOptions` interface** with a `declare module "ofetch"` block in a file included by the
   project's TypeScript configuration. The README's example adds `requiresAuth?: boolean`, readable as
   `context.options.requiresAuth` inside a hook and passable per call.
2. **Own guidance:** a flag that changes what a hook does (whether to attach a token) is a contract between the
   instance and its callers; put it in one documented place and test the hook for both values.

## 2.6 Proxy and certificate settings
1. **In Node, proxy support is not automatic.** The README says Bun and Deno read `HTTP_PROXY` and
   `HTTPS_PROXY`, and that Node needs `NODE_USE_ENV_PROXY=1` to use its built-in proxy support; otherwise pass
   a `dispatcher` built with undici's `ProxyAgent` per call, or set one globally with `setGlobalDispatcher`.
   Bun takes a `proxy` option.
2. **Accepting self-signed certificates turns off protection against interception.** The README shows
   `rejectUnauthorized: false` on an undici agent and labels it use at your own risk. Own guidance: scope it to
   one throwaway test client and never to a shared instance or a production configuration.

## 2.7 Verify
List the options of every client instance and call site: timeout set, retry only where a repeat is safe, the
hooks that run on every attempt, the header and query merging checked with a stub, and no certificate check
disabled.
