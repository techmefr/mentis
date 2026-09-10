# § 3 — Authorisation

> Section 3 of `skills/dotnet-conventions`. Read it when an endpoint is added or modified — a controller
> action, a hub method, a minimal-API route — or when a message consumer does work on someone's behalf.

1. **Every endpoint** — controller action, hub method, minimal-API route — carries an explicit authorisation
   declaration naming the policy it requires, alongside its HTTP verb and response declarations. Per-action
   rather than per-controller: an inherited attribute is invisible at the place a reader is looking. The
   reader in question is usually reviewing a diff that adds one action, where the controller's attribute
   is not in the diff at all.
2. An endpoint with no authorisation declaration is treated as a bug, not as "public by design" — public is
   also a decision that gets written down. The reason it has to be written down is that the absence of an
   attribute and a deliberate public endpoint look identical, so nobody can review either.
3. Minimal API: per-endpoint validation and filters are less visible than in classic controllers. Check they
   exist rather than assuming they're inherited from elsewhere. A route group can carry them, which is
   fine — but then the group is what has to be read, and a route added to the wrong group is authorised by
   accident either way.
4. **Authentication answers who, authorisation answers whether — and a bare authorise marker only asks the
   first question.** It admits every authenticated user, which in a multi-tenant or multi-role app is
   almost never what was meant. Name the policy, so the declaration says what is required rather than
   merely that something is.
5. **A policy on the endpoint says who may call it, never which rows they may touch.** The id in the route
   belongs to somebody, and the caller passing it is not necessarily that somebody. Resource-level checks
   happen where the resource is loaded — scope the query by the caller's tenant or ownership rather than
   loading by id and then comparing, because the version that compares afterwards is the version somebody
   eventually refactors away.
6. **A default-deny fallback policy is what makes point 2 enforceable instead of aspirational.** With a
   fallback configured, an endpoint that carries no declaration is refused rather than served, so the
   failure mode of forgetting is a 403 in the developer's face instead of an open route in production.
   Without it, point 2 is a convention that holds exactly as well as everyone's attention.
7. **The allow-anonymous marker overrides everything above it, including the fallback policy.** That makes
   it the single most consequential attribute in the codebase and the one most likely to be added
   "temporarily" while debugging. It deserves the same review as an authorisation change, and a grep for
   it belongs in any security pass.
8. **Authorise the write, not just the read that produced the form.** A reader who cannot see the edit
   screen can still send the request the screen would have sent. Hiding a button is a UI decision; the
   only thing that stops the action is the check on the endpoint that performs it.
9. **Claims are input, and their trustworthiness is exactly that of whoever issued them.** A role read from
   a request header, a query parameter or a client-supplied field is not authorisation — it is a claim the
   caller made about themselves. Only claims from the validated token or the established identity count,
   and a token's issuer, audience and expiry are part of what has to be validated for that to be true.
10. **Not every entry point is an HTTP endpoint.** A hub method is one and needs the same declaration; a
    queue consumer, a scheduled job or a webhook receiver is not reached by the HTTP middleware at all, so
    its authorisation is its own problem — the message's claimed identity has to be verified against
    something, and a webhook's signature is the equivalent of the token.
11. **Middleware order decides whether any of this runs.** Authorisation placed before authentication, or
    an endpoint reached before either, fails open: the attribute is present, the check never happens, and
    nothing in the code looks wrong. There is no analyser for it (§6.2), so it is read by eye at review and
    covered by one test that asserts an anonymous request is refused.
12. **The test that proves a policy is wired is the negative one.** A test asserting an authorised user
    gets a 200 passes just as happily when the policy is missing entirely. One request per endpoint from a
    caller who should be refused is what makes the declaration real, and it is the test that catches the
    day someone widens a policy for an unrelated reason.
