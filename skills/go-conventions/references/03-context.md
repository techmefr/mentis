# go-conventions §3 — Context

> Section 3 of `skills/go-conventions`.

1. `context.Context` always the first parameter, never stored in a struct.
2. A function propagates the context it received as a parameter, never a `context.Background()` recreated
   deep down, otherwise the upper level's cancellation/timeout gets ignored.
3. HTTP request always with a context (`http.NewRequestWithContext`), never a bare `http.Get`.
4. Work that must survive the request that started it (an audit write, a cleanup) takes
   `context.WithoutCancel` of the request context, so it keeps the values but not the cancellation.
5. `context.Background()` appears at entry points and in tests. Mid-chain, when no context exists yet, use
   `context.TODO()` so the gap stays visible; never pass a nil context, it panics on first use.
6. Context value keys are an unexported type, and values are request-scoped metadata (a request id, a caller
   identity), never a function argument smuggled through.
