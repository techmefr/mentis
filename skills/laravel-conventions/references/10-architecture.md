# laravel-conventions §10 — Architecture

> Section 10 of `skills/laravel-conventions`. Read it when the change spans layers, or a new one is proposed. The other sections and the guardrails stay in `SKILL.md`.

1. Separate the **functional/business** layers from the **technical/shared** ones, with a predictable place
   per domain, and no technical layer importing a functional one.
2. A new dependency is a decision: check what the project already standardises on for the need (factories,
   policies, permissions, media, activity logging, translations, auth tokens, queues, multi-tenancy, static
   analysis) before adding a second library for something already solved.
3. **A version branch past its security-fix end of life is not a maintenance choice.** Both the framework's
   and the language's support windows are published and mechanical, so the question has a date for an
   answer rather than an opinion: a new project starts on the newest stable major and the newest minor that
   major supports, and an existing one is planned off a branch before its security window closes, not after
   an advisory forces it. Staying behind also compounds — each skipped major makes the next upgrade the
   one nobody has budget for.
4. Prefer the framework's own mechanism over a custom one; prefer configuration over a new abstraction. The
   framework already does most of the design-pattern work (`skills/design-patterns`).
5. **Where a layer-package convention (OSDD-style) is installed**, point 1's split is enforced structurally,
   not just by discipline: each functional (`users`, `billing`, ...) or technical domain is its **own
   self-contained Composer package** — `composer.json`, `src/`, its own `database/` (migrations, seeders),
   its own `tests/`, its own service provider — generated and scaffolded through the package's own commands
   rather than by hand. Where installed, it's the house override for point 1: don't hand-roll a `functional/`
   folder convention that competes with it. [`xefi/laravel-osdd`, github.com/xefi/laravel-osdd, read
   2026-08-10.]
6. **Where `laravel/boost` is present, install it with its agent skills (`--skills`), not the MCP server
   alone** — packages now ship their conventions as skills rather than as guidelines, so a guidelines-only
   install reaches nothing package-specific, including the concrete layout point 5 depends on. Run it
   interactively: a non-interactive first install silently drops every third-party skill while still
   reporting success. [`laravel/boost`, github.com/laravel/boost, read 2026-08-11.]
7. **The dependency direction *is* the architecture, so a tool enforces it, not a paragraph.** Point 1's
   split holds for exactly as long as everyone remembers it; expressed as a static-analysis rule or a
   package boundary, a wrong-direction import fails a build instead of waiting for a reviewer who happens
   to know. This is the same argument `skills/code-baseline` §8 makes about guarantees generally: prefer
   the mechanism the toolchain checks over the sentence someone has to recall under deadline.
8. **Say which kind of boundary you actually have.** A folder convention is a convention — nothing stops an
   import across it. A Composer package boundary is enforced by the autoloader and by the package's own
   `composer.json`. Both are legitimate; what causes trouble is treating the first as though it were the
   second, and then being surprised that two domains grew a direct dependency nobody approved.
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
    means designing against an imagined second caller, and the real one, when it arrives, wants something
    else — so the abstraction has to be rebuilt anyway, this time with a consumer attached to it.
13. **Don't add infrastructure the database still handles.** A queue, a cache layer or a search engine each
    bring an operational surface — a failure mode, a deployment step, a staleness question. Reach for one
    when a measurement says the database cannot do it, not because the shape of the problem resembles a
    tutorial.
14. **Keep the dependency set current continuously, or point 3 becomes impossible.** A framework major is
    only reachable when the packages around it are already close to their own latest; a set left to drift
    for a year turns a routine upgrade into a project, which is how a branch ends up past its security
    window in the first place.
15. **An architecture decision that is not written down gets re-litigated.** Record it near the code, in a
    few lines: what was decided, what it rules out, and what would reopen it. The point is not
    documentation for its own sake — it is that the next person arguing the other side deserves to know the
    argument has already happened, and on what grounds (`skills/documentation-adr`, which also says when
    *not* to commit a file for it).
16. **Contextual binding is point 4's "prefer the framework's own mechanism" applied to the container**: when
    two classes need a different implementation of the same interface — a different disk, a different
    driver, a config value — `$this->app->when(A::class)->needs(Interface::class)->give(...)` resolves the
    branch once, in the provider, instead of an `if` inside every constructor that would otherwise ask "who
    is calling me" to pick the right implementation. `giveConfig()` and `giveTagged()` cover the two common
    shapes (an injected config value, an injected set of same-tagged bindings) without a hand-written
    closure for either. [Laravel container docs, laravel.com/docs/12.x/container, read 2026-09-10.]
17. **A binding that is never resolved should never be booted.** A service provider deferred via `$defer =
    true` (or, on newer providers, declared through `provides()`) is only instantiated the first time one of
    its bindings is actually requested — a provider wiring a rarely-used integration stops costing a boot-time
    class load and a container lookup on every request that never touches it. The trade only pays off for a
    provider with no side effect outside its own `register()`; one that also listens for events or registers
    routes in `boot()` cannot be deferred without silently losing that wiring on the requests where nothing
    triggered the resolution.
18. **A middleware group is a named ordering, and the order is the part that breaks silently.** Registering
    `auth` after a rate-limiter that keys its bucket on the authenticated user throttles every guest request
    under one shared bucket, because the middleware that would have identified the user has not run yet. The
    fix is not a smarter limiter, it is reading the group's declared order in `bootstrap/app.php` before
    adding to it — inserting a new entry without checking what runs before and after it is how this
    regresses on an otherwise unrelated change.
19. **A feature toggle is a config value with an environment default, not a hard-coded conditional shipped
    then reverted.** Point 13's "don't add infrastructure the database still handles" cuts the other way
    here too: a boolean in `config/features.php`, read through the config layer per point 1 of
    `skills/laravel-conventions` §7, lets the same deploy run dark in staging and live in production without
    a second branch — reverting a toggle is changing one value, reverting a conditional is a second
    pull request.
20. **Package auto-discovery is a convenience, not a boundary.** Composer wires a package's service provider
    and facades automatically from its `extra.laravel` block, which is why point 2's "check what's already
    standardised on" has to include packages that never appear in a manually maintained providers array —
    they are active anyway. A package that must not run in a given environment (a debug bar, a seeder
    package) is excluded in `composer.json`'s `dont-discover`, not by hoping nothing calls it.
21. **A facade and its underlying binding are two separate things to keep in sync.** A facade is a static
    proxy resolved from the container at call time, so swapping the bound implementation in a provider
    changes what every facade call does without touching a single call site — which is exactly why a test
    that swaps the binding (`$this->app->bind(...)`, a fake) has to happen before the facade is first
    resolved in that request; resolving it once caches the instance and a later rebind is silently ignored
    for the rest of that request/test.
