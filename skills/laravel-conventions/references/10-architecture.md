# laravel-conventions §10 — Architecture

> Section 10 of `skills/laravel-conventions`. Read it when the change spans layers, or a new one is proposed. The other sections and the guardrails stay in `SKILL.md`.

1. Separate the **functional/business** layers from the **technical/shared** ones, with a predictable place
   per domain, and no technical layer importing a functional one.
2. A new dependency is a decision: check what the project already standardises on for the need (factories,
   policies, permissions, media, activity logging, translations, auth tokens, queues, multi-tenancy, static
   analysis) before adding a second library for something already solved.
3. **A version branch past its security-fix end of life is not a maintenance choice.** The framework's and
   the language's support windows are published and mechanical, so the question has a date for an answer,
   not an opinion: a new project starts on the newest stable major and the newest minor that major
   supports, and an existing one is planned off a branch before its security window closes, not after an
   advisory forces it. Staying behind compounds — each skipped major makes the next upgrade the one nobody
   has budget for.
4. Prefer the framework's own mechanism over a custom one; prefer configuration over a new abstraction. The
   framework already does most of the design-pattern work (`skills/design-patterns`).
5. **Where a layer-package convention (OSDD-style) is installed**, point 1's split is enforced structurally,
   not just by discipline: each functional (`users`, `billing`, ...) or technical domain is its **own
   self-contained Composer package** — `composer.json`, `src/`, its own `database/` (migrations, seeders),
   its own `tests/`, its own service provider — generated and scaffolded through the package's own commands
   rather than by hand. It is the house override for point 1: don't hand-roll a `functional/` folder
   convention that competes with it. [`xefi/laravel-osdd`, github.com/xefi/laravel-osdd, read 2026-08-10.]
6. **Where `laravel/boost` is present, install it with its agent skills (`--skills`), not the MCP server
   alone** — packages now ship their conventions as skills rather than as guidelines, so a guidelines-only
   install reaches nothing package-specific, including the concrete layout point 5 depends on. Run it
   interactively: a non-interactive first install silently drops every third-party skill while still
   reporting success. [`laravel/boost`, github.com/laravel/boost, read 2026-08-11.]
7. **The dependency direction *is* the architecture, so a tool enforces it, not a paragraph.** Point 1's
   split holds for as long as everyone remembers it; expressed as a static-analysis rule or a package
   boundary, a wrong-direction import fails a build instead of waiting for a reviewer who happens to know.
   Same argument as `skills/code-baseline` §8 on guarantees: prefer the mechanism the toolchain checks over
   the sentence someone has to recall under deadline.
8. **Say which kind of boundary you actually have.** A folder convention is a convention — nothing stops an
   import across it. A Composer package boundary is enforced by the autoloader and by the package's own
   `composer.json`. Both are legitimate; trouble comes from treating the first as the second, then being
   surprised that two domains grew a direct dependency nobody approved.
9. **A domain is entered through a stated surface, not by reaching into its internals.** When another
   domain calls an action, a service or a documented facade, that surface can change deliberately; when it
   news up an internal class or queries another domain's model directly, every module depends on every
   other module's private structure and the split has become decorative.
10. **The database is a boundary too.** Two domains writing the same table are one domain with two names,
    whatever the folder layout says — and the failure arrives as two pieces of code with different ideas
    about what a column means. Give the table one owner, and let the other side go through it.
11. **Events decouple, and they cost traceability.** A cross-domain flow assembled from events does not
    appear in a stack trace, so "what happens when an invoice is paid" stops being answerable by reading
    one file. Use them where the producer genuinely must not know its consumers; call the action directly
    where it must.
12. **A new layer or abstraction is earned by the second real case.** Building the extension point first
    means designing against an imagined second caller, and the real one wants something else — so the
    abstraction is rebuilt anyway, this time with a consumer attached.
13. **Don't add infrastructure the database still handles.** A queue, a cache layer or a search engine each
    bring an operational surface — a failure mode, a deployment step, a staleness question. Reach for one
    when a measurement says the database cannot do it, not because the problem resembles a tutorial.
14. **Keep the dependency set current continuously, or point 3 becomes impossible.** A framework major is
    only reachable when the packages around it are already close to their own latest; a set left to drift
    for a year turns a routine upgrade into a project, which is how a branch ends up past its security
    window.
15. **An architecture decision that is not written down gets re-litigated.** Record it near the code, in a
    few lines: what was decided, what it rules out, and what would reopen it. The next person arguing the
    other side deserves to know the argument has already happened, and on what grounds
    (`skills/documentation-adr`, which also says when *not* to commit a file for it).
