# laravel-conventions §1 — Where behaviour lives

> Section 1 of `skills/laravel-conventions`. Read it when a model, a controller, a listener or a service is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Keep models thin.** A model holds `$fillable`, `$casts`, relationships, trivial computed accessors
   over its own attributes, and lifecycle traits — with the scopes and the per-concept accessors grouped
   into the concern traits of point 4 rather than accumulating in the class body. Business logic,
   orchestration and anything reaching another aggregate go in an **action or query class** — never a
   generic `*Service`/`*Repository`
   (`code-baseline`'s no-bag-name rule, §2 below). One class, one verb-plus-noun mission
   (`RegisterUser`, `GetActiveSessionsForUser`), never a `UserManager`/`UserService` that accumulates
   unrelated methods over time. A fat model is the class everything imports and nobody can change; a generic
   service is the same failure one layer up.
   1. **An action has one public method, and it returns a value.** Its collaborators arrive through
      constructor promotion, its inputs are typed parameters rather than the request, and its result is
      domain data — never a response, never a redirect. An action that returns an HTTP response cannot be
      called from a command, a job or a test without a fake request, which is how the same rule ends up
      duplicated in the console.
   2. **Separate the read from the write.** A query class answers a question and touches nothing; an action
      changes state. Merging them gives a method whose name cannot be honest (`getOrCreateAndNotify`), and
      the caller can no longer tell whether calling it twice is safe.
   3. **A controller validates, delegates, responds.** Business branching in a controller is the same
      logic the console command will need next month, in the one place a console command cannot reach it.
2. **Events + listeners, never model observers**, for reacting to lifecycle changes. An observer is invisible
   at the call site: something saves a row and unrelated code runs, with no trace in the flow being read.
   Listeners are registered explicitly. This includes the model's own `boot()`: a static `boot()` override
   that registers lifecycle closures (`static::creating(...)`) is the same hidden-effect problem wearing the
   framework's own clothes — the fix is the same listener registered in the `EventServiceProvider`, not a
   closure moved into the model.
3. Reusable cross-cutting model behaviour (historisation, auditing, snapshotting) goes in a trait the model
   **opts into**, shaped like the framework's own (`SoftDeletes`): the model declares what it tracks. A base
   class inherited by everything makes the behaviour mandatory and untestable in isolation.
4. **A concern trait owns its concept end to end** — its relationship, its casts, its scopes, its accessors
   and its predicates live in the same file, the way the framework's soft-delete trait owns its column, its
   global scope and its restore method. Named after the concept (`Publishable`, `HasOwner`), never after the
   filtering (`FiltersByOwner`). What this buys is the model body: it shrinks to a declaration of what the
   model *is* — the fillable list, the casts, and the trait names it opts into — and a query scope stops
   sitting alone in a class body, three hundred lines from the relationship it queries. A scope defined
   inline on the model is the default this displaces, not a violation to hunt down in existing code
   (`code-baseline` §0).
5. **Recognise the two shapes that are a pattern, not a field.** A status/state column whose values move
   through named transitions, with a guard or a side effect on the move, is a **state machine** — read
   `skills/design-patterns` §4 and `skills/domain-modeling` before writing the first transition method. An
   ordered sequence of steps over one payload, growing a step per requirement (validate, dedupe, enrich,
   notify), is a **pipeline** — same reference. Neither arrives phrased in pattern vocabulary: they arrive
   as "add a publish button", "the status should go back to draft", "it should also send a notification".
   That is the whole reason to name the recognition here rather than trusting the pattern block's own
   triggers to fire.
6. **Do not factor out what protects nothing.** A helper wrapping one framework call, a class extracted
   because two lines looked alike, an interface with one implementation "for later" — each adds a hop and
   removes the reader's ability to see what happens. The test is whether the extraction holds an invariant
   somebody could otherwise break: a rule about how a thing must be built, a boundary a caller must not
   cross. Shared shape is not an invariant, and two call sites that happen to look alike today are the most
   common reason a helper ends up with a boolean parameter that switches its behaviour.
7. **Do not build the extension point before the second real case.** A strategy, a registry, an event with
   one listener, a config key with one value — all of them are guesses about a variation that has not
   arrived, and they cost the same whether the guess was right or wrong. `skills/design-patterns` holds the
   threshold; what belongs here is where the pressure comes from in this framework: a package's own
   extension hook makes it feel free, and it still has to be read by whoever comes next.
8. **An accessor is a projection of the row, not a query.** The moment it loads a relation, counts
   something, or reaches configuration, it becomes an N+1 wearing the clothes of a field (§4 point 1), and
   nothing at the call site says so. Anything needing another table is a method with a verb in its name, or
   it belongs in a query class.
9. **No markup in PHP.** A service, action, accessor, controller or job never builds HTML — no tags, no inline
   styles, no concatenated `<span>`. Markup belongs in the view layer; a backend class returns data.
10. **The application owns its domain.** When integrating an external system (payment provider, CRM, ERP), the
   app remains the central source of functional knowledge — it doesn't become a thin proxy whose rules live in
   someone else's product and whose behaviour changes without a deploy.
11. **Contextual binding resolves an interface differently per consumer, declared once in a service provider.**
   `when(X)->needs(Interface)->give(Y)` puts the decision in one place read alongside every other binding; the
   alternative — a constructor argument threaded down from config, or a class checking which implementation it
   should reach for — scatters the same decision across every call site that needed the other implementation,
   and adding a third consumer means finding all of them.
12. **Bind an interface for a genuine second implementation, not for testability alone.** Mocking or faking a
   concrete class works without an interface standing in front of it; a bound contract that has exactly one
   implementation, kept "for testing" or "in case it changes", is point 7's extension-point rule wearing
   dependency-injection clothes — nobody swaps it, and the binding is a second file to open to see what actually
   runs.
13. **`Macroable` extends a class from outside it, and it stays on framework classes built that way.** `Str::macro()`
   or `Response::macro()` bolts a method onto a class the framework already designed for it, discoverable from
   the class itself. Using the same trait to let a project's own class grow methods from arbitrary call sites
   turns "where is this method defined" into a repo-wide search — a subclass or a trait the class opts into says
   the same thing without opening the class to injection from anywhere.
14. **A service provider groups registration by domain, not by framework primitive.** A `BillingServiceProvider`
   registering billing's bindings, listeners and config survives every one of those changing shape; a
   `BindingsServiceProvider` or a `ListenersServiceProvider` organised around the mechanism instead of the
   feature becomes the file every unrelated feature's registration lands in, because the mechanism it's named
   after is shared by everything.
15. **A deferred provider trades eager registration for load-on-demand, and that trade has a condition.** It only
   boots when one of its declared `provides()` bindings is actually resolved — correct for a provider whose only
   job is registering bindings nothing else depends on at boot. A provider that also needs to register a route,
   a listener, or anything the framework must see during boot regardless of whether the binding is ever resolved
   cannot be deferred and still do that; deferring it silently drops the part that was supposed to run eagerly.
16. **`singleton()` and `scoped()` answer different questions about a binding's lifetime, and the wrong
   choice survives unnoticed until the process that exposed it.** A singleton lives for the whole worker
   process — correct for a stateless client wrapper, wrong for anything holding per-request state, because
   the second request on a long-lived Octane worker or queue process then reads the first request's leftover
   state. `scoped()` gives the same one-instance-per-resolution guarantee but flushes it at the boundary of
   each request or job, which is the binding a request-scoped cache or an accumulating collector actually
   needs — a distinction invisible on `php artisan serve`, where every process handles exactly one request
   anyway.
17. **A repository is banned by point 1 as a wrapper *in front of* Eloquent, not as a name for the query
   class point 1.2 already asks for.** The difference is what the class does: a query class named
   `ActiveSubscriptionsForTenant` answers one question over one aggregate and is free to use the query
   builder or Scout underneath; a class named `SubscriptionRepository` promising a general-purpose
   `find`/`all`/`save` surface duck-typing Eloquent's own contract is the pattern the rule actually
   targets, because Eloquent already is that surface.
18. **A trait's abstract method or expected property is declared in a `@property`/`@method` docblock at
   the top of the trait, not left implicit for the consuming class to discover at runtime.** A concern
   trait (point 4) that calls `$this->status` or expects a `scopeActive` sibling method fails silently at
   analysis time and loudly at runtime on the first class that opts in without the expected shape — naming
   the requirement in the trait's own docblock is what lets static analysis, and the next developer, verify
   a class actually satisfies it before running anything.
19. **A pipeline built from Laravel's `Pipeline` facade names each stage as its own invokable class**, not
   as a closure defined inline in the pipeline's construction — the same reasoning as point 1's action
   class: a stage with a name survives being tested alone, reordered, and reused in a second pipeline that
   needs six of the same eight steps, where an inline closure has to be copied.
20. **A global scope applied via `addGlobalScope` is invisible at every call site that benefits from it**,
   which is the tenant-isolation case where that invisibility is the entire point — every query is
   automatically scoped, with no call site able to forget it. The same invisibility is a liability the
   moment the scope encodes business rules that legitimately vary by call site (only sometimes exclude
   archived records); there, an explicit local scope the caller opts into (point 4) keeps the decision
   visible where it is made, rather than requiring `withoutGlobalScope()` to opt back out of a default
   nobody chose at the call site.
21. **Eager-load in the query that produces the collection, not as an afterthought once the N+1 shows up
   in a profiler.** `with()` declared alongside the query a controller or query class builds keeps the
   relationship's cost visible next to the query that needs it; `load()` called later on an
   already-fetched collection is the accepted fallback only when the need for the relation depends on data
   not known until after the first fetch (a policy check on the result, a conditional branch).
22. **A single-action controller (`__invoke()`) is for a route that isn't one of a resource's seven
   verbs**, not a stylistic default applied everywhere. `ImportInvoiceBatch` or `RecalculateTenantUsage`
   name the endpoint the way `authorizeResource()` (§2 point 16) expects a resource controller to be named
   after a model — a project reaching for `__invoke` on every controller loses that convention without
   gaining anything, because a one-method class named after an HTTP verb pair (`show`/`update`) is no
   clearer than a one-method class named after the action it performs.
23. **A value object gains from PHP 8.4's asymmetric visibility what it used to fake with a private
   property and a getter.** `public private(set) Money $total` is readable from outside the class and
   writable only from inside it, in one declaration — the boilerplate this replaces (`private $total;
   public function total(): Money { return $this->total; }`) was never protecting an invariant, it was
   working around the language not having the shape yet. This is for the DTOs and value objects point 1
   already asks actions to return, not for an Eloquent model's own attributes, which the framework's
   `$fillable`/casts machinery already governs.
24. **`once()` memoises a callback for the life of the current request**, which is the correct home for an
   expensive computation a query class or action calls more than once per request and does not want cached
   across requests (that belongs in the cache store instead). A static property used as an informal memo
   cache does the same thing but survives past the request on a long-lived worker (Octane, a queue process)
   the way point 16 describes for a wrongly-scoped singleton — `once()` is scoped correctly by construction.
25. **`Conditionable`'s `when()`/`unless()` on a query builder keeps a conditional filter inside the query
   it modifies**, instead of the caller building the query in an `if`/`else` that duplicates every line
   that doesn't change between branches. `Model::query()->when($filter, fn ($q) => $q->where(...))` reads
   as "this query, conditionally narrowed" at the point the query is assembled; an external `if` around two
   near-identical query blocks is the same defect point 6 already names for factoring out what protects
   nothing, arriving from the query-building side instead.
26. **A queued job's `handle()` method is where behaviour lives for the asynchronous case, and it takes its
   collaborators the same way an action does: through method injection, resolved from the container per
   run**, not through a constructor argument serialised alongside the job's own data. A dependency
   constructor-injected into a job gets serialised with the job (or fails to serialise at all) and is
   stale by the time a queue worker picks it up hours later; one resolved inside `handle()`'s parameters is
   fetched fresh at execution time, which is the job equivalent of point 1's "an action's inputs are typed
   parameters."
27. **A PHP enum implementing an interface guarantees every case answers a method, which a `match`
   scattered across callers cannot.** Point 4 of §3 already puts per-case data as a method on the enum
   itself; the interface is what makes a caller able to type-hint against "any status with a `label()`"
   without knowing which enum, and it is what makes the compiler (via Larastan) refuse a new enum that
   forgets to implement it — a `match` with no `default` arm silently returns null for a case nobody
   remembered to add, where an unimplemented interface method fails at analysis time instead.
28. **A module's own routes are registered from that module's own service provider, not appended to the
   application's single `routes/web.php` or `bootstrap/app.php`.** Where an OSDD-style layer package exists
   (§10 point 5), a `RouteServiceProvider` scoped to that package and booted from the package's own
   provider keeps "where behaviour lives" answerable per domain — a route added straight to the app-wide
   file is discoverable only by opening a file that has nothing to do with the domain it belongs to, and it
   is the one wiring point that quietly survives a domain's move into its own package. [Laravel service
   providers documentation, laravel.com/docs/12.x/providers, read 2026-09-10.]
