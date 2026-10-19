# § 3 — Authorisation

> Section 3 of `skills/dotnet-conventions`. Read it when an endpoint is added or modified — a controller
> action, a hub method, a minimal-API route — or when a message consumer does work on someone's behalf.

1. **Every endpoint** — controller action, hub method, minimal-API route — carries an explicit authorisation
   declaration naming the policy it requires, alongside its HTTP verb and response declarations. Per-action
   rather than per-controller: an inherited attribute is invisible where a reader is looking, usually a diff
   that adds one action, where the controller's attribute isn't in the diff.
2. An endpoint with no authorisation declaration is a bug, not "public by design" — public is also a
   decision that gets written down. A missing attribute and a deliberate public endpoint look identical, so
   neither can be reviewed.
3. Minimal API: per-endpoint validation and filters are less visible than in classic controllers. Check they
   exist rather than assuming they're inherited. A route group can carry them, but then the group is what
   must be read, and a route added to the wrong group is authorised by accident either way.
4. **Authentication answers who, authorisation answers whether — and a bare authorise marker only asks the
   first.** It admits every authenticated user, almost never what a multi-tenant or multi-role app meant.
   Name the policy, so the declaration says what is required.
5. **A policy on the endpoint says who may call it, never which rows they may touch.** The id in the route
   belongs to somebody, and the caller passing it isn't necessarily that somebody. Resource-level checks
   happen where the resource is loaded — scope the query by the caller's tenant or ownership rather than
   loading by id and comparing, because the compare-afterwards version is the one somebody eventually
   refactors away.
6. **A default-deny fallback policy is what makes point 2 enforceable.** With a fallback configured, an
   endpoint with no declaration is refused rather than served: forgetting yields a 403 in the developer's
   face instead of an open route in production. Without it, point 2 holds exactly as well as everyone's
   attention.
7. **The allow-anonymous marker overrides everything above it, including the fallback policy.** It is the
   most consequential attribute in the codebase and the one most likely added "temporarily" while
   debugging. Review it like an authorisation change, and grep for it in any security pass.
8. **Authorise the write, not just the read that produced the form.** A reader who cannot see the edit
   screen can still send the request it would have sent. Hiding a button is a UI decision; only the check on
   the endpoint that performs the action stops it.
9. **Claims are input, and trustworthy only as far as whoever issued them.** A role read from a request
   header, query parameter or client-supplied field is a claim the caller made about themselves, not
   authorisation. Only claims from the validated token or established identity count, and the token's
   issuer, audience and expiry must be validated for that to hold.
10. **Not every entry point is an HTTP endpoint.** A hub method is one and needs the same declaration; a
    queue consumer, scheduled job or webhook receiver is not reached by the HTTP middleware, so its
    authorisation is its own problem — the message's claimed identity must be verified against something,
    and a webhook's signature is the equivalent of the token.
11. **Middleware order decides whether any of this runs.** Authorisation before authentication, or an
    endpoint reached before either, fails open: the attribute is present, the check never happens, and
    nothing looks wrong. No analyser exists for it (§6.2), so read it by eye at review and cover it with one
    test asserting an anonymous request is refused.
12. **The test that proves a policy is wired is the negative one.** A test asserting an authorised user gets
    a 200 passes just as happily when the policy is missing. One request per endpoint from a caller who
    should be refused makes the declaration real, and catches the day someone widens a policy for an
    unrelated reason.
13. **A cross-origin policy is not authorisation, and a wide one is not harmless.** It decides which
    *browser* pages may read our responses and nothing about who may call the endpoint: widening it never
    fixes a 403, closing it never protects an API a script can reach directly. It does change whether
    another site can make an authenticated request on a logged-in user's behalf and read the answer — which
    is why the platform refuses at run time to combine any-origin with credentials, and why the deliberate
    policy is an explicit list of origins. A test-time wildcard left in the pipeline is the usual way it
    ships.
14. **A custom `IAuthorizationHandler` that calls `Succeed` unconditionally on any match short-circuits
    every other handler for that requirement**, so a second, stricter handler never runs once the first
    succeeds. Requirements are additive by design — a handler that wants to *deny* must call `Fail`, not
    merely decline to `Succeed`, or a later handler can override a rejection nobody meant to be overridable.
