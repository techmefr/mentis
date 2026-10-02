# § 5 — The API layer and tests

> Section 5 of `skills/django-conventions`. Read it when an HTTP endpoint (plain Django views or a REST
> framework on top) is written, an error shape is decided, or tests are added. The service and selector layers
> these endpoints call are §1; the error body shape itself is `skills/api-design` §5. The endpoint structure is a
> style guide's preference, the test points are the framework's testing topic. Read 2026-10-02.

1. **One handler per operation, as simple as the framework allows.** Create, read, update and delete are four
   handlers, each with its own permission, input and output; a generic class that wires a serializer to
   persistence is where logic hides from the service layer. The handler fetches what the call needs, calls one
   service or selector, and returns. Pick a convention for where objects are fetched from the path id (in the
   handler, or in the service) and keep it everywhere.
2. **Separate input and output shapes.** A dedicated input serializer for what comes in and a dedicated output
   one for what goes out, defined next to the handler that uses them; reuse them as little as possible, since
   a shared one changes the behaviour of every handler when it changes. A hand-written `Serializer` states
   exactly which fields exist; a model-derived one exposes whatever the model grows next, so choose it knowingly
   (`skills/api-design` §2.2).
3. **One URL per operation, grouped by domain.** Keep a pattern list per domain and include it from the root, so
   the URL file reads as a table of contents.
4. **Decide what an error looks like before the second endpoint exists.** Pick the status for each class of
   failure (validation 400, authentication 401, permission 403, not found 404, throttling 429, server error 500)
   and the body shape, once, and make the framework's exception handling produce it for every route; adopt the
   standard problem-details body if the API has outside consumers (`skills/api-design` §5.7). Never swallow an
   exception that produces a 500: it is reported to the error tracker, and the client gets the stable body, not
   the traceback.
5. **Domain errors are raised by services and translated in one place.** A service raises its own exception
   type; one handler maps it to the agreed status and body. A view that builds an error response by hand is a
   second place for the contract to drift.
6. **Tests mirror the layers.** Tests for models, selectors, services and endpoints live in separate modules,
   one test module per tested unit named after it, one test case per unit. Service tests carry the business
   logic coverage, **hit the database**, and replace only the background-task call and whatever leaves the
   process; a service test that mocks the ORM tests nothing.
7. **Use `TestCase`; it wraps each test in a transaction,** which is the cheap way to isolate the database. A
   test that needs real commits (anything exercising `on_commit` behaviour through real transactions, or
   concurrency) uses the transactional test case, or the `captureOnCommitCallbacks` helper to run the
   callbacks inside an ordinary test.
8. **Build shared data once per class** (`setUpTestData`), not once per test, and build the rest with factories
   so each test states the fields it cares about.
9. **Keep the suite fast, deliberately.** Run tests in parallel when they are isolated; preserve the test
   database between runs locally; swap in a fast password hasher in the test settings module (and keep any
   hasher your fixtures use in the list); keep media files in memory storage. All of these live in the test
   settings, never in the production ones (§4.7).
10. **Assert refusals as well as success** for each endpoint: unauthenticated, wrong user's object, invalid input,
    and the error body shape agreed in point 4.
