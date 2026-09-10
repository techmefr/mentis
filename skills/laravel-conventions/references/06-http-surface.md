# laravel-conventions §6 — HTTP surface

> Section 6 of `skills/laravel-conventions`. Read it when a route, a controller action, a FormRequest, a response shape. The other sections and the guardrails stay in `SKILL.md`.

**Before applying this section's REST/resource-routing point, or an installed catalogue's stricter
version of it (e.g. a mandatory REST package), check the specific controller** — what it returns, where
it's routed — **not just whether the project depends on that package.** A project can genuinely run
Inertia for its pages and a REST package for a separate real API surface at the same time; the package
being installed doesn't make every 5-verb controller a REST endpoint, and an Inertia page controller
(no separate API, a controller returns a page and its props directly) is exactly the shape this catches
wrong if the check stops at the project level. See `skills/inertia-conventions` §4 before applying this
section wholesale to that architecture.

1. REST routes follow one consistent URI structure across the app, declared through the framework's
   resource routing rather than hand-rolled verb by verb. A URI names resources, not actions — the verb is
   the HTTP method, so a path segment that is a verb (`/users/create-and-notify`) is the signal that an
   action class is being exposed as a route instead of a resource. Nesting stops at one level: past that
   the parent is decoration, and the child is addressable on its own.
2. Standard CRUD on a model is declared through the resource/REST mechanism the project standardises on — a
   hand-rolled CRUD stack for a plain model is five endpoints of avoidable code and a sixth behaviour that
   differs. Reach for a hand-written route when the operation is genuinely not CRUD on a resource, and give
   it a resource-shaped URI anyway.
3. **Refer to routes by name, never by rebuilding the URL.** A named route survives a prefix change, a
   locale segment and a domain move; a concatenated string is found later by grep, in the one template
   nobody grepped.
4. **Route binding resolves, it does not authorise.** Implicit binding turns an id into a model and holds no
   opinion about who asked — §2 point 4 is the other half, and a nested route needs its binding **scoped**
   to the parent, or the child of *another* parent resolves happily from a guessed id.
5. **Validation in a FormRequest**, with each field's rules expressed as an **array** of entries rather than
   a pipe-delimited string: a string breaks the moment a rule contains a delimiter, and an array diffs
   cleanly. One request class per action, not one shared between store and update — the two have different
   required fields, and sharing them is how `required` quietly becomes `sometimes` for both.
6. **Use the validated payload, never the raw request afterwards.** Reading the request again past
   validation bypasses it: the value used is the one that was never checked, and mass-assigning the raw
   input reintroduces every field the rules were there to exclude. This is the failure that leaves no
   trace, because the endpoint works for well-behaved callers.
7. **`nullable`, `sometimes` and an absent key are three different contracts**, and a partial update has to
   say which it means: a field absent from a `PATCH` keeps its value, a field sent as `null` clears it, and
   conflating the two makes "clear this field" impossible to express. Pick per field, deliberately.
8. **A FormRequest's `authorize()` is not the policy.** It is a convenient place to call one, and putting
   the rule itself there hides it from every other caller of the same operation. The policy owns the rule
   (§2); the request delegates to it.
9. **Query parameters are input too.** Filters, sorts, includes and page size arrive as strings from the
   client and get validated like a body — an unvalidated sort column is an information leak at best and an
   error at worst, and an unbounded page size is a denial of service anyone can trigger with a URL. Cap it,
   default it, and validate the filter names against a list the endpoint owns.
10. **Serialise through a resource, not the model.** A model returned directly serialises whatever it
    happens to serialise, so a new column reaches the API the day it is migrated and a hidden one reaches
    it the day someone removes it from `$hidden`. A resource makes the payload a decision, and it is where
    the difference between the internal shape and the published shape lives.
11. **A response carries a status/type and a human-readable message**, not just an HTTP code: the frontend
    has to display something. Keep the envelope identical across endpoints, including the error case —
    a client that has to branch on two shapes will handle one of them wrong.
