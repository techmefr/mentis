# go-http-resilience-pitfalls §1 — Server

Applies to the standard `net/http` package; each rule names a version where it is gated.

## 1.1 Build the server yourself, with timeouts
1. **Construct an `http.Server` value and set its timeout fields; do not call the package-level
   `http.ListenAndServe` in production.** The package function takes only an address and a handler, so
   nothing can be configured on it. The static analyser gosec has a rule for exactly this (G114, a serve
   function with no support for timeouts), and another (G112) for a missing `ReadHeaderTimeout`.
2. **`ReadHeaderTimeout` is the one to set first.** Its documented meaning is the time allowed to read the
   request headers; the connection's read deadline is reset after the headers, so the handler decides what is
   too slow for the body. The `ReadTimeout` documentation says that, because it gives handlers no
   per-request decision on body deadline or upload rate, most users will prefer `ReadHeaderTimeout`, and
   that using both is valid.
3. **Know the fallbacks.** If `ReadHeaderTimeout` is zero, `ReadTimeout` is used; if it is negative, or both
   are zero or negative, there is no timeout. `IdleTimeout` (the wait for the next request on a keep-alive
   connection) falls back to `ReadTimeout` the same way. `WriteTimeout` has no fallback: zero or negative
   means none. It is reset when a new request's header is read.
4. **Set all three, with values from the service's slowest legitimate request,** not copied from an example.
   Own guidance on choosing numbers: a streaming or upload endpoint needs a different write or read budget
   than the rest, and the documentation says these fields cannot vary per request.

## 1.2 Limit sizes
1. **`MaxHeaderBytes` limits only the request line and header keys and values, not the body**, and zero
   means `DefaultMaxHeaderBytes` (1 MB). A body limit is a separate step.
2. **Wrap the body with `http.MaxBytesReader(w, r.Body, n)` before reading it.** It is built for incoming
   request bodies: unlike `io.LimitReader` it returns a `*MaxBytesError` on a read past the limit, closes the
   underlying reader on `Close`, and, where it can, asks the `ResponseWriter` to close the connection once
   the limit is passed. Check for that error type in the handler and answer with a client-error status (own guidance).
3. **`MaxHeaderValueCount`** (Go 1.27 and later) bounds the number of header values a server will parse; it
   defaults to `DefaultMaxHeaderValueCount` when zero. Not available on earlier toolchains.

## 1.3 Use the standard mux first
**From Go 1.22, `http.ServeMux` patterns can carry a method and wildcards** (`"POST /items/create"`,
`"/items/{id}"`), the value is read with `Request.PathValue`, and when two patterns overlap the more
specific wins. Reach for a third-party router only after the standard one fell short; that preference is
own guidance. Two version notes: the change breaks backward compatibility in small ways, controlled by the
`httpmuxgo121` `GODEBUG` setting, and from Go 1.26 the mux's trailing-slash redirects use status 307 instead
of 301.

## 1.4 Do not expose profiling by accident
gosec flags a profiling endpoint that is exposed automatically (G108). The Go diagnostics guide shows
profile handlers registered by hand on a custom mux served on its own port. Keep profiling on a separate,
internal listener and never on the public one. The "internal" part is own guidance drawn from that example.
