# § 2 — Dependencies and logging

> Section 2 of `skills/dotnet-conventions`. Read it when a dependency is injected or registered, a service
> lifetime is chosen, configuration is read, or something is logged.

1. Dependencies injected **through the constructor**, as `private readonly` interface fields, written as an
   **explicit constructor** — not a primary constructor on the class header. A primary-constructor parameter
   carries no `readonly` modifier and stays assignable from any member, and there's no constructor body for a
   multi-statement guard or a computed field. (Opposite of PHP's constructor property promotion, which *is*
   mandatory there: a promoted PHP parameter carries `private readonly` in the signature; a C# header
   parameter carries neither.)
   **Where primary constructors stay**: `record`/`record struct` (parameters become public init-only
   properties, not a hidden mutable capture field), a plain `struct`, test fixtures, and
   generated/scaffolded code. Existing primary constructors in older files stay; a new class follows this
   rule regardless of its neighbours.
2. **Never the Service Locator** (`IServiceProvider.GetService`/`GetRequiredService`) inside a class doing
   work: it hides the dependency from the constructor, so nothing fails at composition time and everything
   fails at runtime, and the class is untestable without a container.
3. A service depends only on a service whose lifetime is **equal to or longer than its own**. A `Scoped`
   service injected into a `Singleton` (captive dependency) freezes for the app's lifetime — a `DbContext`
   shared between concurrent requests is the canonical disaster. In production it is no clean failure but
   tracked entities from one user's request appearing in another's, and change tracking that saves the wrong
   row.
4. A `Singleton` or background worker that needs a scoped service creates a scope explicitly
   (`IServiceScopeFactory`), never injects the scoped service directly. The scope is per unit of work — one
   per message, per tick, per batch — and disposed when that unit ends, which also returns the connection to
   the pool.
5. Every working class injects a generic logger parameterised by itself (`ILogger<TSelf>`): the type
   parameter sets the log category, which lets ops filter and route logs. A logger parameterised by a base
   class or shared type collapses several components into one category, and a filter meant to quiet one
   silences all.
6. Too many constructor parameters is a design signal: the class is doing several jobs. The number is not
   the rule — the question is whether any single method uses most of them. When each method uses three of
   nine, there are three classes here.
7. Composition happens at the application root, in one place, not scattered across the modules being
   composed. A module that registers its own dependencies at import time makes the dependency graph
   unreadable and stops a test from substituting anything without loading the module.
8. **Configuration reaches code as a typed object.** Each section is bound and validated **once** at the
   composition root, and the typed accessor is what gets injected — business code never takes the raw
   configuration abstraction nor reads a key by string. A misspelled or missing key becomes a boot error
   naming the section, instead of a null two hours into the first request that needed it.
9. **A log call on a per-item, per-request or per-tick path is declared, not interpolated.** Where the
   platform ships a source generator for log methods, the hot path calls a generated method and pays no
   boxing or string work when the level is disabled; the ordinary logger call stays right for a cold path.
   Everything else about logging — the injected category, the level choice, no interpolation into the
   template — is point 5 and unchanged.
10. **The container verifies a registration when something resolves it, not when it is built.** A missing or
    mis-scoped registration is a 500 on the first request that needs that type — possibly weeks after the
    deploy, on the one endpoint nobody smoke-tested. Turn it into a boot failure: the host can validate the
    graph and the scopes at startup, a switch worth more than any test here.
11. **A disposable resolved from the root provider is held until the process ends.** The container disposes
    what it created when the owning scope is disposed, and the root scope is never disposed while the app
    runs, so a transient disposable resolved outside a request scope accumulates — a slow leak, the hardest
    kind to attribute.
12. **Registration order matters, and the two ways to register mean different things.** For a single
    resolve the last registration wins, so a re-registration silently replaces an earlier one; the try-add
    form registers only if nothing has, which is how a library provides a default without stomping the
    application's choice. The wrong one is how a test's fake ends up unused.
13. **A log template's placeholders are structured fields; interpolating the values destroys them.** The
    message reads the same to a human and stops being queryable — no filtering by order id, no grouping by
    tenant, no alert on a field. The interpolated call costs money without buying what an aggregator is for.
14. **Never log a secret, a token or personal data — log the identifier instead.** A logged request body or
    entity travels to a system with a different retention period, access list, and often jurisdiction from
    its database. Log the id and the outcome; the row stays available to whoever may read it.