29. **A domain that needs data from another domain is handed an interface to depend on, not the other
   domain's concrete model or action class.** §10 point 9 already states that a domain is entered through a
   stated surface; the mechanism that makes the boundary real rather than a naming convention is a contract
   (`BillingLookup`) bound to a concrete implementation in a service provider, resolved by the consuming
   domain through the interface alone — swapping the implementation, or later moving the providing domain
   into its own package, changes zero call sites in every consumer.
30. **A job's cross-cutting behaviour — throttling, preventing overlap, limiting concurrency — is a job
   middleware returned from `middleware()`, not an `if` inside `handle()`.** `WithoutOverlapping`,
   `RateLimited` and `ThrottlesExceptions` each wrap the job the same way HTTP middleware wraps a request,
   which keeps `handle()` reading as pure domain logic (point 1's "an action's inputs are typed parameters,"
   applied to the async case in point 26) instead of interleaving the actual work with the bookkeeping that
   decides whether it should run at all right now. [Laravel queues documentation,
   laravel.com/docs/12.x/queues, read 2026-09-10.]
31. **Route-level middleware defined as a class method, not a constructor call, is where Laravel 11+ expects
   it — the controller constructor's `$this->middleware()` registration was removed from the base
   controller.** A controller implementing `HasMiddleware` and returning its list from a static `middleware()`
   method keeps the same "declared once, close to the controller" property point 22's single-action
   controller already relies on; a project still calling `$this->middleware()` in a constructor on a
   from-scratch Laravel 11+ app is reaching for a base-controller method the skeleton no longer ships, which
   fails immediately rather than silently — but the fix is the new method, not restoring the old base class.
   [Laravel upgrade guide, laravel.com/docs/12.x/upgrade, read 2026-09-10.]
32. **`Model::unguard()` called globally lifts mass-assignment protection for every model for the rest of the
   request, not just the one call site that needed it.** It exists for a seeder or a one-off console command
   that legitimately fills every column of a known-safe payload; wrapping it around a request-driven write —
   or leaving it toggled on without the matching `Model::reguard()` immediately after — reopens exactly the
   gap §2 point 6 already names for a route-level permission that authorises the write but not the fields,
   this time for every model in the app rather than one.
33. **A collection method that returns a new collection, and one that returns a scalar or mutates in place,
   read alike at the call site unless the chain is named — point 18's naming-the-steps advice applies before
   the pipeline gets long enough to need it.** `$collection->each(fn ($item) => $item->save())` returns the
   original collection and reads as if it built something; naming the intermediate step (`$saved = ...`)
   only where a value is actually produced keeps a side-effecting `each()` visibly different from a
   transforming `map()` in a diff, rather than trusting the reviewer to notice which one is which from the
   method name alone.