15. **A real-time connection's authorisation is checked once, at the handshake, not on every message.** A
    hub connection keeps the claims it started with even if the token expires or permissions change
    mid-connection; a long-lived connection needs its own re-validation (periodic claims refresh, forced
    reconnect on permission change) or authorisation is frozen at the moment nobody watches it go stale.
16. **A policy answers a yes/no question about the endpoint; a resource-based check answers it about the
    specific row already loaded.** Calling the authorisation service a second time against the loaded
    entity, before acting on it, is what point 5's "scope the query" becomes when scoping isn't enough,
    typically because the rule needs data only available with the row in hand (an approval state, an owner
    field set after creation). They aren't alternatives: the endpoint policy still answers who may call the
    action, the resource check whether this caller may touch this row.
17. **A custom `IAuthorizationRequirement` is where a rule that doesn't reduce to a role or claim lives**,
    and it is a requirement, not an inline `if` scattered across actions. Declared once, tested once (point
    12's negative test applies to each), reused by name in every policy that needs it — an inline check
    copied into three controllers is one rule with three chances to drift.
18. **Output caching a response makes the cached bytes outlive the request that authorised them**, unless
    the cache key includes whatever the policy depended on. A response cached by URL alone and served to
    the next caller regardless of identity hands a personalised or restricted answer to whoever asks next;
    caching must vary by the dimension the authorisation decision varied by (user, tenant, role), or it is a
    second, unintended bypass in front of the real one.
19. **A minimal-API endpoint filter runs inside the routing pipeline, after model binding and before the
    handler — a different position from middleware.** It is the place for a cross-cutting rule needing the
    bound arguments (validating a route parameter against a claim), where middleware only sees the raw
    request. It does not replace point 1's policy declaration: a filter registered on a group is as
    invisible to a reader of one action as an inherited controller attribute.
20. **A background job or scheduled task acting "as" a user carries that user's identity as data, not as an
    ambient claim it can trust.** Executing queued work with the caller's id read back from the job payload
    re-opens point 9's question at run time — nothing re-validated that the id still refers to someone with
    the right permissions, or that they weren't revoked between enqueue and execution. Re-check
    authorisation at execution time for anything acting on a stored identity.
21. **`IClaimsTransformation` runs after authentication and before authorisation: the one place a claim can
    be added, the wrong place for anything that should have been rejected.** Mapping an external provider's
    group into an internal permission, or attaching a volatile fact (a subscription tier looked up per
    request), belongs here so it stays current without being baked into the token — but it runs on every
    authorisation check for the principal's lifetime, so a database call inside it runs once per request
    whether or not the endpoint needed the claim, and a transformation that throws turns an unrelated
    endpoint's authorisation into an unhandled exception.
22. **A scope and a role answer different questions, and a policy treating a scope claim like a role grants
    more than it means to.** A role asserts what the caller is; a scope asserts what the *token* was issued
    to do on that caller's behalf, which in a delegated or client-credentials flow can be narrower than
    everything that identity may do. Checking `scope` where the policy means `role`, or the reverse,
    refuses a legitimately scoped-down token or accepts one that should never reach the endpoint; both are
    strings on the same principal, so they are easily conflated.
23. **A downstream call on behalf of the caller needs its own token, acquired for that audience —
    forwarding the inbound token to a second API is not the same.** The On-Behalf-Of flow exchanges the
    incoming token for one scoped to the next API, so each hop gets a token whose audience and scopes match
    only what that hop needs; passing the original through makes every downstream service accept a
    credential minted for a different audience, and any one compromised can replay it against the others.
    This is point 9's "claims are input" one hop further down, where the hop is the attacker's easiest
    target.
24. **A GraphQL resolver is an entry point like a controller action, and schema-level type permissions
    don't authorise the field a query actually walks into.** A field returning a related entity (an order's
    customer, a customer's other orders) is reachable by more than one path in the graph, and a check on
    the root query alone leaves every reachable field resolver unauthorised — point 1's "per-action, not
    inherited" in a schema where the reader can't see every path in the diff that adds one field.
25. **Authorisation state in a stateful UI (a Blazor Server circuit, a long-lived SPA session) is cached in
    the client's memory and goes stale when the source of truth changes unseen.** An
    `AuthenticationStateProvider` read once at circuit start reflects permissions as of then; a permission
    revoked server-side leaves the UI showing options the next server check would refuse. That is harmless
    while every action is still checked at the endpoint (point 8) — the failure guarded against is trusting
    the cached state for the decision instead of only for what the UI shows.
26. **`IAuthorizationService.AuthorizeAsync` has an overload taking the resource itself, and the
    resource-less one is how point 5's "scope the query" gets skipped by accident.** Passing the loaded
    entity with the policy name lets a requirement handler read fields only on that row (owner id, approval
    state) inside the same evaluation, instead of a second bespoke `if` beside the call: "check this policy
    against this row" stays one declared check.
27. **A custom `IAuthorizationMiddlewareResultHandler` replaces the framework's default failure handling for
    every endpoint, not just the one it was written for.** The default turns a failed requirement into the
    403 or 401 point 6's fallback relies on; a custom one added for a header or logging line must also
    reproduce that for the general case, or every endpoint's failure response silently changes shape (a
    redirect where a 403 was expected, a 200 with an error body) once it is wired in.