13. **A cross-origin policy is not authorisation, and a wide one is not harmless either.** It decides which
    *browser* pages may read our responses; it decides nothing about who may call the endpoint, so widening
    it never fixes a 403 and closing it never protects an API a script can reach directly. What it does
    change is whether another site can make an authenticated request on a logged-in user's behalf and read
    the answer — which is why the platform refuses at run time to combine any-origin with credentials, and
    why the deliberate version of that policy is an explicit list of origins. A test-time wildcard left in
    the pipeline is the usual way it ships.
14. **A custom `IAuthorizationHandler` that calls `Succeed` unconditionally on any match short-circuits
    every other handler for that requirement**, so a second, stricter handler registered for the same
    requirement never runs once the first one succeeds. Requirements are additive by design — a handler
    that wants to *deny* has to call `Fail`, not simply decline to `Succeed`, or a later handler can still
    override a rejection nobody intended to be overridable.
15. **A real-time connection's authorisation is checked once, at the handshake, not on every message it
    later sends.** A hub connection authorised at connect time keeps whatever claims it started with even
    if the underlying token expires or the caller's permissions change mid-connection — a long-lived
    connection needs its own re-validation strategy (a periodic claims refresh, a forced reconnect on
    permission change) or it is authorisation frozen at the moment nobody is watching for it to go stale.
16. **A policy answers a yes/no question about the endpoint; a resource-based check answers the same
    question about the specific row already loaded.** Calling the authorisation service a second time
    against the loaded entity — after it is fetched, before it is acted on — is what point 5's "scope the
    query" advice becomes when scoping the query isn't enough on its own, typically because the rule needs
    data only available once the row is in hand (an approval state, a owner field set after creation). The
    two aren't alternatives: the endpoint policy still answers who may call the action at all, and the
    resource check answers whether this caller may touch this row.
17. **A custom `IAuthorizationRequirement` is where a rule that doesn't reduce to a role or a claim lives**,
    and it is still a requirement rather than an inline `if` scattered across every action that needs it.
    Business rules expressed as requirements are declared once, tested once (point 12's negative test
    applies to each one), and reused by name in every policy that needs them — an inline check copied into
    three controllers is the same rule with three chances to drift out of sync when it changes.
18. **Output caching a response makes the cached bytes outlive the request that authorised them**, unless
    the cache key includes whatever the policy depended on. A response cached by URL alone and served to
    the next caller regardless of identity hands a personalised or restricted answer to whoever asks next —
    caching has to vary by the same dimension the authorisation decision varied by (the user, the tenant,
    the role), or caching becomes a second, unintended authorisation bypass sitting in front of the real
    one.
19. **A minimal-API endpoint filter runs inside the routing pipeline, after model binding and before the
    handler — which is a different position from middleware and matters for what it can check.** A filter
    is the right place for a cross-cutting rule that needs the bound arguments (validating a route
    parameter against a claim, for instance), where middleware only sees the raw request. It is still not
    a substitute for the policy declaration in point 1: a filter registered on a group is exactly as
    invisible to a reader of one action as an inherited controller attribute, for the same reason given
    there.
20. **A background job or a scheduled task acting "as" a user carries that user's identity as data, not as
    an ambient claim it can trust by default.** Queuing work on behalf of a caller and later executing it
    with the caller's id read back from the job payload re-opens point 9's question at the point the job
    runs — nothing re-validated that the id still refers to someone with the right permissions, or that
    those permissions haven't been revoked between enqueue and execution. Re-check authorisation at
    execution time for anything that acts on a stored identity rather than one just established.
21. **`IClaimsTransformation` runs after authentication and before authorisation, which makes it the one
    place a claim can be added but the wrong place for anything that should have been rejected instead.**
    Mapping an external identity provider's group into an internal permission, or attaching a volatile fact
    (a subscription tier looked up per request) belongs here so it stays current without being baked into
    the token — but the method runs on every authorisation check for the lifetime of the principal, so a
    database call inside it runs once per request whether or not the endpoint being checked needed the
    claim at all, and a transformation that throws turns an unrelated endpoint's authorisation into an
    unhandled exception.
