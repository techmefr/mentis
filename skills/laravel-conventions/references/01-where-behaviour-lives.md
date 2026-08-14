# laravel-conventions §1 — Where behaviour lives

> Section 1 of `skills/laravel-conventions`. Read it when a model, a controller, a listener or a service is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Keep models thin.** A model holds `$fillable`, `$casts`, relationships, simple scopes, trivial computed
   accessors over its own attributes, and lifecycle traits. Business logic, orchestration and anything
   reaching another aggregate go in an **action or query class** — never a generic `*Service`/`*Repository`
   (`code-baseline`'s no-bag-name rule, §2 below). One class, one verb-plus-noun mission
   (`RegisterUser`, `GetActiveSessionsForUser`), never a `UserManager`/`UserService` that accumulates
   unrelated methods over time. A fat model is the class everything imports and nobody can change; a generic
   service is the same failure one layer up.
2. **Events + listeners, never model observers**, for reacting to lifecycle changes. An observer is invisible
   at the call site: something saves a row and unrelated code runs, with no trace in the flow being read.
   Listeners are registered explicitly. This includes the model's own `boot()`: a static `boot()` override
   that registers lifecycle closures (`static::creating(...)`) is the same hidden-effect problem wearing the
   framework's own clothes — the fix is the same listener registered in the `EventServiceProvider`, not a
   closure moved into the model.
3. Reusable cross-cutting model behaviour (historisation, auditing, snapshotting) goes in a trait the model
   **opts into**, shaped like the framework's own (`SoftDeletes`): the model declares what it tracks. A base
   class inherited by everything makes the behaviour mandatory and untestable in isolation.
4. **No markup in PHP.** A service, action, accessor, controller or job never builds HTML — no tags, no inline
   styles, no concatenated `<span>`. Markup belongs in the view layer; a backend class returns data.
5. **The application owns its domain.** When integrating an external system (payment provider, CRM, ERP), the
   app remains the central source of functional knowledge — it doesn't become a thin proxy whose rules live in
   someone else's product and whose behaviour changes without a deploy.
