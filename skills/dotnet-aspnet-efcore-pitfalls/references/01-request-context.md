# dotnet-aspnet-efcore-pitfalls §1 — Request context

`HttpContext` belongs to one request. Holding on to it past the request, or touching it from a second
thread, gives unpredictable results. These rules follow the ASP.NET Core HttpContext guidance.

## 1.1 Lifetime
1. **Do not capture `HttpContext` outside the request flow.** `IHttpContextAccessor.HttpContext` can be
   `null` when read outside it, and the accessor should not be captured in a constructor.
2. **Copy what you need before starting background work.** Read the user id, tenant or header value into a
   local and pass the value. Do not capture the context, or request-scoped services such as a `DbContext`,
   in a fire-and-forget task; create a scope inside the background code (`dotnet-conventions` §2 on
   scopes). The documentation shows copying the needed values for background threads.
3. **`IHttpContextAccessor` is a last resort.** Pass the value through the call chain when you can. This
   is our own guidance.

## 1.2 Threads and response
1. **`HttpContext` is not thread safe.** Accessing it from several threads can cause exceptions and data
   corruption; copy the values first.
2. **An app cannot modify headers after the response has started.** Writing to the body, or flushing it,
   starts the response unless response buffering is on (it is off by default).

## 1.3 Body IO
1. **Request and response body IO should be asynchronous.** Kestrel's `AllowSynchronousIO` defaults to
   `false`; the documentation warns that many blocking synchronous operations can starve the thread pool
   and says to enable it only for a library that cannot do asynchronous IO.
2. **Read form data with `ReadFormAsync`.** The documentation links the reason in its API table.
3. **Read the request body forward-only when you can.** The body can be read once; `EnableBuffering`
   enables several reads but buffers the body (large ones to disk by option), so use it only when a second
   read is needed, and call it before the first read.

## Verification
- A search for `IHttpContextAccessor` fields on singletons, and for `HttpContext` captured by lambdas
  handed to `Task.Run` or a channel, returns nothing.
- A load test with a background task started from a handler shows no exception and no cross-request value.
