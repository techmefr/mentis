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
