# laravel-conventions §6 — HTTP surface

> Section 6 of `skills/laravel-conventions`. Read it when a route, a controller action, a FormRequest, a response shape. The other sections and the guardrails stay in `SKILL.md`.

**Before applying this section's REST/resource-routing point, or an installed catalogue's stricter
version of it (e.g. a mandatory REST package), check the specific controller** — what it returns, where
it's routed — **not just whether the project depends on that package.** A project can run Inertia for its
pages and a REST package for a separate real API at the same time; the package being installed doesn't
make every 5-verb controller a REST endpoint, and an Inertia page controller (returning a page and its
props directly) is the shape caught wrong if the check stops at the project level. See `skills/inertia-conventions` §4 before applying this section wholesale to that
architecture.

1. REST routes follow one consistent URI structure across the app, declared through the framework's
   resource routing rather than hand-rolled verb by verb. A URI names resources, not actions — the verb is
   the HTTP method, so a verb segment (`/users/create-and-notify`) signals an action class exposed as a
   route instead of a resource. Nesting stops at one level: past that
   the parent is decoration, and the child is addressable on its own.
2. Standard CRUD on a model is declared through the resource/REST mechanism the project standardises on — a
   hand-rolled CRUD stack for a plain model is five endpoints of avoidable code and a sixth behaviour that
   differs. Use a hand-written route when the operation is genuinely not CRUD on a resource, and give
   it a resource-shaped URI anyway.
3. **Refer to routes by name, never by rebuilding the URL.** A named route survives a prefix change, a
   locale segment and a domain move; a concatenated string is found later by grep, in the one template
   nobody grepped.
4. **Route binding resolves, it does not authorise.** Implicit binding turns an id into a model and holds no
   opinion about who asked — §2 point 4 is the other half, and a nested route needs its binding **scoped**
   to the parent, or the child of *another* parent resolves from a guessed id.
5. **Validation in a FormRequest**, with each field's rules expressed as an **array** of entries rather than
   a pipe-delimited string: a string breaks the moment a rule contains a delimiter, and an array diffs
   cleanly. One request class per action, not one shared between store and update — the two have different
   required fields, and sharing them is how `required` quietly becomes `sometimes` for both.
6. **Use the validated payload, never the raw request afterwards.** Reading the request again past
   validation bypasses it: the value used was never checked, and mass-assigning the raw input reintroduces
   every field the rules excluded — with no trace, since well-behaved callers still work.
7. **`nullable`, `sometimes` and an absent key are three different contracts**, and a partial update has to
   say which it means: a field absent from a `PATCH` keeps its value, a field sent as `null` clears it, and
   conflating the two makes "clear this field" impossible to express. Pick per field, deliberately.
8. **A FormRequest's `authorize()` is not the policy.** It is a convenient place to call one, and putting
   the rule itself there hides it from every other caller of the same operation. The policy owns the rule
   (§2); the request delegates to it.
9. **Query parameters are input too.** Filters, sorts, includes and page size arrive as strings and get validated like a body — an
   unvalidated sort column is an information leak at best, and an unbounded page size is a denial of service
   anyone can trigger with a URL. Cap it, default it, and validate filter names against a list the endpoint
   owns.
10. **Serialise through a resource, not the model.** A model returned directly serialises whatever it
    serialises, so a new column reaches the API the day it is migrated and a hidden one the day it leaves
    `$hidden`. A resource makes the payload a decision, and holds the difference between internal and
    published shape.
11. **A response carries a status/type and a human-readable message**, not just an HTTP code: the frontend
    has to display something. Keep the envelope identical across endpoints, including the error case —
    a client that has to branch on two shapes will handle one of them wrong.
12. **The status code is part of the contract, and the defaults are not enough.** A creation answers 201
    with the location of the thing created, a delete that returns nothing answers 204, a validation failure
    422, a conflicting state 409. And the authorisation pair is a decision, not an accident: 403 tells the
    caller the record exists, 404 does not (§2 point 4).
13. **Never hand-roll content negotiation.** The framework already decides JSON versus a rendered response
    from the request itself; a controller branching on whether the caller expects JSON is a second
    implementation that drifts — one branch gets the new field. §11 carries the same rule for exceptions,
    where it usually starts.
14. **An HTTP API has consumers you do not deploy.** Removing a field, renaming one, or narrowing a type is
    breaking even when every in-repo caller is updated, so it goes through the additive-then-remove path in
    `skills/deprecation-migration`, not one commit. §10 holds the layer question; this is the contract
    question.
15. **A `POST` may run twice.** Clients retry, users double-click, proxies replay. An endpoint whose second
    execution creates a second row needs either a natural uniqueness constraint in the database or an
    idempotency key the caller supplies — a check-then-insert in PHP loses the race it was written for.
16. User-facing email or in-app messaging is not the controller's job: it goes through a notification, and
    §8 owns why.