22. **A scope and a role answer different questions, and a policy that treats a scope claim like a role
    grants more than it means to.** A role asserts what the caller (a user, typically) is; a scope asserts
    what the *token* was issued to do on that caller's behalf, which for a delegated or client-credentials
    flow can be narrower than everything that identity is normally allowed. Checking `scope` where the
    policy actually means `role` — or the reverse — either refuses a legitimately scoped-down token or
    accepts one that never should have reached that endpoint, and the two claim types are easy to conflate
    because both end up as strings on the same principal.
23. **A downstream call made on behalf of the caller needs its own token, acquired for that specific
    audience — forwarding the inbound token to a second API is not the same thing.** The On-Behalf-Of flow
    exchanges the incoming token for one scoped to the API being called next, so each hop in a chain gets a
    token whose audience and scopes match only what that hop needs; passing the original token straight
    through instead means every downstream service now accepts a credential minted for a different
    audience, and any one of them compromised can replay it against the others. This is point 9's "claims
    are input" applied one hop further down the chain, where the hop itself is the attacker's easiest
    target.
24. **A GraphQL resolver is an entry point the same as a controller action, and schema-level type
    permissions don't authorise the field a specific query actually walks into.** A field returning a
    related entity (an order's customer, a customer's other orders) can be reached through more than one
    path in the graph, and a check placed on the root query alone leaves every field resolver it can reach
    unauthorised on its own — the same "per-action, not inherited" reasoning as point 1, applied to a schema
    where the reader can't see every path in the diff that adds one field.
25. **Real-time authorisation state in a stateful UI (a Blazor Server circuit, a long-lived SPA session) is
    cached in the client's own memory, and it goes stale the moment the source of truth changes without the
    client knowing.** An `AuthenticationStateProvider` read once at circuit start reflects permissions as
    of that moment; a permission revoked server-side mid-session leaves the UI showing options the next
    server-side check would refuse, which is harmless as long as every action is still checked at the
    endpoint (point 8) — the failure mode this point actually guards against is trusting that cached state
    for the decision instead of just for what the UI shows.
26. **`IAuthorizationService.AuthorizeAsync` has an overload that takes the resource itself, and reaching for
    the resource-less one is how point 5's "scope the query" advice gets skipped by accident.** Passing the
    loaded entity alongside the policy name lets a requirement handler read fields only available on that
    row — an owner id, an approval state — inside the same evaluation the policy already runs, instead of a
    second bespoke `if` written next to the call. The overload exists specifically so "check this policy
    against this row" stays one declared check rather than a policy check plus a hand-rolled comparison
    living beside it.
27. **A custom `IAuthorizationMiddlewareResultHandler` replaces the framework's default failure handling for
    every endpoint, not just the one it was written for.** The default handler is what turns a failed
    requirement into the 403 or 401 point 6's fallback relies on; a custom one registered to add a header or
    a logging line on failure has to also reproduce that behaviour for the general case, or every endpoint's
    failure response silently changes shape (a redirect where a 403 was expected, a 200 with an error body)
    the moment the custom handler is wired in, whether or not it was meant to touch that endpoint.
28. **A permission checked through a custom `IAuthorizationPolicyProvider` is resolved by name at
    evaluation time, not enumerated at startup — which moves the typo from a compile error to a silent
    allow-nothing policy.** A dynamic provider that builds a policy per requested permission string (rather
    than registering each one up front) makes `[Authorize(Policy = "orders:approve")]` valid syntax for any
    string at all; a policy name that doesn't match what the provider expects resolves to a policy with no
    requirements or fails open depending on how the provider's fallback is written; a test for the exact
    string, not just for "some policy is attached," is what point 12 still asks for here.