15. **A collaborator with no state is not a service, and the analyser says so first.** A class written as
    point 1 asks but holding no fields — a parser, a formatter, a pure check — trips CA1822 on every method
    (*member does not access instance data and can be marked as static*; on by default in .NET 10 only at
    suggestion level), a build failure wherever the zero-new-warning rule is enforced at a higher severity. The three ways out are not equivalent: injecting a logger it doesn't
    need so it has a field, suppressing the rule, or making it static and taking it out of the container.
    Prefer the last and keep the seam at the boundary that does I/O, because the substitutability point 2
    protects belongs to whatever talks to the outside, not to a pure function.
16. **Validating configuration at startup is opt-in twice, and one half alone is silent.** The
    validate-on-start call only forces the *registered* validations to run early; with no validator
    registered it runs nothing, and boot succeeds on an unchecked options object. The data-annotations
    validator is the other half and ships in its own package that the hosting metapackage does not bring in
    — the honest failure is a compile error, the quiet one a chain that reads as validated. Register a
    validator **and** validate on start, then break a key on purpose once and watch boot fail: the only way
    to tell the two apart.
17. **Two implementations of one interface are a keyed registration, not a factory of your own.** Where the
    container supports keys, register each implementation under a name and ask for the one you want, which
    keeps the choice in the composition root where §2.2 says it belongs. Both alternatives are worse: a
    hand-written factory resolving from the provider is the service locator again, and injecting the whole
    collection to pick one by a property makes every implementation a dependency of the caller. Out of scope
    for a key: a choice depending on request data (a strategy the caller passes in) and a choice made once
    per environment (configuration deciding a single registration).
18. **The three ways to read options are three lifetimes, and mixing them is a captive dependency.** The
    plain form is a value read once for the process; the snapshot form is per-request and recomputed; the
    monitor form is a long-lived object that also reports changes. A snapshot injected into a singleton is a
    request-scoped value pinned for the process lifetime — §2.11's bug without its symptoms, since the value
    is merely stale rather than disposed. A singleton that must see changed configuration takes the monitor;
    anything else takes the plain form.
19. **A named or typed `HttpClient` is registered, never constructed with `new`.** The factory owns the
    handler pool behind the client it hands out, so §5.10's rule (take it from the factory, never dispose
    it) starts at registration: `AddHttpClient<TClient>()` gives the typed client its configuration — base
    address, default headers, the resilience pipeline from §8 — declared once at the composition root
    instead of copied into every constructor.
20. **Decorating a registered service is composition-root work, not a wrapper the consuming class builds.**
    Re-register an interface with a class that takes the previous implementation as a constructor
    dependency (a logging or caching wrapper): which behaviour gets added is decided in the one place point
    7 puts every registration. A class that `new`s its own wrapper around an injected dependency has
    reintroduced the service locator's problem — the real implementation is chosen inside the class.
21. **A logging scope carries a value across every log call inside it, without threading a parameter.**
    `ILogger.BeginScope` attached once at the start of a unit of work — a correlation id, a tenant, a batch
    number — appears on every structured entry written while it is active, including code several calls
    deeper that never received the value. It makes point 13's structured fields queryable *across* a
    request rather than within one call, and costs nothing where point 5's per-type category exists.
22. **A `BackgroundService` whose `ExecuteAsync` throws takes the whole host down by default**, not just
    that worker: an unhandled exception escaping the loop stops that service and, unless the host is
    configured otherwise, shuts the application down — rarely intended for a job whose failure should be
    logged and retried. The loop body needs its own try/catch around each unit of work. This differs from
    §5.5's swallowed catch: the goal is to keep the host alive across one iteration's failure, logged rather
    than silent.
23. **Cross-field validation that data annotations can't express is an `IValidateOptions<T>`, not a check
    in the constructor consuming the options.** A rule spanning two properties (an end date after a start
    date, a maximum meaningful only relative to a minimum) belongs in a validator registered alongside
    point 8's binding, so it runs at point 16's startup validation and fails boot with the same
    section-named error instead of surfacing at runtime when both fields are first read together.