17. **`HandlePrecognitiveRequests` runs the route's middleware and resolves the controller's dependencies,
    including the FormRequest, then skips the controller method.** Adding it to a route makes point 5's real
    rules reusable for as-you-type validation without a second endpoint. The traps are a rule that is costly
    or calls an outside service, a rule that needs an uploaded file (files are not sent by default), and a
    middleware with a side effect: condition them on `isPrecognitive()`. The full set is in
    `skills/laravel-precognitive-request-scoping`. [Laravel Precognition docs 12.x, read 2026-10-20.]
18. **`Http::pool()` runs independent outbound calls concurrently from one place, not from several
    sequential `Http::get()` calls inside a loop.** It is the outbound equivalent of
    `skills/python-conventions` §4.1's `gather`: three sequential 300 ms calls are a near-second response
    that profiles as "the third-party API is slow". Decide failure per response — failing the whole pool because one call failed loses the ones that
    succeeded.
19. **A rate limit is declared per named limiter, not read inline in the route.** `RateLimiter::for('api', ...)`
    in a service provider's `boot()` centralises the policy (the docs' example limits per minute by user id,
    falling back to the IP address) so every route naming it shares one definition; a `throttle:60,1`
    scattered across routes with different numbers is the same limit reimplemented each time, and "what's our
    API rate limit" needs a grep of every route file. [Laravel routing docs 12.x, "Rate Limiting", read
    2026-10-21.]
20. **A resource's conditional attribute (`whenLoaded`, `when`, `mergeWhen`) keeps a payload honest about what was
    actually fetched, instead of forcing every relation to load so the resource can serialise it.** `whenLoaded`
    only emits the field if the relation was eager-loaded, so an endpoint that didn't ask for it doesn't pay
    for it or return a null that looks like missing data. `when($condition, ...)` does the same for a field
    gated on the caller's own permissions.
21. **A resource collection's pagination metadata is the contract for "how many more," and hand-rolling it drifts
    from what the paginator actually did.** A paginator wrapped in a `ResourceCollection` carries `links` and
    `meta` (current page, total, per-page) generated from it; a hand-built `{data, total}` must be kept in
    sync whenever the pagination strategy changes.
22. **A custom validation rule (`implements ValidationRule`) is for a check that recurs across FormRequests, not
    for one used once.** A single-use check inline as a closure rule reads at the point it applies; promoting every
    closure to a class is over-factoring (§1 point 6) — the class earns its place once a second FormRequest
    needs the same check.
23. **The `api` and `web` middleware groups apply different defaults, and moving a route between them changes
    behaviour nobody asked for.** In 12.x the `web` group holds cookie encryption, queued cookies, the session,
    error sharing from the session, CSRF token validation and route binding; the `api` group holds route
    binding only. An endpoint moved to the other group either loses the session it relied on, or gains CSRF
    verification a token-authenticated client will never satisfy. The group is part of the route's contract.
    [Laravel middleware docs 12.x, "Middleware Groups", read 2026-10-21.]
24. **`apiResource` and `apiResources` exclude `create`/`edit` by default, and adding them back on an API
    controller is the tell that a form-rendering route leaked into a JSON surface.** Those two actions serve
    HTML for a browser form, so declaring them on an `apiResource` controller usually means point 1's
    Inertia-page caveat got mixed into a pure API resource. `Route::apiResources([...])` registers several
    resource controllers in one call. [Laravel controllers docs, laravel.com/docs/12.x/controllers, read
    2026-09-10.]
25. **`only()`/`except()` on a resource route narrow which of the seven conventional actions get registered,
    and that list is the authorisation surface too.** A resource that only ever supports read (`only(['index',
    'show'])`) should not register `store`/`update`/`destroy` routes at all — leaving them in and relying on
    the policy to reject every write adds a layer around routes that never needed to exist, and a route
    that always 403s still shows in a route list as supported. [Laravel controllers
    docs, laravel.com/docs/12.x/controllers, read 2026-09-10.]
26. **A single-action controller (`__invoke()`) is for one route that is genuinely not a CRUD action on a
    resource, and giving it a resource-shaped URI (point 1's closing clause) still applies to it.** Like
    a custom validation rule (point 22), reach for it once, not by default; five unrelated one-off routes
    accumulating in it are five actions on a resource, point 2's case.
27. **A route model binding's resolution can be scoped to a specific column without a separate lookup
    endpoint.** `Route::get('/posts/{post:slug}', ...)` resolves the bound model by its `slug` column instead
    of its key, the framework's own mechanism (point 4 of `skills/laravel-conventions` §10 — prefer it over
    a custom one) for a public-facing URL that should never expose a numeric id; it still resolves only, so
    point 4's authorisation caveat and parent-scoping requirement for a nested route apply as before.
