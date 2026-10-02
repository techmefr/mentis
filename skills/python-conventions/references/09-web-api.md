# python-conventions §9 — The web API layer

> Section 9 of `skills/python-conventions`. Read it when an HTTP endpoint, a request or response model, an
> authentication dependency, a CORS setting or an API test is written on an ASGI framework with declarative
> request models (FastAPI is the one the examples mean; the rules hold on any framework of that shape). The
> general async rules are §4, the dependency lifetimes are §6, the persistence rules are §7. The other
> sections and the guardrails stay in `SKILL.md`.

1. **The application is built by a function, not at import.** A `create_app()` that takes its settings and
   returns the application lets a test build one with different configuration, lets a worker import the
   module without starting a server, and keeps import free of side effects (§5). A module-level
   application instance configured from the environment at import is the singleton of §6, point 2, and the
   reason tests share state.
2. **A router is thin: transport in, transport out.** It parses the request, calls one function that holds
   the behaviour, and shapes the response and the status code. Persistence and business rules live in a
   service the router calls, so the same behaviour is reachable from a command, a worker or a test without
   an HTTP client.
3. **Request, update and response models are different classes.** The model a client sends to create a
   record, the one it sends to change part of it, and the one the server returns carry different fields:
   the id and timestamps exist only on the way out, the update model has every field optional, the create
   model has required ones. One shared model with everything optional validates nothing and leaks anything.
4. **Every endpoint that returns application data declares its response model.** The declared model is a
   filter: the framework serialises only its fields, so a field added to the database row does not appear on
   the wire until someone adds it on purpose. Returning an ORM object or a dictionary with no declared model
   is how a password hash, a token or another tenant's column reaches a client. Response models never include
   credentials, hashes, tokens, internal flags or authorisation state.
5. **Constraints belong in the model.** Length, range, pattern, enum membership and cross-field rules are
   declared on the model and validated before the handler runs; a hand-written `if` in the handler repeats
   the declaration and drifts from the documentation the framework generates from it. The generated schema
   is the contract the client is built against, so the declaration is also the documentation.
6. **Authentication and the database session are dependencies, not inline code.** A handler receives the
   current user and the session as parameters resolved by the framework; it does not create a session or
   read a header itself (§6, point 23). A handler that opens its own client or session inside the function
   body cannot be overridden in a test and holds a resource the framework does not manage.
7. **`async def` is for endpoints that await.** An endpoint doing I/O uses the async clients (database, HTTP,
   cache) end to end; a blocking call inside it stalls the event loop for every other request (§4). A plain
   `def` endpoint is run in a worker thread by the framework and is the right form for CPU-bound or blocking
   code that has no async equivalent. Mixing the two silently, an `async def` calling a synchronous driver, is
   the failure.
8. **Token validation checks everything the token claims.** A JWT verification names the accepted
   algorithms in a fixed list (never the one the token's header asks for), checks the signature against the
   issuer's key, and checks expiry, issuer and audience. Accepting an unsigned token or a token whose
   algorithm field selects the verification method is the classic bypass. Keys come from configuration and
   are rotated; the claim set is minimal. The session and cookie rules are `skills/auth-session-conventions`.
9. **Authorisation is checked per object, in the dependency or the service.** Authentication says who; the
   check that this user may read this record (not merely that some user is logged in) runs for every handler
   that takes an identifier from the path, or the endpoint is an enumeration oracle (`skills/security-hardening`
   §3).
10. **CORS lists origins, per environment.** The allowed origins are an explicit list from configuration; a
    wildcard is not combined with credentials; the allowed methods and headers are the ones the front end
    uses. Origins differ between development, staging and production, and the production list is reviewed
    when it changes.
11. **Rate limits cover the entry points that cost something or can be guessed.** Login, token exchange,
    password reset, code verification and anything that sends a message or runs an expensive job are limited
    by the identity being attacked as well as by address, and answer with a retry hint.
12. **Credentials are redacted from logs and errors.** Request logging does not record authorisation headers,
    cookies, bodies of authentication endpoints or tokens in URLs. The exception handler returns a stable
    error body to the client and logs the detail server-side with a correlation id; a stack trace in a
    response is information disclosure.
13. **One error shape for every failure.** Validation errors, authentication failures, not-found and
    conflicts return the same structure with a machine-readable code, mapped from domain exceptions in
    exception handlers registered once, so a handler raises a domain error and never builds an error
    response by hand (`skills/api-design`).
14. **Tests override the exact dependency the handler declares.** The framework's override mapping is keyed
    by the dependency callable used in the signature, so overriding a different function with the same name
    changes nothing and the real dependency runs. The mapping is cleared in teardown, since it is
    process-wide and the next test inherits it (§8, point 12). Use the async test client for an async
    application, and assert the refusal paths (401 without a token, 403 for another user's record, 422 for an
    invalid body) next to the success.
15. **The generated contract is checked in.** The schema the framework generates is exported in CI and
    compared with the committed one, so an accidental breaking change (a removed field, a changed type) fails
    a build instead of a client (`skills/api-design`).