24. **`PostConfigure` runs after every `Configure` call and after configuration binding, not in
    registration order among them.** A `PostConfigure` registered before the section is bound is not
    "early": the binder still overwrites what it set, because every `Configure`/binding call runs first and
    every `PostConfigure` last, whatever the order in the composition root. A value set there survives only
    in a field the binder doesn't touch, so use it for a derived or defaulted value computed from the bound
    section, never to override a key the section provides.
25. **`ServiceProviderOptions.ValidateOnBuild` is on by default only in Development, so a container that
    validates cleanly there can still fail in Production the first time the untested path resolves.** The
    check that turns a missing or mis-scoped registration into a boot failure (point 10's fix) runs by
    default in the environment least likely to exercise every registration, and is silently off where a
    deploy matters unless the composition root sets it. Setting it to `true` unconditionally makes point
    10's "boot failure instead of a 500 three weeks later" true in every environment.
26. **A dependency built with `ActivatorUtilities.CreateInstance` instead of resolved from the container is
    still constructor injection, and still bypasses the composition root.** It exists for when some
    constructor arguments are known only at the call site (a factory with per-call data) and the rest come
    from DI; using it to sidestep registering a type reintroduces point 7's scattered composition: the
    dependency graph is decided at every call site rather than once at the root, and a test substituting a
    dependency must reconstruct the same call instead of swapping a registration.
27. **A caught exception logged and then rethrown produces two records of one failure**, one where caught
    and one where the rethrow is eventually caught (or the unhandled-exception middleware logs it again).
    Point 5's rule against swallowing does not mean log-then-rethrow at every frame: log once, at the
    boundary that decides what happens next (a controller filter, a background loop's own catch from point
    22), and let frames in between propagate it unlogged. Two entries for one incident look like two
    incidents on a dashboard counting errors.
28. **`IServiceProviderIsService` answers "is this type registered" without resolving it, the check a
    factory or conditional registration needs instead of a `try`/`catch` around `GetService`.** A resolve
    attempted only to see if it throws still resolves, still runs the found constructor, and couples the
    caller to the container like a real resolution — point 2's service-locator objection by the back door.
29. **A structured log correlated to a distributed trace needs the trace's own identifiers on the entry, not
    a second, independently generated correlation id.** Where the platform's tracing API is in use for a
    request, its current activity carries a trace id and span id that a log entry picks up through the
    logging provider's enrichment. A separate GUID threaded through `BeginScope` (point 21) duplicates the
    trace and guarantees the two systems disagree the first time only one is sampled.
30. **Two services registered under the same key are still last-registration-wins for that key**, as point
    12 states for an unkeyed registration. Keyed registration (point 17) chooses *which* implementation a
    key resolves to; it does not exempt the key from replace-on-reregister, so a module registering a keyed
    service the root already registered under that key silently replaces the root's choice — point 12's
    failure, one layer further from where a reader would look.
31. **`AddHttpClient` and keyed registration compose (.NET 9+), which changes point 19's "never `new` it up"
    for more than one configuration of the same client type.** `AddKeyedTransient` and `AddHttpClient`
    sharing a key let a typed or named client be requested with `[FromKeyedServices]` as point 17 resolves
    any keyed interface, instead of resolving by string through `IHttpClientFactory.CreateClient("name")` at
    every call site. The factory still owns the handler pool either way — the key changes how the caller
    asks, not who owns the lifetime.
32. **A constructor parameter can request its own keyed dependency without the class touching
    `IServiceProvider`, which keeps point 17's keyed registration from becoming point 2's service locator.**
    `[FromKeyedServices("name")]` on a constructor parameter resolves that argument from the keyed
    registration while the rest resolves normally — the class still declares every dependency in its
    signature, still fails at composition time if the key is missing, and still substitutes in a test,
    which a resolve from inside the class body never could.
33. **The data-annotations validator (point 16) covers common cases with the platform's own attributes
    that once needed a hand-written `IValidateOptions<T>`.** `[AllowedValues]`, `[DeniedValues]` and
    `[Base64String]` cover rules like "one of a fixed set" and "must decode" that previously meant a custom
    validator or point 23's `IValidateOptions<T>` for a mere whitelist; use the built-in attribute first so
    a trivial rule doesn't grow its own validator class.
34. **`TimeProvider` is a service like any other here, and injecting it extends the testability
    argument to time.** Code reading `DateTime.UtcNow` or scheduling through `Task.Delay` reaches an
    untestable dependency every time; a `TimeProvider` taken through the constructor (point 1) is
    substituted with a fake clock as a fake repository substitutes for a real one, and the ordinary DI
    container already registers `TimeProvider.System` as the default.
35. **A `Meter`'s counters and histograms are a different signal from a log line on the same hot path; a
    point-9 declared log call where a metric was wanted answers a question nobody asked.** A per-request or
    per-item event that must be *counted or aggregated* (requests per second, latency percentiles) belongs
    on a `Counter<T>`/`Histogram<T>` registered once per category as point 5 registers a logger per type,
    because counting log lines is slower and costlier than a metric built for it. The log line answers "what
    happened to this one", the metric "how is the system doing across all of them".
36. **A logging level changed in configuration at runtime reaches running code only if something listens,
    and point 8's plain `IConfiguration` binding is not that listener.** The logging provider registered
    through the hosting metapackage subscribes to configuration reload tokens itself, so lowering a category
    from `Warning` to `Debug` takes effect without a restart for logging specifically. It is not a property
    of options bound through point 8, where point 18's monitor form is what a class must ask for to see such
    a change.
37. **`IHostedLifecycleService` splits `IHostedService`'s two methods into eight, and ordering across several
    hosted services is the reason to use it instead of cramming everything into `StartAsync`.**
    `StartingAsync` runs for every registered hosted service before any `StartAsync`, then every
    `StartAsync`, then every `StartedAsync`, with the reverse fan-out on shutdown, so one hosted service can
    depend on another having finished a phase without merging them into one class; point 22's "unhandled
    exception takes the host down" applies to every one of these hooks, not only `ExecuteAsync`.
38. **`TryAddEnumerable` registers into the collection an `IEnumerable<TInterface>` resolves, without the
    last-registration-wins replacement point 12 describes for a single-instance registration.** A library
    and the application can both add their own `IValidateOptions<T>` or health check without displacing
    each other — the multi-implementation case point 17's keyed registration deliberately doesn't cover,
    since here every registered instance runs rather than exactly one being chosen.
39. **A health check that captures a scoped dependency (a `DbContext`, a repository) in its constructor is
    registered as a singleton by the health-check framework by default, reproducing point 3's captive
    dependency one layer from where it's usually sought.** The check is long-lived so the periodic probe
    pays no fresh construction cost, but a scoped collaborator resolved once at construction is pinned for
    the app's lifetime; a health check needing a scoped service creates its own scope per check (point 4)
    rather than taking one through the constructor.
40. **`GetRequiredKeyedService<T>` inside a factory that is itself composed at the root is not the service
    locator point 2 forbids: the factory's graph, including the provider it holds, was assembled once at the
    root and is itself injected where needed.** The distinction is where the call lives: a working class
    reaching into `IServiceProvider` to pick a keyed implementation by a value it computes is point 2's
    anti-pattern; a small, purpose-built factory whose only job is that one keyed resolution, registered and
    injected like anything else, keeps the choice visible at the boundary instead of buried in business
    logic.
41. **A `[LoggerMessage]`-generated method's parameter names become the structured field names on every
    entry, so renaming a parameter is a logging-schema change, not a cosmetic edit.** Point 9 covers the
    generator's performance case; the naming half is easy to miss in review — renaming `orderId` to `id`
    silently renames the field a saved query or alert filtered on, where the interpolated form point 13
    warns about would at least keep the words in the message text.
42. **Configuration validated through `ValidateOnStart` runs its registered validators in registration
    order, and the first to throw stops the rest.** Where point 16 asks for a validator beside the binding,
    several options types validated at startup fail one at a time rather than all at once — the second
    misconfigured section's error never appears in that boot's logs, so each fix-and-redeploy surfaces the
    next, an avoidable round trip unless every validator is checked by hand before the first fix ships.
43. **`ValidateOnStart` fires when the host starts, not when it is built.** Point 16's validations run
    from a hosted service during `StartAsync`; a program that calls `Build()` and resolves a service
    without starting the host (a hand-written console entry point, a test fixture over the root provider)
    boots on unchecked options and fails at the first resolve of the options object instead, with a
    stack that points at a constructor rather than at the configuration. Start the host in any path that
    is meant to prove the configuration. Point 16's "own package" half also depends on the SDK: a project
    on the web SDK gets the data-annotations validator from the shared framework and needs no package.