16. **Contextual binding is point 4's "prefer the framework's own mechanism" applied to the container**: when
    two classes need a different implementation of the same interface — a different disk, a different
    driver, a config value — `$this->app->when(A::class)->needs(Interface::class)->give(...)` resolves the
    branch once, in the provider, instead of an `if` inside every constructor asking "who is calling me".
    `giveConfig()` and `giveTagged()` cover the two common shapes (an injected config value, an injected
    set of same-tagged bindings) without a hand-written closure. [Laravel container docs,
    laravel.com/docs/12.x/container, read 2026-09-10.]
17. **A binding that is never resolved should never be booted.** A service provider deferred via `$defer =
    true` (or, on newer providers, declared through `provides()`) is only instantiated the first time one of
    its bindings is requested — a provider wiring a rarely-used integration stops costing a boot-time class
    load and container lookup on every request that never touches it. The trade only pays off for a provider
    with no side effect outside its own `register()`; one that also listens for events or registers routes in
    `boot()` cannot be deferred without silently losing that wiring on requests where nothing triggered the
    resolution.
18. **A middleware group is a named ordering, and the order is the part that breaks silently.** Registering
    `auth` after a rate-limiter that keys its bucket on the authenticated user throttles every guest request
    under one shared bucket, because the middleware that would identify the user has not run yet. The fix is
    not a smarter limiter: read the group's declared order in `bootstrap/app.php` before adding to it —
    inserting an entry without checking what runs before and after is how this regresses on an unrelated
    change.
19. **A feature toggle is a config value with an environment default, not a hard-coded conditional shipped
    then reverted.** Point 13's "don't add infrastructure the database still handles" cuts the other way
    here too: a boolean in `config/features.php`, read through the config layer per point 1 of
    `skills/laravel-conventions` §7, lets the same deploy run dark in staging and live in production without
    a second branch — reverting a toggle is changing one value, reverting a conditional is a second pull
    request.
20. **Package auto-discovery is a convenience, not a boundary.** Composer wires a package's service provider
    and facades automatically from its `extra.laravel` block, so point 2's "check what's already
    standardised on" has to include packages that never appear in a manually maintained providers array —
    they are active anyway. A package that must not run in a given environment (a debug bar, a seeder
    package) is excluded in `composer.json`'s `dont-discover`, not by hoping nothing calls it.
21. **A facade and its underlying binding are two separate things to keep in sync.** A facade is a static
    proxy resolved from the container at call time, so swapping the bound implementation in a provider
    changes what every facade call does without touching a call site — which is why a test that swaps the
    binding (`$this->app->bind(...)`, a fake) must do so before the facade is first resolved in that
    request; resolving it once caches the instance and a later rebind is silently ignored for the rest of
    that request/test.
22. **`register()` binds, `boot()` uses other bindings — and mixing the two breaks on load order, not on
    logic.** Resolving a second provider's service from inside `register()` assumes that provider has
    already registered, which Laravel does not guarantee: providers register in listed order, then every
    provider's `boot()` runs only after every `register()` has. Reaching across providers belongs in
    `boot()`, the one place the whole container is known to be wired.
23. **A published config file is a fork, not a copy the package keeps updating for you.** `vendor:publish`
    writes the package's config into the app's own `config/`, and a new option the package ships later
    never appears there on its own — the app's copy falls behind until someone diffs the two by hand.
    Publish the file only once a value in it needs overriding, and note the fork where point 15's
    architecture record would look for it.
24. **A test that swaps a container binding has to unbind it, or the next test inherits today's fake.** The
    container is a singleton across a test run unless the framework's own test traits reset it between
    cases; a `$this->app->bind(...)` left in place is silent for every later test that happens not to check
    the thing that changed, and the eventual failure points at the wrong test. `swap()` and the framework's
    container-reset traits exist so a rebind is scoped to the test that made it.
25. **A closure passed to `$this->app->singleton()` runs once, and a value captured in it stays captured for
    the life of the container.** Binding a request-scoped value — the current tenant, the caller's locale —
    as a singleton at boot freezes whatever it was at first resolution, then serves it to every later
    request in the same worker; resolve it fresh per request (a plain `bind`) or read it from something
    itself request-scoped, never baking a per-request fact into a process-lifetime singleton.
