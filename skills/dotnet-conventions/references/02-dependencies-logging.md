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
