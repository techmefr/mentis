# § 2 — Server: errors, authorization, batching, HTTP, demand control

> Section 2 of `skills/graphql-conventions`. Read it when a resolver, an error path, an authorization check,
> the HTTP endpoint or an abuse limit is written. Read 2026-10-02 from the GraphQL learning guides (error
> handling, authorization, performance, security, serving over HTTP). The GraphQL-over-HTTP specification they
> cite was a draft on that date.

1. **Two error channels, chosen by whether the failure is exceptional.** Infrastructure failures, invalid
   documents and missing authentication go in the top-level `errors` list. Expected business failures
   (a username taken, a validation failure, insufficient stock) are data in the schema: typed error objects in
   the mutation payload, discoverable through introspection and type-checked by clients.
2. **Authorization lives in the business logic layer, not in resolvers.** A rule written in a resolver has to be
   duplicated at every entry point to the data and drifts. Resolvers call a function that takes the
   authenticated user (pass the fully loaded user object, not an opaque token) and decides. A schema directive
   may declare a generic rule (a required role) but the logic it applies stays in the business layer.
3. **Authenticate before GraphQL runs; authorise during execution.** Place the GraphQL handler after the
   authentication middleware, put the identity into the request context, and make no per-field authorization
   decisions until execution begins.
4. **Batch the data loads of resolvers to avoid N+1.** Per-field resolvers are simple but issue one fetch per
   item; collect the keys requested within a short window and fetch them in one call to the database or
   service (a batching loader), with a per-request cache.
5. **Serve over one endpoint, with JSON.** Accept POST for queries and mutations with a JSON body (the query,
   and optionally operation name, variables, extensions); GET is allowed for queries only. A missing content
   type is a 4xx. Clients state the response media type they accept. Use HTTPS, request timeouts, and cache
   sensitive responses privately or not at all.
6. **GET plus persisted documents is the route to HTTP and CDN caching.** Long documents do not fit in a URL,
   so send a document identifier (a trusted or persisted document) instead of the text. It also shrinks the
   request.
7. **Public and private clients get different demand control.** For first-party clients only, allow-list the
   operations (trusted documents): production runs only documents built and reviewed in development. This does
   not work for a public API, which relies on the limits below.
8. **Limit what one operation can ask for.** Bound the size of any list (pagination with a maximum page size),
   the overall depth, and a smaller depth for nested lists (their cost grows exponentially), the number of
   top-level fields and aliases, and the number of operations in a batch. Reject over-limit documents before
   execution. These are numbers for the team to choose and record; the guide gives none.
9. **Add rate limiting or cost analysis for what limits cannot see.** A field can be expensive without being deep.
   Weight types and fields and reject operations whose estimated cost exceeds a per-request budget, and rate
   limit per client in the network or business layer.
10. **Validate and sanitise argument values in the business layer** (unsafe HTML in a free-text field), since the
    type system checks type but not meaning; a custom scalar can surface the rule in the schema.
11. **Mask error details outside development.** Validation hints with schema suggestions and the messages of
    errors raised in resolvers can reveal the schema and the backends. Turning introspection off for a
    first-party-only API is allowed but is obscurity, not protection: the allow-list in point 7 is the more
    effective control.
12. **Monitor per operation and field.** Collect metrics, traces and logs (an open telemetry instrumentation is the
    named option) to see which fields are slow before tuning them; and enable response compression.