29. **A `required` init-only property on a command or DTO removes the "was this ever set" question the
    authorisation code below it silently depended on.** Before `required` (C# 11), an `OwnerId` or
    `TenantId` left as its type's default on a payload that skipped validation could sail through a
    resource-based check that trusted the field was populated by the model binder — the check ran, just
    against a zero or a null it never questioned. Marking the identity-bearing property `required` turns a
    missing value into a construction-time failure before the authorisation code is reached at all, rather
    than a value the authorisation logic has to defensively re-validate on every path that builds the type.
30. **A step-up or re-authentication requirement is a second authorisation decision layered on the first,
    not a stronger version of the same policy.** An action sensitive enough to need a fresh MFA
    challenge — changing a payment destination, elevating another user's role — needs its own requirement
    that inspects how recently the current session actually re-proved the second factor (an `amr` or `auth_time`
    claim), because the ordinary policy only proves the session is still valid, not that it was recently
    re-confirmed; treating "authenticated an hour ago" as equivalent to "just re-entered a code" collapses
    two different guarantees into one check that only ever validates the weaker one.
31. **A permission model built on named roles hard-codes the org chart into the authorisation code, and the
    fix is a permission the role is assigned rather than a role name compared directly.** `[Authorize(Roles =
    "Manager")]` reads as a policy but is really string comparison against a job title; the day a new title
    needs the same access, or an existing one needs less, the fix is a code change and a redeploy rather than
    a data change. A policy built from a permission claim the role grants keeps the redeploy for when the
    *rule* changes and turns "who has this role" into administration instead of engineering.
32. **ASP.NET Core's built-in authentication and authorisation metrics (`System.Diagnostics.Metrics`) surface
    a failing policy without a hand-written log line, and reaching for a custom counter first duplicates
    what's already emitted.** The framework instruments the authentication and authorisation middleware
    itself, so a spike in refused requests for one policy is visible to whatever reads the `Meter` — the same
    signal point 12's negative test only proves once, at build time — the counter shows it happening in
    production, continuously, without a bespoke log-then-count pipeline built around point 27's rule about
    logging at the boundary.
33. **A cookie-authenticated endpoint answers a browser and an API caller differently, and which one it
    thinks it's talking to changes point 6's fallback failure mode.** Cookie authentication historically
    redirected an unauthenticated request to a login page regardless of caller, which is correct for a
    browser navigation and wrong for a fetch from a script — the platform now distinguishes the two and
    returns a bare 401/403 to a request that looks like an API call instead of a redirect it can't follow
    usefully, but the detection is heuristic (an `Accept` header, a same-site check), so a caller wired to
    expect a status code and receiving a redirect page instead — or the reverse — is this distinction guessing
    wrong, not the fallback itself failing.
34. **A passkey (WebAuthn) credential registered through ASP.NET Core Identity changes what "the same
    factor, twice" means for point 30's step-up requirement.** A resident key backed by platform
    authentication already asserts user presence and, depending on the authenticator, user verification at
    the moment it's used — so a policy written assuming every session needs a separate second factor on top of
    a password has to ask what a passkey's own assertion already proves, or it demands a redundant challenge
    for a credential whose entire design point was replacing that challenge with the sign-in step itself.
35. **`RequireAuthorization()` chained on a route group and again on one endpoint inside it does not replace
    the group's policy with the endpoint's — it adds a second requirement to satisfy, which is a different
    failure shape from point 12's "missing entirely."** Calling it a second time layers requirements the same
    way multiple `[Authorize]` attributes on one action do; an endpoint meant to *loosen* the group's policy
    for one route needs `AllowAnonymous` (point 7) or a differently-scoped group, not a second, narrower
    `RequireAuthorization` call that a reader might expect to override rather than accumulate.
36. **Minimal API's built-in request validation runs as an endpoint filter, which places it after the
    authorisation decision in the pipeline, not before it.** Validation attributes on a route's parameters
    are checked by a filter (point 19) that executes once binding and authorisation have already run — so a
    payload that fails validation was still authorised to reach the handler, and a policy that depends on a
    validated shape of the request (a tenant id that must already be well-formed before a resource-based
    check reads it) cannot rely on validation having happened first; the resource-based check in point 16
    still has to defend against a value that passed authorisation but hasn't been validated yet.
37. **Rate limiting placed after authentication and authorisation in the middleware pipeline limits the wrong
    thing, and placed before it limits by an identity nothing has verified yet.** The rate limiter middleware
    reads whatever it's configured to partition on — often the caller's identity — so registering it after
    authentication lets it key correctly per authenticated user, matching the ordering point 11 already
    insists on for authentication and authorisation themselves; registered before authentication instead, it
    can only partition by IP or an anonymous key, which throttles a shared NAT or proxy as one caller and
    never distinguishes the users behind it — a decision made once, at the same composition root point 11
    already points to, not discovered per endpoint.
38. **The fallback policy (point 6) and the default policy answer two different questions, and configuring
    only one leaves the other's gap exactly where it was.** The default policy is what a bare `[Authorize]`
    with no policy name evaluates against; the fallback policy is what applies to an endpoint carrying no
    authorisation metadata at all. Widening the default policy tightens every unnamed `[Authorize]` in the
    codebase without touching a single endpoint that has no attribute whatsoever — point 2's "no declaration
    is a bug" is only enforced by the second setting, and a team that configures the first alone has fixed a
    different problem than the one point 6 describes.
39. **A fallback policy reaches endpoints the team didn't write authorisation for because it forgot they
    exist, not only ones it forgot to annotate — the app's own OpenAPI document and a Scalar/Swagger UI
    endpoint are typically registered without an explicit policy and inherit the fallback like anything
    else.** Where the fallback is authenticated-user-required, an API surface meant to stay publicly
    browsable now 401s at the door unless it's explicitly carved out with `AllowAnonymous` (point 7) — which
    is the fallback doing exactly what point 6 asks of it, surfacing as a bug report about the docs page
    rather than a security gap, because nobody thought of the docs page as "an endpoint."
40. **`AddAuthorizationBuilder` centralises every policy declaration in one fluent chain at the composition
    root, but it does not configure a fallback or default policy on its own — leaving either unset is a
    choice made by omission, not a safe default the builder API supplies for you.** The builder is a better
    place to satisfy point 6 than a bare `AddAuthorization` delegate, precisely because every policy is
    declared in the same readable chain a reviewer can scan top to bottom for a missing `.SetFallbackPolicy()`
    call — but the chain itself does not warn when that call is absent, so the builder changes where the gap
    is visible without changing whether it exists.
41. **`IAuthorizationRequirementData` lets a custom attribute be both the thing decorating the action and the
    requirement the policy evaluates, collapsing point 17's "declare the requirement once" into one
    declaration instead of two.** A hand-rolled requirement still needs a named policy string wired to it
    separately from the attribute that references that name; a requirement-data attribute is applied directly
    to the action (`[MinimumAge(18)]`) and generates its own requirement and policy behind the scenes, which
    removes the step where the attribute's policy-name string and the policy registration's own string can
    drift out of sync with each other — the same class of typo point 28's dynamic provider already has to
    guard against for a hand-strung policy name.
42. **A dynamic `IAuthorizationPolicyProvider` (point 28) combining several attributes on one action into a
    single evaluated policy runs that combination on every request the endpoint serves, not once at
    startup.** Where `[Authorize]` is stacked with a resource-based check or a custom requirement attribute
    from point 41, the provider's job is to fold them into one policy result each time — a provider that
    recomputes an expensive combination per request rather than caching by the exact attribute set pays that
    cost on the hot path point 3's "read it by eye at review" doesn't catch, because nothing about the
    attributes on the action looks like a performance decision.
43. **`RequireAuthorization()` chained through nested `MapGroup` calls accumulates the same way point 35
    already describes for one group and one endpoint, and nesting hides how many layers actually stacked.**
    A route group inside another route group, each adding its own `RequireAuthorization`, means an endpoint at
    the innermost level satisfies every requirement from every enclosing group at once — which is the correct
    behaviour, but a reader checking one group's policy for what an endpoint requires has to walk every
    ancestor group to see the whole set, the same "invisible at the one place a reader is looking" problem
    point 1 states for a controller-level attribute, now one nesting level per group instead of one class.
