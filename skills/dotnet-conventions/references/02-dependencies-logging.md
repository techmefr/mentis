# § 2 — Dependencies and logging

> Section 2 of `skills/dotnet-conventions`. Read it when a dependency is injected or registered, a service
> lifetime is chosen, configuration is read, or something is logged.

1. Dependencies injected **through the constructor**, as `private readonly` interface fields, written as an
   **explicit constructor** — not a primary constructor on the class header. The two look like the same
   feature but aren't: a primary-constructor parameter carries no `readonly` modifier at all and stays
   assignable from any member the moment something reads it, and there's no constructor body for a
   multi-statement guard or a computed field. (This is the opposite conclusion from PHP's constructor
   property promotion, which *is* mandatory there — a promoted PHP parameter carries `private readonly` in
   the signature itself, so it's the full property declaration; a C# header parameter carries neither.)
   **Where primary constructors stay**: `record`/`record struct` (their parameters become public init-only
   properties, not a hidden mutable capture field — the objection doesn't apply), a plain `struct`, test
   fixtures, and generated/scaffolded code. Existing primary constructors in older files stay; a new class
   follows this rule regardless of what sits next to it.
2. **Never the Service Locator** (`IServiceProvider.GetService`/`GetRequiredService`) inside a class doing
   work: it hides the dependency from the constructor, so nothing fails at composition time and everything
   fails at runtime. It also makes the class untestable without a container, which is how a unit test ends
   up building half the application to exercise one method.
3. A service depends only on a service whose lifetime is **equal to or longer than its own**. A `Scoped`
   service injected into a `Singleton` (captive dependency) freezes for the app's lifetime — a `DbContext`
   shared between concurrent requests is the canonical disaster. What that looks like in production is not
   a clean failure: it is tracked entities from one user's request appearing in another's, and change
   tracking that saves the wrong row.
4. A `Singleton` or background worker that needs a scoped service creates a scope explicitly
   (`IServiceScopeFactory`), never injects the scoped service directly. The scope is per unit of work — one
   per message, per tick, per batch — and it is disposed when that unit ends, which is also what returns
   the connection to the pool.
5. Every working class injects a generic logger parameterised by itself (`ILogger<TSelf>`): the type
   parameter sets the log category, which is what lets ops filter and route logs at all. A logger
   parameterised by a base class or by some shared type collapses several components into one category,
   and the filter that was meant to quiet one of them silences all of them.
6. Too many constructor parameters is a design signal, not a formatting problem: the class is doing several
   jobs. The number is not the rule — the question is whether any single method uses most of them. When
   each method uses three of the nine, there are three classes here.
7. Composition happens at the application root, in one place, not scattered across the modules being
   composed. A module that registers its own dependencies at import time makes the app's dependency graph
   unreadable and makes a test unable to substitute anything without loading the module.
8. **Configuration reaches code as a typed object.** Each section is bound and validated **once** at the
   composition root, and what gets injected is the typed accessor — business code never takes the raw
   configuration abstraction and never reads a key by string. What this buys is when the failure happens: a
   misspelled or missing key becomes a boot error with the section named, instead of a null two hours into
   the first request that needed it.
9. **A log call on a per-item, per-request or per-tick path is declared, not interpolated.** Where the
   platform ships a source generator for log methods, the hot path calls a generated method and pays no
   boxing or string work when the level is disabled; the ordinary logger call stays right for a cold path.
   Everything else about logging — the injected category, the level choice, no interpolation into the
   template — is point 5 and unchanged.
10. **The container verifies a registration when something resolves it, not when it is built.** So a
    missing or mis-scoped registration is a 500 on the first request that needs that type — possibly weeks
    after the deploy, on the one endpoint nobody smoke-tested. Turn it into a boot failure: the host can
    validate the graph and the scopes at startup, and that switch is worth more than any test here.
11. **A disposable resolved from the root provider is held until the process ends.** The container disposes
    what it created when the owning scope is disposed, and the root scope is never disposed while the app
    runs — so a transient disposable resolved outside a request scope accumulates. It looks like a slow
    leak, which is the hardest kind to attribute.
12. **Registration order matters, and the two ways to register mean different things.** For a single
    resolve the last registration wins, so a re-registration silently replaces an earlier one; the
    try-add form registers only if nothing has, which is how a library provides a default without stomping
    the application's choice. Using the wrong one is how a test's fake ends up not being used at all.
13. **A log template's placeholders are structured fields; interpolating the values destroys them.** The
    message reads the same to a human and stops being queryable — no filtering by order id, no grouping by
    tenant, no alert on a field. Since the reason to have a log aggregator is exactly that, the
    interpolated call is the one that costs money without buying anything.
14. **Never log a secret, a token or personal data — log the identifier instead.** A logged request body or
    a logged entity travels to a system with a different retention period, a different access list, and
    frequently a different jurisdiction from the database it came from. Log the id and the outcome; the
    row is still available to whoever is allowed to read it.
15. **A collaborator with no state is not a service, and the analyser says so before you notice.** A class
    written the way point 1 asks but holding no fields — a parser, a formatter, a pure check — trips
    CA1822 on every method (*member does not access instance data and can be marked as static*), which is
    a build failure wherever the guardrail's zero-new-warning rule is enforced. The three ways out are not
    equivalent: injecting a logger it does not need so that it has a field, suppressing the rule, or
    making it static and taking it out of the container. Prefer the last and keep the seam at the boundary
    that does I/O, because the substitutability point 2 is protecting belongs to whatever talks to the
    outside, not to a pure function.
16. **Validating configuration at startup is opt-in twice, and one half alone is silent.** The
    validate-on-start call only forces the *registered* validations to run early; with no validator
    registered it runs nothing, and boot succeeds on an options object nobody checked. The
    data-annotations validator is the other half and ships in its own package that the hosting
    metapackage does not bring in — so the honest failure is a compile error and the quiet one is a chain
    that reads as validated. Register a validator **and** validate on start, then break a key on purpose
    once and watch boot fail, because that is the only thing that distinguishes the two.
17. **Two implementations of one interface are a keyed registration, not a factory of your own.** Where the
    container supports keys, registering each implementation under a name and asking for the one you want
    keeps the choice in the composition root, which is where §2.2 says it belongs. The alternatives are
    both worse in a specific way: a hand-written factory resolving from the provider is the service locator
    again, and injecting the whole collection of implementations to pick one by a property makes every
    implementation a dependency of the caller. Two remain out of scope for a key: a choice that depends on
    request data — that is a strategy the caller passes in — and a choice made once per environment, which
    is configuration deciding a single registration.
18. **The three ways to read options are three lifetimes, and mixing them is a captive dependency.** The
    plain form is a value read once for the process; the snapshot form is per-request and recomputed; the
    monitor form is a long-lived object that also reports changes. So a snapshot injected into a singleton
    is a request-scoped value pinned for the lifetime of the process — the same bug as §2.11, with none of
    the symptoms, because the value is merely stale rather than disposed. A singleton that has to see a
    changed configuration takes the monitor; anything else takes the plain form and stops there.
19. **A named or typed `HttpClient` is registered, never constructed with `new`.** The factory owns the
    handler pool behind the client it hands out, so §5.10's rule (take it from the factory, never dispose
    it) starts at registration: `AddHttpClient<TClient>()` gives the typed client its own configuration —
    base address, default headers, the resilience pipeline from §8 — declared once at the composition root
    instead of copied into every constructor that needs to talk to that dependency.
20. **Decorating a registered service is still composition-root work, not a wrapper the consuming class
    builds for itself.** Re-registering an interface with a class that takes the previously-registered
    implementation as a constructor dependency (a logging wrapper, a caching wrapper) keeps the decision
    of which behaviour gets added in the one place point 7 already puts every other registration — a class
    that instead `new`s up its own wrapper around an injected dependency has quietly reintroduced the
    service locator's problem: the real implementation is chosen inside the class instead of at the root.
21. **A logging scope carries a value across every log call inside it, without threading a parameter
    through each one.** `ILogger.BeginScope` attached once at the start of a unit of work — a correlation
    id, a tenant, a batch number — appears on every structured log entry written while the scope is active,
    including ones written by code several calls deeper that never received that value as an argument. It
    is the mechanism that makes point 13's structured fields queryable *across* a request rather than only
    within one log call, and it costs nothing where point 5's per-type category already exists.
22. **A `BackgroundService` whose `ExecuteAsync` throws takes the whole host down with it by default**, not
    just the one worker. An unhandled exception escaping the loop stops that hosted service and, unless the
    host is configured otherwise, triggers the entire application to shut down — which is rarely what was
    intended for a background job whose failure should be logged and retried, not treated as the process
    itself being unhealthy. The loop body needs its own try/catch around each unit of work, distinct from
    the swallowed-catch anti-pattern in §5.5 because here the goal is explicitly to keep the host alive
    across one iteration's failure, logged rather than silent.
23. **Cross-field validation that data annotations can't express is an `IValidateOptions<T>`, not a check
    bolted onto the constructor that consumes the options.** A rule spanning two properties — an end date
    after a start date, a maximum only meaningful relative to a minimum on the same object — belongs in a
    validator registered alongside the options binding from point 8, so it runs at the same startup
    validation point 16 already established, and fails boot with the same section-named error instead of
    surfacing as a runtime check the first time both fields happen to be read together.
24. **`PostConfigure` runs after every `Configure` call and after configuration binding, not in registration
    order among themselves.** A `PostConfigure` registered before the section is bound is not "early" in any
    sense that matters — the binder still overwrites whatever it set, because the actual sequence is every
    `Configure`/binding call first and every `PostConfigure` call last, regardless of the order the calls
    appear in the composition root. The only place a value set in `PostConfigure` survives is a field the
    binder does not touch, so use it for a derived or defaulted value computed from the bound section, never
    to override a key the section itself provides.
25. **`ServiceProviderOptions.ValidateOnBuild` is on by default only in Development, and a container that
    validates cleanly there can still fail the same way in Production the first time the untested path
    resolves.** The check that would have turned a missing or mis-scoped registration into a boot failure —
    the exact fix point 10 asks for — runs by default in the environment least likely to exercise every
    registration, and is silently off where a deploy actually matters unless the composition root sets it
    explicitly. Setting it to `true` unconditionally is what makes point 10's "boot failure instead of a
    500 three weeks later" true in every environment rather than only in the one nobody deploys.
26. **A dependency constructed with `ActivatorUtilities.CreateInstance` instead of resolved from the
    container is still constructor injection, and still bypasses the composition root.** It exists for the
    case where some constructor arguments are known only at the call site (a factory pattern with per-call
    data) and the rest should come from DI — but reaching for it to sidestep registering a type properly
    reintroduces point 7's scattered composition in a different shape: the object's dependency graph is now
    decided at every call site that constructs it, rather than once at the root, and a test substituting one
    of those dependencies has to reconstruct the same call instead of swapping a registration.
27. **A caught exception logged and then rethrown produces two records of the same failure**, one at the
    point it was caught and one wherever the rethrow is eventually caught again (or the unhandled-exception
    middleware logs it a second time). Point 5's rule against swallowing does not mean log-then-rethrow at
    every frame the exception passes through — log it once, at the boundary that actually decides what
    happens next (a controller filter, a background loop's own catch from point 22), and let every
    frame in between propagate it unlogged. Two log entries for one incident is not twice the information;
    it is one incident that looks like two on a dashboard counting errors.
28. **`IServiceProviderIsService` answers "is this type registered" without resolving it, which is the check
    a factory or a conditional registration needs instead of a `try`/`catch` around `GetService`.** Asking
    the provider itself whether a type is registered — rather than attempting the resolve and treating the
    failure as the answer — keeps the service-locator objection in point 2 from creeping back in through a
    "just checking" call: a resolve attempted only to see if it throws still resolves, still runs the
    constructor of whatever it finds, and still couples the caller to the container the same way a real
    resolution would.
29. **A structured log correlated to a distributed trace needs the trace's own identifiers on the log entry,
    not a second, independently generated correlation id.** Where the platform's tracing API is already in
    use for a request, its current activity carries a trace id and span id that a log entry can pick up
    automatically through the logging provider's own enrichment — inventing a separate GUID at the top of the
    request and threading it through `BeginScope` (point 21) duplicates what the trace already provides and
    guarantees the two systems disagree the first time only one of them is sampled.
30. **Two services registered under the same key are still last-registration-wins for that key**, the same
    rule point 12 states for an unkeyed registration. Keyed registration (point 17) chooses *which*
    interface implementation a given key resolves to; it does not exempt that key from the ordinary
    replace-on-reregister behaviour, so a module that registers a keyed service the composition root already
    registered under that key silently replaces the root's choice — the failure mode point 12 already
    describes, now one layer further from the registration a reader would think to check first.
31. **`AddHttpClient` and keyed registration compose (.NET 9+), and that changes what point 19's "never `new`
    it up" rule looks like for more than one configuration of the same client type.** `AddKeyedTransient` and
    `AddHttpClient` sharing a key let a typed or named client be requested with `[FromKeyedServices]` the same
    way point 17 resolves any other keyed interface, instead of a named client resolved by string through
    `IHttpClientFactory.CreateClient("name")` at every call site. The factory still owns the handler pool
    either way — the key changes how the caller asks for the client, not who owns its lifetime.
32. **A constructor parameter can request its own keyed dependency without the class ever touching
    `IServiceProvider`, and that is what keeps point 17's keyed registration from becoming point 2's service
    locator by another name.** `[FromKeyedServices("name")]` on a constructor parameter resolves that one
    argument from the keyed registration while the rest of the constructor still resolves normally — the
    class still declares every dependency in its constructor signature, still fails at composition time if
    the key is missing, and still substitutes cleanly in a test, which a hand-written resolve from inside the
    class body never could.
33. **The data-annotations validator (point 16) has more to enforce with the platform's own attributes than a
    hand-written `IValidateOptions<T>` used to need for the common cases.** `[AllowedValues]`, `[DeniedValues]`
    and `[Base64String]` cover a class of options-validation rule — this field is one of a fixed set, this
    string must decode — that previously meant a custom validator or point 23's `IValidateOptions<T>` for
    something no more complex than a whitelist; reaching for the built-in attribute first is what keeps a
    trivial rule from growing its own validator class only to enforce a check the framework already ships.
34. **`TimeProvider` is a service like any other in this section, and injecting it is what makes point 5's
    testability argument apply to time the same way it applies to a database or an HTTP call.** Code that
    reads `DateTime.UtcNow` or schedules through `Task.Delay` reaches a different, untestable dependency
    every time it runs; a `TimeProvider` taken through the constructor (point 1) is substituted with a fake
    clock in a test exactly the way a fake repository substitutes for a real one, and the ordinary DI
    container already registers `TimeProvider.System` as the default — nothing about wiring it up asks the
    class to know it's a special case.
35. **A `Meter`'s counters and histograms are a different signal from a log line on the same hot path, and
    reaching for point 9's declared log call where a metric was wanted answers a question nobody asked.** A
    per-request or per-item event that needs to be *counted or aggregated* — requests per second, latency
    percentiles — belongs on a `Counter<T>`/`Histogram<T>` registered once per category the same way point 5
    registers a logger per type, because a log aggregator answering "how many" by counting log lines is
    slower and costs more than a metric built to answer exactly that; the log line still exists for "what
    happened to this one," the metric for "how is the system doing across all of them."
36. **A logging level changed in configuration at runtime only reaches already-running code if something is
    actually listening for the change, and the plain `IConfiguration` binding in point 8 is not that
    listener.** The logging provider registered through the hosting metapackage subscribes to configuration
    reload tokens itself, so lowering a category from `Warning` to `Debug` in the backing configuration source
    and having it take effect without a restart works out of the box for logging specifically — it is not a
    general property of options bound through point 8, where point 18's monitor form is what a class has to
    ask for explicitly to see the same kind of change.