26. **A queued job serialises the model, not the query that produced it — and a job dispatched from a
    request that hasn't committed yet races its own data.** `SerializesModels` stores an id and re-fetches
    the model when the job runs, which is why §8 point 4's "dispatch after commit" matters doubly for a job:
    dispatched before commit, the worker can re-fetch before the transaction lands, finding a stale row or
    none — a race that reads as intermittent because it depends on worker speed, not on the code.
27. **A config value read through `env()` outside `config/*.php` is invisible to `config:cache`.** Caching
    compiles every `config/*.php` file into one file and stops reading `.env` on every request — a direct
    `env()` call anywhere else (a controller, a service, a provider's `boot()`) freezes at whatever it read
    when the cache was built, so a value changed in `.env` after deploy looks ignored until someone
    remembers `config:clear`. `env()` belongs in `config/*.php` only; the rest of the app reads `config()`.
28. **A trait shared across models to add a behaviour is not the same decision as an interface those models
    implement, and conflating them hides which one a caller can rely on.** A trait supplies an
    implementation (real code, silently overridable by whichever class declares it last if two traits
    collide); an interface supplies a contract a caller can type-hint against without knowing which trait,
    if any, backs it. Reaching for a trait because "several models need this" without asking whether
    callers need to depend on the *capability* rather than the *models* is how a `HasSlug`-style trait ends
    up duck-typed everywhere instead of declared once as `Sluggable` and checked with `instanceof`.
29. **Laravel 12's default skeleton centralises what used to be spread across several kernel classes into
    `bootstrap/app.php`.** There is no `app/Console/Kernel.php` and no `app/Http/Middleware/*` array to
    maintain by default; middleware groups (point 18), exception handling (`skills/laravel-conventions` §11
    point 15) and console scheduling are all configured through the same file's fluent builder. A project
    upgraded from an older skeleton keeps its kernel classes working, but a new one reads its cross-cutting
    wiring in one place instead of three — point 15's "write the decision down near the code" with the
    framework itself choosing where "near" is.
30. **Multiple database connections declared in `config/database.php` are a routing decision that belongs on
    the model, not on the call site.** A model's `protected $connection = 'reporting';` states once which
    store owns it, as point 10 asks a table to have one owner; `DB::connection('reporting')` scattered
    through query classes makes the same fact undiscoverable from the model, and a later move to another
    connection means finding every call site instead of editing one property.
31. **The `/up` health-check route, configured via `->withRouting(health: '/up')`, is infrastructure for the
    load balancer, not an endpoint to protect with the application's own auth middleware.** Requiring a
    session or a token on it defeats the load balancer's ability to probe it, the one caller it exists for;
    where it must not be publicly reachable, restrict it at the network layer (an internal-only route, a
    firewall rule) rather than folding it into the app's authorisation model alongside real endpoints.
32. **Enabling `sticky` on a read-replica connection trades replica lag for read-your-own-write correctness,
    and turning it on globally applies that trade to every request, not only the one that just wrote.** With
    `sticky` on, a request that has performed a write reads from the primary for the rest of that request,
    avoiding the classic "save then reload and the change isn't there yet" replica-lag bug; the cost is that
    every other read in that request also skips the replica — a deliberate exception, not a free correctness
    upgrade to leave on everywhere without measuring the load it shifts back to the primary.
33. **Anything cached in-process — a static property, an array, an OPcache-backed APCu entry — is invisible
    to every other worker or container the load balancer sends the next request to.** A horizontally scaled
    app has no single process to hold that state, so a design that "works" against one `php artisan serve`
    process or one local container verifies a topology production does not have; state that must be seen by
    every worker belongs in the cache store or the database, the boundary point 13 draws between what the
    database still handles and what needs real infrastructure.
34. **A read model built by joining across two domains' tables in raw SQL is a dependency the folder
    structure doesn't show.** Point 9's "entered through a stated surface" still applies to a reporting
    query that flattens `orders` and `subscriptions` into one `SELECT` for a dashboard — it now silently
    depends on both domains' schemas, and a migration changing either table breaks a report nobody thought
    to check because it lives outside both domains' directories.
35. **A module's own routing is registered from that module's own `RouteServiceProvider`, booted from the
    module's main provider, rather than the app's `bootstrap/app.php` collecting every module's routes by
    hand.** This is point 5's structural enforcement applied to routing: `bootstrap/providers.php` lists one
    provider per module, and that provider owns how its routes are wired (prefix, middleware group, route
    file) — an app-wide routing file listing every module's routes side by side is the "folder convention
    instead of an enforced boundary" gap of point 8, for the entry point every request goes through first.
36. **A cross-module dependency is bound to an interface, not to the other module's concrete class, and the
    binding lives in a service provider — never a `new OtherModule\SomeAction()` inside this module's code.**
    Point 9 says a domain is entered through a stated surface; the container makes that surface swappable
    rather than aspirational — a consuming module type-hints `BillingLookup`, the providing module's
    service provider binds the concrete implementation, and a later refactor of the providing side changes
    one binding instead of every import across every module that reached for the concrete class.
37. **A local module package is installed through a Composer path repository, not copied into `vendor/` by
    hand or published to a registry before it is ready.** `{"type": "path", "url": "packages/billing"}` in
    the root `composer.json` lets each OSDD package (point 5) be developed and required like a real
    dependency — versioned, autoloaded, with its own `composer.json` — while living in the same repository
    checkout; requiring it from a registry too early adds a publish-and-tag step to every local change, and
    hand-editing `vendor/` silently loses the change on the next `composer install`.
38. **A shared kernel package — the one technical layer every functional module is allowed to depend on — is
    still a dependency direction to declare, not an exemption from point 1's rule.** A `shared`/`core`
    package holding cross-cutting concerns (a base model trait, a common value object) is legitimate
    because every functional module may depend on it and it depends on none of them back; the failure mode
    is a "shared" package that quietly grows a dependency on one functional module's class, so every other
    module importing "shared" transitively imports that module too, and nobody chose that.
39. **Horizon's queue configuration groups workers by connection and queue name, and a module's job classes
    are only isolated from another module's if their queue names actually differ.** Two OSDD packages
    (point 5) both dispatching to the implicit `default` queue share one worker pool and one set of Horizon
    metrics — a slow or failing job in one then starves or masks failures in the other, which reads as "the
    queue is slow" rather than "one module's jobs are colliding with another's", because nothing about the
    job classes shows they share a lane. [Laravel Horizon documentation, laravel.com/docs/12.x/horizon,
    read 2026-09-10.]
40. **A closure bound with `App::bind()` inside one module's service provider can still resolve a class from
    another module if the container is asked to — the container itself enforces no module boundary at all.**
    Point 36's interface binding is a discipline the codebase's conventions choose to keep, not something
    Laravel's container refuses on its behalf; the boundary is only as real as the static-analysis rule
    point 7 asks for, because nothing at runtime stops a provider from binding a concrete class straight out
    of another module's namespace and every caller resolving it none the wiser.
41. **A functional or technical layer is named for what it owns, never for its position** (`core`,
    `common`, `shared`, `socle`, `transverse`, `utils`). A positional name refuses no file, so every
    unplaced piece of code lands there until the layer is the application and every other layer depends
    on it — see `skills/no-catch-all-layer` for the naming rule, the placement question, and how an
    existing catch-all is dissolved rather than added to.
42. **In a database-per-tenant project, tenancy is one named technical layer** (point 1's split
    applies to it exactly like any other infrastructure concern), and each functional/technical layer
    keeps its own tenant schema under its `database/migrations/tenant/`, declared from the same layer
    buckets point 5's scaffolding already tracks. See `skills/laravel-tenant-context-by-default` for
    what belongs centrally versus per tenant, and `skills/laravel-tenant-replica` for the one shape of
    record that legitimately exists on both sides.
43. **Post-response work that needs no retry and no durability can use the framework's deferred-function helper
    instead of a job; anything that must survive a crash or be retried is still a job.** A deferred function
    normally runs after the response, in the same PHP process, so a fatal error or a restart loses it. Page-view
    logging qualifies; sending an invoice does not.
44. **Request-scoped context is for data that must follow a request through logs and into the jobs it queues.**
    The framework's context facade adds visible values (they appear in log context) and hidden ones (they
    propagate to queued jobs without appearing in logs). A secret placed in it travels to every queued job, so
    put nothing there that should not propagate. Reaching for it to avoid passing a plain argument one layer
    down is the wrong use.
45. **Independent work can run through the concurrency facade, with a cost.** With a process-based driver each
    closure runs in its own PHP process that boots the application, so it pays only for independent queries,
    outbound calls or computations that are individually slow; the synchronous driver runs them one after
    another and is what tests use.
46. **Depend on a contract at a boundary only when testability or interchangeable implementations justify
    it.** A payment gateway, a notification channel and an external service are the usual places; an interface
    in front of a class with one implementation and no test seam is over-abstraction
    (`skills/over-engineering-review`).
