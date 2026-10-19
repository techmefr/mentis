# laravel-conventions §1 — Where behaviour lives

> Section 1 of `skills/laravel-conventions`. Read it when a model, a controller, a listener or a service is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Keep models thin.** A model holds `$fillable`, `$casts`, relationships, trivial computed accessors
   over its own attributes, and lifecycle traits — with the scopes and the per-concept accessors grouped
   into the concern traits of point 4 rather than accumulating in the class body. Business logic,
   orchestration and anything reaching another aggregate go in an **action or query class** — never a
   generic `*Service`/`*Repository`
   (`code-baseline`'s no-bag-name rule, §2 below). One class, one verb-plus-noun mission
   (`RegisterUser`, `GetActiveSessionsForUser`), never a `UserManager`/`UserService` that accumulates
   unrelated methods. A generic service is a fat model one layer up.
   1. **An action has one public method, and it returns a value.** Its collaborators arrive through
      constructor promotion, its inputs are typed parameters rather than the request, and its result is
      domain data — never a response, never a redirect. An action that returns an HTTP response cannot be
      called from a command, a job or a test without a fake request, which is how the same rule ends up
      duplicated in the console.
   2. **Separate the read from the write.** A query class answers a question and touches nothing; an action
      changes state. Merging them gives a method whose name cannot be honest (`getOrCreateAndNotify`), and
      the caller can no longer tell whether calling it twice is safe.
   3. **A controller validates, delegates, responds.** Business branching in a controller is logic
      the console command will need next month, where it cannot reach it.
2. **Events + listeners, never model observers**, for reacting to lifecycle changes. An observer is invisible
   at the call site: something saves a row and unrelated code runs, with no trace in the flow being read.
   Listeners are registered explicitly. This includes the model's own `boot()`: a static `boot()` override
   that registers lifecycle closures (`static::creating(...)`) is the same hidden effect — the fix is the
   same listener registered in the `EventServiceProvider`, not a closure moved into the model.
3. Reusable cross-cutting model behaviour (historisation, auditing, snapshotting) goes in a trait the model
   **opts into**, shaped like the framework's own (`SoftDeletes`): the model declares what it tracks. A base
   class inherited by everything makes the behaviour mandatory and untestable in isolation.
4. **A concern trait owns its concept end to end** — its relationship, casts, scopes, accessors and
   predicates live in the same file, the way the framework's soft-delete trait owns its column, its
   global scope and its restore method. Named after the concept (`Publishable`, `HasOwner`), never after the
   filtering (`FiltersByOwner`). The model body shrinks to a declaration of what the model *is* — fillable list, casts, opted-in
   trait names — and a scope stops sitting hundreds of lines from the relationship it queries. A scope defined inline on the model is
   the default this displaces, not a violation to hunt down in existing code (`code-baseline` §0).
5. **Recognise the two shapes that are a pattern, not a field.** A status/state column whose values move
   through named transitions, with a guard or a side effect on the move, is a **state machine** — read
   `skills/design-patterns` §4 and `skills/domain-modeling` before writing the first transition method. An
   ordered sequence of steps over one payload, growing a step per requirement (validate, dedupe, enrich,
   notify), is a **pipeline** — same reference. Neither arrives in pattern vocabulary but as "add a publish
   button", "the status should go back to draft", "it should also send a notification".
6. **Do not factor out what protects nothing.** A helper wrapping one framework call, a class extracted
   because two lines looked alike, an interface with one implementation "for later" — each adds a hop and
   removes the reader's ability to see what happens. The test is whether the extraction holds an invariant
   somebody could otherwise break: a rule about how a thing must be built, a boundary a caller must not
   cross. Shared shape is not an invariant; two call sites that look alike today are the usual
   reason a helper grows a boolean parameter that switches its behaviour.
7. **Do not build the extension point before the second real case.** A strategy, a registry, an event with
   one listener, a config key with one value — each is a guess about a variation that has not arrived, and
   costs the same whether the guess was right or wrong. `skills/design-patterns` holds the threshold; the
   pressure specific to this framework is that a package's own extension hook makes it feel free, and it
   still has to be read by whoever comes next.
8. **An accessor is a projection of the row, not a query.** The moment it loads a relation, counts
   something, or reaches configuration, it becomes an N+1 wearing the clothes of a field (§4 point 1), and
   nothing at the call site says so. Anything needing another table is a method with a verb in its name, or
   belongs in a query class.
9. **No markup in PHP.** A service, action, accessor, controller or job never builds HTML — no tags, no inline
   styles, no concatenated `<span>`. Markup belongs in the view layer; a backend class returns data.
10. **The application owns its domain.** When integrating an external system (payment provider, CRM, ERP), the
   app remains the central source of functional knowledge — it doesn't become a thin proxy whose rules live in
   someone else's product and whose behaviour changes without a deploy.
11. **Contextual binding resolves an interface differently per consumer, declared once in a service provider.**
   `when(X)->needs(Interface)->give(Y)` puts the decision in one place read alongside every other binding; a
   constructor argument threaded down from config, or a class checking which implementation to reach for,
   scatters the decision across every call site, and a third consumer means finding all of them.
12. **Bind an interface for a genuine second implementation, not for testability alone.** Mocking or faking a
   concrete class works without an interface in front of it; a bound contract with exactly one
   implementation, kept "for testing" or "in case it changes", is point 7's rule in dependency-injection
   clothes — nobody swaps it, and the binding is a second file to open to see what runs.
13. **`Macroable` extends a class from outside it, and it stays on framework classes built that way.** `Str::macro()`
   or `Response::macro()` bolts a method onto a class the framework designed for it, discoverable from the
   class itself. Letting a project's own class grow methods from arbitrary call sites turns "where is this
   method defined" into a repo-wide search — use a subclass or an opt-in trait.
14. **A service provider groups registration by domain, not by framework primitive.** A `BillingServiceProvider`
   registering billing's bindings, listeners and config survives each of them changing shape; a
   `BindingsServiceProvider` or `ListenersServiceProvider` organised around the mechanism becomes the file
   every unrelated feature's registration lands in, because everything shares the mechanism.
15. **A deferred provider trades eager registration for load-on-demand, and that trade has a condition.** It only
   boots when one of its declared `provides()` bindings is resolved — correct for a provider whose only
   job is bindings nothing depends on at boot. A provider that also registers a route, a listener, or
   anything the framework must see during boot cannot be deferred; deferring silently drops that part.
16. **`singleton()` and `scoped()` answer different questions about a binding's lifetime, and the wrong
   choice survives unnoticed until the process that exposed it.** A singleton lives for the whole worker
   process — correct for a stateless client wrapper, wrong for anything holding per-request state, because
   the second request on a long-lived Octane worker or queue process reads the first request's leftover
   state. `scoped()` flushes the instance at the boundary of each request or job, which is what a
   request-scoped cache or accumulating collector needs — invisible on `php artisan serve`, where every
   process handles one request.
17. **A repository is banned by point 1 as a wrapper *in front of* Eloquent, not as a name for the query
   class point 1.2 asks for.** A query class named `ActiveSubscriptionsForTenant` answers one question over
   one aggregate and is free to use the query builder or Scout underneath; a `SubscriptionRepository`
   promising a general-purpose `find`/`all`/`save` surface duck-typing Eloquent's own contract is the
   pattern the rule targets, because Eloquent already is that surface.
18. **A trait's abstract method or expected property is declared in a `@property`/`@method` docblock at
   the top of the trait, not left implicit for the consuming class to discover at runtime.** A concern
   trait (point 4) that calls `$this->status` or expects a `scopeActive` sibling fails loudly at runtime
   on the first class that opts in without the expected shape — the docblock lets static analysis and the
   next developer verify it before running anything.
19. **A pipeline built from Laravel's `Pipeline` facade names each stage as its own invokable class**, not
   as an inline closure — the same reasoning as point 1's action class: a named stage survives being
   tested alone, reordered, and reused in a second pipeline that needs six of the same eight steps, where an
   inline closure has to be copied.
20. **A global scope applied via `addGlobalScope` is invisible at every call site that benefits from it**,
   which is the tenant-isolation case where that invisibility is the point — every query is automatically
   scoped, with no call site able to forget it. It is a liability once the scope encodes business rules that
   vary by call site (only sometimes exclude archived records); there, an explicit local scope the caller
   opts into (point 4) keeps the decision visible, rather than `withoutGlobalScope()` opting out of a
   default nobody chose at the call site.
21. **Eager-load in the query that produces the collection, not as an afterthought once the N+1 shows up
   in a profiler.** `with()` declared alongside the query keeps the relationship's cost visible next to
   the query that needs it; `load()` on an already-fetched collection is the accepted fallback only when
   the need depends on data not known until after the first fetch (a policy check on the result, a
   conditional branch).
22. **A single-action controller (`__invoke()`) is for a route that isn't one of a resource's seven
   verbs**, not a stylistic default. `ImportInvoiceBatch` or `RecalculateTenantUsage` name the endpoint as
   `authorizeResource()` (§2 point 16) expects a resource controller to be named after a model — using
   `__invoke` everywhere loses that convention for nothing.
23. **A value object gains from PHP 8.4's asymmetric visibility what it used to fake with a private
   property and a getter.** `public private(set) Money $total` is readable from outside the class and
   writable only from inside it, in one declaration — replacing a private property plus getter that never protected an invariant. This is for the DTOs and value objects point 1 asks actions to return, not for an Eloquent
   model's own attributes, which `$fillable`/casts already govern.
24. **`once()` memoises a callback for the life of the current request**, the correct home for an
   expensive computation a query class or action calls more than once per request and does not want cached
   across requests (that belongs in the cache store). A static property used as a memo cache survives past
   the request on a long-lived worker (Octane, a queue process), as in point 16 — `once()` is scoped
   correctly by construction.
25. **`Conditionable`'s `when()`/`unless()` on a query builder keeps a conditional filter inside the query
   it modifies**, instead of an `if`/`else` that duplicates every line that doesn't change between
   branches. `Model::query()->when($filter, fn ($q) => $q->where(...))` reads as "this query, conditionally
   narrowed"; an external `if` around near-identical query blocks is point 6's defect.
26. **A queued job's `handle()` method is where behaviour lives for the asynchronous case, and it takes its
   collaborators the same way an action does: through method injection, resolved from the container per
   run**, not through a constructor argument serialised alongside the job's data. A constructor-injected
   dependency gets serialised with the job (or fails to) and is stale when a worker picks it up hours
   later; one resolved in `handle()`'s parameters is fresh at execution.
27. **A PHP enum implementing an interface guarantees every case answers a method, which a `match`
   scattered across callers cannot.** §3 point 4 puts per-case data as a method on the enum itself; the
   interface lets a caller type-hint against "any status with a `label()`" without knowing which enum, and
   makes Larastan refuse a new enum that forgets to implement it — a `match` with no `default` arm silently
   returns null for a case nobody added, where an unimplemented interface method fails at analysis time.
28. **A module's own routes are registered from that module's own service provider, not appended to the
   application's single `routes/web.php` or `bootstrap/app.php`.** Where an OSDD-style layer package exists
   (§10 point 5), a `RouteServiceProvider` scoped to that package and booted from its own provider keeps
   "where behaviour lives" answerable per domain — a route in the app-wide file is found only by opening a
   file unrelated to its domain. [Laravel service providers documentation,
   laravel.com/docs/12.x/providers, read 2026-09-10.]
29. **A domain that needs data from another domain is handed an interface to depend on, not the other
   domain's concrete model or action class.** §10 point 9 states that a domain is entered through a
   stated surface; what makes the boundary real rather than a naming convention is a contract
   (`BillingLookup`) bound to a concrete implementation in a service provider, resolved by the consumer
   through the interface alone — swapping the implementation, or moving the providing domain into its own
   package, changes zero call sites in every consumer.
30. **A job's cross-cutting behaviour — throttling, preventing overlap, limiting concurrency — is a job
   middleware returned from `middleware()`, not an `if` inside `handle()`.** `WithoutOverlapping`,
   `RateLimited` and `ThrottlesExceptions` wrap the job as HTTP middleware wraps a request, keeping
   `handle()` pure domain logic (point 26 applied to the async case) instead of interleaving the work with
   the bookkeeping that decides whether it should run now. [Laravel queues documentation,
   laravel.com/docs/12.x/queues, read 2026-09-10.]
31. **Route-level middleware defined as a class method, not a constructor call, is where Laravel 11+ expects
   it — the controller constructor's `$this->middleware()` registration was removed from the base
   controller.** A controller implementing `HasMiddleware` and returning its list from a static `middleware()`
   method keeps the "declared once, close to the controller" property point 22 relies on; a Laravel 11+ app
   calling `$this->middleware()` in a constructor fails immediately — the fix is the new method, not
   restoring the old base class. [Laravel upgrade guide, laravel.com/docs/12.x/upgrade, read 2026-09-10.]
32. **`Model::unguard()` called globally lifts mass-assignment protection for every model for the rest of the
   request, not just the one call site that needed it.** It exists for a seeder or a one-off console command
   that fills every column of a known-safe payload; wrapping it around a request-driven write — or leaving
   it on without `Model::reguard()` immediately after — reopens the gap §2 point 6 names for a route-level
   permission that authorises the write but not the fields, for every model in the app.
33. **A collection method that returns a new collection, and one that returns a scalar or mutates in place,
   read alike at the call site unless the chain is named — point 18's naming-the-steps advice applies before
   the pipeline gets long enough to need it.** `$collection->each(fn ($item) => $item->save())` returns the
   original collection and reads as if it built something; naming the step (`$saved = ...`) only where a
   value is produced keeps a side-effecting `each()` visibly different from `map()` in a diff.
