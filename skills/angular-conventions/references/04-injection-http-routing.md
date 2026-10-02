# angular-conventions §4 — Injection, HTTP and routing

> Section 4 of `skills/angular-conventions`. Read it when a service, an interceptor, a route or a guard is
> written. The other sections and the guardrails stay in `SKILL.md`.

1. **Inject with `inject()`, not constructor parameters.** It reads better with many dependencies, infers types
   better, and lets a field initialiser use an injected value without splitting declaration and assignment.
   `inject()` only works in an injection context: construction of a class the injector creates, its field
   initialisers, a provider or token factory, and the stack frames the router and `HttpClient` run guards,
   resolvers and interceptors in. Called from a timer, a promise callback or an event handler it throws
   `NG0203`. Capture the dependency first, or run the code through `runInInjectionContext` with an injector.
2. **A service has one responsibility and is provided once.** On v22 and later a new singleton is a class with
   `@Service()` (root-provided, tree-shakable, `inject()` only); keep `@Injectable` when you need
   constructor injection, `useClass` / `useValue` / `useExisting`, or a non-root scope. A service scoped to a
   route or component is provided there (`autoProvided: false` for `@Service`), so its lifetime ends with
   that scope.
3. **Provide a service at the narrowest level that works.** A route-level provider reaches the guards and
   resolvers of that route and its children; do not promote to root just to avoid thinking about scope.
4. **HTTP interceptors are functions registered with `withInterceptors`**, in the order of the list: the first
   sees the request first and the response last. The DI-class form works identically but its order depends on
   provider registration and is hard to predict in a layered configuration.
5. **An interceptor never mutates the request.** Requests and responses are immutable; call `.clone()` with the
   changed property. That immutability is what makes retries safe, because the same request can pass the chain
   twice. The body is not deeply protected, so an interceptor that edits it must tolerate running twice on the
   same request.
6. **Metadata for an interceptor travels in `HttpContext`, not in headers.** Define an `HttpContextToken` with
   a default factory (an object or array default is created per request) and read it in the interceptor, so a
   flag such as "do not cache" never leaves the browser. The context is mutable, which is useful when an
   interceptor leaves a note for itself across a retry, and a surprise otherwise.
7. **An interceptor is the home of cross-cutting HTTP concerns**: an authentication header for a given API,
   retry with backoff, caching with invalidation by mutations, timing and logging, a loading indicator, a
   request deadline. A single feature's special case belongs at the call site, not in a global interceptor
   that every request pays for.
8. **Send credentials only to your own origin.** The authentication interceptor checks the target URL before it
   adds a token; a header added to every request leaks the token to third-party hosts.
9. **Lazy-load every route except the landing path.** `loadComponent` and `loadChildren` take a function that
   returns the import; a `default` export can be returned directly. Eager loading suits the first screens users
   always hit, because lazy loading trades bundle size for later requests, and nested lazy levels multiply
   those requests.
10. **A route guard redirects by returning a `UrlTree` or `RedirectCommand`**, never by returning `false` and
    then calling `navigate`. `CanMatch` is different: returning `false` makes the router try the next matching
    route instead of blocking.
11. **A guard is never the access control.** Everything in the browser can be edited by whoever runs it; the
    server enforces authorisation on every request, and the guard is the experience layered over that.
12. **Name guard files with the `-guard.ts` suffix** and keep them as functions; they get route-level services
    and the `route` and `state` snapshots as arguments.
13. **Data a route needs before it renders is a resolver** (a `ResolveFn`, which can also handle the fetch error
    before navigation completes and keeps server rendering consistent), or a route-level resource when the
    page can render progressively. It is not a fetch in the constructor of the routed component.
14. **Test HTTP with the testing providers, not a hand-made fake of `HttpClient`** (§6).

## Mechanical checks

```
grep -rnE "constructor\(.*(private|public|protected|readonly)" src --include=*.ts
grep -rnE "HTTP_INTERCEPTORS|implements HttpInterceptor" src
grep -rnE "req\.(headers|body)\.[a-z]+ *=|\.headers\.set\(" src --include=*.ts
grep -rnE "return false;" src --include=*guard*.ts
grep -rnE "component: [A-Z]" src --include=*.routes.ts
```

- A constructor-injection hit is a migration candidate, never a defect on a pre-`inject()` project.
- A `return false` in a guard followed by `navigate` is the pattern of rule 10.
- Eagerly imported route components other than the landing path are rule 9 candidates.
