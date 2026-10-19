# python-conventions §11 — FastAPI specifics

> Section 11 of `skills/python-conventions`. Read it when the web framework is FastAPI and a dependency with
> cleanup, a lifespan, a response model, a background task, the settings object, a proxy setting or a deployment
> shape is written. §9 holds the rules that hold on any ASGI framework (thin routers, separate models, per-object
> authorisation, CORS lists, error shape); this section adds what is specific to FastAPI and does not repeat
> them. Read 2026-10-02 from the FastAPI documentation at the version found in the repository (0.142.2). Points
> that depend on a release carry its number; a project on an older release reads them as "check first".

1. **Declare constraints with `Annotated`.** Put the parameter metadata (`Query`, `Path`, `Body`, a dependency)
   in `Annotated[type, metadata]` and keep the default as a real default. Supported and recommended since
   0.95; the older form with the marker as the default value is still seen in existing code.
2. **The return type is a filter and a validator.** The annotated return type (or `response_model`) validates
   what the handler returns, so a handler that omits a required field fails with a server error instead of
   emitting wrong data, and limits the output to the declared fields. When the handler returns a richer object
   than the response (a database row with a password hash) declare the response class with `response_model`,
   and annotate the return type as `Any` for the type checker if needed; if both are present `response_model`
   wins; `response_model=None` turns it off and is for return types that are not valid fields. Never turn it
   off on an endpoint that returns application data (§9.4).
3. **Startup and shutdown go in the `lifespan` function,** an async context manager passed to the application:
   code before its `yield` runs once before requests are accepted, code after it once after the last request.
   Open pools and load shared models there. If a lifespan is provided, the older startup and shutdown event
   handlers are ignored: use one or the other. Not at import time, so a test that imports the module does not
   pay for it (§9.1).
4. **A dependency that owns a resource uses `yield`, once.** The code before `yield` sets up, the yielded value is
   injected, and the code after it cleans up; nested dependencies are cleaned up in reverse order. A `try`
   around the `yield` receives any exception raised later in the request, so it is where a rollback belongs
   (§7).
5. **When a dependency with `yield` catches an exception, re-raise it** unless it raises another meaningful
   exception. Swallowing it yields a 500 response with nothing in the server logs.
6. **Know when cleanup runs.** By default the exit code runs after the response has been sent
   (`scope="request"`, release 0.121 or later); a dependency declared with `scope="function"` closes right after
   the handler returns and before the response is sent, which suits a session used only to check the caller
   when the response is a long stream, so the connection is not held while bytes travel. The
   sub-dependencies of a request-scoped dependency must themselves be request-scoped.
7. **Background tasks get their own resources.** From 0.106 the exit code of a `yield` dependency no longer waits
   for background tasks, so a task must not use a session yielded by a dependency: open a new one inside the
   task and pass identifiers, not loaded objects. The framework's background tasks run in the same process after
   the response and suit small jobs such as a notification; work that is heavy, must survive a restart, or must
   run on other machines goes to a queue (`skills/background-jobs-conventions`).
8. **A plain `def` handler or dependency runs in a worker thread pool;** an `async def` one runs on the event
   loop. Helper functions you call yourself are not moved anywhere: a blocking `def` called from an `async def`
   handler blocks the loop (§4, §9.7).
9. **Settings are an object read once and injected.** Use a settings class (the pydantic settings package) loaded
   from the environment or a dotenv file, exposed through a dependency function cached so the file is read once
   (`lru_cache`). Tests override that dependency with their own settings instead of editing the environment
   (§9.14); a module-level settings object read at import is the singleton of §6.2.
10. **Override dependencies by the exact callable and reset after.** The application's override mapping is keyed by
    the original function and works for any place it is used (a handler, a decorator, a router include);
    reset it to an empty mapping at the end of the test or in a fixture teardown (§9.14).
11. **Keep strict content-type checking on for JSON bodies.** By default a JSON body is only parsed when the
    request declares a JSON content type; this blocks a cross-site request that a browser sends without a
    preflight and without credentials (a `fetch` with a blob body), which matters for an API with no
    authentication on a local or internal network. Switch it off only for a client that cannot send the header,
    and know that you are removing that protection.
12. **Trust forwarded headers only from the proxy you run.** The server ignores `X-Forwarded-For`, `-Proto` and
    `-Host` unless told which source addresses may supply them; set the allowed-addresses option to the proxy's
    address, not to a wildcard that trusts every sender, since then a client can forge its address and scheme.
13. **Hash passwords with a memory-hard algorithm through a maintained library;** the tutorial's recommended
    algorithm is Argon2 through `pwdlib`, which also reads hashes made by other frameworks (so a migration can
    verify old hashes and write new ones). When authentication looks the user up, verify against a dummy hash
    when the user does not exist so the response time does not reveal which usernames are real. The token and
    session rules are §9.8 and `skills/auth-session-conventions`.
14. **One process per container on an orchestrator.** Process replication with worker processes is the answer on a
    single machine; when containers are replicated by Kubernetes or similar, run a single server process per
    container and let the platform scale.