28. **A route's `withoutMiddleware()` is a narrower tool than removing the route from a group, and using it
    to strip authentication is a decision that deserves the same visibility as adding a public carve-out
    (§2 point 9).** It removes a named middleware from one route inside a group that otherwise applies it
    — a reviewer should ask "why does this one route opt out," because the same call silently defeats a
    CSRF check, a rate limiter, or the ability check point 19 relies on.
29. **A resource's `toArray()` returning a plain array is the common case; returning `array_merge(parent::toArray($request),
    [...])` from a child resource is how a payload shape is composed instead of duplicated across near-identical
    resources.** Two resources differing by one or two fields suggest one should extend the other — but
    `skills/laravel-conventions` §3 point 12's test applies here in the other direction: merge two
    resources only once they also share the reason their fields exist.
30. **A route's explicit HTTP verb and its resource-registered sibling can silently diverge once both exist
    for the same URI.** A hand-written `Route::post('/orders/{order}/cancel', ...)` alongside a resource
    route for the same model is fine per point 2 — the trap is letting it drift out of the naming,
    middleware, or throttling convention (point 19) its siblings share, since nothing forces it to match
    the way `Route::resource()` does.
31. **A signed URL is the framework's answer to "this link must not be forgeable", and it is a different
    guarantee from the token-authenticated request point 19's rate limiter already assumes.**
    `URL::temporarySignedRoute()` embeds an expiry and a signature the route's own `signed` middleware
    verifies, which is what an unsubscribe link, an invoice download, or an email-verification link needs —
    none carry a session or bearer token, so without a signature the URL is the only credential. Use it
    instead of a hand-rolled hash-in-the-query-string check. [Laravel URL generation docs,
    laravel.com/docs/12.x/urls, read 2026-09-10.]
32. **A Sanctum token's abilities scope what that specific token may do, and checking them is a separate
    step from checking the user is authenticated.** `$request->user()->tokenCan('orders:write')` answers "did
    the caller present a token narrow enough for this action," which point 8's policy check does not cover
    — a read-only reporting token must still fail a write endpoint though the user could perform it, and
    forgetting `tokenCan()` means every token minted for that user carries all the user's permissions.
33. **A FormRequest's `prepareForValidation()` runs first, and `passedValidation()` runs only once the rules
    pass.** In the framework source, `validateResolved()` calls `prepareForValidation()` before it checks
    `authorize()`, then builds the validator, then calls `passedValidation()`. So `prepareForValidation()` is
    where a slug is lowercased or a phone number stripped *before* a rule checks it, and a request can have
    been normalised before authorisation refuses it, so keep it free of side effects; in `passedValidation()`
    the rules have already validated the raw input. [Laravel validation docs 12.x; framework source
    `ValidatesWhenResolvedTrait.php` (12.x), read 2026-10-21.]
34. **Cursor pagination (`cursorPaginate()`) works from where clauses on the ordered columns, not an offset,
    which offset pagination (point 21) cannot offer.** An offset-based page skips N rows at query time, so a
    row inserted or deleted ahead of the page shifts every later page by one. The docs describe cursor
    pagination as the most efficient method for large sets and infinite scroll; it needs an order by clause
    on columns of the paginated table, and it gives up jumping to an arbitrary page number, so it is wrong for
    a numbered table. [Laravel pagination docs 12.x, read 2026-10-21.]
35. **`JsonResource::withoutWrapping()` decides whether the outermost payload is `{"data": ...}` or the bare
    object, and it is a project-wide decision made once.** It is a static call on the base class, typically
    placed in a service provider's `boot()`. The docs add two limits: it only affects the outermost response,
    and a paginated response is still wrapped in `data` because it always carries `meta` and `links`. A resource
    can also override its own `$wrap`, which yields some endpoints wrapped and some not, the inconsistency
    point 11's envelope rule forbids. [Laravel Eloquent resources docs 12.x, "Data Wrapping", read
    2026-10-21.]
36. **`Http::retry()` bounds how many times an outbound call is retried and with what wait.** `Http::retry(3, 100)`
    retries a failing request up to three times, waiting 100 ms between attempts, before the caller sees the
    exception; the wait can also be a closure of the attempt number. A third argument, a callable receiving
    the exception and the request, narrows which failures are worth retrying (the docs' example retries only
    connection exceptions), so a 422 from the far side is not retried. It is the right tool for transient
    failures of a flaky third-party API, not a substitute for point 18's concurrency answer. [Laravel HTTP
    client docs 12.x, "Retries", read 2026-10-21.]
37. **CORS is one configuration, not a header set by hand in a controller or middleware.** The `HandleCors`
    middleware is part of the application's global middleware stack and answers CORS `OPTIONS` requests with
    values you configure; to change them, publish the file with `php artisan config:publish cors` and edit
    `config/cors.php`. A controller setting `Access-Control-Allow-Origin` duplicates that decision and drifts
    when the allowed-origins list changes and one controller is missed. [Laravel routing docs 12.x, "Cross-Origin
    Resource Sharing (CORS)", read 2026-10-21.]
