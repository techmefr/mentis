# python-sqlalchemy-fastapi-pitfalls §2 — FastAPI handlers and declarations

Applies to the FastAPI documentation and the FastAPI repository's own agent skill read on the date in the
origin file. Items marked "from" a version are gated on it.

## 2.1 `def` or `async def`
1. **When in doubt, write a plain `def` handler.** FastAPI runs a `def` path operation in an external
   thread pool so it cannot block the event loop; an `async def` handler runs on the loop itself, where one
   blocking call stalls every request in the process. Use `async def` only when everything you call inside
   is awaitable and non-blocking (the rule is `python-async-no-blocking-calls`).
2. **The same applies to dependencies:** a `def` dependency runs in the thread pool, an `async def` one on
   the loop.
3. **The thread pool is finite.** Starlette runs sync endpoints through AnyIO, whose default thread limiter
   has 40 tokens, shared with everything else in the process that uses it, including FastAPI's sync
   dependencies. Forty simultaneous blocking calls fill it, and the forty-first request waits, for a reason
   that no request log shows.
4. **Raising the limit is a trade:** more threads cost memory and contention (the Starlette documentation
   says so). The fix for slow blocking calls is usually fewer or shorter ones, not a bigger pool.
5. **Mixing:** blocking code needed in an async handler goes to a thread explicitly, and async code needed
   in a sync handler goes through the framework's helpers rather than a hand-made loop.

## 2.2 Dependencies
1. **Declare dependencies with `Annotated[T, Depends(fn)]` and give the annotated type a name** so it is
   reused across routes; it keeps the signature valid outside FastAPI and reads as a type.
2. **Avoid class dependencies and a bare `Depends()` on a class.** The repository's skill says to write a
   plain function that returns an instance instead; the class form hides which parameters come from the
   request.
3. **A dependency with `yield` runs its exit code after the response is sent by default;** FastAPI's newer
   `scope="function"` runs it after the response data is generated and before the response is sent. Use
   the narrower scope when the resource (a session, a lock) must not outlive the handler; check the
   FastAPI version in use before relying on `scope`.

## 2.3 Declarations
1. **Do not use `...` (Ellipsis) for a required parameter or a model field.** It is not needed: a field
   with no default is already required, and `Field(gt=0)` alone is the constraint.
2. **Avoid `RootModel`.** Use an annotated type (`Annotated[list[int], Field(min_length=1), Body()]`);
   FastAPI wraps it in a type adapter, so the type works without a wrapper class.
3. **Put `prefix`, `tags` and shared `dependencies` on the `APIRouter`** rather than on the
   `include_router` call, so a router carries its own contract wherever it is mounted.
4. **One HTTP operation per function.** Do not branch on the method inside a function registered for
   several; each operation gets its own route function, which keeps the signature, the response type and
   the permissions in one place.
5. **Declare the response type.** The return annotation (or `response_model`) validates, filters, documents
   and serialises the response, so an internal field cannot leave through a forgotten `return`. Use
   `response_model` when the returned object legitimately differs from the public shape, and annotate the
   function `-> Any` in that case.
6. **A response that does not match the declared type is a server error,** by design: it means your code is
   wrong, not the client. Test the shape.

## 2.4 Middleware
1. **`BaseHTTPMiddleware` stops context variable changes propagating upwards.** The Starlette documentation
   says a value set in an endpoint is not visible to the middleware, and that it also breaks propagation for
   pure ASGI middleware placed later in the stack that depends on it. Request ids, tracing and
   per-request logging context are exactly these.
2. **Write context-dependent middleware as pure ASGI middleware,** as the Starlette documentation advises.

## Verification
- A `def` handler with a blocking call and an `async def` one were load-tested at more than 40 concurrent
  requests, and the difference was seen where it is expected.
- A response with a missing or extra field was returned deliberately and the declared type caught it.
- A context variable set in a handler is visible to the middleware that logs it.
