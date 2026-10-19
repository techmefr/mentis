# go-http-resilience-pitfalls §2 — Client

Applies to the standard `net/http` package; each rule names a version where it is gated. Passing the request
context (`http.NewRequestWithContext`) and closing the body are `go-conventions` §3.3 and §4.1.

## 2.1 Never use the default client
1. **`http.Get`, `Head` and `Post` use `DefaultClient`, and a client's `Timeout` of zero means no timeout.**
   A call to a server that accepts the connection and never answers then blocks until something else
   cancels it. Build your own `http.Client` with `Timeout` set.
2. **`Client.Timeout` covers more than connecting.** It includes connection time, any redirects and
   **reading the response body**; the timer keeps running after `Do` returns and interrupts reads of the
   body. A long streaming download therefore needs a per-request context deadline chosen for it (own
   guidance) rather than a short client-wide `Timeout`.

## 2.2 Create one client and reuse it
The documentation says clients and transports are safe for concurrent use by many goroutines and, for
efficiency, should be created once and reused. A client built per request throws away the transport's
connection pool. Share one client per set of settings, and pass it in rather than reading a global.

## 2.3 Drain and close the response body
1. **Read the body to EOF and close it, or the connection may not be reused.** `Client.Do`'s documentation
   says that if the body is not both read to EOF and closed, the transport may be unable to reuse a
   persistent connection for a later keep-alive request.
2. **Go 1.27 and later:** the release notes say an HTTP/1 `Response.Body` now drains unread content when it
   is closed, up to a conservative limit, for better reuse. On earlier toolchains, and for bodies larger than
   that limit, drain explicitly. Own guidance: drain through a size-limited reader so a hostile or endless
   body cannot hold the goroutine.
3. **Close on every path, including the error branch of the status check.** Covered by
   `go-conventions` §4.1; the failure mode here is the non-2xx branch that returns without draining.

## 2.4 Build addresses with `net.JoinHostPort`
`go vet` reports `fmt.Sprintf("%s:%d", host, port)` used to build an address for `net.Dial` and suggests
`net.JoinHostPort`, which is needed for IPv6 addresses. The `hostport` analyser arrived with Go 1.25.

## 2.5 Redirect policy
A custom `CheckRedirect` can carry sensitive headers to a different host; gosec flags an unsafe redirect
policy that may propagate them (G119). The default client behaviour forwards most headers on redirect and
withholds sensitive ones such as `Authorization` and `Cookie` when the target is not trusted; read the
`Client` documentation before replacing it.