12. **The status code is part of the contract, and the defaults are not enough.** A creation answers 201
    with the location of the thing created, a delete that returns nothing answers 204, a validation failure
    422, a conflicting state 409. And the authorisation pair is a decision, not an accident: 403 tells the
    caller the record exists, 404 does not (§2 point 4).
13. **Never hand-roll content negotiation.** The framework already decides JSON versus a rendered response
    from the request itself; a controller branching on whether the caller expects JSON is a second
    implementation of that decision, and it drifts — one branch gets the new field. §11 carries the same
    rule for exceptions, which is where it usually starts.
14. **An HTTP API has consumers you do not deploy.** Removing a field, renaming one, or narrowing a type is
    breaking even when every in-repo caller is updated, so it goes through the additive-then-remove path in
    `skills/deprecation-migration` rather than landing in one commit. §10 holds the layer question; this is
    the contract question.
15. **A `POST` may run twice.** Clients retry, users double-click, proxies replay. An endpoint whose second
    execution creates a second row needs either a natural uniqueness constraint in the database or an
    idempotency key the caller supplies — a check-then-insert in PHP loses the race it was written for.
16. User-facing email or in-app messaging is not the controller's job: it goes through a notification, and
    §8 owns why.
17. **`HandlePrecognitiveRequests` runs the same FormRequest the real submission runs, stopped before the
    controller.** Adding it to a route is what makes point 5's rules reusable for as-you-type validation
    without a second endpoint — the trap is a rule that only makes sense once the operation actually runs
    (a uniqueness check against a row the precognitive request itself is about to create) reporting a false
    positive on every keystroke; scope those rules to skip during a precognitive request rather than
    disabling the check.
18. **`Http::pool()` runs independent outbound calls concurrently from one place, not from several
    sequential `Http::get()` calls inside a loop.** It is the outbound-call equivalent of
    `skills/python-conventions` §4.1's `gather`: three sequential 300 ms calls are a near-second response
    that profiles as "the third-party API is slow", and nothing on their side will move it. Failure still
    needs a decision per response — the pool returns one response or exception per call, and treating the
    whole pool as failed because one call did loses the ones that succeeded.
19. **A rate limit is declared per named limiter, not read inline in the route.** `RateLimiter::for('api', ...)`
    in a service provider centralises the policy (per-user, per-IP, tiered by plan) so every route naming that
    limiter shares one definition; a `throttle:60,1` scattered across routes with different numbers per endpoint
    is the same limit reimplemented slightly differently each time, and nobody can answer "what's our API rate
    limit" without grepping every route file.
20. **A resource's conditional attribute (`whenLoaded`, `when`, `mergeWhen`) keeps a payload honest about what was
    actually fetched, instead of forcing every relation to load so the resource can serialise it.** `whenLoaded`
    only emits the field if the relation was eager-loaded, so an endpoint that didn't ask for it doesn't pay for
    it and doesn't return a subtly-null field that looks like missing data instead of a field the caller never
    requested. `when($condition, ...)` does the same for a field gated on the caller's own permissions.
21. **A resource collection's pagination metadata is the contract for "how many more," and hand-rolling it drifts
    from what the paginator actually did.** Wrapping a paginator in a `ResourceCollection` carries `links` and
    `meta` (current page, total, per-page) generated from the paginator itself; a controller that manually builds
    `{data, total}` has to keep that shape in sync by hand every time the pagination strategy changes.
22. **A custom validation rule (`implements ValidationRule`) is for a check that recurs across FormRequests, not
    for one used once.** A single-use business check inline as a closure rule is fine and reads at the point it
    applies; promoting every closure to its own class is over-factoring past point 5's rule from `§1` — the
    class earns its place once a second FormRequest needs the same check and would otherwise copy the closure.
23. **The `api` and `web` middleware groups apply different defaults, and moving a route between them changes
    behaviour nobody asked for.** `web` carries session state and CSRF verification; `api` typically doesn't —
    an endpoint built for one and later exposed through the other either loses the session it was relying on, or
    gains CSRF verification a token-authenticated client was never going to send. The group a route sits in is
    part of its contract, not an artifact of which file it was defined in.
