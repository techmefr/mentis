# nestjs-node-conventions §5 — The request pipeline: what runs where

> Section 5 of `skills/nestjs-node-conventions`. Read it when a middleware, guard, interceptor, pipe or exception
> filter is written or bound, or when code runs in an unexpected order. The other sections and the guardrails
> stay in `SKILL.md`. Pinned to NestJS 12 (documentation read 2026-10-02).

## Order
1. **The order is fixed; learn it once.** Incoming request, then middleware (global, then module-bound by
   path), guards (global, controller, route), interceptors before the handler (global, controller, route),
   pipes (global, controller, route, then parameter pipes), the handler, interceptors after the handler in the
   reverse order, then the response. Components of one kind run in the order they are bound.
2. **Parameter pipes run from the last parameter to the first**, and controller-level and route-level pipes
   apply to each parameter in that same reversed order. Do not write a pipe that depends on another parameter
   having been validated first.
3. **Interceptors wrap the handler.** Code before `handle()` runs before the handler; code after is on the
   returned stream, and the stream is resolved last-in-first-out on the way out. An interceptor that never calls
   `handle()` skips the handler. A `tap()` runs only on a value: to act on failure too, observe the error
   channel or catch it.
4. **Exception filters resolve from the lowest level up**: route, then controller, then global. An exception
   caught by a lower filter is not passed to a higher one. Filters run only for an exception nobody caught; a
   `try/catch` you wrote never reaches them, and once an uncaught exception occurs the rest of the pipeline is
   skipped.
5. **Errors thrown in middleware are handled only by global filters**, because no route has been chosen yet.
   A filter bound with a decorator on a controller or a route does not see them.

## What goes in which component
6. **Middleware for request-shaping that does not need the route** (request ids, cookies).
   **Guards for the allow-or-deny decision** (authentication, authorisation, rate limiting), reading route
   metadata through the reflector rather than hard-coding paths. **Pipes for validating and converting input.**
   **Interceptors for what wraps a call** (timing, response mapping, caching, serialisation). **Filters for
   turning an exception into a response.** A guard that also reshapes the body, or a pipe that checks
   permissions, is in the wrong component.
7. **Deny by default.** Bind the authentication guard globally and mark the public routes with a decorator
   that sets metadata the guard reads, rather than decorating each protected route and forgetting one.
8. **Bind a global component through the module token** (`APP_GUARD`, `APP_PIPE`, `APP_INTERCEPTOR`,
   `APP_FILTER`) whenever it needs injected dependencies. A component registered with `app.useGlobal...()`
   lives outside any module and cannot inject anything. In a hybrid application or a gateway, the
   `useGlobal...()` form also does not cover the connected microservices by default.
9. **Throw the framework's HTTP exceptions from services, and extend its exception base class for your own**,
   so the built-in filter recognises them. The built-in filter does not log the framework's HTTP exceptions
   (they are normal flow) and answers an unrecognised error with a generic 500; add a global filter for
   logging and for a stable error body, and extend the built-in filter when you only want to change a case.
10. **Do not expose internal detail in the error body.** The filter is the one place that maps an exception to
    a status and a safe message; stack traces and driver messages are logged, not returned.

## Responses and streams
11. **Serialise at the boundary, declaratively.** The class-based serialiser interceptor applies the entity's
    exclude and transform decorators (a password never leaves); the schema-based one validates and transforms the
    response against a Standard Schema. Neither serialises a streamed file response.
12. **Stream large files, don't buffer them**: return the framework's streamable file wrapper from the
    handler. Validate uploads at the pipe with the file pipe and its validators (size and type; the type
    validator reads the content's magic number by default, not the client's declared type), and bound the size.

## Mechanical checks

```
grep -rnE "useGlobal(Guards|Pipes|Interceptors|Filters)\(new " src
grep -rnE "APP_(GUARD|PIPE|INTERCEPTOR|FILTER)" src
grep -rnE "@UseFilters|@UseGuards|@UseInterceptors|@UsePipes" src
grep -rnE "catch *\(" src --include=*.controller.ts
grep -rnE "res\.(send|json|status)\(|@Res\(" src
grep -rnE "readFileSync|readFile\(" src --include=*.controller.ts
```

- `useGlobal...(new X())` for a class with a constructor dependency is a finding (rule 8).
- A `try/catch` in a controller that swallows the exception hides it from the filters (rule 4).
- `@Res()` switches that route to the platform's own response handling and disables the framework's standard
  handling (the returned value is no longer sent for you); set `passthrough: true` to only touch headers or
  cookies, otherwise give a stated reason.
