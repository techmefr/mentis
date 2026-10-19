# § 12 — Web API shape: minimal APIs, results and errors

> Section 12 of `skills/dotnet-conventions`. Read it when an HTTP endpoint is added or its result type,
> status code or error response changes. Authorisation is §3, publish-time behaviour of the route handlers
> is §9.

1. **Follow the project's endpoint style and do not mix.** If controllers exist, continue with controllers;
   if minimal APIs exist, continue with them; in a new project default to minimal APIs unless controllers
   are requested.
2. **Group minimal endpoints by resource.** One static class per resource with a static method that maps its
   routes, called from the entry point, so the entry file stays a list of resources.
3. **Prefer the typed results factory to the untyped one.** It puts the response types in the signature, so
   the OpenAPI generator sees them. When a handler returns several result types, declare the union return
   type on the lambda; a bare conditional of two different typed results does not compile to a request
   delegate and fails with a misleading arity error. Fall back to the untyped factory only for a handler with
   many branches.
4. **Dedicated request and response types, never the persistence entity.** Sealed records, named by role
   (create request, update request, response, list response). Date and time values are offset-carrying so the
   serialized form is unambiguous; enums serialize as strings so a reordering does not change the contract.
5. **Status codes follow the operation.** A create returns 201 with a location pointing at the new resource;
   a delete returns 204; a missing resource is 404; a conflict is 409. The same table holds for controllers
   and minimal endpoints.
6. **Every endpoint accepts a cancellation token and forwards it** to the service, the query and the outbound
   call, so a disconnected client stops the work.
7. **Errors are one global handler returning problem details**, not a try/catch per endpoint. Map exception
   types to statuses in one exception-handler class; an exception it does not recognise returns false so the
   default handling deals with it, and one it handles is logged before the handler returns true, since true
   suppresses the diagnostics middleware.
8. **Describe each endpoint for the generated OpenAPI**: a name, a summary, the produced types and status
   codes. On the current platform line use the built-in OpenAPI support; do not add the older third-party
   generator to a project on a platform line where it is known to conflict, and keep it where it is already
   installed (`skills/source-freshness`: the line cut-over is version information to re-read).
9. **Stricter JSON handling (strict numbers, exact property casing, no duplicate properties) applies to new
   projects or on request**; an existing API keeps its settings, since clients may rely on them.