24. **`apiResource` and `apiResources` exclude `create`/`edit` by default, and adding them back on an API
    controller is the tell that a form-rendering route leaked into a JSON surface.** Those two actions exist
    to serve HTML for a browser form; a controller registered through `apiResource` never needs them, so a
    project that finds itself declaring `create`/`edit` on an `apiResource` controller has usually mixed
    point 1's Inertia-page caveat into what was meant to be a pure API resource. Registering several resource
    controllers in one call (`Route::apiResources([...])`) is the same convention applied to a whole set at
    once, rather than repeating the call per model. [Laravel controllers docs, laravel.com/docs/12.x/controllers,
    read 2026-09-10.]
25. **`only()`/`except()` on a resource route narrow which of the seven conventional actions get registered,
    and that list is the authorisation surface too.** A resource that only ever supports read (`only(['index',
    'show'])`) should not register `store`/`update`/`destroy` routes at all — leaving them in and relying on
    the policy alone to reject every write is an extra layer of defence around routes that never needed to
    exist, and a route that exists but always 403s still shows up in a route list as something the API
    supports. [Laravel controllers docs, laravel.com/docs/12.x/controllers, read 2026-09-10.]
26. **A single-action controller (`__invoke()`) is for one route that is genuinely not a CRUD action on a
    resource, and giving it a resource-shaped URI (point 1's closing clause) still applies to it.** It is the
    class-per-operation answer to the same shape point 22 of `skills/laravel-conventions` §4 already resolves
    for a custom validation rule: reached for once, not promoted by default, and it should not quietly become
    the place five unrelated one-off routes accumulate — at that point they are five actions on a resource,
    which is point 2's case, not five reasons to invoke a controller.
27. **A route model binding's resolution can be scoped to a specific column without a separate lookup
    endpoint.** `Route::get('/posts/{post:slug}', ...)` resolves the bound model by its `slug` column instead
    of its key, which is the framework's own mechanism (point 4 of `skills/laravel-conventions` §10 — prefer
    it over a custom one) for a public-facing URL that should never expose a numeric id; it still resolves
    only, so point 4's authorisation caveat and its parent-scoping requirement for a nested route apply
    exactly as before.
28. **A route's `withoutMiddleware()` is a narrower tool than removing the route from a group, and using it
    to strip authentication is a decision that deserves the same visibility as adding a public carve-out
    (§2 point 9).** It removes a named middleware from one route inside a group that otherwise applies it
    everywhere — legitimate for a genuinely different requirement on one endpoint, and a place a reviewer
    should always ask "why does this one route opt out," because the same call silently defeats a CSRF check,
    a rate limiter, or the ability check point 19 relies on being present by default.