28. **A permission checked through a custom `IAuthorizationPolicyProvider` is resolved by name at
    evaluation time, not enumerated at startup — moving the typo from a compile error to a silent
    allow-nothing policy.** A dynamic provider building a policy per permission string makes
    `[Authorize(Policy = "orders:approve")]` valid syntax for any string; a name the provider doesn't expect
    resolves to a policy with no requirements or fails open, depending on its fallback. Point 12 still
    asks for a test of the exact string, not just "some policy is attached".
29. **A `required` init-only property on a command or DTO removes the "was this ever set" question the
    authorisation code below silently depended on.** Before `required` (C# 11), an `OwnerId` or `TenantId`
    left at its default on a payload that skipped validation could pass a resource-based check that trusted
    the binder had populated it — the check ran against a zero or null it never questioned. Marking the
    identity-bearing property `required` turns a missing value into a construction-time failure before the
    authorisation code is reached, instead of a value it must defensively re-validate on every path.
30. **A step-up or re-authentication requirement is a second authorisation decision layered on the first,
    not a stronger version of the same policy.** An action needing a fresh MFA challenge — changing a
    payment destination, elevating another user's role — needs its own requirement inspecting how recently
    the session re-proved the second factor (an `amr` or `auth_time` claim), because the ordinary policy
    proves only that the session is valid. Treating "authenticated an hour ago" as "just re-entered a code"
    collapses two guarantees into one check that validates only the weaker.
31. **A permission model built on named roles hard-codes the org chart into the authorisation code; assign
    the role a permission instead of comparing a role name.** `[Authorize(Roles = "Manager")]` reads as a
    policy but is string comparison against a job title; when a new title needs the same access, or an
    existing one less, the fix is a code change and redeploy instead of a data change. A policy built from
    a permission claim the role grants keeps redeploys for when the *rule* changes and makes "who has this
    role" administration, not engineering.
32. **ASP.NET Core's built-in authentication and authorisation metrics (`System.Diagnostics.Metrics`)
    surface a failing policy without a hand-written log line; a custom counter first duplicates what is
    emitted.** The framework instruments the middleware itself, so a spike in refused requests for one
    policy is visible to whatever reads the `Meter` — what point 12's negative test proves once at build
    time, shown continuously in production without a bespoke log-then-count pipeline against point 27's
    rule about logging at the boundary.
33. **A cookie-authenticated endpoint answers a browser and an API caller differently, and which it thinks
    it faces changes point 6's fallback failure mode.** Cookie authentication historically redirected any
    unauthenticated request to a login page — right for a browser navigation, wrong for a script's fetch.
    The platform now returns a bare 401/403 to a request that looks like an API call, but detection is
    heuristic (an `Accept` header, a same-site check), so a caller expecting a status code and getting a
    redirect page, or the reverse, is this distinction guessing wrong, not the fallback failing.
34. **A passkey (WebAuthn) credential registered through ASP.NET Core Identity changes what "the same
    factor, twice" means for point 30's step-up.** A resident key backed by platform authentication already
    asserts user presence and, depending on the authenticator, user verification when used, so a policy
    assuming every session needs a separate second factor on top of a password must ask what the passkey's
    own assertion already proves, or it demands a redundant challenge for a credential designed to replace
    that challenge with the sign-in step.
35. **`RequireAuthorization()` chained on a route group and again on one endpoint inside it adds a second
    requirement rather than replacing the group's — a different failure shape from point 12's "missing
    entirely".** A second call layers requirements as multiple `[Authorize]` attributes on one action do;
    an endpoint meant to *loosen* the group's policy needs `AllowAnonymous` (point 7) or a differently
    scoped group, not a narrower `RequireAuthorization` a reader might expect to override.
36. **Minimal API's built-in request validation runs as an endpoint filter, after the authorisation
    decision.** Validation attributes on route parameters are checked by a filter (point 19) that runs
    after binding and authorisation, so a payload failing validation was still authorised to reach the
    handler, and a policy depending on a validated shape (a tenant id that must be well-formed before a
    resource-based check reads it) cannot assume validation ran first; point 16's resource-based check must
    still defend against a value that passed authorisation but isn't validated.
37. **Rate limiting placed after authentication and authorisation in the pipeline limits the wrong thing,
    and placed before it limits by an identity nothing has verified.** The limiter partitions on whatever
    it is configured to — often the caller's identity — so registering it after authentication keys per
    authenticated user, matching point 11's ordering; before authentication it can only partition by IP or
    an anonymous key, throttling a shared NAT or proxy as one caller. Decide it once, at the composition
    root point 11 points to, not per endpoint.
38. **The fallback policy (point 6) and the default policy answer different questions; configuring only one
    leaves the other's gap where it was.** The default policy is what a bare `[Authorize]` with no policy
    name evaluates against; the fallback applies to an endpoint with no authorisation metadata at all.
    Widening the default tightens every unnamed `[Authorize]` without touching an endpoint that has no
    attribute — point 2's "no declaration is a bug" is enforced only by the second setting.
39. **A fallback policy reaches endpoints the team forgot exist, not only ones it forgot to annotate: the
    app's own OpenAPI document and a Scalar/Swagger UI are typically registered without a policy and inherit
    the fallback.** Where the fallback requires an authenticated user, an API surface meant to stay publicly
    browsable now 401s unless carved out with `AllowAnonymous` (point 7) — the fallback doing what point 6
    asks, surfacing as a bug report about the docs page rather than a security gap, because nobody thought
    of the docs page as "an endpoint".
40. **`AddAuthorizationBuilder` centralises every policy declaration in one fluent chain at the composition
    root, but sets no fallback or default policy on its own — leaving either unset is a choice by omission,
    not a safe default.** It is a better place to satisfy point 6 than a bare `AddAuthorization` delegate
    because a reviewer can scan one chain for a missing `.SetFallbackPolicy()`, but the chain doesn't warn
    when it is absent: the builder changes where the gap is visible, not whether it exists.
41. **`IAuthorizationRequirementData` lets a custom attribute be both the decoration on the action and the
    requirement the policy evaluates, collapsing point 17's "declare the requirement once" into one
    declaration.** A hand-rolled requirement needs a named policy string wired separately from the
    attribute referencing it; a requirement-data attribute applied directly (`[MinimumAge(18)]`) generates
    its own requirement and policy, removing the step where the attribute's policy-name string and the
    registration's string drift apart — the typo class point 28's dynamic provider must guard against for a
    hand-strung name.
42. **A dynamic `IAuthorizationPolicyProvider` (point 28) combining several attributes on one action into a
    single policy runs that combination on every request, not once at startup.** Where `[Authorize]` is
    stacked with a resource-based check or a point-41 requirement attribute, the provider folds them into
    one result each time; one that recomputes an expensive combination per request instead of caching by the
    exact attribute set pays on the hot path, which point 11's "read it by eye at review" doesn't catch
    because nothing about the attributes looks like a performance decision.
43. **`RequireAuthorization()` chained through nested `MapGroup` calls accumulates as point 35 describes
    for one group and one endpoint, and nesting hides how many layers stacked.** An endpoint in a group
    inside another group, each adding `RequireAuthorization`, satisfies every requirement of every
    enclosing group at once — correct, but a reader checking one group for what an endpoint requires must
    walk every ancestor group, point 1's "invisible at the one place a reader is looking", now one nesting
    level per group instead of one class.
