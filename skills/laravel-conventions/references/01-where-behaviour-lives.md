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
6. **No markup in PHP.** A service, action, accessor, controller or job never builds HTML — no tags, no inline
   styles, no concatenated `<span>`. Markup belongs in the view layer; a backend class returns data.
7. **The application owns its domain.** When integrating an external system (payment provider, CRM, ERP), the
   app remains the central source of functional knowledge — it doesn't become a thin proxy whose rules live in
   someone else's product and whose behaviour changes without a deploy.