29. **A resource's `toArray()` returning a plain array is the common case; returning `array_merge(parent::toArray($request),
    [...])` from a child resource is how a payload shape is composed instead of duplicated across near-identical
    resources.** Two resources that differ by one or two fields are a sign one should extend the other rather
    than repeat the whole field list — the same "factor by shared meaning, not shared shape" test
    `skills/laravel-conventions` §3 point 12 applies to a table applies here to a resource class, in the
    other direction: two resources sharing most of their fields today are worth merging only once they also
    share the reason those fields exist.
30. **A route's explicit HTTP verb and its resource-registered sibling can silently diverge once both exist
    for the same URI.** Declaring a hand-written `Route::post('/orders/{order}/cancel', ...)` alongside a
    resource route for the same model is fine per point 2's "reach for a hand-written route when the
    operation is genuinely not CRUD" — the trap is letting that hand-written route drift out of the naming,
    middleware, or throttling convention (point 19) the resource routes around it all share, because nothing
    forces it to look like its siblings the way `Route::resource()` forces its five.
31. **A signed URL is the framework's answer to "this link must not be forgeable", and it is a different
    guarantee from the token-authenticated request point 19's rate limiter already assumes.** `URL::temporarySignedRoute()`
    embeds an expiry and a signature the route's own `signed` middleware verifies, which is what an
    unsubscribe link, an invoice download, or an email-verification link needs — none of them carry a
    session or a bearer token, so without a signature the URL itself is the only credential and anyone who
    guesses or forwards it gets in. Reach for it instead of a hand-rolled hash-in-the-query-string check,
    which reimplements the expiry and the tamper-detection worse. [Laravel URL generation docs,
    laravel.com/docs/12.x/urls, read 2026-09-10.]
32. **A Sanctum token's abilities scope what that specific token may do, and checking them is a separate
    step from checking the user is authenticated.** `$request->user()->tokenCan('orders:write')` answers "did
    the caller present a token narrow enough for this action," which point 8's policy check does not cover
    on its own — a personal-access token issued for read-only reporting must still fail a write endpoint even
    though the underlying user could otherwise perform it, and forgetting `tokenCan()` on a token-issued route
    means every token minted for that user carries every permission the user has, regardless of what it was
    actually created for.
33. **A FormRequest's `prepareForValidation()` runs before the rules, and `passedValidation()` runs only once
    they pass — using the wrong one turns normalisation into a second validation pass.** `prepareForValidation()`
    is where a slug gets lowercased or a phone number stripped of formatting *before* a rule checks it;
    putting that same normalisation in `passedValidation()` means the rules validated the raw, unnormalised
    input instead. Neither hook is where point 8's authorisation belongs — both run after `authorize()`,
    not in place of it.
34. **Cursor pagination (`cursorPaginate()`) trades random page access for a stable result under concurrent
    writes, which offset pagination (point 21) cannot offer.** An offset-based page is computed by skipping N
    rows at query time, so a row inserted or deleted ahead of the cursor shifts every later page by one — the
    same class of bug point 21 of `skills/laravel-conventions` §4 describes for `chunk()`. A cursor instead
    encodes the last row's sort key in an opaque token, so "page two" means "rows after this key" regardless
    of what changed before it. It costs the ability to jump to an arbitrary page number, which is the
    trade-off to name before reaching for it on an infinite-scroll feed versus a numbered results table.
35. **A resource's `wrap()`/`withoutWrapping()` decides whether the payload's top level is `{"data": {...}}`
    or the bare object, and that decision has to be made once for the whole API, not per resource.** The
    default `data` wrapper is what point 21's collection metadata (`links`, `meta`) sits alongside; calling
    `JsonResource::withoutWrapping()` in a service provider for an API that a frontend already unwraps
    manually removes a redundant nesting level, but flipping it resource-by-resource produces an API where
    some endpoints are wrapped and some are not, which is the same inconsistency point 11's envelope rule
    already forbids for the response shape.
36. **`Http::retry()` bounds how many times an outbound call is retried and on what backoff, and it composes
    with point 18's `Http::pool()` rather than replacing it.** `Http::retry(3, 100)` retries a failing request
    up to three times with a growing delay before the caller ever sees the exception, which is the right tool
    for a flaky third-party API's transient 500s and timeouts — it is not a substitute for point 18's
    concurrency answer to "three slow calls in a loop," because a retried call is still one call, just tried
    more than once. A retry callback (`retry($times, $sleep, $when)`) can also narrow which failures are worth
    retrying, so a 422 from a validation problem on the far side does not get retried into a rate limit.
37. **CORS is one configuration file, not a header set by hand in a controller or middleware.** `config/cors.php`
    declares which origins, methods and headers a browser-based cross-origin caller may use, and the framework's
    own `HandleCors` middleware applies it consistently to every route in the group it's attached to — a
    controller that manually sets `Access-Control-Allow-Origin` on its response duplicates a decision the config
    file already owns, and it is the version that drifts the day the allowed-origins list changes and one
    controller is missed. [Laravel routing docs — CORS, laravel.com/docs/12.x/routing, read 2026-09-10.]
