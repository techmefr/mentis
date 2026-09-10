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
